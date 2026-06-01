# WS1A.Q18 Flavor-Pool Research-and-Lock Hive-Mind Wave

**STATUS:** CURRENT (operational sequence ratified 2026-06-01)
**Date:** 2026-06-01
**Author:** gandalf (story-and-design steward) per Pattern B session 2026-06-01
**Authority:** Matt 2026-06-01 ratifications:
  - "ratify hive-mind path; author the operational sequence"
  - "Can we not have this made into one long hive mind wave? This would be my leaning to do so (wave with all sessions as gated phases if needed)." (wave-shape framing)
**Workstream tag:** `WS1A.Q18-flavor-pool-research`
**Hive-mind framing:** WS1A.Q18 single-wave hive-mind cycle (5 phases internally gated) — sets composition pattern for Q16/Q17/Q19 wave structures
**Companion docs:**
- `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md` § 1.7 + § 8b Q18 (parent question)
- `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md` § 5.2 (WS1A gate sequence)
- `agentic_orchestration/operating-procedures/hive-mind-protocol.md` (composition target)
- `canonical/00-ground-state.md` § 1 (WS1A architectural foundations active workstream)

---

## 0. TL;DR + purpose

WS1A.Q18 asks: **for each of the 8 canonical primary elements (fire / water / earth / wind / lightning / holy / shadow / physical), what locked sub-element / flavor-element allow-list represents the kit-identity vocabulary that WS1A.3 (per-kit sub-element selection) and WS1A.4 (per-skill bounded LLM flavor judgment) consume?**

**Wave shape:** single hive-mind wave with 5 phases gated internally. Wave-open dispatch fires once; phases execute sequentially with internal parallelism (Phase 1 spawns 3 samplers in parallel; Phase 3 spawns ≤6 expansion sub-agents in parallel). Wave-close criterion: locked canonical doc + jack-ryan Gate-2 PASS. Gandalf phase-gate ratifications fire as in-wave sub-agent invocations, not as session-end gates.

The locked artifact at wave-close is a CURRENT canonical doc at `canonical/story/2026-06-XX-flavor-pool-per-primary-element-lock.md` carrying:
- 7-vs-8 empirical decision (does physical have a sub-element allow-list, or not?)
- Per-primary curated allow-list (target floor ~12-15 entries per rotating primary)
- Q18.a-e structural decisions (primary scope; source of authority; flex semantics; d1_status filter; cardinality target)
- Research provenance trail (3 tracks × 8 primaries empirical inventory)
- Operational-migration dispatch hook for extending `data/seasonal_elements/pool.json`

**Empirical state at session-open (2026-06-01):** the existing `data/seasonal_elements/pool.json` (156 entries; 60 allow-list) covers only 4 primaries (earth/fire/water/wind) at asymmetric cardinality (22/20/11/7); lightning/holy/shadow have ZERO flavor entries; physical absent by design (open empirical question). Matt's iter 2 mental model already references entries that aren't in the pool (bone for earth; umbra for shadow). The pool needs research-grounded expansion before lock, not designer-assertion expansion.

**Methodology principle (substrate-led applied to vocabulary):** the locked allow-list per primary emerges from genre-precedent vote count + statistical analysis + design curation. Prior pool authoring was exploratory; this cycle grounds the lock empirically. Mirrors the P2/P3 substrate-axis discovery methodology pattern at the vocabulary layer.

---

## 1. Workstream identity

| Property | Value |
|---|---|
| Wave name | WS1A.Q18 flavor-pool research-and-lock wave |
| Wave shape | Single hive-mind wave; 5 phases gated internally; sub-agent parallelism within phases |
| Substrate | `data/seasonal_elements/pool.json` (existing) + `config/elements.yaml` (canonical-7+1) + research synthesis (new) |
| Commissioner | gandalf (story-and-design steward) |
| Wave orchestrator | knight-rider (wave-state file + dispatch authoring + phase-gate sequencing) |
| Critique-pair | jack-ryan Gate-1 (on wave-open + phase dispatches as KR authors them) + Gate-2 (on Phase 5 canonical write at wave-close) |
| Cost bound | Single wave; ≤ 1 (Phase-0 elrond) + 3 (Phase-1 samplers) + ≤ 6 (Phase-3 expansion) + 1 (Phase-4 elrond) sub-agent fan-outs; gandalf phase-gates fire as ≤4 sub-agent invocations |
| Architectural-commitment level | Vocabulary-lock; requires Matt sign-off per ADR-002 tiered approval at Phase 5b |
| Composition with WS1A | Hard-blocker for WS1A.3 (per-kit sub-element selection) and WS1A.4 (per-skill flavor judgment); pattern-sets Q16/Q17/Q19 wave structures |
| Composition with hive-mind protocol | Full wave-state-file maintenance per `operating-procedures/hive-mind-protocol.md`; decision routing per Matt 2026-05-23 directive (seam-owners decide in-scope; Matt last-resort) |
| Wave-close criterion | Canonical write committed at `canonical/story/2026-06-XX-flavor-pool-per-primary-element-lock.md` + jack-ryan Gate-2 PASS + 00-ground-state.md § 1 update + 02-roadmap.md update |

---

## 2. The 5-phase wave structure

**Wave-open trigger:** KR authors wave-open dispatch citing this operational sequence; wave-state file initialized at `agentic_orchestration/cycle-15-ws1a-q18-flavor-pool-research/wave-state.md`; Phase 0 fires immediately.

**Phase-gate discipline:** each phase produces an artifact that gates the next phase. Gandalf phase-gate ratifications fire as in-wave sub-agent invocations (Pattern A-light verdicts returned to wave); they are NOT session-end / session-resume gates. The wave runs end-to-end as a single orchestrated unit.

