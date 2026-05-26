# Phase 5 Regen Design-Fit Pass — Pattern A-Deep Verdict

> **STATUS:** RATIFIED 2026-05-25 — autonomous design-fit critique of v2_narrow_phase_5 regen output per Matt 2026-05-25 pre-authorized routing chain (rocket regen → jack-ryan Gate-2 PASS-with-WARN → gandalf design-fit pass)

**Author:** gandalf (story-and-design steward; design-fit critique seam-owner)
**For:** knight-rider forward routing + Matt cycle-13 readiness signal + T4 post-mortem session 1 unblock
**Pattern:** Pattern A-deep substantive verdict per gandalf OP § 2 (multi-question structure + per-finding verdict + forward routing recommendation)

**Authority chain composing:**
- Authorship of Phase 5 spec (`canonical/story/phase-5-cohesion-judge-calibration-spec-2026-05-25.md`)
- Prior design-fit pass surfacing the two findings (`agentic_orchestration/gandalf/notes/2026-05-25-engine-generation-special-case-summary.md`)
- Matt 2026-05-25 verbal pre-authorization for autonomous fire
- jack-ryan Gate-2 PASS-with-WARN verdict (`agentic_orchestration/qa/findings/2026-05-25-phase5-skill-node-naming-gate2-findings.md`)

---

## 0. Top-line — headline verdict

**Finding 1 (placeholder issue):** **RESOLVED — substantively.**
**Finding 2 (degenerate balance_metadata):** **FRAMING WAS WRONG; resolution is NOT about win-rate signal.** The "all-0.5 win-rate" claim in my prior pass § 3.7 cited fields (`actual_winrate`, `convergence_iterations`, `converged`) **that do not exist in the v2 engine schema**. Those fields are loadout-app `BalanceMetadata` interface fields inherited from the legacy export schema; the v2 engine emits ONLY `converged_modifier: 1.0`. The v2 engine pipeline does NOT run BalanceLoop / gauntlet / sim at all — by structural design, not by Phase 5 omission.

**Load-bearing addition to prior framing:** the binary "RESOLVED vs PERSISTS vs AMBIGUOUS-PENDING-SIM-RERUN" choice presupposed an architecture where sim is part of the v2 pipeline and could be re-run. **Empirical refutation:** no sim integration exists in v2 generation runs. Re-running Phase 5 with real skill content does not, cannot, and was not designed to produce fight-outcome differentiation in the v2_narrow export schema.

This is a **framing-audit catch** (per gandalf OP § 4.1 three-question protocol): Q2 refutation evidence available in current scope; Q3 ruling — refine the framing rather than execute the original Finding-2 question as-posed. The escalation path enumerated in the invocation brief ("L3 skill generator / Phase 3 convergence / gamora sim integration") collapses to a SINGLE candidate: **gamora sim integration is structurally absent from v2 generation runs.** L3 and Phase 3 are not the issue because they do not exist as candidate failure surfaces in this pipeline.

**Forward routing recommendation:** **Cycle 12 closes on Finding 1 alone.** Milestone tag `v2.0-phase-5-skill-node-naming` fires after rocket's WARN remediations land. T4 post-mortem session 1 is unblocked. Finding 2 reframes from "diagnose all-0.5 persistence" into a **Cycle 13 architecture decision**: should v2 engine integrate balance-loop / gauntlet sim as part of generation? OR is the v2 engine intentionally generation-only and downstream sim is a separate cycle invoked on emitted forms? This is a Matt design call, not a gandalf design-fit-pass-resolvable item.

---

## 1. Framing-audit (gandalf OP § 4.1 three-question protocol)

| Q | Question | Answer |
|---|---|---|
| **Q1** | What load-bearing framing assumptions does this work depend on? | (a) Phase 5 ran at skill-node level and produced real names/flavor/effects per spec. (b) The v2_narrow_phase_5 regen could/should have re-run sim to produce updated win-rate signal. (c) Prior pass § 3.7 finding ("all 35 forms identical 0.5 win-rate, 1 iteration, modifier=1.0") was empirically grounded in v2_narrow output. |
| **Q2** | What evidence currently in hand could refute these? | (a) Empirically supported — 0/289 placeholders, all schema fields populated, mean cohesion 0.838, jack-ryan Gate-2 PASS. (b) Empirically refuted — `scripts/v2_narrow_phase_5_generation_run_2026_05_25.py` does NOT invoke BalanceLoop; `scripts/v1_narrow_generation_run_2026_05_25.py` (which produced v2_narrow source) ALSO does not invoke BalanceLoop. (c) Empirically refuted — the cited fields (`actual_winrate`, `convergence_iterations`, `final_modifier`, `converged`) do NOT exist in v2_narrow's `balance_metadata` either; v2_narrow form 0 `balance_metadata` keys are identical to v2_narrow_phase_5 form 0 keys. The "all-0.5 win-rate" must have been read from a different artifact (likely loadout-app's coerced view where missing fields display as defaults) or from a legacy season (e.g., `season_001001` HAS these fields with REAL variation 0.4767-0.6567 and REAL iterations 1-9; v2 dropped them). |
| **Q3** | Refine framing OR execute as-framed? | **REFINE.** The Finding-2 question as invocation-posed (RESOLVED vs PERSISTS vs AMBIGUOUS-PENDING-SIM-RERUN) presupposed an architecture that doesn't match the v2 engine's actual emission schema. Re-running Phase 5 with real skill content cannot produce different sim-fight outcomes because the v2 pipeline doesn't run sim at all. The verdict reframes Finding 2 from "design-fit pass on win-rate differentiation" to "structural observation about v2 engine generation-vs-sim partitioning, surfaced for Cycle 13 scope decision." |