### Phase 0 — Pre-wave elrond data-medium consultation

**Owner:** elrond (data steward seam)
**Pattern:** single-question consultation; in-wave sub-agent invocation
**Trigger:** KR wave-open dispatch routes pre-wave consultation question to elrond as Phase-0 sub-agent invocation

**Question to elrond:**
> Per the WS1A.Q18 research cycle (5-step sequence-then-parallel; gandalf-commissioned; legolas executes via 3 parallel samplers then up to 6 expansion sub-agents), the captured dataset shape is:
> - per-candidate × per-primary × per-source × per-track records
> - fields include: candidate keyword string, primary element, source citation, recognizability score (1-3), substrate type tag, cross-primary contamination flag
> - estimated size: 200-800 rows total across 8 primaries
> - downstream consumer: elrond statistical analysis at Phase 4
>
> What medium do you recommend for legolas's sub-agent samplers to author into? Options:
> (E.α) Python notebook + Parquet/CSV
> (E.β) substrate DB extension with new `element_flavor_candidates` table
> (E.γ) flat JSON authored by samplers + pandas/numpy stats at Phase 4
>
> Constraint: medium choice should support Phase 3 incremental writes (samplers + expansion sub-agents emit rows continuously) and Phase 4 statistical analysis (frequency distributions, contamination matrix, cluster analysis, cardinality recommendations).

**Output:** elrond names the medium + format spec at `agentic_orchestration/elrond/consultations/2026-06-XX-q18-flavor-pool-data-medium.md`

**Phase-gate criteria:** medium decision binds before Phase 1 fires. Legolas's sub-agent prompts (drafted in Appendix A below) get medium-specific output instructions inserted post-elrond-response. KR confirms wave-state file updated with elrond's medium-spec before Phase-1 dispatch authoring.

---

### Phase 1 — Parallel sample (3 sub-agents fan-out from legolas)

**Owner:** legolas (Mode A seam — commissioner + coordinator)
**Sub-agents spawned:** Sampler-A, Sampler-B, Sampler-C (concurrent invocation)
**Pattern:** legolas spawns the 3 samplers in a single multi-agent invocation; samplers execute web research in parallel; outputs return to legolas

**Sub-agent briefs:** see Appendix A for full sub-agent prompt drafts

| Sub-agent | Track | Sources (target) | Per-primary sample target |
|---|---|---|---|
| Sampler-A | ARPG canon | D1/D2/D3/D4/Immortal + PoE 1+2 + Last Epoch + Grim Dawn + Lost Ark + Torchlight 2/Infinite + Wolcen/Chronicon/Titan Quest | 5-10 candidate keywords surfaced per primary |
| Sampler-B | JRPG / isekai / anime canon | Final Fantasy series + Persona/SMT + Mushoku Tensei + KonoSuba + Slime + Solo Leveling + Overlord + Tower of God/Berserk/Black Clover | 5-10 per primary |
| Sampler-C | Tabletop + mythological + alchemical | D&D 5e + Pathfinder + MTG color pie + Wu Xing + Western alchemical + folklore/mythology focused on lightning/holy/shadow gap | 5-10 per primary |

**Sample report format (per sub-agent):**

Authored at `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-XX/sample-<A|B|C>.md` (or to elrond-named medium):

1. **Raw inventory** — per primary, list of candidates with: keyword, source citation, recognizability score (1=niche / 2=common / 3=ubiquitous), substrate type tag (material / phenomenon / proper-noun / mythological / mechanical-keyword / etc.), cross-primary flag
2. **Source coverage breadth** — which sources yielded strong signal; which were sparse; which were misaligned with sub-agent scope
3. **Per-primary yield score** — qualitative `STRONG` / `MEDIUM` / `WEAK` / `MISALIGNED` per primary
4. **Substrate-tagging gaps observed** — keywords with heavy cross-primary contamination
5. **Sub-agent continue/stop/expand recommendation per primary** — sub-agent's read on whether deeper research in this track on this primary yields more

**Bound:** parallel fan-out; samplers complete concurrently. Sampler is a *sampler*, NOT exhaustive inventory.

**Phase-gate:** none at Phase 1 close (Phase 2 fires automatically once all 3 samplers return — legolas absorbs reports in-wave)

---

### Phase 2 — In-seam analysis + triage verdict (legolas alone)

**Owner:** legolas (analyzer role)
**Pattern:** legolas absorbs all 3 sample reports in-wave; produces triage verdict

**Output:** `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-XX/sample-triage.md`

Carries:
1. **Track-viability matrix (8 × 3):** 8 primaries × 3 tracks; per cell: `STRONG` / `MEDIUM` / `WEAK` / `MISALIGNED`
2. **Per-track keep/drop/narrow recommendation** with reasoning anchored on yield evidence
3. **Per-primary preliminary cross-source contamination report** — keywords appearing in multiple primaries; flex-candidates surfaced
4. **Content/constraint/alignment issues per Matt's framing:**
   - Constraint: source-X anti-pattern vocab (e.g., over-religious-coded for holy)
   - Alignment: track-X off-Reincarnated-positioning (e.g., overly grim-dark for isekai-provisional tone)
   - Content: track-primary cells with zero useful yield
5. **Scope-adjustment proposal for Phase 3:**
   - **EXPAND** — track × primary cells with strong signal + remaining gap
   - **TERMINATE** — track × primary cells with weak signal or misalignment
   - **NARROW** — track × primary cells with deep yield but pre-conditioned scope
6. **Preliminary 7-vs-8 signal** — does Sampler-A/B/C output reveal physical-sub-element vocabulary emerging, or does the candidate pool collapse?

**Phase-gate 1 (in-wave):** KR routes Phase-2 triage verdict to gandalf as Pattern A-light sub-agent invocation; gandalf returns ratification verdict within the wave.

**Pattern A-light critique exchange (gandalf):**
- Confirm/dissent each EXPAND/TERMINATE/NARROW recommendation
- Surface any design-side override (e.g., if legolas terminates a track for "weak signal" but gandalf judges the signal substrate-honest as a "this primary genuinely has thin vocab" — preserve as data point)
- Lock the soft cap at 6 expansion sub-agents (over-cap requires gandalf re-ratification per Q-shape-3)

**Phase-gate-1 output:** `agentic_orchestration/gandalf/notes/2026-06-XX-q18-gate-1-triage-ratification.md` (brief — Pattern A-light scope; ratifies Phase 3 scope; returned to wave for KR to author Phase-3 dispatches)

---

### Phase 3 — Adaptive-scope full research (parallel within Phase-gate-1 scope)

**Owner:** legolas (commissioner + coordinator)
**Sub-agents spawned:** ≤ 6 expansion sub-agents (Phase-gate-1-bounded; soft-cap)
**Pattern:** for each Phase-gate-1-EXPAND cell, legolas spawns a deeper-research sub-agent; TERMINATE cells skip; NARROW cells run within Phase-gate-1-bounded scope

**Expansion sub-agent shape:** each focused on 1-2 primaries × 1 track at the full depth Phase-gate-1 ratified

**Output per expansion sub-agent:** `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-XX/full-<track>-<primary>.md` (or to elrond-named medium)