---

## 2. Finding 1 — placeholder issue — RESOLVED

### 2.1 Empirical verification (structural)

| Criterion | Spec § 6 target | Verified empirically |
|---|---|---|
| Phase 5 fires at skill-node level for ALL nodes | 289 nodes named | 289/289 nodes have real names; 0 placeholder strings matching `^Chain [A-D] T\d \d+$` |
| Per-node schema § 2.1 populated | name + flavor_text + effect_description + thematic_tags | 0 nodes missing any of these fields |
| Cohesion-judge per-node firing | per-node phase5_cohesion_score | 289/289 nodes have phase5_cohesion_score + phase5_cohesion_breakdown (5-dimension) + phase5_attempt_number |
| First-attempt PASS rate ≥ 70% | 70% | 91.3% (264/289) — exceeds spec by 21 pts |
| Re-roll rate ≤ 15% | 15% | 13.5% — within target |
| Final FAIL rate ≤ 5% | 5% | 0.0% — exceeds |
| Cost-per-run | $0.50-$2.00 range | $0.7392 — within |

All structural acceptance criteria met. jack-ryan Gate-2 PASS verdict empirically corroborated by independent inspection.

### 2.2 Substantive design-fit verification — sampled forms

Read full skill trees for 9 forms across element / culture / chain / tier diversity: form-000 (Rampart Knight european physical_warrior), form-003 (Khyber Shadow Dancer south_asian rogue+Alexander), form-008 (Sunstone Spearthrower mesoamerican fire_mage+Moctezuma), form-013 (Ashen Geomancer european earth_caster), form-018 (Twilight Rod Sage fantasy shadow_caster), form-021 (Galeborn Standard Bearer wind_controller), form-022 (Crimson Leaf Binder east_asian physical_grappler), form-025 (Moctezuma's Jade Warlord mesoamerican physical_warrior+Moctezuma anchor), form-030 (Iron Shilpi Veer south_asian+Wayland Anglo-Saxon).

**Substantive observations:**

| Form | Skill-tree identity | Design-fit verdict |
|---|---|---|
| **form-000 Rampart Knight** | Shield Wall Command → Advance the Line → Break Their Ranks (chain A); Crushing Advance → Stalwart Advance → Unyielding Advance → Indomitable Advance (chain B). Coherent formation-hold → advance arc; "Advance" echoes build tier weight; T3 "Indomitable" climactic. | ⭐ **strong cohesion.** Reads as a single deliberate paladin/footman kit, not 10 disconnected skills. Diablo II Defender-paladin analog. |
| **form-003 Khyber Shadow Dancer** | Shadowed Blade Rush → Phantom Step Surge → Eclipse Whirlwind Strike (chain A); Whirling Dust Slash → Sandstorm Bind → Desert Tempest Vortex (chain B); Dust Devil Sweep → Cyclone Dust Surge → Maelstrom Dust Command (chain C). Kukri + Alexander + Khyber-pass geography all converge — dust/shadow/storm metaphor across chains. | ⭐ **strong cohesion.** "Where Alexander's phalanx broke through, the Shadow Dancer dissolves into motion" surfaces explicitly in T2 flavor. Cross-civilizational Macedonia-meets-Himalayan-pass marriage is mythologically defensible AND chain progression honored. |
| **form-008 Sunstone Spearthrower** | Solar Stride → Sunburst Volley → Blazing Sun Barrage (chain A); Solar Javelin Burst → Solar Javelin Recall → Solar Javelin Tempest (chain B); Sunstone Javelin Summon → Sunstone Javelin Command (chain C). Mesoamerican-solar-warrior consistently. Tonatiuh sun-god surfaces in flavor. Recall-mechanic (chain B T2) is a strong design touch — recalling spears is a real Aztec atlatl-warrior trope. | ⭐ **strong cohesion.** Element=physical underlying but compensates via solar/fire vocabulary at narration layer (this is exactly what my prior pass flagged as the form-layer Phase 5 doing load-bearing work; now extended to skill layer). |
| **form-013 Ashen Geomancer** | Stone Shard Volley → Gravel Burst Salvo → Earthen Shackle Ring (chain A); Dust Veil Shroud → Ashen Dust Familiar → Cinder Dust Eruption → Cinder Dust Aegis (chain B). | ⭐ **strong skill-tree cohesion.** Phase 5 LLM rescued the substrate misfit at narration layer — "Powder tester" never appears; vocabulary is dust/stone/cinder/ash. **However:** my prior pass's MEDIUM-severity substrate-tagging misfit (gunpowder-quality-test instrument bound to Totem Hierophant earth-caster) is **unchanged** at the substrate-binding layer. Phase 5 papered it over at narration; the underlying museum-keyword-mismatch persists. |
| **form-018 Twilight Rod Sage** | Shadow Step → Umbral Rod Surge → Twilight Cataclysm Strike (chain A); Dusk Bolt Strike → Dusk Binding Wave → Dusk Phantom Rush (chain B); Dusk Step Surge → Dusk Binding Surge (chain C). Necromancer Summoner cell → "Twilight Rod Sage" rendered as a controlled-shadow scholar archetype (not gothic-necromancer). | ⭐ **strong cohesion.** The TRADE_OFF keystone (no-crits / reliability) reads as "methodical shadow-scholar" via the Sage framing. Flutterby Rod substrate (D&D-source) is invisible in narration. |
| **form-021 Galeborn Standard Bearer** | Galeborn Advance → Galeborn Surge → Galeborn Tempest Charge (chain A); Galeborn Wind Burst → Galeborn Gust Barrage → Galeborn Storm Edict (chain B); Galeborn Squall Lance + more (chain C). | ⚠️ **strong NAMING cohesion but ALGORITHM misfit persists.** Naming is coherent (every skill uses "Galeborn" prefix; vocabulary is wind/gust/tempest/squall/gale). BUT the underlying GEOMETRY_COLLAPSE keystone (AoE shrinks to 0.5×, damage grows 1.5×) on a storm-caller archetype is **not addressed by Phase 5**. Phase 5 LLM did its job — naming on top of mechanics is coherent. The architecture-vs-class-fantasy mismatch I flagged in prior pass § 4.2 is a § 8 algorithm-amendment item for Cycle 13, NOT a Phase 5 spec scope item. |
| **form-022 Crimson Leaf Binder** | Crimson Leaf Summons → Crimson Leaf Chorus → Crimson Leaf Surge → Crimson Leaf Tempest (chain A); Crimson Leaf Dash → Crimson Leaf Ward → Crimson Leaf Maelstrom (chain B). "Crimson Leaf" repeats EVERY node. | ⚠️ **MEDIUM cohesion — over-uniformized.** Every skill name uses the "Crimson Leaf X" template. Reads as one motif, not as a kit-with-variety. This is the **kit-internal vocabulary-collapse pattern** — Phase 5 honored kit-identity cohesion (§ 3.1 weight 0.30) at the expense of inter-skill differentiation. Compare to form-018 Twilight Rod Sage which varies "Shadow / Umbral / Twilight / Dusk" — much better intra-kit lexical variety. |
| **form-025 Moctezuma's Jade Warlord** | Obsidian Sweep → Jade Tempest Strike → Jade Warrior's Lunge → Jade Warlord's Command (chain A); Jade Fury Cleave → Jade Fury Maelstrom → Jade Fury Dominion → Jade Fury Ascendant (chain B). Obsidian/jade vocabulary; named-bearer "Moctezuma" surfaces in chain A T3 flavor; jaguar metaphor (T2 chain A) is on-tradition. | ⭐ **highest-coherence form.** Substrate (Aztec war-club macuahuitl) + named bearer (Moctezuma) + § 8 algorithm (RESOURCE_CONVERSION → blood-magic-rage) + Phase 5 narration ALL converge. Chain B variants ("Maelstrom/Dominion/Ascendant") show tier-appropriate climactic weight. The "Jade Fury" template-repeat is more acceptable here because chain A uses different vocabulary (Obsidian/Tempest/Warrior/Warlord) — within-form vocabulary variety preserved. |
| **form-030 Iron Shilpi Veer** | Shaping Strike → Kavacha Stance → Mandala Bind → Vishwakarma's Fury (chain A); Forge Golem Call → Golem's Iron Grasp → Golem Warden's Command → Golem Titan's Rampage (chain B). | ⭐ **substantively strong.** "Shilpi" (Sanskrit for craftsperson) + Kavacha (Vedic armor) + Mandala + Vishwakarma (Hindu divine craftsman) → Phase 5 LLM correctly resolved the south_asian cultural-tradition tag at narration layer. Wayland (Anglo-Saxon smith anchor) integrated as "Forged in Wayland's sacred fire... where ancient craft meets the dharma of devastation." This is the LLM doing a difficult cross-civilizational synthesis well at NARRATION layer. **However:** my prior pass's HIGH-severity flag (substrate = `.476 Nitro Express` 1880s British hunting cartridge bound to Wayland Anglo-Saxon smith with cultural_tradition=south_asian/classical metadata) **persists structurally.** Phase 5 papered it over (Nitro Express never surfaces in narration; "Iron" stands in); jack-ryan's `actual_winrate` semantics don't apply. The substrate-binding incoherence is what it was. |

### 2.3 Named-bearer attribution prominence — discipline check

Per spec § 4 #9 (NAMED_BEARER_PROMINENCE param, default "subtle"). Empirical observation across the 5 anchor-bearing forms sampled:

| Form | Bearer | Attribution pattern | Verdict |
|---|---|---|---|
| form-003 | Alexander the Great | Surfaces in T2 chain A flavor only ("Where Alexander's phalanx broke through with force..."); form name doesn't contain bearer | **subtle — appropriate** |
| form-008 | Moctezuma | Form name "Sunstone Spearthrower" doesn't contain bearer; form flavor mentions "Moctezuma's burning will"; skill flavor uses "Tonatiuh" sun-god name not "Moctezuma" | **subtle — appropriate; Tonatiuh substitution is a refined touch** |
| form-009 | Roland | Form name "Paladin of Durandal" contains weapon-name not bearer-name; subtle | **subtle — appropriate** |
| form-025 | Moctezuma | Form name "Moctezuma's Jade Warlord" contains bearer prominently; T3 flavor "Moctezuma's jade warriors" reinforces | **prominent — appropriate for highest-coherence anchor form** |
| form-030 | Wayland | Form name "Iron Shilpi Veer" doesn't contain bearer; form flavor "Forged in Wayland's sacred fire" mentions; skill names invoke other anchors (Vishwakarma) | **subtle — but cross-civilizational metadata tagging inconsistency persists** (south_asian/classical conflicts with Wayland=european_medieval) |

**Verdict on attribution prominence calibration:** **well-calibrated.** Named bearers surface where load-bearing (form-025 high anchor relevance) and recede where the substrate/cultural context can carry weight (form-003, form-008). This is a successful spec § 4 #9 outcome.

### 2.4 Cross-form thematic distinction — empirical check

Sampled four fire_mage forms with shared "Ember" naming convention (forms 012, 015, 016, 033):

| Form | Distinguishing metaphor | Skill-name signature |
|---|---|---|
| **012 Ember Arithmetician** | mathematical equations | Cinder Arc / Smoldering Calculus / Thermal Equation Lock / Conflagration Theorem |
| **015 Ember Academician** | manuscripts + familiar | Ember Familiar / Cinder Burst / Blazing Salvo / Inferno Salvo |
| **016 Ember Cartographer** | territory + boundary lines | Ember Step / Ashen Ward / Cinder Bind / Scorched Earth Seal |
| **033 Ember Scholiast** | annotations + marginalia | Smoldering Lexicon / Annotated Ember Codex / Blazing Marginalia / Infernal Tome Censure |

**Verdict:** ⭐ **genuinely distinct kit identities** with shared element vocabulary. The "scholarly fire_mage" archetype has been differentiated into four sub-archetypes (mathematician / scholar-with-familiar / cartographer / annotator) each with a distinct intellectual register. This is **substantively beyond what spec § 3.1 weight 0.30 minimally required** — Phase 5 LLM produced **genuine inter-kit narrative differentiation**, not just cohesion within kit. Strong result.

Compare bladedancer family (forms 2 + 7 + 17 + 27):

| Form | Archetype/role | Distinguishing pattern |
|---|---|---|
| **002 Menuki Bladedancer** | physical_warrior/damage | "Whirling Steel Dance", "Iron Petal Guard" — sacred-ornament-fist register |
| **007 Sadamune Bladedancer** | physical_skirmisher/damage | "Rushing Wind Step", "Flowing River Dash" — wind-water elemental register |
| **017 Menuki Phantom** | physical_skirmisher/damage | "Phantom Step Echo", "Ghost Blade Summons" — spectral-blade register |
| **027 Menuki Bladedancer** | physical_warrior/damage | "Whirling Steel Dance" + "Tempest Blade Rush" — overlaps 002 |

**Form 002 + Form 027 duplicate:** identical form name, identical form flavor text verbatim. Phase 5 spec did NOT address form-layer uniqueness (only skill-node uniqueness). Skill-node names diverge somewhat between the pair (002: Whirling Steel Dance / Iron Petal Guard / Tempest Blade Sovereign; 027: Whirling Steel Dance / Iron Petal Cyclone / Crimson Lotus Maelstrom), but kit identity at form level reads identical. **My prior pass § 2.6 flagged this; it persists.** Not a Phase 5 failure — Phase 5 did its scope; the form-name uniqueness gap was deferred per scope-doc and remains a future Phase-5-extension or composition-policy gate item.

**Verdict:** within-family distinction is **GOOD** for fire_mage Ember family, **MODERATE** for bladedancer Menuki family, **TIGHTLY-OVER-UNIFORMIZED** within form-022 Crimson Leaf Binder (every skill uses "Crimson Leaf X").

### 2.5 Cohesion-judge programmatic scoring vs gandalf subjective read — drift check

| Form | Cohesion-judge mean | gandalf subjective read | Agreement |
|---|---|---|---|
| form-000 Rampart Knight | high (multiple 1.000, several 0.95+) | ⭐ strong | ✅ agree |
| form-003 Khyber Shadow Dancer | mixed (0.708 to 0.970) | ⭐ strong | ✅ judge slightly under-rates |
| form-008 Sunstone Spearthrower | mostly 0.818-0.925 | ⭐ strong | ✅ agree |
| form-013 Ashen Geomancer | 0.703-0.843 | ⭐ strong narration, ⚠️ substrate misfit | ✅ judge correctly flags borderline (0.703 lowest) |
| form-018 Twilight Rod Sage | mostly 0.825-0.895 | ⭐ strong | ✅ agree |
| form-021 Galeborn Standard Bearer | 0.843-0.963 | ⚠️ naming-cohesion strong / algorithm misfit (out of Phase 5 scope) | ✅ judge correctly rates HIGH on naming (since judge doesn't evaluate algorithm fit) |
| form-022 Crimson Leaf Binder | 0.708-0.820 | ⚠️ over-uniformized | ✅ judge correctly rates lowest among samples — agreement |
| form-025 Moctezuma's Jade Warlord | 0.787-1.000 (multiple 1.000) | ⭐ highest-coherence | ✅ judge correctly rates highest — agreement |
| form-030 Iron Shilpi Veer | 0.708-0.970 | ⭐ strong cross-civ narration | ✅ judge agrees on most; lowest 0.708 (Golem's Iron Grasp) is borderline |

**Verdict:** **substantial agreement** between programmatic cohesion-judge and subjective design-fit read. The programmatic judge appropriately rates form-022 (over-uniformized) and form-013 (borderline lines) lower; rates form-025 (highest-coherence) highest. **No significant drift.** This is empirical validation of the spec § 3 cohesion rubric calibration.

### 2.6 Finding 1 verdict: **RESOLVED**

- Structural: all spec § 6 acceptance criteria met or exceeded
- Substantive: skill trees read as coherent kit identities (not 10 disconnected skills)
- Quality: named bearers surface at appropriate prominence; cross-form thematic distinction strong in some families (Ember fire_mages excellent)
- Calibration: programmatic cohesion-judge agrees with subjective design-fit read; no significant drift

**Residual MEDIUM-severity items NOT addressed by Phase 5 (deferred per scope):**
1. Within-kit vocabulary over-uniformization (form-022 Crimson Leaf X pattern) — could be addressed by an in-kit lexical-variety check; Phase 5 v1.1 spec item
2. Form-name uniqueness (form-002 + form-027 both "Menuki Bladedancer") — explicitly out of Phase 5 spec scope; composition-policy or Phase-5-form-layer-extension item
3. Substrate-binding misfits persist at substrate layer (form-013 Powder Tester, form-030 .476 Nitro Express + Wayland metadata trio) — Phase 5 narrative-papering masks but doesn't fix; substrate-tagging / composition-policy item for Cycle 13

These items do NOT change the RESOLVED verdict on Finding 1 — they are scoped-out residuals appropriately deferred per my prior pass § 4.6 v1.1+ queue.

---

## 3. Finding 2 — degenerate balance_metadata — FRAMING REFUTED

### 3.1 Empirical evidence — schema inspection

I independently inspected `balance_metadata` keys across v2_narrow vs v2_narrow_phase_5 vs legacy `season_001001`:

| Schema | balance_metadata keys |
|---|---|
| `season_001001` (legacy) | `actual_winrate` ✓, `target_winrate` ✓, `final_modifier` ✓, `convergence_iterations` ✓, `converged` ✓, `gauntlet_results` ✓ |
| `v2_narrow` (source) | `converged_modifier`, `engine_version`, `source_library`, `generation_seed`, `bc_target_cell`, `mechanical_substrate_triple`, `substrate_binding_relaxation_level`, `cell_routing_source`, `attribute_coupling`, `cultural_tradition`, `lineage`, `period`, `generation_params` — **NO `actual_winrate`, NO `convergence_iterations`, NO `converged`, NO `final_modifier`, NO `gauntlet_results`** |
| `v2_narrow_phase_5` (regen) | **IDENTICAL keys to v2_narrow** — Phase 5 modified `skills[].name/flavor_text/effects/phase5_*` only |

**Distribution check on the cited "all-0.5" fields across 35 forms of v2_narrow_phase_5:**

```
actual_winrate: Counter({None: 35})
convergence_iterations: Counter({None: 35})
final_modifier: Counter({None: 35})
converged: Counter({None: 35})
```

All 35 forms return `None` for these fields because **the fields are not in the v2 schema.** They do not exist to be 0.5.

**Distribution of the field that IS in the v2 schema (`converged_modifier`):** all 35 forms = `1.0`. This is a default-value emission from the substrate-binding step, NOT a balance-loop convergence output.

### 3.2 Empirical evidence — pipeline inspection

```bash
grep -n "BalanceLoop|balance_loop|run_balance|simulation|actual_winrate|gauntlet" \
    scripts/v1_narrow_generation_run_2026_05_25.py \
    scripts/v2_narrow_phase_5_generation_run_2026_05_25.py
# (no matches)
```

**Neither the v1_narrow generation script (which produced v2_narrow source) NOR the Phase 5 regen script invokes BalanceLoop, sim, or gauntlet.** The v2 engine emission pipeline is generation-only by structural design. The `BalanceLoop` class exists at `src/reincarnated/simulation/balance_loop.py` and is integrated in `season_orchestrator.py` for season generation paths, but the v1_narrow / v2_narrow_phase_5 scripts use the engine_v2 generation path that bypasses season_orchestrator's balance integration.

### 3.3 Where my prior pass § 3.7 finding came from

My prior pass cited the four fields with specific values:
- `final_modifier: 1.0`
- `convergence_iterations: 1`
- `converged: true`
- `actual_winrate: 0.5`
- `target_winrate: 0.5`

These are the default values for the loadout app's `BalanceMetadata` TypeScript interface (`src/data/types.ts` lines 35-41), which DOES define these fields and which the analytics hook `src/hooks/useAnalytics.ts` reads. When the loadout app loads a v2_narrow class with missing `balance_metadata.actual_winrate`, the field is `undefined` (not 0.5) at TypeScript level — but the loadout app's analytics path may coerce / null-guard these into defaults, OR the field was reported via a non-strict inspection.

**This was a prior-pass attribution error on my part.** The narrative ("35 forms with identical 0.5 win-rate, 1 iteration, modifier=1.0") was constructed against the loadout-side schema, not the engine emission schema. The legacy `season_001001` schema (which retained these fields with real variation 0.4767-0.6567, real iterations 1-9) is the ONLY artifact that has populated values for these fields, because legacy season generation invoked BalanceLoop. v2 generation does not.

### 3.4 The escalation path collapses

The invocation brief enumerated three candidates for "deeper issue if all-0.5 persists":
- **Layer 3 skill generator** (skills different in name but mechanically equivalent → invariant violation at L3)
- **Phase 3 convergence** (trivial convergence loop in balance pipeline)
- **Gamora sim integration** (sim doesn't react to skill content — only stats)

Empirical refutation by candidate:

| Candidate | Verdict on this run |
|---|---|
| L3 skill generator producing mechanically-equivalent skills | **REFUTED.** Skill mechanical fields show real variance: `damage_multiplier` ranges 1.05 → 1.249 with many unique values; `cooldown_seconds` and `energy_cost` vary; `bc_axis_contribution` per-axis values are non-uniform per skill. L3 IS producing differentiation. |
| Phase 3 convergence trivial | **NOT EVALUABLE on this run.** Phase 3 convergence is a balance-loop concept that operates on the BalanceLoop output. BalanceLoop didn't fire on v2_narrow_phase_5 generation, so Phase 3 didn't fire either. Cannot say convergence is trivial; can only say convergence didn't run. |
| Gamora sim integration absent | **CONFIRMED — structurally.** The v2 engine generation pipeline does not invoke sim. Not a bug; not a "didn't react" — sim simply isn't in the pipeline. |

Of the three candidates, the only empirically-supported one is **gamora sim integration is structurally absent from v2 generation runs.** And this is by design, not by failure — the v2 engine produces forms; sim is a separate concern that the legacy season pipeline integrated and the v2 generation pipeline does not (yet).

### 3.5 Finding 2 verdict: **FRAMING REFUTED; reframed as Cycle 13 architecture decision**

Per scope-doc § 5 escape-hatch protocol, the verdict on "PERSISTS / RESOLVED / AMBIGUOUS-PENDING-SIM-RERUN" is:

**The question as posed presupposed an architecture that does not exist.** The verdict is NOT "PERSISTS" (would imply sim ran and produced all-0.5 — empirically refuted; sim did not run). The verdict is NOT "RESOLVED" (would imply Phase 5 fixed the all-0.5 outcome — empirically refuted; the fields don't exist in v2 schema to be 0.5). The verdict is NOT "AMBIGUOUS-PENDING-SIM-RERUN" (would imply a sim re-run could discriminate — empirically refuted; the v2 pipeline does not invoke sim at all, and no rocket regen of v2_narrow_phase_5 with sim added is an architectural change, not a re-run).

**The actual reframed verdict:** Cycle 12 closes on Finding 1 alone (placeholder issue RESOLVED). Finding 2 dissolves into a **Cycle 13 architecture decision Matt should signal on:**

| Question | Cycle 13 candidate response |
|---|---|
| Is the v2 engine intentionally generation-only? | Plausible per substrate-led discipline — substrate + generation + Phase 5 narration is the engine seam; sim is a separate concern. |
| Should v2 forms be sim-evaluable downstream? | If YES → Cycle 13 scope: route v2 forms into BalanceLoop adapter post-generation OR teach v2 schema to carry sim-output fields when sim is run on emitted forms. |
| Was the legacy season schema's sim integration a feature to preserve or a coupling to break? | Matt design call — legacy season pipeline had `gauntlet_results`, `convergence_iterations`, `actual_winrate` populated by integrated balance loop. v2 separated this. The separation may be intentional Architecture B partitioning OR an inherited gap. |

**Empirical-evidence criterion for re-engagement on Finding 2:** Matt design signal on whether v2 forms need sim integration as part of the v2 cycle. If YES, a Cycle 13 scope-doc proposes the integration architecture; gamora's seam owns the sim execution; star-lord owns the export-schema extension to carry sim outputs back into the v2 emission. If NO, the Finding-2 question retires permanently.

---

## 4. Per-option assessment (composition with knight-rider routing)

| Forward routing branch | Decision | Reasoning |
|---|---|---|
| **Both RESOLVED → cycle closes; T4 post-mortem unblocked; milestone tag fires after WARN remediation** | ✅ **PARTIALLY APPLIES** | Finding 1 RESOLVED. T4 post-mortem session 1 unblocked. Milestone tag `v2.0-phase-5-skill-node-naming` fires after rocket WARN remediations land per jack-ryan Gate-2 verdict § 4. |
| **Finding 1 RESOLVED + Finding 2 PERSISTS → escalate to KR per scope-doc § 5: deeper-issue investigation among 3 candidates** | ❌ DOES NOT APPLY | Finding 2 doesn't PERSIST (would imply sim ran and produced all-0.5); the fields cited don't exist in v2 schema. The 3-candidate escalation collapses to a single empirical fact: sim is structurally absent from v2 generation. |
| **Finding 1 RESOLVED + Finding 2 AMBIGUOUS → recommend specific empirical test (sim re-run with new skill content) before escalation** | ❌ DOES NOT APPLY | A sim re-run is an architectural change (adding sim to v2 pipeline), not a re-run of existing infrastructure. Cannot discriminate by adding capability that doesn't exist. |
| **NEW BRANCH — Finding 1 RESOLVED + Finding 2 FRAMING REFUTED → Cycle 12 closes on Finding 1; Finding 2 reframes as Cycle 13 architecture decision** | ✅ **APPLIES** | This is the empirically-supported routing. Matt signal needed on whether v2 forms need sim integration in Cycle 13. |

---

## 5. Ranked recommendation

| Tier | Action | Owner | When |
|---|---|---|---|
| **Tier 1 — must fire** | Cycle 12 closes on Finding 1 RESOLVED. Knight-rider routes forward to T4 post-mortem session 1 readiness. Milestone tag `v2.0-phase-5-skill-node-naming` fires after rocket's 2 WARN remediations land. | knight-rider | post this verdict |
| **Tier 1 — must fire** | This design-fit pass note is captured at `agentic_orchestration/gandalf/notes/2026-05-25-phase-5-regen-design-fit-pass.md` for downstream-consumer access (Matt review; T4 post-mortem session 1 inputs; Cycle 13 scope-doc anchor). | gandalf (self) | this session |
| **Tier 2 — primary path** | Matt signals on the reframed Finding 2 question: **does v2 engine need sim integration in Cycle 13, or is generation-vs-sim partitioning intentional?** This decision unlocks Cycle 13 scope-doc authoring. | Matt → knight-rider | next workstream gap |
| **Tier 2 — primary path** | T4 post-mortem session 1 substantively evaluates skill-tree feel using v2_narrow_phase_5 output. Matt can now read 35 named kits with coherent skill trees and produce hand-authored alternatives per my prior pass § 5 agenda Block 3. Note that fight-behavior evaluation (the prior pass § 5 Block 4 candidates) remains gated on the Cycle 13 architecture decision. | Matt + gandalf | next sustained design session |
| **Tier 3 — supplement** | Add to my prior pass § 4.6 v1.1+ queue: residual Phase-5 items surfaced by this design-fit read — (a) within-kit lexical-variety check to address form-022-style vocabulary collapse; (b) form-layer uniqueness gate to address form-002/form-027 duplicate-name pattern. | gandalf (Cycle 13 scope-doc) | post-Matt-signal on Finding 2 reframing |
| **Reserve** | If Matt signals v2 needs sim integration → Cycle 13 scope-doc proposes architecture; jack-ryan + gamora + star-lord + rocket cross-seam pass. If Matt signals v2 stays generation-only → Finding 2 retires; sim is a separate downstream cycle. | knight-rider | scoping after Matt signal |
| **Reject** | The original Finding-2 escalation path (L3 skill generator investigation / Phase 3 convergence investigation / gamora sim integration investigation as parallel candidates). Empirically, only the gamora-integration candidate has substance, and it's a structural-absence observation not a bug-to-investigate. | — | — |

---

## 6. Decisions-log proposal

**Proposed entry candidate** (per gandalf OP § 3.2 + reincarnated-decision-log-format skill — gandalf proposes; routes via knight-rider; jack-ryan authors after Matt approval):

> **2026-05-25 — v2 engine generation-vs-sim partitioning surfaced as architecture decision deferred to Cycle 13**
>
> **Decision:** TBD — Matt signal required.
>
> **Reasoning:** The v2 engine emission pipeline (v1_narrow → v2_narrow → v2_narrow_phase_5) does not invoke BalanceLoop / gauntlet / sim. The legacy season pipeline did. The v2 schema does not carry `actual_winrate`, `convergence_iterations`, `final_modifier`, `converged`, or `gauntlet_results` fields. This is a structural property of v2 engine architecture, surfaced by gandalf design-fit pass on Phase 5 regen output 2026-05-25.
>
> **Alternatives considered:**
> - Option A: v2 stays generation-only; sim is a separate downstream cycle invoked on emitted v2 forms by a separate gamora pipeline.
> - Option B: v2 integrates sim as part of generation (legacy season pipeline pattern); schema extends to carry sim outputs.
> - Option C: hybrid — v2 generation emits forms; an optional `--with-sim` flag triggers BalanceLoop run; schema-extension is opt-in per emission.
>
> **Status:** OPEN — pending Matt signal in Cycle 13 scoping.
>
> **Related:** `agentic_orchestration/gandalf/notes/2026-05-25-phase-5-regen-design-fit-pass.md`, `agentic_orchestration/gandalf/notes/2026-05-25-engine-generation-special-case-summary.md` § 3.7, `canonical/story/phase-5-cohesion-judge-calibration-spec-2026-05-25.md` § 7 (explicitly noted "Per-form sim re-run after Phase 5 names land — implementation decision; if names don't affect mechanics, sim is independent" — the spec recognized this scope gap)

**This entry is GANDALF PROPOSAL ONLY.** Routing: knight-rider relays to Matt for signal; jack-ryan authors the canonical decisions-log entry after Matt-approval per ADR-002 tiered approval.

---

## 7. Composition with prior framing

### 7.1 What my prior pass got right

- Finding 1 (placeholder issue): correctly identified, scoped, and gated on Phase 5 spec authoring → rocket regen → re-check. Empirical resolution path executed exactly per the plan.
- Substrate-binding misfits (form-013 Powder Tester, form-030 Wayland + Nitro Express): correctly identified at substrate-tagging layer; correctly noted that Phase 5 narrative-coalescence might paper over but not fix.
- The duplicate form-name pattern (form-002 + form-027): correctly identified as a Phase 5 calibration gap requiring future address.
- The L9 algorithm-vs-class-fantasy misfit (form-021 Galeborn): correctly identified as a § 8 algorithm-amendment item beyond Phase 5 scope.

### 7.2 What my prior pass got wrong — pre-imposed assumption failure

The Finding 2 framing (§ 3.7 "all 35 forms identical 0.5 win-rate, 1 iteration, modifier=1.0; with placeholder skills, kits can't meaningfully differentiate → no observable fight-behavior variance") **inherited the legacy season schema's mental model and projected it onto v2 output without verifying the v2 schema carries those fields.** This is precisely the failure mode the framing-audit checklist (gandalf OP § 4.1) is designed to catch — Q2 evidence (v2 schema doesn't carry those fields) was surfaceable from current scope and would have refuted the framing before Phase 5 spec authoring positioned itself as "the gating piece for meaningful fight-behavior signal" (spec § 1.3 verbatim).

**The spec § 1.3 framing did not become FALSE** (Phase 5 IS necessary for skill-tree feel evaluation, which IS the primary T4 post-mortem use case). But the spec's framing **OVERSTATED** by including "meaningful fight-behavior differentiation" as a Phase 5 deliverable. Spec § 7 partially corrected this with the note "Per-form sim re-run after Phase 5 names land — implementation decision; if names don't affect mechanics, sim is independent." But the framing brief and prior design-fit pass both still operated as if Finding 2 was a Phase-5-resolvable item.

**Discipline observation (for OP § 4 amendment candidate):** **prior-pass-finding inheritance is a framing-audit risk pattern.** When a downstream pass inherits a finding from an upstream pass, the inheriting pass should re-apply Q2 (refutation evidence) on the inherited finding, not just on the new work. The inherited "all-0.5 win-rate" finding should have been re-verified against v2 schema during Phase 5 spec authoring (when I authored the spec) and again during this design-fit pass (when I executed against the regen). The pattern: **inherited findings deserve fresh Q2 audit; treat them as new assumptions, not as established facts.**

### 7.3 Empirical-evidence criterion for Cycle 13 architecture decision

Per recognition-validate-commit discipline (OP § 3.4): **recognition** is captured here (v2 generation-vs-sim partitioning is structural, surfaced 2026-05-25). **Validation** gating commits to a Cycle 13 architecture choice = (a) Matt design signal on Option A / B / C above; (b) if Option B or C: cross-seam round-trip (gamora + star-lord + rocket) to evaluate cost and architectural fit; (c) jack-ryan engineering-disciplines review on the schema extension. **Commit** fires when Matt approves the Cycle 13 architecture scope-doc.

---

## 8. Sign-off

**Author:** gandalf 2026-05-25 (Pattern A-deep substantive design-fit verdict, autonomous fire per Matt 2026-05-25 routing chain pre-authorization)
**Status:** RATIFIED — design-fit verdict authored; routing recommendation to knight-rider for Cycle 12 closeout + Cycle 13 scope-doc framing
**Effort:** ~90 min autonomous (within Pattern A-deep budget)

**Disciplines applied:**
- gandalf OP § 4.1 framing-audit (caught the prior-pass inherited-assumption failure on Finding 2)
- gandalf OP § 3.1 push-back-hard (refusal to accept the original Finding-2 framing; refusal to escalate against an empirically-absent architecture)
- gandalf OP § 3.4 recognition-validate-commit (Cycle 13 architecture decision deferred pending Matt signal + empirical validation)
- gandalf OP § 3.2 Mathematical Layer routing (Finding 2 reframing is a structural / architectural observation, not a math-hotspot; no methodology consultation required)
- gandalf OP § 3.5 NO sleep recommendations (verified absent)
- gandalf OP § 3.6 timezone-agnosticism (verified absent — only workstream-relative framing throughout)

**Downstream consumers:**
- knight-rider — route forward per § 5 ranked recommendation Tier 1; relay decisions-log entry candidate to Matt
- Matt — review verdict; signal on Finding 2 reframing (Option A / B / C); confirm T4 post-mortem session 1 readiness signal; signal milestone tag fire after rocket WARN remediations
- rocket — proceed with 2 WARN remediations per jack-ryan Gate-2 § 4; targeted re-smoke (form-015 + form-032 within-form uniqueness gate); MIGRATION.md uniqueness-metric clarification
- jack-ryan — author canonical decisions-log entry after Matt signal on Cycle 13 architecture (per decision-log-format skill)
- gandalf (self) — author Cycle 13 sub-cycle scope-doc on form-uniqueness + within-kit lexical-variety per § 5 Tier 3 recommendation, post-Matt-signal

**Cross-references:**
- `canonical/story/phase-5-cohesion-judge-calibration-spec-2026-05-25.md` (spec authorship)
- `agentic_orchestration/gandalf/notes/2026-05-25-engine-generation-special-case-summary.md` (prior pass)
- `agentic_orchestration/qa/findings/2026-05-25-phase5-skill-node-naming-gate2-findings.md` (jack-ryan Gate-2)
- `agentic_orchestration/cycles/cycle-12-hive-mind-scope.md` § 5 escape-hatch protocol (invocation context)
- `/Users/admin/Games/reincarnated-engine/exports/v2_narrow_phase_5/classes.json` (regen output; load-bearing evidence)
- `/Users/admin/Games/reincarnated-engine/scripts/v2_narrow_phase_5_generation_run_2026_05_25.py` (regen script; empirical refutation of Finding-2 framing)
- `/Users/admin/Games/reincarnated-loadout/src/data/types.ts` § BalanceMetadata (legacy-schema field source — where my prior pass inherited the field list)