Each carries:
- **Full candidate inventory** per primary (Phase-gate-1-bounded)
- **Source citations** per candidate
- **Recognizability score** per candidate (1-3)
- **Substrate type categorization**
- **Cross-primary contamination flag** per candidate
- **Suggested ranking** within primary (sub-agent's read on which candidates are strongest)

**In-flight phase-gate-1.5 (over-cap or NARROW→EXPAND amendment):** if during Phase 3 a sub-agent surfaces unexpected yield evidence (e.g., a NARROW-scoped cell suddenly producing strong signal), legolas pauses the sub-agent and surfaces an in-flight amendment to gandalf via KR-mediated sub-agent invocation. Gandalf returns ratification (extend / hold original scope). Wave continues without exit.

**Phase-gate at Phase 3 close:** none formal (Phase 4 fires automatically once all Phase-gate-1-ratified expansion sub-agents complete; legolas signals KR to fire Phase 4 dispatch)

**Bound:** ≤ 6 sub-agents fanned out (parallel); soft cap binds without gandalf re-ratification

---

### Phase 4 — Elrond statistical analysis

**Owner:** elrond (data steward + statistical analysis seam)
**Pattern:** elrond absorbs the full research dataset (Phase 1 + Phase 3 outputs) in-wave; runs statistical analysis per medium-format from Phase 0; produces stats verdict

**Output:** `agentic_orchestration/elrond/analysis/element-flavor-mapping-stats-2026-06-XX.md` + raw data artifact at elrond-named medium

Carries:
1. **Per-primary candidate frequency distribution** — count of how many sources cite each candidate; weighted by track + recognizability score
2. **Cross-primary contamination matrix** — which candidates show flex behavior; how strongly
3. **Cluster analysis on candidates per primary** — do candidates fall into sub-categories (e.g., earth → materials cluster + minerals cluster + organic cluster + structural cluster)?
4. **Cardinality recommendations** — for each primary, what's the empirically-supported floor cardinality given the survived pool?
5. **Track-source weighting validation** — how much did each track contribute; was track-balance achieved or did one dominate?
6. **7-vs-8 empirical answer** — physical sub-element vocabulary cluster meaningfully, or does the candidate-frequency distribution collapse?
7. **Statistical confidence per primary** — for primaries with sparse research yield, name the confidence-degradation explicitly

**Phase-4 contingency (per framing-audit):** if Phase 0 elrond consultation surfaces data shape too qualitative for statistical analysis (e.g., narrative-heavy recognizability), Phase 4 collapses into a lighter "data-shape verification + cross-source agreement audit" without full statistical analysis. Decision routes to gandalf via in-flight amendment; wave continues without exit.

**Phase-gate 2 (in-wave):** KR routes Phase-4 stats verdict to gandalf as sub-agent invocation; gandalf returns ratification — dataset sufficient to proceed to Phase 5 OR Phase-3 amendment-loop fires (routes back to Phase 3 with additional expansion sub-agents).

**Phase-gate-2 output:** `agentic_orchestration/gandalf/notes/2026-06-XX-q18-gate-2-stats-ratification.md`

---

### Phase 5 — Gandalf synthesis + Matt-ratification + canonical write (wave terminus)

**Owner:** gandalf (synthesis + canonical authoring)
**Pattern:** gandalf integrates research + stats + design judgment + existing-pool audit in-wave; produces draft synthesis; Pattern B session with Matt ratifies; final canonical write fires; wave-close sequence

**Sub-phase 5a — Draft synthesis:**
- Author `agentic_orchestration/gandalf/notes/2026-06-XX-q18-flavor-pool-research-synthesis.md`
- Carries: per-primary allow-list recommendation (curated from research+stats); 7-vs-8 verdict (anchored on stats); Q18.a-e structural decisions (anchored on evidence); existing-pool audit (preserve/demote/extend per entry); composition with `data/seasonal_elements/pool.json` migration

**Sub-phase 5b — Matt-ratification Pattern B (Phase-gate 3 = wave-terminus architectural commitment):**
- gandalf walks Matt through synthesis; Pattern B substantive design call (this IS the Pattern-B engagement Matt has with gandalf for the wave; the rest of the wave runs orchestrated)
- Matt lock decisions on: 7-vs-8; Q18.a-e (primary scope; source of authority; flex semantics; d1_status filter; cardinality target); per-primary allow-list final curation
- Phase-gate 3 = Matt ratifies the lock (ADR-002 architectural commitment scope)

**Sub-phase 5c — Final canonical write:**
- Author `canonical/story/2026-06-XX-flavor-pool-per-primary-element-lock.md`
- STATUS: CURRENT; load-bearing; cross-references to hypothesis-flow architecture + canonical-7+1 + seasonal-pool migration
- Update `canonical/00-ground-state.md` § 1 — add new CURRENT entry
- Update `canonical/02-roadmap.md` — move WS1A.Q18 to closed

**Sub-phase 5d — jack-ryan Gate-2 wave-close review** (process discipline; CRITIQUE-PAIR; this IS the wave-close criterion):
- jack-ryan reviews the canonical write per Gate-2 protocol; BLOCK authority on drift / math-before-code violations / cross-seam impact unaddressed
- Standard Gate-2 INFO/WARN/BLOCK verdicts apply
- Gate-2 PASS = wave closes; Gate-2 BLOCK = amendment cycle re-fires sub-phase 5c

**Sub-phase 5e — Wave-close + design-quality audit:**
- KR authors wave-close record at `canonical/story/2026-06-XX-ws1a-q18-flavor-pool-wave-close-record.md` per wave-close discipline
- gandalf design-quality audit per OP § 4.6 (Discipline #43 candidate; A1-A5 questions; PASS / PASS-with-design-concerns / DRIFT-DETECTED)
- WS1A.Q18 wave CLOSED

**Sub-phase 5f — Operational migration dispatch (POST-WAVE):**
- KR authors operational dispatch extending `data/seasonal_elements/pool.json` per the lock
- elrond + star-lord surface touches (pool migration; d1_status updates; downstream consumer updates)
- This dispatch executes OUTSIDE the WS1A.Q18 wave; wave is closed; migration is downstream composition

---

## 3. Phase-gates + responsibilities matrix

All phase-gates fire WITHIN the wave (in-wave sub-agent invocations or in-wave Pattern B). The wave runs end-to-end as a single orchestrated unit; gates do NOT exit the wave.

| Phase-gate | Trigger | Who decides | Scope | Output artifact |
|---|---|---|---|---|
| PG-0 | Pre-Phase-1 | elrond | Data medium for research dataset | `elrond/consultations/2026-06-XX-q18-flavor-pool-data-medium.md` |
| PG-1 | Post-Phase-2 (sample triage) | gandalf | Phase-3 scope adjustment (expand/terminate/narrow); soft cap ≤6 sub-agents | `gandalf/notes/2026-06-XX-q18-gate-1-triage-ratification.md` |
| PG-1.5 | In-flight Phase-3 amendment | gandalf | Over-cap or NARROW→EXPAND mid-research | In-flight Pattern A-light reply (in-wave) |
| PG-2 | Post-Phase-4 (elrond stats) | gandalf | Dataset sufficient to proceed to synthesis; OR route additional Phase-3 expansion | `gandalf/notes/2026-06-XX-q18-gate-2-stats-ratification.md` |
| PG-3 (architectural-commitment) | Post-sub-phase-5b (Pattern B session) | Matt | Final lock per Q18.a-e + 7-vs-8 + allow-list per primary | Ratified in Pattern B; canonical write fires |
| PG-4 (process gate; wave-close criterion) | Post-sub-phase-5c (canonical write) | jack-ryan | Gate-2 INFO/WARN/BLOCK on canonical write | `qa/findings/2026-06-XX-q18-flavor-pool-lock-gate-2.md` |

**Decision routing per hive-mind directive Matt 2026-05-23:**
- Seam-owners decide in-scope per their seam authority
- gandalf decides design-side scope (PG-1, PG-1.5, PG-2)
- elrond decides data-medium scope (PG-0)
- jack-ryan decides process-gate scope (PG-4 = wave-close criterion)
- Matt decides architectural commitment (PG-3) — LAST-resort per ADR-002 tiered approval; vocabulary-lock IS architectural

**Wave-close criterion:** PG-4 PASS = wave closed. PG-4 BLOCK = amendment cycle re-fires sub-phase 5c; wave remains open until PG-4 PASS.

---

## 4. Sub-agent fan-out patterns

### 4.1 Phase 1 fan-out (3 parallel samplers)

```
                         legolas (Mode A coordinator)
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        Sampler-A         Sampler-B         Sampler-C
        (ARPG canon)      (JRPG/isekai)     (tabletop/myth)
              │               │               │
              ▼               ▼               ▼
        sample-A.md       sample-B.md       sample-C.md
              │               │               │
              └───────────────┼───────────────┘
                              ▼
                      legolas analyzes
                              ▼
                       sample-triage.md
```

Sub-agent type: `general-purpose` (web search + research + structured output capability). Legolas spawns all 3 in a single multi-agent invocation per parallel-fan-out discipline.

### 4.2 Phase 3 fan-out (adaptive ≤6 expansion sub-agents)

```
              PG-1 ratified scope: e.g.,
              {A, fire}, {A, water}, {A, earth}, {A, wind}, {B, holy}, {C, shadow}

                       legolas (Mode A coordinator)
                              │
       ┌──────────┬──────────┼──────────┬──────────┬──────────┐
       ▼          ▼          ▼          ▼          ▼          ▼
    Exp-A.1    Exp-A.2    Exp-A.3    Exp-A.4    Exp-B.1    Exp-C.1
    (A,fire)  (A,water)  (A,earth)  (A,wind)   (B,holy)   (C,shadow)
       │          │          │          │          │          │
       ▼          ▼          ▼          ▼          ▼          ▼
       └──────────┴──────────┼──────────┴──────────┴──────────┘
                              ▼
                       full datasets
                       (to elrond medium)
```

Soft cap: 6. Over-cap → gandalf re-ratification (PG-1.5; in-wave).

### 4.3 Sub-agent prompt drafts (Appendix A — for KR to consume + finalize)

See § 9 Appendix A below.

---

## 5. Cost + horizon

Single wave; cost measured per phase (sub-agent fan-out count + nominal work-unit).

| Phase | Sub-agent fan-out | Work shape |
|---|---|---|
| Phase 0 — Elrond consultation | 1 elrond invocation | Pre-wave consultation; minimal |
| Phase 1 — Parallel sample | 3 (Sampler-A/B/C, concurrent) | Web research; parallel |
| Phase 2 — Triage | 1 legolas analyzer invocation | Synthesis of 3 sample reports |
| PG-1 — gandalf ratification | 1 gandalf sub-agent invocation | Pattern A-light verdict (in-wave) |
| Phase 3 — Adaptive expand | ≤6 expansion sub-agents (concurrent) | Deep web research; parallel |
| PG-1.5 — in-flight amendment (conditional) | 1 gandalf sub-agent invocation | Pattern A-light verdict (in-wave; only fires if needed) |
| Phase 4 — Elrond stats | 1 elrond invocation | Statistical analysis |
| PG-2 — gandalf ratification | 1 gandalf sub-agent invocation | Pattern A-light verdict (in-wave) |
| Sub-phase 5a — gandalf synthesis draft | 1 gandalf sub-agent invocation OR session-active gandalf | Draft synthesis authoring |
| Sub-phase 5b — Pattern B + PG-3 | session-active gandalf + Matt | Pattern B substantive design call (THIS is the Pattern-B engagement Matt has with gandalf for the wave) |
| Sub-phase 5c — Canonical write | session-active gandalf | Final canonical write authoring |
| Sub-phase 5d — jack-ryan Gate-2 (PG-4) | 1 jack-ryan sub-agent invocation | Wave-close critique |
| Sub-phase 5e — KR wave-close + gandalf design-quality audit | 1 gandalf + 1 KR sub-agent invocation | Wave-close discipline |

**Total sub-agent invocations:** ~13-19 (3 samplers + ≤6 expansion + 4 phase-gate gandalf + 2 elrond + 1 legolas analyzer + 1 jack-ryan + 1 KR-wave-close + 1 gandalf-audit; conditional PG-1.5 adds 1).

**Wave wall-clock:** depends on sub-agent execution time per invocation. With parallel fan-outs at Phase 1 (3 concurrent) and Phase 3 (≤6 concurrent), and serialized phases between, the wave should execute end-to-end in a single sustained orchestration unit. Matt's Pattern B engagement at sub-phase 5b is the rate-limiter on wall-clock (when Matt is available for the sub-phase 5b dialogue, the wave proceeds to terminus).

**Cost notes:**
- Web research is the dominant cost; samplers + expansion sub-agents do most work
- LLM API cost is per-sub-agent invocation; bounded by sub-agent cap (≤9 research + ≤10 orchestration = ~19 invocations)
- Sustained-background-process discipline per hive-mind protocol applies (long-running sub-agents fire in-background when supported)

---

## 6. Hive-mind composition

Per `agentic_orchestration/operating-procedures/hive-mind-protocol.md`:

**Wave-state file:** KR initializes WS1A.Q18 wave-state file at `agentic_orchestration/cycle-15-ws1a-q18-flavor-pool-research/wave-state.md` (or equivalent per cycle-naming convention). Wave-state carries:
- Wave-open timestamp + wave-close criterion (canonical write + PG-4 PASS)
- Active sub-agents + their assigned scope (live updates as phases fire)
- Phase + phase-gate status (Phase 0 → Phase 5; PG-0 → PG-4)
- Artifact path index (updated per phase close)
- Decision log (timestamped phase-gate ratifications)
- Cross-wave composition note: pattern-sets Q16/Q17/Q19 wave structures

**Critique-pair coverage (jack-ryan):**
- Gate-1 on KR's dispatch authoring (wave-open dispatch + per-phase dispatches as KR authors them; jack-ryan reviews pre-fire)
- Gate-2 on sub-phase 5c canonical write (wave-close critique; BLOCK authority; PG-4 = wave-close criterion)

**Decision routing per Matt 2026-05-23 verbatim:**
- Seam-owners decide in-scope per their seam authority
- Matt is LAST-resort escalation for: (a) decisions exceeding seam authority per ADR-002, (b) push-to-remote (default), (c) scope-amendment
- PG-3 (architectural commitment lock) IS Matt-decision per ADR-002 architectural-commitment scope

**Wave cadence:** WS1A.Q18 is a single wave with 5 phases gated internally. Wave-close criterion: PG-4 PASS = wave CLOSED. The wave runs as a single orchestrated unit; phase-gates do NOT exit the wave (they fire as in-wave sub-agent invocations).

**Wave-close discipline:**
- Sub-phase 5e KR wave-close record at `canonical/story/2026-06-XX-ws1a-q18-flavor-pool-wave-close-record.md`
- Gandalf design-quality audit per OP § 4.6 (Discipline #43 candidate)
- Wave-state file marked CLOSED; pattern-set captured for Q16/Q17/Q19 composition

**Composition with Q16/Q17/Q19:** when Q18 wave closes, Q16 (per-skill flavor judgment LLM prompt) + Q17 (hybrid pair selection) + Q19 (emergent naming consistency) compose into the same WS1A wave structure pattern. The wave-state lineage, dispatch-authoring discipline, phase-gate structure, and critique-pair coverage carry forward. Pattern-setting at Q18 reduces orchestration overhead for subsequent Q waves.

**Sustained-background-process discipline:** per hive-mind protocol, long-running sub-agents (samplers + expansion sub-agents) fire in-background where supported; KR monitors completion notifications without polling. Wave proceeds phase-by-phase as sub-agents complete and phase-gates ratify.

---

## 7. Risk register + failure modes

| Risk | Failure mode | Mitigation |
|---|---|---|
| F-1 | Sampler sub-agent web-research yields stale/inaccurate data (Sampler hallucinates skill names not in actual games) | Each candidate requires source citation; Phase 4 stats validates cross-source agreement; gandalf Phase 5 audit demotes uncited entries |
| F-2 | One track dominates the candidate pool (e.g., ARPG canon overwhelms JRPG + tabletop signal) | Phase 4 stats track-source weighting validation surfaces; gandalf synthesis weights tracks per Reincarnated positioning |
| F-3 | Lightning/holy/shadow yield is uniformly weak (substrate-honest "the genre doesn't say much here") | Phase 2 triage surfaces; Phase 3 expansion focuses on weakest primaries; Phase 5 surface explicit confidence-degradation per primary |
| F-4 | Existing pool entries contradict research findings (e.g., a current allow-list entry has no genre precedent) | Phase 5 existing-pool audit (integrated per Matt's Q-shape-4 ratification); demote-to-eligible or remove |
| F-5 | Sub-agent cost overrun (>6 expansion sub-agents requested at PG-1) | Soft cap binds; over-cap requires gandalf re-ratification (PG-1.5; in-wave); honest accept-or-trim |
| F-6 | Phase 4 data shape too qualitative for statistical analysis | Phase 4 contingency: collapse to "data-shape verification + cross-source agreement audit"; route in-flight to gandalf; wave continues |
| F-7 | Matt ratification (PG-3) blocks on cardinality target dispute | Pattern B sub-phase 5b resolves; if irreconcilable, additional Phase-3 expansion routes per PG-2 amendment loop (wave does NOT exit; amendment-loops back to Phase 3) |
| F-8 | jack-ryan Gate-2 BLOCK at PG-4 (wave-close criterion) | Standard Gate-2 remediation; canonical write amendment per BLOCK finding; re-PG-4; wave-close gates on PG-4 PASS |
| F-9 | Operational migration dispatch (sub-phase 5f) surfaces schema-extension complications in `data/seasonal_elements/pool.json` | KR routes to elrond + star-lord per standard cross-seam migration discipline; POST-WAVE; not WS1A.Q18 wave scope |

**Substrate-led discipline composition (Discipline #41):** this entire operational sequence is substrate-led applied to vocabulary itself. The pool emerges from genre vote; designer curation post-research is the validation gate per Disc #41 refinement (engineering generation permitted; encoding gate bound).

**Framing-audit composition (Discipline #42):** applied to this operational sequence at authoring time:
- Q1 load-bearing assumptions: (a) canonical-7+1 stable; (b) sample-then-expand yields better than exhaustive-upfront; (c) 4-6 session horizon achievable; (d) statistical analysis grounds cardinality decisions
- Q2 refutation evidence in current scope: confirms (a) per engine commit; (b) per substrate-axis discovery precedent; (c) per Wave-5 closure cascade time; (d) per Phase 5 cohesion judge precedent
- Q3 refinement needed: F-6 contingency built in (Phase 4 qualitative-data collapse path); no other refinements surfaced

---

## 8. Artifact path index

| Phase | Artifact | Path |
|---|---|---|
| Wave-open | KR wave-state file | `agentic_orchestration/cycle-15-ws1a-q18-flavor-pool-research/wave-state.md` (or per KR cycle-naming convention) |
| Phase 0 | Elrond data-medium consultation | `agentic_orchestration/elrond/consultations/2026-06-XX-q18-flavor-pool-data-medium.md` |
| Phase 1 | Sampler-A output (ARPG canon) | `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-XX/sample-A.md` |
| Phase 1 | Sampler-B output (JRPG/isekai) | `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-XX/sample-B.md` |
| Phase 1 | Sampler-C output (tabletop/myth) | `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-XX/sample-C.md` |
| Phase 2 | Legolas triage verdict | `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-XX/sample-triage.md` |
| PG-1 | Gandalf ratification | `agentic_orchestration/gandalf/notes/2026-06-XX-q18-gate-1-triage-ratification.md` |
| Phase 3 | Expansion sub-agent outputs | `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-XX/full-<track>-<primary>.md` |
| Phase 4 | Elrond stats verdict + raw data | `agentic_orchestration/elrond/analysis/element-flavor-mapping-stats-2026-06-XX.md` + medium-specific raw data path |
| PG-2 | Gandalf ratification | `agentic_orchestration/gandalf/notes/2026-06-XX-q18-gate-2-stats-ratification.md` |
| Sub-phase 5a | Gandalf synthesis draft | `agentic_orchestration/gandalf/notes/2026-06-XX-q18-flavor-pool-research-synthesis.md` |
| Sub-phase 5c | Final canonical write | `canonical/story/2026-06-XX-flavor-pool-per-primary-element-lock.md` |
| PG-4 (sub-phase 5d) | Jack-ryan Gate-2 finding | `agentic_orchestration/qa/findings/2026-06-XX-q18-flavor-pool-lock-gate-2.md` |
| Wave-close (sub-phase 5e) | KR wave-close record | `canonical/story/2026-06-XX-ws1a-q18-flavor-pool-wave-close-record.md` |
| Wave-close (sub-phase 5e) | Gandalf design-quality audit | `agentic_orchestration/gandalf/notes/2026-06-XX-ws1a-q18-wave-close-design-quality-audit.md` |

Date stamps `2026-06-XX` resolve to actual dates as artifacts land.

---

## 9. Appendix A — Sub-agent prompt drafts (KR consumes + finalizes per medium spec)

These are gandalf-authored brief drafts. KR finalizes per elrond's Gate-0 medium decision (inserting output-format instructions) and authors as formal dispatches.

### 9.1 Sampler-A brief (ARPG canon)

> You are an isekai-and-ARPG genre researcher commissioned by gandalf (story-and-design steward) via legolas (research seam). Your task: sample the ARPG canon for **sub-element / flavor-element vocabulary** mapped to **8 canonical primary elements** (fire / water / earth / wind / lightning / holy / shadow / physical).
>
> **Primary sources to survey (target 5-10 per primary):**
> - Diablo 1, 2, 3, 4, Immortal (skill databases per class tree; legendary/unique affix vocabulary; ailment vocab)
> - Path of Exile 1 + 2 (passive tree clusters; gem categories; ascendancy theming; ailment vocab — Ignite/Shock/Chill/Freeze/Bleed/Impale/Poison)
> - Last Epoch (skill trees + mastery elemental sub-categories; status effect taxonomy; minion theming)
> - Grim Dawn (devotion constellations; Eldritch/Order/Primordial category; Aether/Chaos/Vitality/Eldritch fifth-element vocab — load-bearing for shadow/holy mapping)
> - Lost Ark (engraving + skill names by class element)
> - Torchlight 2 / Infinite (skill trees; legendary set theming)
> - Wolcen / Chronicon / Titan Quest (skill/passive vocab per element)
>
> **For each primary element (fire / water / earth / wind / lightning / holy / shadow / physical), surface 5-10 candidate sub-element/flavor keywords with:**
> 1. Candidate keyword
> 2. Source citation (game + skill/affix/passive name where keyword appears)
> 3. Recognizability score (1=niche / 2=common / 3=ubiquitous across multiple sources)
> 4. Substrate type tag (material / phenomenon / proper-noun / mythological / mechanical-keyword)
> 5. Cross-primary contamination flag (does this keyword also appear under a different primary in genre canon?)
>
> **Also report:**
> - Per-primary yield score: STRONG / MEDIUM / WEAK / MISALIGNED (does the ARPG canon say much about this primary?)
> - Source coverage breadth: which sources yielded; which were sparse
> - Substrate-tagging gaps: keywords with heavy cross-primary contamination
> - Continue/stop/expand recommendation per primary within track (your read on whether deeper ARPG research yields more)
>
> **Specifically focus on:**
> - **Lightning gap-fill** (plasma / arc / volt / surge / storm / thunder / bolt / coil / static / spark — what does genre actually use)
> - **Holy gap-fill** (light / radiant / dawn / sanctum / blessed / consecrated / divine — but flag over-religious-coded risk)
> - **Shadow gap-fill** (umbra / void / shade / wraith / abyss / dusk / night — distinguish from earth-decay e.g. miasma, water-deep e.g. abyss)
> - **The 7-vs-8 empirical question for physical:** does ARPG canon treat physical with sub-element vocabulary (bleed / pierce / blunt / crush / sever / impale) AS sub-elements, or as flat-primary with no sub layer? Grim Dawn treats piercing/bleeding as sibling damage types; PoE has bleed+impale+maim as ailments not subs. Survey carefully; answer empirically.
>
> **Bound:** parallel fan-out (concurrent with Sampler-B + Sampler-C within Phase 1). You are a SAMPLER, not exhaustive inventory. Surface 5-10 candidates per primary; let downstream Phase 3 expansion deepen.
>
> **Output format:** [INSERTED PER ELROND PG-0 MEDIUM DECISION]

### 9.2 Sampler-B brief (JRPG / isekai / anime canon)

> You are an isekai-and-ARPG genre researcher commissioned by gandalf via legolas. Sample the JRPG / isekai / anime canon for sub-element / flavor-element vocabulary mapped to 8 canonical primary elements.
>
> **Primary sources to survey (target 5-10 per primary):**
> - Final Fantasy series (Fire/Fira/Firaga + Blizzard/Blizzara + Thunder + Aero + Holy + Drain + Bio + Stone families — 30-year locked spell-element vocab)
> - Persona / SMT (Agi=fire / Bufu=ice-water / Zio=lightning / Garu=wind / Hama=light-holy / Mudo=shadow-dark / Megido=almighty; sub-element vocab is rigidly structured)
> - Mushoku Tensei (spell categorization: Fire / Water / Earth / Wind / Detoxification / Healing / Curse / Summoning / Sword Magic)
> - KonoSuba (spell-name conventions; isekai-genre-typical flavor markers)
> - Slime / That Time I Got Reincarnated (magicule + element classifications)
> - Solo Leveling / Overlord (necromancy + shadow-element vocab specifically — load-bearing for shadow pool)
> - Tower of God / Berserk / Black Clover (element-magic vocab; unusual primary mappings)
>
> [Same per-primary deliverable shape as Sampler-A; same focus areas; same 7-vs-8 empirical question for physical; same bound.]
>
> **Specific to track B:**
> - Reincarnated is PROVISIONALLY isekai-positioned per D10; this track informs player-facing flavor vocabulary recognizability
> - Persona's element-vocab is canonical-locked across 30 years of JRPG genre; treat as load-bearing reference
> - Solo Leveling's shadow-army vocabulary is the strongest isekai-shadow precedent; mine deeply

### 9.3 Sampler-C brief (tabletop + mythological + alchemical)

> You are a genre-cross-check researcher commissioned by gandalf via legolas. Sample tabletop + mythological + alchemical sources for sub-element / flavor-element vocabulary mapped to 8 canonical primary elements.
>
> **Primary sources to survey (target 5-10 per primary):**
> - D&D 5e + Pathfinder (energy damage types: Fire / Cold / Acid / Electricity / Sonic / Radiant / Necrotic / Force / Psychic; spell-school taxonomy; sub-element keywords)
> - MTG color pie (White=holy, Blue=water+lightning, Black=shadow, Red=fire, Green=earth+wind — loose alignment; mine card-name vocab)
> - Western alchemical tradition (four-classical + ether/aether; sub-substance vocab — sulphur / mercury / salt / etc.)
> - Eastern five-element Wu Xing (Wood/Fire/Earth/Metal/Water; cross-check on substrate-coherent vocab)
> - Folklore / mythology (especially for holy gap — sanctum / blessed / consecrated / sacred / divine — and shadow gap — umbra / abyss / void / wraith / shade)
>
> [Same per-primary deliverable shape; same focus areas; same 7-vs-8 empirical question for physical; same bound.]
>
> **Specific to track C:**
> - This track is the CROSS-CHECK that prevents over-fitting to ARPG (Track A) or JRPG/isekai (Track B) quirks
> - Tabletop sources are most rigorous for damage-type taxonomy; treat as recognizability-validation reference
> - Mythological sources are load-bearing where ARPG + JRPG yield is weak (especially holy + shadow; possibly lightning)

---

## 10. Cross-references

### 10.1 Composes with (existing canon)
- `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md` § 1.7 (per-skill flavor judgment architecture; WS1A.4 spec) + § 8b Q18 (parent question)
- `canonical/story/2026-05-29-designer-writes-substrate-player-names-experience-principle.md` (foundational substrate-led principle)
- `agentic_orchestration/operating-procedures/hive-mind-protocol.md` (composition target for cycle orchestration)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 41 (substrate-led discipline) + § 42 (framing-audit) + § 18 (math-hotspot methodology consultation)
- `~/Games/reincarnated-engine/config/elements.yaml` (canonical-7+1 element catalog — substrate)
- `~/Games/reincarnated-engine/data/seasonal_elements/pool.json` (existing 156-entry pool — substrate to extend)

### 10.2 Pattern-sets (future composition)
- WS1A.Q16 (per-skill flavor judgment LLM prompt design) — composes into same hive-mind cycle pattern
- WS1A.Q17 (hybrid kit element pair selection) — same
- WS1A.Q19 (emergent kit concept naming consistency) — same

### 10.3 Authorizes downstream
- Operational migration dispatch (sub-step 5e) — extends `data/seasonal_elements/pool.json` per locked allow-list
- WS1A.3 (per-kit sub-element selection) implementation — consumes locked pool
- WS1A.4 (per-skill bounded LLM flavor judgment) implementation — consumes locked pool

### 10.4 Does NOT replace or amend
- Canonical-7+1 element catalog (substrate; preserved as-is)
- Existing seasonal_elements/pool.json (audited + extended; not retired)
- Hypothesis-flow architecture (this sequence executes § 8b Q18 closure path)

---

## 11. Sign-off

**Authored:** gandalf (story-and-design steward) per Pattern B session 2026-06-01
**Ratified shape:** Matt 2026-06-01 verbatim ratifications:
- Q-shape-1: legolas as commissioner+analyzer; samplers as parallel sub-agents
- Q-shape-2: pre-Phase-1 elrond consultation on data medium
- Q-shape-3: soft cap at 6 expansion sub-agents
- Q-shape-4: existing-pool audit integrated into Phase 5
- Orchestration mode: KR hive-mind cycle (not direct-from-gandalf)

**Next action:** KR consumes this operational sequence + initializes WS1A.Q18 wave-state file + authors wave-open dispatch + routes Phase-0 elrond consultation dispatch.

**Authority for decisions in this wave:**
- PG-0 (data medium): elrond seam authority
- PG-1 / PG-1.5 / PG-2: gandalf design-side seam authority (in-wave Pattern A-light sub-agent invocations)
- PG-3 (final lock): Matt architectural-commitment authority per ADR-002 (Pattern B sub-phase 5b)
- PG-4 (wave-close process gate): jack-ryan BLOCK authority

**Composition note:** this operational sequence pattern-sets the WS1A wave structure. Q16/Q17/Q19 waves compose into the same orchestration pattern with workstream-specific scope substitution. Pattern-setting at Q18 reduces orchestration overhead for subsequent Q waves.

**Single-wave discipline confirmed (Matt 2026-06-01):** "Can we not have this made into one long hive mind wave? This would be my leaning to do so (wave with all sessions as gated phases if needed)." — wave structure replaces multi-session sequencing; all phase-gates fire in-wave; wave-close criterion is PG-4 PASS; Matt's only direct Pattern-B engagement during the wave is at sub-phase 5b (PG-3 architectural lock).

**End of operational sequence.**
