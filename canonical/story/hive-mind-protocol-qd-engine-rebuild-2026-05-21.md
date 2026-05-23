# Hive-Mind Protocol — QD-Engine Rebuild

> **STATUS:** CURRENT (load-bearing as of 2026-05-23) — see `canonical/00-ground-state.md`

**Status:** v1.3 (amended 2026-05-22 — folds 2026-05-21 evening protocol amendments + 2026-05-22 W1.13 rescope)
**v1.0 → v1.1 changes:** D1-D6 resolutions, substrate-as-cohesion recommitment, W0.9 + W0.10 additions, W1.13 added per math note
**v1.1 → v1.2 changes (per coherence review 2026-05-21):** P1 W1.13 explicit + Tier 1 playability + substrate quantitative target; P2 T_AXIS_SENS calibration; P3 kit_specification format; **P4 trigger interaction + Tier 4 keystone sim support (significant scope addition)**; **P5 reframed as empirical-validation phase for substrate-as-cohesion architecture (epistemic correction per Matt 2026-05-21 catch)**; P6 Profile A export format; P7 Pattern-A residual measurement + v2 trajectory documentation; § 1.3 v2 canonical-parity expansion as out-of-current-hive-scope
**v1.2 → v1.3 changes (2026-05-22 fold-in per `agentic_orchestration/hive-mind-protocol-amendments-2026-05-21-evening.md` + critique-pair W1.13 rescope):** (a) BDI resonance formalism added as foundational mathematical structure (`canonical/story/historical/build-defining-resonance-formula-2026-05-21.md`); 5 hypothesis tests H1-H5 added as P1+ diagnostic workstreams W1.20-W1.22; (b) Gear-as-substrate LITE path adopted — `signature_gear_archetype` lands as DERIVED TAG in V1 (not generative substrate), promoting to full substrate in v1.1/v2 post-P7; new P1 workstream W1.15-LITE + P5 W5.3-LITE; (c) Tier 4 keystone architecture defaults adopted (T4-A) — 1 signature capstone + 1-3 secondary; hand-authored catalogue v1 ~30-50; gear-anchored signature; phasing T4-A→T4-E; (d) W1.13 rescope under Scenario B dual-witness + Surface A footnote per `canonical/story/w1-13-rescope-disposition-2026-05-22.md` — FIRE-GATE closed; empirical urgency reduced; architectural urgency preserved (Track C + W0.10 + BDI + T4 mandate)

**Author:** gandalf — authored overnight 2026-05-20/21 per Matt's directive
**Author:** gandalf (story-and-design steward + theoretical mathematician + senior designer)
**Companions:**
- `canonical/story/historical/engine-architecture-vision-qd-profile-2026-05-19.md` — vision (QD-engine + 4 profiles)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — operational spec (8 axes, 68,040 cells)
**Audit inputs synthesized:**
- `agentic_orchestration/legolas/research/substrate-sufficiency-audit-2026-05-20/phase-1-reconnaissance/` (legolas Phase 1)
- `agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/` (jack-ryan 62-entry constraint inventory)

**Estimated duration:** 22-33 weeks (audit-driven; longer than vision-doc § 8 18-26 week estimate due to comprehensive constraint cleanup and substrate enrichment requirements that the audits surfaced)

---

## 0. TL;DR

This is the comprehensive hive-mind protocol for the QD-engine rebuild. It synthesizes the architectural vision (5-axis sketch → 8-axis lock), the legolas substrate-sufficiency audit (which confirmed 4 structural substrate gaps and surfaced 4 vision-layer geometry gaps), and the jack-ryan legacy-constraint audit (62 constraints, 12 HIGH-risk).

The rebuild proceeds in **8 phases** over 22-33 weeks:

| Phase | Name | Duration | Critical work |
|---|---|---|---|
| **P0** | Constraint removal + drift cleanup | 2-3 weeks | Resolve 12 HIGH-risk LCs; B6 energy-type fix; foundation validator decision |
| **P1** | Substrate enrichment | 4-6 weeks | Schema extensions; HP-econ + charge-stack + damage-converts creation; VFX procurement; Mixamo integration |
| **P2** | BC measurement infrastructure | 3-4 weeks | All 8 axes operational; Discipline #17 calibration sweeps |
| **P3** | MAP-Elites archive implementation | 2-3 weeks | Pareto / crowding / Mahalanobis / hypervolume / KL gates |
| **P4** | Sim extensions for deferred bins | 4-6 weeks | Proxy support; dodger sub-cases; charge mechanics; damage-conversion; channel mechanics |
| **P5** | Theme coalescence + cohesion-BC + visual-BC | 3-5 weeks | LUCB1; joint-gate; cipher migration coordination |
| **P6** | Profile assembly layer | 2-3 weeks | 4 profiles operational; coreset + submodular |
| **P7** | Validation gauntlet + production cutover | 2-3 weeks | Reference-archetype validation; Profile A ship |

**Critical decision-points — ALL RESOLVED 2026-05-21 by Matt-delegation to gandalf** (see § 4):

| ID | Decision | RESOLUTION (2026-05-21) |
|---|---|---|
| **D1** | Unity render pipeline | **URP** ✓ |
| **D2** | Phase 0 element scope | **7 elements** (fire / water / earth / wind / lightning / holy / shadow) ✓ |
| **D3** | Cohesion-BC sequencing | **Sequenced** (post-cipher migration) ✓ |
| **D4** | BC Axis 2 measurement context | **All fights, fight-context-tagged** ✓ |
| **D5** | Foundation validator scope | **7-substrate** (aligns with D2; closes LC-012 drift) ✓ |
| **D6** | Vision-layer geometry gap response | **Document for v1.1 axis-lock revision** (do not block P0) ✓ |

P0 is unblocked. Knight-rider drafts decisions-log entry on session-open; jack-ryan reviews; Matt's explicit delegation is the approval.

**The audits validated the architecture.** The 8-axis lock is sound; the substrate gaps were correctly anticipated; the deferred-bin mechanism is the right answer. The work ahead is execution against a clean specification.

**v1.3 architectural additions (2026-05-22):**

| Addition | Doc | Phase | Scope |
|---|---|---|---|
| **BDI resonance formalism** | `canonical/story/historical/build-defining-resonance-formula-2026-05-21.md` | P1+ diagnostic | Build-Defining Index measuring interaction-term dominance; ω/τ field equations; rank-3 γ-triples as signature builds; Tier 4 keystones as rank-completers. 5 hypothesis tests H1-H5 against archive (W1.20-W1.22) |
| **Gear-as-substrate LITE** | `canonical/story/historical/gear-as-substrate-2026-05-21.md` § 0.5.6 | P1 W1.15-LITE + P5 W5.3-LITE | `signature_gear_archetype` as DERIVED TAG in V1 via deterministic rule table (15 archetypes; substrate-vector→gear-archetype); cross-repo coherence solved; full-substrate promotion deferred to v1.1/v2 post-P7 |
| **Tier 4 architecture defaults (T4-A)** | `canonical/story/tier-4-architecture-defaults-2026-05-22.md` | T4-A pre-P3; T4-B P3-P4; T4-C P5; T4-D pre-P5 | 1 signature capstone (rank-3 completer; gear-anchored when signature_gear_archetype present) + 1-3 secondaries; hand-authored catalogue v1 ~30-50; each keystone designed as third leg of known high-β substrate-pair |
| **W1.13 rescope (Scenario B)** | `canonical/story/w1-13-rescope-disposition-2026-05-22.md` | P1 W1.13 (still gated on substrate enrichment + Matt framing approval) | FIRE-GATE closed; dual-witness (Track C + W0.10) + Surface A footnote (LC-011 reframed; 5% boundary not 42% historical; Surface_A% = 66.67%); BDI/T4 architectural alignment preserved |

The BDI formalism is the **bridge between vision-layer and operational-layer**: the substrate-architecture commitment (vision) gets a mathematical predictor (interaction-term dominance over linear terms) that the composer (operational) can optionally weight + the cohesion-judge (operational) reads through different sensors. The two layers now share a resonance-detection structure.

---

## 1. Provenance, scope, dependencies

### 1.1 How this protocol came to be

The QD-engine vision emerged from a Pattern-B theory-craft session 2026-05-19 between Matt and gandalf. The 8-axis operational spec emerged from a follow-on theory-craft 2026-05-19/20. The two audits (substrate + constraints) emerged from Matt's end-of-session directive 2026-05-20 to ensure no legacy constraints throw off rebuild testing. This protocol synthesizes all three layers (vision, axis-lock, audits) into an executable plan.

**2026-05-21 evening additions (folded into v1.3 2026-05-22):**

- **BDI resonance formalism** emerged from Matt + gandalf sustained design dialogue 2026-05-21 evening; captures the genre's signature-build phenomenon (Pain Attunement Witch, Frozen Orb Sorc, Smoke-Vampire) as interaction-term dominance over linear terms in WR landscape; provides empirically-testable hypothesis battery (H1-H5) that runs against the QD archive non-invasively (diagnostic, not generative)
- **Gear-as-substrate LITE timing decision** emerged from Matt cross-repo concern (legacy archetype-locking removal in W0.2 left demo/Unity/loadout without canonical class-identity-to-gear coherence between now and P7); LITE path adopted as middle road — `signature_gear_archetype` as DERIVED TAG in V1, full-substrate promotion deferred to v1.1/v2
- **Tier 4 architecture surfacing** emerged from gandalf math note v1.1 § 4 + legolas ARPG-canon survey + BDI § 6 rank-completer framing; surfaced four open questions (hierarchy / authorship pattern / gear-anchoring / catalogue size); resolved 2026-05-22 morning under Matt pre-authorization C as T4-A defaults

**2026-05-22 morning addition (folded into v1.3):**

- **W1.13 rescope under Scenario B** emerged from LC-011 ablation recovery 2026-05-22 morning under Matt's prolonged-autonomy mandate; recovery confirmed boundary-signal magnitude (5%) rather than historical floor-lock (41.8%); critique-pair (jack-ryan process + gandalf design) landed dual-witness + Surface A footnote disposition under Matt pre-authorization D (β autonomous); FIRE-GATE on W1.13 dispatch closes; implementation remains gated on P1 substrate enrichment + Matt W1.13 framing approval

These four 2026-05-21-evening / 2026-05-22-morning additions do NOT change the P0-P7 critical-path structure. They add scope, sharpen architecture, and surface explicit open questions for design-call resolution.

### 1.2 Two layers, three documents, one execution path

| Layer | Document | Purpose |
|---|---|---|
| **Vision** | `engine-architecture-vision-qd-profile-2026-05-19.md` | Architectural commitment (QD-engine + 4 profiles + IDC meta-principle) |
| **Operational** | `qd-engine-bc-axes-lock-2026-05-20.md` | 8-axis specification (bins, measurements, thresholds, substrate flags) |
| **Execution** | THIS DOCUMENT | Phased rebuild plan with dispatches, gates, specialists, conventions |

The three layers form a coherent stack. Vision = what we're building. Operational = how it measures. Execution = how we build it.

### 1.3 Scope and exclusions

**In scope:**
- All 8 mechanical BC axes (the locked spec)
- Substrate enrichment (internal + external acquisition)
- Sim extensions for deferred bins
- Theme coalescence + cohesion-BC + visual-BC integration
- All 4 profiles (A Reincarnated, B B2B, C mod-pack, D solo-dev)
- Production cutover for Profile A (Reincarnated Phase 0)

**Out of scope (deferred to post-rebuild Phase 8+):**
- Earth Meta-Layer gameplay (the post-Phase-0 game-of-games surface)
- Multiplayer / rift events (PVP / PVE multiplayer scope)
- Mod-pack distribution infrastructure (Profile C produces packs; distribution is separate)
- B2B SaaS commercial operations (Profile B produces customer-curated archives; SaaS billing/auth is separate)

### 1.4 Dependencies entering P0

| Dependency | Status | Blocks |
|---|---|---|
| Recompose-validation hive ship | In flight (Phase 2 firing as of 2026-05-20 evening; 60% empirical signal) | P0 start preferred but not strictly required |
| Legolas Phase 1 reconnaissance | **COMPLETE** | Already synthesized into this protocol |
| Jack-ryan constraint audit | **COMPLETE** | Already synthesized into this protocol |
| Matt resolution of D1-D6 | **PENDING** | P0 must wait on D1, D2, D5 minimum; D3/D4/D6 can be resolved during P0 |
| Engineering disciplines #1-#17 | LIVE | Continuous compliance throughout |
| Discipline #18 (joint-gate) candidate | PROPOSED in P5 § 3.5 | P5 ratifies after empirical validation |

---

## 2. The two-layer architecture (vision + operational)

### 2.1 Vision layer

The QD-engine is a Quality-Diversity optimizer (MAP-Elites algorithm) over a behavior-characteristic (BC) space defined by 8 mechanical axes plus 2 adjacent BC archives (cohesion + visual). The engine operates under 4 profiles (A/B/C/D) that filter the archive for distinct deployment targets. The Information-Deferred-to-Coalescence (IDC) meta-principle governs: information that can be deferred to coalescence (post-convergence theme assignment) should be — early-binding contaminates measurement.

### 2.2 Operational layer

The 8 BC axes (`qd-engine-bc-axes-lock-2026-05-20.md`):

| # | Axis | Bins | Bin labels |
|---|---|---|---|
| 1 | Engagement profile | 6 | close-fast / close-slow / mid-fast / mid-slow / ranged-fast / ranged-slow |
| 2 | Damage geometry | 5 | single-target / small-AOE / large-AOE / chain / multi-spawn |
| 2A | Proxy density | 3 | solo / proxy-light / proxy-heavy |
| 2B | Control density | 3 | damage-pure / mixed / control-pure |
| 3A | Damage tempo | 3 | low / medium / high |
| 3B | Damage amplitude variance | 3 | flat / variable / spiky |
| 4 | Defensive profile | 4 | tank / mitigator / dodger / glass |
| 5 | Resource economy | 7 | HP-economy / charge-stack / damage-taken-converts / starved / overflow / generator-spender / steady |

Total: 68,040 cells. Profile A operational cell-space (with deferred bins excluded): 25,920 cells.

### 2.3 Adjacent BC archives (parallel work)

| Archive | Owner | Math gate | Populated when |
|---|---|---|---|
| Mechanical BC | gandalf + gamora | Pareto / Mahalanobis / hypervolume | P2 (BC measurement) |
| Cohesion BC | gandalf | LUCB1 / information bottleneck | P5 (theme coalescence) |
| Visual BC | galadriel | CV-similarity scoring | P5 (visual-BC integration) |

The three archives feed the joint-gate (Discipline #18 candidate) which becomes the ship criterion.

### 2.4 BDI as bridge between vision and operational layers (v1.3 addition)

The BDI resonance formalism (`canonical/story/historical/build-defining-resonance-formula-2026-05-21.md`) sits between vision and operational layers as a **resonance-detection structure shared by both**:

- **Vision side:** the substrate-as-cohesion architecture commits that identity emerges from mechanical signature; the cohesion-judge intuits identity-patterns from kit data. BDI formalizes WHAT the judge is detecting — interaction-term dominance over linear terms; rank-2 paired-identity; rank-3 signature-build γ-triples
- **Operational side:** the composer's substrate-vector selection can OPTIONALLY weight high-BDI vectors (post H1-H4 confirmation in W1.21); the convergence loop's Tier 4 keystone selection is a rank-completer (per BDI § 6); the cohesion-judge prompt extensions (P5 W5.3 + W5.3-LITE) feed the judge identity hints aligned with BDI rank structure

The math model and the narrative model **read the same resonance through different sensors.** Hypothesis test H5 explicitly validates this bridge (BDI score correlates with cohesion-judge score). The two layers are not parallel-but-independent; they are dual sensors on the same underlying substrate-architecture phenomenon.

---

## 3. Audit-driven prerequisites

### 3.1 Jack-ryan constraint audit synthesis (62 constraints, 12 HIGH-risk)

**Top 5 HIGH-risk constraints (LC-001 through LC-005) requiring resolution in P0:**

1. **LC-001 — Archetype template hardcoded dict.** The 13-template `ARCHETYPE_TEMPLATES` dict bounds kit variety. Without Path-a refactor (on-boot composition from substrate identity declarations × role shapes), the QD archive fills with template-clones rather than diverse kits. **Disposition: Path-a refactor in P0 W0.2 (LC-001 fix).**

2. **LC-004 — Energy-type ~3-5× DPS gradient.** Systematically distorts modifiers across archetype spectrum (0.09-0.52 observed). BC axes measuring modifier-normalized properties (3A tempo, 3B variance, 4 defensive) reflect energy-type gradient rather than kit diversity. **Disposition: B6 energy-type-aware tier assignment (Matt-approved per decisions-log 2026-05-16; rocket execution in P0 W0.1).**

3. **LC-012 — Foundation validator drift vs. 6-substrate commitment.** `foundation/foundation.py:39-43` still enforces 4-rotating + 1-physical; decisions-log 2026-05-17 committed to 6-substrate expansion. Discipline #13a drift. **Disposition: depends on D5; trivially actionable once decision lands. P0 W0.3.**

4. **LC-006 — Canonical-four universally exposed to LLM.** Every prompt-construction site exposes canonical-four labels despite doc 37 § 6 specifying they must be hidden. Cohesion-BC archive contamination source. **Disposition: depends on D3 (sequencing); Stage 3 cipher migration is the structural fix; either sequence cohesion-BC after Stage 3 or accept contaminated baseline. Surfaces in P5.**

5. **LC-003 — Modifier floor / calibration epoch.** Even with 0.05 floor widened, calibration epoch places elemental mages at 0.07-0.11, physical warriors at 0.32-0.59. **Disposition: B6 work (LC-004 fix) is the lever; verify before P2 starts.**

**Remaining 7 HIGH-risk constraints (LC-006 through LC-012):**
- LC-006: covered above
- LC-007 — Humanoid gear schema (Axis 4/5 measurement assumption) — REMOVE in P4 (sim extensions enable non-humanoid)
- LC-008 — STR/DEX/INT math-bearing labels (LLM exposure drift) — D3/cipher migration territory
- LC-009 — Hunter modifier range 1.82 (BC cell-address instability) — ABLATE in P1 W1.6
- LC-010 — Sim is solo-only (no proxy) — REMOVE in P4 W4.1 (already deferred per axis-lock § 5)
- LC-011 — Controller/mage iteration overhead — ABLATE in P1 (QD archive economics implication)
- LC-012: covered above

**Risk distribution:** 12 HIGH, 18 MEDIUM, 32 LOW. The full inventory at `agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/constraint-inventory.md`.

**Drift candidates (Discipline #13a) requiring explicit attention:** LC-006, LC-007, LC-012, LC-014, LC-028. Each represents a code-vs-canonical-doc gap that must be either closed or formally documented.

### 3.2 Legolas substrate audit synthesis (Phase 1 reconnaissance)

**Confirmed full substrate gaps (0 substrate exists):**

| Axis × bin | Gap | Resolution |
|---|---|---|
| Axis 5 HP-economy | No `cost_type` field in `Ability` schema; no Blood Magic equivalent | P1 W1.2 substrate creation |
| Axis 5 damage-taken-converts | Mechanic doesn't exist in generation OR simulation | P1 W1.3 + P4 W4.7 |
| Axis 2A proxy-light + proxy-heavy | Correctly deferred per axis-lock § 5 | P1 W1.6 substrate prep; P4 W4.1 sim |

**Schema extensions required for BC measurement** (P1 W1.1):

- `cost_type` (Ability)
- `movement_displacement_per_cast` (Ability)
- `aoe_radius` (Ability)
- `is_chain` (Ability)
- `is_multi_spawn` (Ability)
- `is_channel` (Ability — likely exists; verify)
- `is_reactive_trigger` (Ability — for thorns/reflection)
- `grants_evasion` / `grants_stealth` / `grants_iframes` / `grants_reflection` (Ability)
- `is_charge_pool` / `charge_cap` / `charge_decay` (Ability)
- `damage_to_resource_conversion` (Ability)
- `regen_per_sec` distinct from mitigation (sim telemetry)
- `shield_pool` distinct from HP (sim telemetry)
- Per-event source-tagged damage attribution: `cast` / `reactive` / `proxy` / `environmental` (sim telemetry)

**Substrate sufficiency status per axis (from Phase 1):**

| Axis | Required (5×) | Current estimate | Verdict |
|---|---|---|---|
| 1 Engagement | ~30 | ~15-20 | PARTIAL — metadata gap blocks measurement |
| 2 Geometry | ~25 | ~18-20 | PARTIAL — chain thin, multi-spawn thin |
| 2A Proxy | ~15 | ~5 (solo only) | DEFERRED GAP |
| 2B Control | ~15 | ~10-12 | PARTIAL |
| 3A Tempo | ~15 | ~12-15 | LIKELY OK |
| 3B Variance | ~15 | ~12-15 | LIKELY OK |
| 4 Defensive | ~20 | ~10-12 | PARTIAL |
| 5 Economy | ~35 | ~15-20 | GAP — 3 bins at 0 |

**External procurement candidates (Phase 1 shortlist):**

| Pack | Price | Coverage |
|---|---|---|
| Hovl Studio RPG VFX Bundle | $48 | Multi-element, all 5 geometry bins, all render pipelines |
| PixPlays Elemental Spells Full Pack | $36 | 24 spells × 4 elements × shield/AOE/projectile/aura/blast/beam |
| Archanor Magic Arsenal | $30 | Multi-element, Built-in+URP |
| Kalamona MOBA/ARPG Effect Pack | $19 | ARPG-specific design |
| Digital Ruby Fire & Spell Effects | FREE | Baseline fire VFX |
| Hovl Studio Magic Effects FREE | FREE | Stylized sampler |

**Element count finding:** the engine's `config/substrate_identities/` declares 7 elements (fire / water / earth / wind / lightning / holy / shadow). The `config/elements.yaml` declares only 4 rotating. **D5 resolution required** — this is the foundation validator drift.

**Vision-layer geometry gaps (4 patterns don't fit the 5 bins):**

| Pattern | Canonical exemplar | Disposition |
|---|---|---|
| Orbital / rotating projectile | D2/D3 Blessed Hammer | Document as v1.1 axis-lock candidate; defer past P0 |
| Attached-to-enemy persistent | PoE Storm Brand | Document as v1.1 candidate; defer past P0 |
| Multi-stage trap | PoE Saboteur | Document as v1.1 candidate; defer past P0 |
| Multi-location teleport-strike | D3 Seven-Sided Strike | Document as v1.1 candidate; defer past P0 |

These don't block P0. They're known coverage gaps to revisit when archive maturity surfaces real need.

**Mixamo constraints:**
- HUMANOID-ONLY hard constraint (propagates backward through pipeline)
- ~2500 animations
- No weapon socket bones (Unity Animation Rigging package required for VFX attachment)
- License: free for commercial use (confirm TOS in P1)

**Pipeline economics:**
- ~$0.45 per character (ChatGPT + Meshy)
- 10-15 minutes hands-on per archetype

### 3.3 Cross-audit synthesis — what we know now

**Confirmed:**
- Architecture is sound (8 axes capture ARPG canon well; only 4 minor gaps at vision-layer)
- Operational spec correctly identified all required substrate flags
- 4 substrate gaps are structural (require generation-system extension, not just enrichment)
- 12 HIGH-risk legacy constraints exist; most have clear dispositions

**Newly surfaced from audits:**
- 7 elements (not 5 or 4) — substrate scope expansion
- Foundation validator drift on substrate count
- 4 vision-layer geometry patterns to track for v1.1 lock revision
- Energy-type DPS gradient distortion (LC-004) — single biggest measurement contaminant
- Convergence iteration overhead per archetype type — QD archive economics issue

**Still pending:**
- Code-side specialist audit (P2 of constraint audit; fires in P0 W0.4 post-recompose-hive)
- Legolas Phase 2 (depth pass on Unity + ARPG canon) — fires in P1 W1.7
- Empirical calibration of all thresholds — fires in P2 per Discipline #17

---

## 4. Matt decision points — ALL RESOLVED 2026-05-21

These six decisions blocked P0 start. **All six resolved 2026-05-21 by Matt-delegation to gandalf.** P0 is unblocked.

**Resolution status at-a-glance:**

| ID | RESOLUTION |
|---|---|
| D1 | **URP** |
| D2 | **7 elements** |
| D3 | **Sequenced (post-cipher)** |
| D4 | **All fights, fight-context-tagged** |
| D5 | **7-substrate** |
| D6 | **Document for v1.1; do not block P0** |

Detail per decision below preserved for record (rationale, alternatives considered, downstream effects).

### 4.1 D1 — Unity render pipeline — **RESOLVED: URP**

**Question:** Should the Reincarnated game use Unity's Universal Render Pipeline (URP), Built-in render pipeline, or HDRP?

**Impact:** Blocks VFX procurement. Many Unity Asset Store VFX packs are render-pipeline-specific.

**Options:**
- **URP** — modern, mobile-friendly, good asset support, balanced performance. Most VFX packs support it.
- **Built-in** — legacy, broadest asset compatibility, lower mobile performance, sunset path
- **HDRP** — high-end, PC/console only, limited asset support, overkill for ARPG

**Recommendation: URP.** Aligns with mobile-first considerations (per pet-system discussion 2026-05-11), modern best-practice, broad asset compatibility, includes most procurement candidates identified in legolas Phase 1.

**If Matt picks Built-in:** Hovl RPG VFX Bundle still works (multi-pipeline), but Ultimate Movement FX (URP-only) and VFX Graph - Summon Creatures Vol.1 (URP/HDRP only) are unavailable.

### 4.2 D2 — Phase 0 element scope — **RESOLVED: 7 elements**

**Question:** Should Phase 0 (Reincarnated initial ship) target all 7 elements (fire / water / earth / wind / lightning / holy / shadow) or only the 4-core (fire / water / earth / wind)?

**Impact:** Doubles or halves substrate enrichment scope. Affects Track B VFX procurement and validation gauntlet duration.

**Options:**
- **7 elements** — matches committed substrate identities; aligns with Phase-1 P1 expansion plan; expands shipped variety
- **4 core** — narrower scope; faster ship; defers lightning/holy/shadow to Phase 1 expansion

**Recommendation: 7 elements.** The substrate identities for lightning/holy/shadow already exist in `config/substrate_identities/`. The foundation validator drift (LC-012) needs resolution either way. Shipping all 7 from the start avoids a foundation-validator round-trip and matches the committed direction.

**If Matt picks 4 core:** P1 W1.11 limits to 4 elements; lightning/holy/shadow defer to a post-rebuild Phase-1 expansion. Saves 2-3 weeks in P1.

### 4.3 D3 — Cohesion-BC sequencing — **RESOLVED: Sequenced (post-cipher migration)**

**Question:** Should the cohesion-BC archive (LLM-judge measurement) be implemented in parallel with mechanical BC (P2/P5), or sequenced after the Stage 3 cipher migration ships?

**Impact:** Cohesion-BC depends on LLM judge output, which is contaminated by canonical-four label exposure (LC-006) until cipher migration ships. Parallel implementation risks contaminated baseline; sequenced implementation delays Discipline #18 joint-gate by ~5-8 weeks.

**Options:**
- **Parallel** — implement cohesion-BC in P5 with contaminated baseline; recalibrate post-cipher-migration
- **Sequenced** — implement cohesion-BC after cipher migration; clean measurements from start

**Recommendation: Sequenced.** Discipline #17 (empirical-calibration smoke gate) makes parallel risky — early measurements set baselines that subsequent calibration must overcome. Sequenced gives clean baseline. The 5-8 week delay is absorbable; Profile A ship doesn't strictly require cohesion-BC (mechanical BC suffices for shipping). Cohesion-BC matures the engine; Profile A ships ahead of it.

**If Matt picks parallel:** P5 includes explicit "pre-cipher contaminated baseline" calibration flag; post-cipher recalibration becomes a P7+ task.

### 4.4 D4 — BC Axis 2 measurement context — **RESOLVED: All fights, fight-context-tagged**

**Question:** Should Axis 2 (damage geometry) be computed from all fight telemetry, only non-pack fights (per Option 2 convergence rule), or only pack fights?

**Impact:** Axis 2 BC measurement spec ambiguity (jack-ryan MQ-1).

**Options:**
- **All fights** — captures both AOE-against-packs and single-target-against-bosses; widest signal
- **Non-pack only** — matches convergence-targeting; loses AOE characterization signal
- **Pack only** — captures AOE-vs-single-target boldly; loses boss-fight single-target measurement

**Recommendation: All fights, with explicit per-context fields.** Compute Axis 2 from all damage events but tag each event with its fight-context (pack / boss / mini-boss). The argmax bin assignment uses damage-weighted across all contexts. Profile filtering can opt to weight by context (Profile B may want pack-emphasized for swarm-clearing customers).

**If Matt picks non-pack only:** AOE kits get systematically misclassified as single-target specialists. Strongly recommend against unless there's a structural reason.

### 4.5 D5 — Foundation validator scope — **RESOLVED: 7-substrate**

**Question:** Should the `foundation/foundation.py:39-43` validator be updated to enforce 4-substrate, 6-substrate, or 7-substrate (matching `config/substrate_identities/`)?

**Impact:** LC-012 Discipline #13a drift resolution. Affects whether 6-substrate or 7-substrate season generation succeeds.

**Options:**
- **4-substrate** — preserve current code; reject substrate-identity-expansion as drift
- **6-substrate** — match decisions-log 2026-05-17 commitment (fire/water/wind/earth + lightning + holy/shadow)
- **7-substrate** — match `config/substrate_identities/` (fire/water/earth/wind/lightning/holy/shadow)

**Recommendation: 7-substrate.** Coheres with D2 default + substrate identities + Phase-1 P1 commitment. The 6-vs-7 distinction in jack-ryan's count was a 2026-05-17 decisions-log entry that probably grew to 7 in substrate_identities/ — the audit can confirm. Either way, the validator should match committed direction, not enforce 4-substrate against committed expansion.

**If Matt picks 4-substrate:** Documents the committed direction as deferred-or-canceled. May require revisiting decisions-log entries.

### 4.6 D6 — Vision-layer geometry gap response — **RESOLVED: Document for v1.1 axis-lock revision; do not block P0**

**Question:** How should the 4 vision-layer geometry patterns that don't fit our 5 bins (Blessed Hammer / Storm Brand / Saboteur / Seven-Sided Strike) be handled?

**Impact:** Whether to expand Axis 2 bin count (raising cell count further) or document as canonical coverage gaps.

**Options:**
- **Expand bins now** — add orbital + attached-persistent + multi-stage-trap + multi-location-teleport-strike to Axis 2. Cell count rises to 6×9×3×3×3×3×4×7 = 122,472 (1.8× current).
- **Document for v1.1 revision** — track as known gaps; revisit after Profile A ships and archive maturity surfaces real demand
- **Selectively expand** — add 1-2 most-load-bearing (Blessed Hammer / Seven-Sided Strike are most iconic) without all 4

**Recommendation: Document for v1.1 revision.** Each gap is a recognizable archetype, but each is also a corner-case in the broader canon. Profile A ship doesn't require their coverage. Expanding the bin count now compounds the cell-count-coverage concerns (current 1.5% would drop further). Better to ship Profile A with the 5 locked bins, observe which gaps players notice, then revise in v1.1.

**If Matt picks expand selectively:** Recommend Blessed Hammer + Seven-Sided Strike (most iconic ARPG-canon archetypes); skip Storm Brand + Saboteur (PoE-specific). Adds 2 bins → 6×7×3×3×3×3×4×7 = 95,256 cells.

---

## 5. Phase architecture overview

```
P0 ──┬── P1 ──┬── P2 ──┬── P3 ──┬── P4 ──┬── P5 ──┬── P6 ──┬── P7
     │        │        │        │        │        │        │
     │        │        │        │        │        │        │
 Constraint   Substrate BC Meas  Archive  Sim Ext  Coal +   Profiles
  Removal    Enrichment            +Math   +Defer  CohBC +    A/B/C/D
                                   Gates           VisBC
                                                              │
                                                              └── Validation
                                                                  + Cutover
```

**Critical-path dependencies:**

- P0 → P1: substrate gaps can't fill until LC-001/LC-004 fixes land (otherwise generation produces template-clones with energy-gradient distortion)
- P1 → P2: BC measurement infrastructure requires schema extensions from P1
- P2 → P3: archive needs BC coordinates to insert/dominate/measure
- P3 → P4: sim extensions populate deferred bins into the existing archive (parallel to P5)
- P3 → P5: theme coalescence reads from archive
- P5 → P6: profiles filter on joint-gate verdict
- P6 → P7: cutover requires profiles operational

**Parallel work permissible:**

- P4 (sim extensions) can run parallel to P5 (coalescence) once P3 ships
- Galadriel visual-BC work can run continuously starting P1 (asset visual style validation feeds VFX procurement)
- Drax demo-side integration can run in P6+ (Profile A presentation surface)

**v1.3 additional phase layers (parallel to P0-P7 critical-path):**

| Phase layer | Scope | Critical-path timing |
|---|---|---|
| **G0** | Gear-as-substrate architectural commitment | DONE (2026-05-21 evening) |
| **G1-LITE** | Gear-archetype rule-table v1 (15 archetypes; deterministic mapping) | Pre-P1 (gandalf + Matt design call; T4-A morning session 2026-05-22) |
| **G2-LITE** | Generation-pipeline `signature_gear_archetype` computation + telemetry column + per-class persistence | **P1 (W1.15-LITE; ~3-5 days; rocket)** |
| G3-LITE | DEFERRED — gear-instance generation constrained by archetype | v1.1/v2 (post-P7) |
| **G4-LITE** | Cohesion-judge light prompt extension (signature_gear_archetype as identity hint) | **P5 (W5.3-LITE; ~1 day; star-lord)** |
| **G5-LITE** | Demo + loadout app + Unity consume signature_gear_archetype | P1+ (drax + Unity team; parallel work) |
| G6 | Spirit-swap meta-layer integration (Spirit's Core Gear) | Post-P5 (unchanged) |
| G7-LITE | DEFERRED — 4-substrate empirical validation gate | v1.1/v2 |
| G-PROMOTE-v1.1 | Promote rule-table to search-space (signature_gear_archetype becomes generative substrate) | v1.1/v2 (post-P7) |
| **T4-A** | Tier 4 architecture defaults (1 signature + 1-3 secondary; hand-authored ~30-50; gear-anchored signature; phasing T4-A→T4-E) | Pre-P3 (DONE 2026-05-22; per `canonical/story/tier-4-architecture-defaults-2026-05-22.md`) |
| **T4-B** | Tier 4 catalogue authorship (~30-50 keystones; each as rank-3 completer for known high-β substrate-pair) | **P3-P4 (gandalf + Matt design + rocket engine integration)** |
| **T4-C** | Cohesion-judge prompt extension for signature-vs-secondary capstone distinction | **P5 (star-lord + gandalf)** |
| T4-D | Gear-anchored signature capstone extension | Pre-P5 (parallel to G1-LITE) |
| T4-E | Procedural/LLM-augmented Tier 4 variant generation | Deferred v2+ |
| **BDI-A** | BDI formalism authorship | DONE (2026-05-21 evening) |
| **BDI-B** | ω/τ tables v1 finalization (15-archetype × 7-element starting reference) | Pre-P1 (DONE 2026-05-22) |
| **BDI-C** | Hypothesis test infrastructure (model-fit harness + ω/τ data structures) | **P1 (W1.20; ~1-2 weeks; rocket + legolas)** |
| **BDI-D** | Hypothesis tests H1-H4 execution + result synthesis | **P1 (W1.21; ~1 week; rocket + legolas + gandalf)** |
| **BDI-E** | BDI-E gate decision (adopt/refine/park formalism per H1-H4 results) | **P1 end (W1.22; ~0.5 day; gandalf + Matt)** |
| BDI-F | BDI-aware composer extension (optional; if H1-H4 confirm) | P2+ |
| BDI-G | BDI integration with cohesion-judge prompt (per H5 confirmation) | P5+ |
| BDI-H | Rank-4+ exploration | Deferred v2+ |

These layers ADD to P0-P7 without modifying the critical-path structure. G1-LITE/G2-LITE land in P1 alongside W1.1-W1.13. T4-A is done; T4-B fires in P3-P4. BDI-A/B are done; BDI-C-E run as P1 diagnostic workstreams.

---

## 6. Per-phase detail

### 6.1 Phase P0 — Constraint Removal + Drift Cleanup

**Duration:** 2-3 weeks
**Tag namespace:** `qd-rebuild/v0.X-constraint-removal-N`
**Prerequisites:** Matt resolves D1, D2, D5 (minimum); recompose-validation hive ships preferably
**Specialists:** rocket (generation), gamora (simulation), star-lord (telemetry), jack-ryan (drift verify)

#### 6.1.1 Scope

Resolve every HIGH-risk legacy constraint identified in jack-ryan's audit. Close every DRIFT-CANDIDATE entry. Verify every MEDIUM-risk constraint scheduled for P0. Land B6 energy-type-aware tier assignment (LC-004). Resolve foundation validator drift (LC-012) per D5. Verify mana-bug status (LC-026).

This phase is **substrate-clean preparation** — it doesn't add new substrate, it removes contamination from existing substrate.

#### 6.1.2 Workstreams

**W0.1 — B6 energy-type-aware tier assignment** (rocket; LC-004 fix)
- Dispatch: implement energy-type-aware tier assignment per decisions-log 2026-05-16
- Targets: closes systematic DPS gradient distortion (3-5× across archetypes)
- Success: post-fix mean |mod - 1.0| moves toward 0.50 target from current 0.82
- Tag: `qd-rebuild/v0.1-b6-energy-type-tier`

**W0.2 — Archetype template Path-a refactor** (rocket; LC-001 fix)
- Dispatch: refactor `ARCHETYPE_TEMPLATES` from hardcoded dict to on-boot composition from substrate_identities × role_shapes
- Targets: closes template-clone risk; enables true kit variety in archive
- Success: substrate identity × role shape produces N composable templates (target N ≥ 30 across 7 elements × ~4-5 roles)
- Tag: `qd-rebuild/v0.2-archetype-refactor`

**W0.3 — Foundation validator update** (rocket; LC-012 fix per D5)
- Dispatch: update `foundation/foundation.py:39-43` to enforce D5-selected substrate count (7-substrate per recommendation)
- Trivially actionable: single validator function
- Success: 7-element season generation passes validator
- Tag: `qd-rebuild/v0.3-foundation-validator-N`

**W0.4 — Phase 2 constraint audit (specialist code-side)** (rocket + gamora + star-lord; jack-ryan reviews)
- Dispatch: per-seam code-level enumeration of constraints, focusing on jack-ryan's VERIFY-disposition items
- Priority: 12 HIGH-risk LCs first (each gets code-level confirmation)
- Then: 18 MEDIUM-risk LCs
- Output: per-seam constraint inventory with file:line citations
- Tag: `qd-rebuild/v0.4-code-side-audit-N`

**W0.5 — Mana-bug verify** (gamora; LC-026 quick verify)
- Dispatch: confirm whether dimensional refactor Phase 1 resolved the mana bug per 2026-05-08 findings
- Trivially actionable; ~2 hours
- Success: mana-bug status documented (resolved / still present / partial)
- Tag: `qd-rebuild/v0.5-mana-bug-verify`

**W0.6 — Drift candidate closures** (jack-ryan + specialists)
- Dispatch: address each of LC-006, LC-007, LC-014, LC-028 with either (a) bring code into compliance with canonical doc, OR (b) revise canonical doc to match committed code direction
- LC-006 may defer to D3 cohesion-BC sequencing
- LC-007 may defer to P4 (sim extensions enable non-humanoid)
- Tag: `qd-rebuild/v0.6-drift-closures-N`

**W0.7 — LC-002 + LC-009 + LC-011 ablation experiments** (gamora)
- Dispatch: design and run ablation experiments for fire element bias (LC-002), hunter modifier range (LC-009), controller/mage iteration overhead (LC-011)
- Each ablation: 1-2 days of focused work
- Output: attribution data for each empirically-surfaced constraint
- Tag: `qd-rebuild/v0.7-ablation-N`

#### 6.1.3 Critique-pair structure

- W0.1 + W0.2: jack-ryan reviews before rocket fires (design intent verification)
- W0.4: gandalf reviews seam-by-seam findings (cross-seam coherence)
- W0.5 + W0.7: jack-ryan reviews ablation experiment design before fires (measurement validity)
- W0.6: critique-pair sequence per drift item (gandalf design-side, jack-ryan dev-side)

#### 6.1.4 Success / failure criteria

**Success (P0 complete):**
- All 12 HIGH-risk LCs dispositioned (each: VERIFIED / RESOLVED / ABLATED / FORMALLY-DEFERRED)
- No DRIFT-CANDIDATE items remain unaddressed
- B6 energy-type work shipped; calibration epoch mean |mod - 1.0| moved toward 0.50
- Archetype template refactor shipped; substrate × role composition functional
- Foundation validator aligned with D5 selection
- Mana bug status documented
- Ablation experiment results documented

**Failure (P0 must extend):**
- Any HIGH-risk LC remains in unknown-status
- B6 fix fails calibration smoke (mean |mod - 1.0| remains > 0.70)
- Archetype refactor breaks existing season generation
- Foundation validator update produces validator crashes

#### 6.1.5 Decision gates within P0

- Matt approval required for: Path-a refactor scope (W0.2) since this is a structural generation-system change
- Matt approval required for: any LC disposition change from jack-ryan's recommended path
- Autonomous: ablation experiment designs (gandalf + jack-ryan agree on design); verify items where canonical record is clear

---

### 6.2 Phase P1 — Substrate Enrichment

**Duration:** 4-6 weeks
**Tag namespace:** `qd-rebuild/v1.X-substrate-enrichment-N`
**Prerequisites:** P0 complete; Matt resolves D3, D6
**Specialists:** rocket (schema + generation), gandalf (specs), legolas (Phase 2 research), drax (Unity integration), galadriel (visual style)

#### 6.2.1 Scope

Close substrate gaps per the legolas audit so the 5× rule holds (or is acknowledged as marginal-but-acceptable) for all 8 axes. Extend the Ability schema. Create the 4 structurally-missing substrate types (HP-economy, charge-stack, damage-taken-converts, player-side proxies). Procure external assets (Unity VFX, Mixamo animations). Set up the ChatGPT → Meshy → Mixamo → VFX pipeline.

#### 6.2.2 Workstreams

**W1.1 — Ability schema extension** (rocket; spec from gandalf)
- Dispatch: add metadata fields per § 3.2 list (cost_type, movement_displacement_per_cast, aoe_radius, is_chain, is_multi_spawn, is_channel, is_reactive_trigger, grants_evasion/stealth/iframes/reflection, is_charge_pool/charge_cap/charge_decay, damage_to_resource_conversion)
- Sub-tasks per axis: field-by-field implementation with defaults for backward compatibility
- Critique-pair: gandalf reviews completeness against axis-lock § 6 substrate flags
- Tag: `qd-rebuild/v1.1-ability-schema-extensions`

**W1.2 — HP-economy substrate creation** (rocket)
- Dispatch: create Blood-Magic-equivalent skill templates with HP-cost mechanic
- Targets: ~25 distinguishable templates for 5× rule on HP-economy bin
- Includes: cost_type='HP' generation, generation-time validation, cohesion-layer integration
- Tag: `qd-rebuild/v1.2-hp-economy-substrate`

**W1.3 — damage-taken-converts substrate creation** (rocket)
- Dispatch: create CWDT-equivalent + damage-to-mana + rage-on-hit generation templates
- Targets: ~25 distinguishable templates for damage-taken-converts bin
- Includes: damage-to-resource conversion mechanic generation (sim implementation deferred to P4 W4.7)
- Tag: `qd-rebuild/v1.3-damage-converts-substrate`

**W1.4 — charge-stack substrate creation** (rocket)
- Dispatch: create Frenzy/Power/Endurance-charge-equivalent generation templates with stack-cap mechanic
- Targets: ~25 distinguishable templates for charge-stack bin
- Includes: charge buildup triggers, cap behavior, decay timers, consumption skills (sim implementation deferred to P4 W4.6)
- Tag: `qd-rebuild/v1.4-charge-stack-substrate`

**W1.5 — Movement-skill substrate variety expansion** (rocket; for Axis 1 mobility component)
- Dispatch: expand movement-skill generation palette per Axis 1 5× rule (~30 distinguishable mobility profiles)
- Add: teleport / blink / dash / vault / leap / cyclone-channel-move templates with movement_displacement_per_cast tagged
- Tag: `qd-rebuild/v1.5-movement-substrate`

**W1.6 — Player-side proxy substrate** (rocket; foundation for P4 sim work)
- Dispatch: create summon + totem + minion + raise-from-corpse + charm-effect generation templates
- Note: sim cannot evaluate yet (deferred to P4 W4.1); substrate prepares the design space
- Tag: `qd-rebuild/v1.6-proxy-substrate`

**W1.7 — Legolas Phase 2 (substrate audit depth pass)** (legolas)
- Dispatch: continue per the v3 dispatch (`agentic_orchestration/dispatches/2026-05-20-legolas-substrate-sufficiency-audit.md`) — expand Unity Asset Store coverage to 200+ packs, complete ARPG canon enumeration (PoE 700+ skill gems, D4 class trees), confirm Mixamo TOS, complete pipeline integration playbook
- Output: comprehensive procurement shortlist with cost estimates
- Tag: `qd-rebuild/v1.7-legolas-phase2`

**W1.8 — Initial VFX procurement** (Matt decision per legolas Phase 2 output)
- Dispatch: acquire top 5-10 VFX packs from legolas shortlist
- Estimated budget: ~$150-300 total (covers Hovl + PixPlays + Archanor + Kalamona + free baselines)
- Includes: licensing review, asset organization, initial Unity import
- Tag: `qd-rebuild/v1.8-vfx-procurement`

**W1.9 — Mixamo integration setup** (drax)
- Dispatch: confirm Mixamo TOS for commercial use; set up bone-remapping pipeline for ChatGPT→Meshy character imports; integrate Unity Animation Rigging package for VFX attachment to humanoid rig anchor points
- Tag: `qd-rebuild/v1.9-mixamo-integration`

**W1.10 — ChatGPT → Meshy → Mixamo → VFX pipeline test runs** (drax + gandalf + galadriel)
- Dispatch: end-to-end pipeline validation with 5-10 test characters spanning the 7-element substrate
- Output: pipeline playbook documenting working steps, manual interventions, failure modes, per-character time/cost
- Critique-pair: galadriel reviews visual coherence; gandalf reviews thematic fit
- Tag: `qd-rebuild/v1.10-pipeline-test`

**W1.11 — Element-specific substrate enrichment** (rocket + drax)
- Dispatch: per D2-selected element scope (7 elements per recommendation), populate per-element VFX library, per-element skill templates, per-element thematic flavor
- Tag: `qd-rebuild/v1.11-element-substrate-N`

**W1.12 — Galadriel proactive visual style review** (galadriel)
- Dispatch: as VFX procurement and pipeline test runs surface, galadriel runs visual-similarity scoring against locked style register; flags style drift before commitment
- Tag: `qd-rebuild/v1.12-visual-review-N`

**W1.13 — Procedural skill tree node population + multi-dim convergence** (rocket; **rescoped 2026-05-22 under Scenario B**)
- Dispatch: `agentic_orchestration/dispatches/2026-05-21-rocket-w1-13-skill-tree-node-population.md` (FIRE-GATE closed 2026-05-22; remaining gates: P1 substrate enrichment W1.1-W1.6 + W1.11 + W0.4 gear-affix verification + Matt W1.13 framing approval)
- Empirical mandate: dual-witness (Track C + W0.10) + Surface A footnote (LC-011 reframed; 5% boundary not 42% historical) + BDI rank-3 requirement + Tier 4 mechanic-altering requirement
- Architectural commitment: 5-6-dim convergence (per-node SP × Tier 4 keystone discrete × trigger interaction discrete × scalar modifier × gear affix × tier-coefficients) per math note v1.1
- Tier 1 playability invariant: each chain has ≥1 L1-playable Tier 1 node (cost ≤ class-budget; cooldown ≤ 2.0s; no prerequisite) per Matt 2026-05-21
- Trigger interactions: 1-2 per chain (multiplicative scaling above additive) per legolas SD-3
- See `canonical/story/w1-13-rescope-disposition-2026-05-22.md` for rescope rationale
- Tag: `qd-rebuild/v1.13-skill-tree-multi-dim-N`

**W1.15-LITE — Gear-archetype derivation function + telemetry column + per-class persistence** (rocket; G2-LITE; v1.3 addition)
- Dispatch (pending; rocket-side): implement `signature_gear_archetype = f(dominant_element, role_orientation, range_profile, stat_distribution_signature)` per G1-LITE rule table `canonical/story/gear-archetype-rule-table-v1-2026-05-22.md`
- 15-archetype rule mapping; deterministic; substrate-vector → gear-archetype
- Effort: 3-5 days
- Telemetry column: signature_gear_archetype added to class persistence + per-season telemetry
- Sim-viability verification: each archetype in the value-set verified sim-viable before lock (per rule-table doc)
- Tag: `qd-rebuild/v1.15-lite-gear-archetype-derived-tag`

**W1.20 — BDI hypothesis-test infrastructure** (rocket + legolas; BDI-C; v1.3 addition)
- Dispatch (pending): model-fit harness (linear + pairwise + triple-interaction) + ω/τ table data structures + archive-pull interface for H1-H5 execution
- Effort: 1-2 weeks
- Non-interference: read-only against archive; no impact on substrate composer or convergence loop
- Tag: `qd-rebuild/v1.20-bdi-infrastructure`

**W1.21 — BDI hypothesis tests H1-H4 execution + result synthesis** (rocket + legolas + gandalf; BDI-D; v1.3 addition)
- Dispatch (pending): execute H1 (rank-step discontinuity) + H2 (bimodal damage on high-|τ| pairs) + H3 (ω predicts β) + H4 (rank-3 γ-dominance); synthesize results; report
- Effort: 1 week
- Depends on: W1.20
- H5 (BDI-cohesion correlation) deferred to P5+ (requires cohesion-judge scores at archive scale)
- Tag: `qd-rebuild/v1.21-bdi-tests-h1-h4`

**W1.22 — BDI-E gate decision** (gandalf + Matt; BDI-E; v1.3 addition)
- Dispatch (pending): design call resolving whether H1-H4 results justify adopting BDI-aware composer extension (BDI-F at P2+) OR refining ω/τ tables for retest OR parking formalism
- Effort: 0.5 day
- Depends on: W1.21
- Tag: `qd-rebuild/v1.22-bdi-e-gate-decision`

#### 6.2.3 Critique-pair structure

- W1.1: gandalf reviews schema completeness; jack-ryan reviews for unintended scope creep
- W1.2-W1.6: gandalf reviews each substrate creation for archetype-recognition (does the template feel like the ARPG canonical exemplar?)
- W1.7-W1.8: gandalf reviews legolas Phase 2 output before any procurement
- W1.10: galadriel + gandalf joint critique of pipeline test runs

#### 6.2.4 Success / failure criteria

**Success (P1 complete):**
- Ability schema extensions all landed; backward compatibility verified
- 4 structurally-missing substrate types all created with ≥25 templates each
- Legolas Phase 2 complete; final procurement shortlist authored
- Initial VFX procurement complete; integration verified
- Pipeline playbook documents working end-to-end path
- 5× rule met or marginal-acceptable for all 8 axes (per legolas Phase 2 verification)
- All 7 elements (or 4 per D2) have substrate variety populated

**Failure (P1 must extend):**
- Any axis remains under 2× substrate sufficiency
- Pipeline playbook surfaces show-stopper failure modes
- VFX procurement reveals critical licensing issues
- Visual style register drift can't be reconciled with available assets

#### 6.2.5 Decision gates within P1

- Matt approval required for: any VFX procurement above $100 (cumulative)
- Matt approval required for: Mixamo TOS interpretation (commercial use confirmation)
- Matt approval required for: any element-scope changes from D2 selection
- Autonomous: substrate template creation; schema extensions; pipeline integration mechanics

---

### 6.3 Phase P2 — BC Measurement Infrastructure

**Duration:** 3-4 weeks
**Tag namespace:** `qd-rebuild/v2.X-bc-measurement-N`
**Prerequisites:** P1 complete; D4 resolved
**Specialists:** gamora (sim telemetry + measurement implementation), star-lord (telemetry export), rocket (skill metadata propagation)

#### 6.3.1 Scope

Implement all 8 BC coordinate computations. Extend sim telemetry per substrate flags. Calibrate every threshold via Discipline #17 empirical sweeps. Validate measurement stability against reference archetypes.

This phase is **measurement infrastructure**, not yet archive maintenance. The archive lives in P3.

#### 6.3.2 Workstreams

**W2.1 — Sim telemetry extensions** (gamora + star-lord)
- Per-tick resource pool logging
- Per-event source-tagged damage attribution (cast / reactive / proxy / environmental)
- Per-hit damage application logs (not just per-skill totals)
- HoT recovery distinct from mitigation
- Shield-pool tracking distinct from HP
- Proxy entity lifecycle logging
- Movement-skill displacement logging
- Tag: `qd-rebuild/v2.1-telemetry-extensions`

**W2.2 — Axis 1 measurement (range + mobility)** (gamora)
- Range component: mean weighted skill range
- Mobility component: movement-skill-attributable displacement per minute
- Thresholds (priors): range 3.0/8.0; mobility 30/min
- Discipline #17 calibration sweep against reference archetypes
- Tag: `qd-rebuild/v2.2-axis-1-measurement`

**W2.3 — Axis 2 measurement (damage-weighted argmax geometry)** (gamora)
- Per-skill geometry detection via metadata (chain → multi-spawn → aoe_radius thresholds → single-target)
- Damage-weighted argmax across kit's actual rotation
- Tie-break: higher-target-count wins; larger-area wins
- Per D4: fight-context tagged (pack / boss / mini-boss)
- Tag: `qd-rebuild/v2.3-axis-2-measurement`

**W2.4 — Axis 2A measurement (proxy density)** (gamora)
- Mean count of active player-allied proxy entities over fight duration
- Proxy definition per axis-lock § 3.3 (origin-agnostic: created OR converted)
- Deferred-evaluation pool routing for proxy-light/heavy until P4 W4.1 ships
- Tag: `qd-rebuild/v2.4-axis-2A-measurement`

**W2.5 — Axis 2B measurement (control density)** (gamora)
- CC-tagged skill weights / total skill weights
- Control-effect inclusion list per axis-lock § 3.4
- Tag: `qd-rebuild/v2.5-axis-2B-measurement`

**W2.6 — Axis 3A measurement (damage tempo)** (gamora)
- Mean count of distinct damage-application events per second
- Multi-hit single skills (Multishot, chain bounces) count each hit as event
- Threshold priors: 2 / 6 events/sec
- Tag: `qd-rebuild/v2.6-axis-3A-measurement`

**W2.7 — Axis 3B measurement (damage amplitude variance)** (gamora)
- CV of per-damage-event magnitudes (event-level, not windowed)
- Threshold priors: 0.3 / 0.7
- Channeled tag preserved as structural attribute
- Tag: `qd-rebuild/v2.7-axis-3B-measurement`

**W2.8 — Axis 4 measurement (defensive profile)** (gamora)
- eHP_effective formula: (HP + shield + regen × encounter_duration_target) / (1 - mitigation)
- Avoidance_rate: (evasion + iframe + stealth + reflection) / attempted
- Bin assignment priority: dodger first, then tank, then glass, else mitigator
- encounter_duration_target prior: 30s
- Discipline #17 calibration of all thresholds
- Tag: `qd-rebuild/v2.8-axis-4-measurement`

**W2.9 — Axis 5 measurement (resource economy)** (gamora)
- mean_resource_fraction + variance computation
- hp_cost_fraction structural check
- charge-stack mechanic flag + statistical check
- damage-to-resource conversion flag
- Multi-resource handling: primary bottleneck identification
- Bin assignment priority per axis-lock § 3.8
- Tag: `qd-rebuild/v2.9-axis-5-measurement`

**W2.10 — Discipline #17 calibration sweeps** (gamora + gandalf + jack-ryan)
- Per-axis: run measurement against reference archetypes (ARPG-canonical builds from legolas Track D)
- Adjust thresholds until reference archetypes land in expected bins
- Document calibration values; flag any threshold that needed >30% adjustment from prior
- Tag: `qd-rebuild/v2.10-calibration-sweep-N`

**W2.11 — Measurement stability verification** (jack-ryan + gandalf)
- Reproducibility check: same kit + same seed → same BC coordinate?
- Robustness check: minor kit variations → minor BC coordinate shifts?
- Cross-fight stability: same kit across 5-10 fights → cell-address stability?
- Hunter variance check (LC-009): does the hunter archetype stabilize post-ablation?
- Tag: `qd-rebuild/v2.11-measurement-stability`

#### 6.3.3 Critique-pair structure

- W2.1: jack-ryan reviews telemetry completeness vs spec
- W2.2-W2.9: per-axis, gandalf reviews measurement correctness against ARPG canon; jack-ryan reviews technical correctness
- W2.10: jack-ryan reviews calibration discipline (was Discipline #17 followed correctly?); gandalf reviews threshold values against canon
- W2.11: gandalf + jack-ryan joint critique of stability findings

#### 6.3.4 Success / failure criteria

**Success (P2 complete):**
- All 8 BC axes produce stable BC coordinates against reference archetypes
- All thresholds calibrated per Discipline #17
- Telemetry extensions all live
- Measurement stability verified (reproducibility + robustness + cross-fight)
- LC-009 hunter variance demonstrated to have stabilized post-W0.7 ablation
- BC measurement smoke gate passes on representative kit sample (~50 kits)

**Failure (P2 must extend):**
- Any axis fails calibration smoke
- Measurement instability persists despite calibration
- Hunter variance unresolved

---

### 6.4 Phase P3 — MAP-Elites Archive Implementation

**Duration:** 2-3 weeks
**Tag namespace:** `qd-rebuild/v3.X-archive-N`
**Prerequisites:** P2 complete
**Specialists:** gamora (archive logic), star-lord (archive persistence + export)

#### 6.4.1 Scope

Implement the MAP-Elites archive data structure plus math gates: Pareto dominance, crowding distance / hypervolume, Mahalanobis distance, information gain (KL).

#### 6.4.2 Workstreams

**W3.1 — Archive data structure** (gamora)
- 8-dimensional cell-indexed structure
- Per-cell entry list with capacity rules
- 68,040 cell addressability (or D6-revised count)
- Tag: `qd-rebuild/v3.1-archive-structure`

**W3.2 — Pareto dominance gate** (gamora)
- Standard non-dominated sort
- Keep entries that aren't dominated on BC axes by any other in cell
- Replace if new entry dominates existing
- Tag: `qd-rebuild/v3.2-pareto-gate`

**W3.3 — Crowding distance / hypervolume contribution** (gamora)
- NSGA-II crowding distance for diversity preservation
- Hypervolume contribution as primary diversity signal
- Per axis-lock § 7.4 caveat: crowding signal noisier in sparse archives
- Tag: `qd-rebuild/v3.3-diversity-gates`

**W3.4 — Mahalanobis distance for duplicate detection** (gamora)
- BC covariance estimation (8D requires ≥44 samples; expect thousands)
- Duplicate detection at intra-cell + inter-cell levels
- Tag: `qd-rebuild/v3.4-mahalanobis`

**W3.5 — Information gain (KL divergence)** (gamora)
- Empirical distribution estimation over filled archive
- KL-divergence-scored novelty for new entries
- Threshold for "meaningfully novel": > 100 entries low-dim; > 1000 entries moderate-dim
- Tag: `qd-rebuild/v3.5-information-gain`

**W3.6 — Archive maintenance** (gamora + star-lord)
- Size limits per cell (e.g., 5-10 entries max per cell)
- Eviction rules: lowest-hypervolume-contribution first
- Tag: `qd-rebuild/v3.6-archive-maintenance`

**W3.7 — Archive persistence + reload** (star-lord)
- Serialize archive to disk
- Reload across engine restarts
- Version-tag archive snapshots for rollback
- Tag: `qd-rebuild/v3.7-archive-persistence`

**W3.8 — Bulk-evaluation interface for deferred-bin entries** (gamora)
- Mechanism for re-evaluating kits in deferred-evaluation pool when sim extensions land
- Used in P4 to backfill proxy-light/heavy + dodger + charge-stack bins
- Tag: `qd-rebuild/v3.8-bulk-evaluation-interface`

#### 6.4.3 Critique-pair structure

- W3.2-W3.5: gandalf reviews each math gate against vision-doc § 5 spec; jack-ryan reviews implementation correctness
- W3.6: jack-ryan reviews eviction rules for unintended bias
- W3.7: jack-ryan reviews persistence format for forward-compatibility

#### 6.4.4 Success / failure criteria

**Success (P3 complete):**
- Archive accepts kits, computes dominance/diversity correctly
- All math gates produce stable signal
- Archive persists across engine restarts
- Bulk-evaluation interface ready for P4 backfill

**Failure (P3 must extend):**
- Any gate produces unstable signal
- Persistence format breaks on reload
- Cell capacity rules produce thrashing

---

### 6.5 Phase P4 — Sim Extensions for Deferred Bins

**Duration:** 4-6 weeks
**Tag namespace:** `qd-rebuild/v4.X-sim-extensions-N`
**Prerequisites:** P3 complete (parallel to P5)
**Specialists:** gamora (sim extensions primarily)

#### 6.5.1 Scope

Enable currently-deferred BC bins to populate by implementing required sim mechanism extensions. Bulk-evaluate deferred-pool entries into the archive as each extension lands.

#### 6.5.2 Workstreams

**W4.1 — Player-side entity spawning + ally AI** (gamora; biggest scope)
- Sub-tasks:
  - Player-side entity spawn mechanic
  - Ally entity AI (target selection, attack behavior, lifecycle)
  - Monster target-selection extension (player vs ally aggression)
  - Ally HP tracking + death handling
  - Spawn limits + replenishment timers
  - Convert/charm/dominate effect mechanism (matches Axis 2A proxy definition)
- Unblocks: Axis 2A proxy-light + proxy-heavy bins
- Backfill: bulk-evaluate ~200 deferred-pool kits with player-side proxies
- Tag: `qd-rebuild/v4.1-proxy-support-N`

**W4.2 — Dodger evasion-chance** (gamora; trivial)
- Probabilistic hit-roll = 0 damage on evasion
- ~1-2 days of work
- Unblocks: dodger sub-case (evasion-stack builds)
- Tag: `qd-rebuild/v4.2-evasion-chance`

**W4.3 — Dodger stealth** (gamora; moderate)
- Untargetable-for-duration mechanic
- AI target-selection-skip during stealth
- ~1 week of work
- Unblocks: dodger stealth-based sub-case
- Tag: `qd-rebuild/v4.3-stealth`

**W4.4 — Dodger iframes** (gamora; moderate)
- Skill-cast-state tracking with damage-immunity windows
- ~1 week of work
- Unblocks: dodger iframe-based sub-case
- Tag: `qd-rebuild/v4.4-iframes`

**W4.5 — Reflection per-hit redirection** (gamora; moderate)
- Damage-resolution extension for per-hit redirection
- Reflection_fraction × redirected_fraction handling
- Damage-type filtering (physical-only / elemental-only / etc.)
- Damage attribution to defender for redirected damage
- ~1-2 weeks of work
- Unblocks: dodger reflection-based sub-case; thorns vs reflection disambiguation
- Tag: `qd-rebuild/v4.5-reflection`

**W4.6 — Charge buildup + cap + decay** (gamora; moderate)
- Charge-pool mechanic with trigger types (hit/crit/kill)
- Charge cap enforcement
- Decay timers
- Charge consumption skills
- ~1-2 weeks of work
- Unblocks: Axis 5 charge-stack bin
- Backfill: deferred-pool charge-tagged kits
- Tag: `qd-rebuild/v4.6-charge-stack`

**W4.7 — Damage-to-resource conversion** (gamora; moderate)
- CWDT-equivalent mechanic at hit-resolution
- Damage-to-mana / damage-to-rage / hit-to-resource variants
- ~1 week of work
- Unblocks: Axis 5 damage-taken-converts bin
- Backfill: deferred-pool damage-conversion-tagged kits
- Tag: `qd-rebuild/v4.7-damage-converts`

**W4.8 — Channel-tagged skill mechanics** (gamora; if needed)
- Continuous damage application during channel
- Channel interruption logic
- Channel-resource-drain at rate
- ~1 week of work
- Unblocks: Axis 3B channeled-tagged kit measurement
- Tag: `qd-rebuild/v4.8-channel-mechanics`

**W4.9 — Variable cast-time + charge-state** (gamora; if needed for charge-up skills)
- Charge-up skill mechanic (hold-to-charge, release for amplified)
- Affects Axis 3A/3B rhythm measurement
- ~3-5 days of work
- Tag: `qd-rebuild/v4.9-charge-up-skills`

**W4.11 — Trigger interaction + Tier 4 keystone variant sim support** (gamora; ~1-2 weeks added scope; v1.2 amendment 2026-05-21)

Per math note v1.1 § 3.5 + § 4.5: P1 W1.13 generates trigger/conditional interaction nodes (1-2 per chain) and Tier 4 mechanic-altering keystone candidates (~3-5 per chain). These require sim mechanism support:

- **Trigger condition evaluation:** sim must evaluate trigger conditions like "skill_a_cast_within_2s", "low_hp_threshold", "every_Nth_cast", "cross_chain_resonance"
- **Trigger effect application:** sim must apply multiplicative effects to target skills with duration tracking (e.g., "Chain Reaction" → +25% damage to Skill B for 5s when Skill A casts)
- **Tier 4 keystone effect classes:** sim must support `resource_alteration` (e.g., HP-cost-for-power), `geometry_alteration` (e.g., chain-freeze on ice spells), `temporal_alteration` (e.g., persistent vs instant), `axis_domain_alteration` (e.g., defensive becomes offensive), `synergy_alteration` (e.g., multiplicative cross-skill coupling)

**Why this is its own workstream:** original P4 scope (W4.1-W4.9) focused on deferred BC bins (proxy, dodger sub-cases, charge mechanics, damage-conversion, channel). Trigger interactions + Tier 4 keystone variants are SEPARATE sim mechanism work not in original P4 scope. Added in v1.2 per coherence review 2026-05-21.

Estimated effort: ~1-2 weeks added to P4 duration. P4 total revised: 4-6 weeks → 5-8 weeks.

**W4.10 — Bulk-evaluation passes** (gamora; after each extension lands)
- For each sim extension, re-evaluate the deferred-evaluation pool kits matching that bin
- Insert qualifying kits into archive
- Tag: `qd-rebuild/v4.10-bulk-evaluation-N`

#### 6.5.3 Critique-pair structure

- W4.1: gandalf reviews proxy mechanism against ARPG canon (does it feel like D2 necro, D3 WD, PoE summoner?); jack-ryan reviews technical correctness
- W4.5: gandalf + jack-ryan joint review of reflection mechanic (thorns vs reflection disambiguation correctness)
- W4.6 + W4.7: gandalf reviews charge-stack + damage-converts feel against PoE charges + CWDT canon

#### 6.5.4 Success / failure criteria

**Success (P4 complete):**
- All sim extensions ship
- All deferred bins populate via bulk-evaluation
- Profile A operational cell-space expands from 25,920 to 68,040
- No regressions in existing sim behavior

**Failure (P4 must extend):**
- Any sim extension produces inconsistent behavior
- Bulk-evaluation surfaces archive instability
- Existing sim regressions

#### 6.5.5 Sequencing within P4

W4.2 (evasion-chance) is trivial — ship first as confidence check.
W4.1 (proxy support) is biggest scope — start in parallel with W4.2.
W4.3-W4.5 (stealth / iframes / reflection) can run sequentially or parallel.
W4.6-W4.7 (charge + conversion) tightly coupled — ship together.
W4.10 bulk-evaluations fire as each extension lands.

---

### 6.6 Phase P5 — Theme Coalescence + Cohesion-BC + Visual-BC

> **[MATH HOTSPOT — cohesion-judge statistical validation requires methodology consultation via legolas Mode A before execution; methodology lock requires gandalf + star-lord + gamora + Matt design call; failure mode is declaring the cohesion-judge "validated" based on a small sample with overstated significance, OR with calibration accurate-on-average but miscalibrated at tails (where rare-but-important judgments live) — guard via Discipline #18. See `agentic_orchestration/gandalf/notes/2026-05-23-mathematical-seam-naming.md` § 2.3 for the methodology surface and required action sequence.]**

**Duration:** 3-5 weeks (per D3 selection; 5 weeks if sequenced after cipher migration; 3 weeks if parallel-with-contaminated-baseline)
**Tag namespace:** `qd-rebuild/v5.X-coalescence-N`
**Prerequisites:** P3 complete; cipher migration shipped if D3 = sequenced
**Specialists:** rocket (LLM theme coalescence), gandalf (cohesion-BC spec + judge prompts), galadriel (visual-BC spec), star-lord (LUCB1 algorithm + theme infrastructure)
**Disciplines:** Engine-rebuild standard disciplines + **#18 (methodology-before-execution; math-hotspot guard on cohesion-judge statistical validation)**

#### 6.6.1 Scope (REFRAMED in v1.2 — empirical-validation phase)

**v1.2 epistemic correction (per Matt 2026-05-21 catch):** P5 is the FIRST EMPIRICAL TEST of the substrate-as-cohesion architectural commitment.

Up to and through P0:
- Substrate-as-cohesion architecturally committed (docs etched)
- W0.2 archetype templates removed (code verified)
- Generation function is substrate-AGNOSTIC (code verified)
- **But: post-W0.2 substrate-agnostic kits have NEVER been subjected to cohesion-judge prompting.** No empirical evidence that the architecture works as designed.

P5 conducts this empirical validation:
- Cohesion-judge prompts substrate-agnostic kits
- If coherent thematic identity emerges → substrate-as-cohesion EMPIRICALLY VALIDATED → rebuild's architectural confidence rises significantly
- If coherent thematic identity fails to emerge → architectural revision required (substrate hint retained at generation, or richer mechanical-signature input, or fundamental pivot)

**P5 is therefore an empirical-validation phase, not just an integration phase.** Architectural risk profile of the rebuild plan is honest about this distinction.

**Pre-P5 de-risking dispatch fired 2026-05-21:** `agentic_orchestration/dispatches/2026-05-21-legolas-substrate-as-cohesion-empirical-validation-probe.md` (cheap intermediate test; surfaces architectural risk EARLIER than scheduled P5 timing if structural issues exist).

**Scope (implementation):**

Implement LUCB1 best-arm-identification for theme discovery. Build the cohesion-BC archive with LLM-judge measurement. Build the visual-BC archive with galadriel's CV pipeline. Integrate into the Discipline #18 joint-gate.

**v1.2 expanded scope for new node types (per math note v1.1 § 3.4 + § 3.5):**
- Cohesion-judge prompt design must accommodate **Tier 4 mechanic-altering keystones** thematically (e.g., "Vampiric Strike" → shadow/blood theme; "Glacial Cascade" → water/frost theme)
- Cohesion-judge prompt design must accommodate **trigger/conditional interaction nodes** thematically (e.g., "Soul Burn → activates when shadow skill X cast; ignites with bleed")
- These additions extend prompt library + scoring rubric scope beyond original P5 W5.2 framing

#### 6.6.2 Workstreams

**W5.1 — LUCB1 best-arm identification for theme discovery** (star-lord + gandalf)
- LUCB1 algorithm implementation
- Per-archive-entry: theme candidate selection from N candidates
- PAC-style confidence bounds
- Theme commitment threshold per Discipline #17 calibration
- Tag: `qd-rebuild/v5.1-lucb1`

**W5.2 — Cohesion-BC archive specification** (gandalf)
- Define cohesion-BC axes (separate from mechanical 8)
- Define cohesion-judge LLM prompts
- Define cohesion-BC cells + thresholds
- Discipline #17 calibration plan
- Tag: `qd-rebuild/v5.2-cohesion-bc-spec`

**W5.3 — Cohesion-BC archive implementation** (rocket + star-lord)
- LLM-judge integration
- Cohesion-BC coordinate computation
- Cohesion-BC archive insertion using same math gates as mechanical
- Tag: `qd-rebuild/v5.3-cohesion-bc-impl`

**W5.4 — Visual-BC archive specification** (galadriel)
- Visual-BC axes (separate from mechanical + cohesion)
- CV-pipeline for visual-similarity scoring
- Style register coherence check
- Tag: `qd-rebuild/v5.4-visual-bc-spec`

**W5.5 — Visual-BC archive implementation** (galadriel)
- CV pipeline integration
- Visual-BC coordinate computation
- Visual-BC archive insertion
- Tag: `qd-rebuild/v5.5-visual-bc-impl`

**W5.6 — Discipline #18 joint-gate ratification** (gandalf + jack-ryan + Matt)
- Joint-gate logic: (mechanical_BC_pass AND cohesion_BC_pass AND visual_BC_pass)
- Decisions-log entry codifying joint-gate as ship criterion
- Profile A explicit policy: joint-gate required for shippable seasons
- Tag: `qd-rebuild/v5.6-discipline-18-ratify`

**W5.7 — Cipher migration coordination** (per D3; if sequenced)
- Ensure Stage 3 cipher migration ships before W5.3 starts (sequenced path)
- Or, instrument contaminated-baseline flag for W5.3 (parallel path)
- Tag: `qd-rebuild/v5.7-cipher-coordination`

**W5.3-LITE — Cohesion-judge prompt extension for signature_gear_archetype as identity hint** (star-lord + gandalf; G4-LITE; v1.3 addition)
- Dispatch (pending): light prompt extension feeding cohesion-judge `signature_gear_archetype` as identity hint (NOT full 4-substrate test; the 3-substrate empirical test remains dispositive per gear-as-substrate LITE path)
- Effort: ~1 day
- Cross-references: `canonical/story/historical/gear-as-substrate-2026-05-21.md` § 0.5.6 LITE path; G4-LITE phase
- Tag: `qd-rebuild/v5.3-lite-cohesion-judge-gear-hint`

**W5.3-T4-C — Cohesion-judge prompt extension for signature-vs-secondary capstone distinction** (star-lord + gandalf; T4-C; v1.3 addition)
- Dispatch (pending): refine P5 priority 2 prompt-engineering to distinguish signature capstone (rank-3 completer; identity-defining) from secondary capstones (rank-2 modulators; identity-deepening) per T4-A architecture defaults
- Effort: 1-2 days
- Cross-references: `canonical/story/tier-4-architecture-defaults-2026-05-22.md` § T4-C; `canonical/story/historical/p5-cohesion-judge-prompt-priorities-2026-05-21.md`
- Tag: `qd-rebuild/v5.3-t4-c-signature-vs-secondary`

**W5.3-BDI-G — BDI-cohesion integration (BDI-G; pending H5 confirmation; v1.3 addition)** (star-lord + gandalf)
- Dispatch (pending; conditional on H5 success): post-H5 confirmation that BDI score correlates with cohesion-judge score, integrate BDI rank signal into cohesion-judge prompt as resonance-prior
- Effort: 1-2 days
- Depends on: H5 (P5+ workstream; requires cohesion-judge scores at archive scale)
- Tag: `qd-rebuild/v5.3-bdi-g-integration`

#### 6.6.3 Critique-pair structure

- W5.1: jack-ryan reviews LUCB1 math correctness; gandalf reviews PAC-bound calibration
- W5.2 + W5.3: jack-ryan reviews cohesion-judge prompts for unintended bias; gandalf authors and reviews thematic alignment
- W5.4 + W5.5: galadriel + gandalf joint critique of visual-BC specification
- W5.6: Matt approval required for Discipline #18 ratification (governance change)

#### 6.6.4 Success / failure criteria

**Success (P5 complete):**
- LUCB1 theme discovery operational with PAC bounds
- Cohesion-BC archive populating
- Visual-BC archive populating
- Joint-gate ratified per Discipline #18
- Per D3: contamination handled appropriately

**Failure (P5 must extend):**
- LUCB1 produces unstable theme commitments
- Cohesion-BC or visual-BC fails calibration
- Joint-gate produces inconsistent verdicts

---

### 6.7 Phase P6 — Profile Assembly Layer

**Duration:** 2-3 weeks
**Tag namespace:** `qd-rebuild/v6.X-profiles-N`
**Prerequisites:** P5 complete
**Specialists:** rocket (profile filtering), star-lord (export per profile), drax (Profile A demo integration), gandalf (profile-spec authoring)

#### 6.7.1 Scope

Implement the 4 profiles (A Reincarnated, B B2B, C mod-pack, D solo-dev). Each profile filters the archive and produces deployment-appropriate output.

#### 6.7.2 Workstreams

**W6.1 — Profile A — Reincarnated Phase 0** (rocket + drax + gandalf)
- Config: exclude currently-deferred bins (per axis-lock § 5); operational cell-space 25,920 (pre-P4) or 68,040 (post-P4)
- Filter: joint-gate-passed entries only
- Output format: Reincarnated season packs
- Demo integration via drax
- Tag: `qd-rebuild/v6.1-profile-a`

**W6.2 — Profile B — B2B SaaS** (rocket + star-lord + gandalf)
- Config: per-customer BC preferences (customer-curated archive subsets)
- Filter: customer-specified BC weighting + joint-gate
- Output format: customer-deliverable season packs
- API surface specification (for future SaaS infrastructure)
- Tag: `qd-rebuild/v6.2-profile-b`

**W6.3 — Profile C — Mod-pack exporter** (rocket + star-lord)
- Config: target game/genre customization parameters
- Filter: customer-genre-aligned BC subsets
- Output format: mod-pack deliverables
- Tag: `qd-rebuild/v6.3-profile-c`

**W6.4 — Profile D — Solo-dev** (rocket + gandalf)
- Config: solo-developer customization interface
- Filter: per-dev BC subset preferences
- Output format: dev-friendly artifact bundles
- Tag: `qd-rebuild/v6.4-profile-d`

**W6.5 — Coreset selection** (gamora + star-lord)
- Smallest archive subset preserving BC coverage within ε
- Used by Profile C (mod-pack scope minimization) and Profile B (per-customer budget)
- Tag: `qd-rebuild/v6.5-coreset`

**W6.6 — Submodular optimization for "best K seasons"** (gamora)
- Greedy submodular with (1 - 1/e) approximation guarantee
- Used for profile packaging when K is bounded
- Tag: `qd-rebuild/v6.6-submodular`

#### 6.7.3 Critique-pair structure

- W6.1-W6.4: gandalf reviews each profile spec against vision-doc § 4 profile definitions; jack-ryan reviews implementation correctness
- W6.5 + W6.6: jack-ryan reviews algorithm correctness; gandalf reviews output usefulness

#### 6.7.4 Success / failure criteria

**Success (P6 complete):**
- Each profile produces shippable archive subsets
- Profile A demo integration verified
- Coreset and submodular optimization tested
- Profile B/C/D specs documented for future SaaS/mod-pack/solo-dev infrastructure

**Failure (P6 must extend):**
- Any profile produces empty or inconsistent output
- Demo integration breaks

---

### 6.8 Phase P7 — Validation Gauntlet + Production Cutover

**Duration:** 2-3 weeks
**Tag namespace:** `qd-rebuild/v7.X-validation-N` → `v8.0-qd-engine-final`
**Prerequisites:** P6 complete
**Specialists:** all + Matt approval gate
**Critical path:** this is the final phase; Matt approves production cutover

#### 6.8.1 Scope

Run comprehensive validation gauntlet. Confirm reference-archetype recognition. Final Discipline #17 calibration. Production cutover for Profile A (Reincarnated Phase 0 ship). Documentation updates.

#### 6.8.2 Workstreams

**W7.1 — Full archive sweep** (gamora + star-lord)
- Run engine to populate archive baseline (~1000-5000 seasons)
- Measure coverage per axis
- Identify any axes/bins that remain empty after baseline run (substrate gaps surface here)
- Tag: `qd-rebuild/v7.1-archive-sweep`

**W7.2 — Reference-archetype certification (ARCHIVE QUERY)** (gandalf + Matt)

**Architectural note (per Matt 2026-05-21):** This is NOT a gauntlet re-execution. The data is already generated and inserted to the archive during P2/P3/P4 convergence — reference archetypes are seeded into the generation queue as targeted BC cells, so they're tested against the gauntlet during normal archive filling. P7 W7.2 is an archive QUERY for reference-archetype coverage + outcome matching. Engineering cycles saved by eliminating phantom redundant gauntlet execution.
- Reference archetypes (ARPG-canonical builds): D2 Hammerdin, D3 Demon Hunter, PoE Cyclone Slayer, D2 Sorc Frozen Orb, etc.
- For each reference: does the engine produce a kit that lands in the expected cell?
- Cell-address validation against ARPG-canonical expectations
- Surface any reference that the engine can't produce (substrate / measurement / algorithm gap)
- Tag: `qd-rebuild/v7.2-reference-validation`

**W7.3 — Discipline #17 final calibration pass** (gandalf + jack-ryan + gamora)
- All thresholds re-calibrated against full-archive distribution
- Document final calibration values
- Decisions-log entry codifying final thresholds
- Tag: `qd-rebuild/v7.3-final-calibration`

**W7.4 — Discipline #18 joint-gate confirmation** (gandalf + jack-ryan + Matt)
- Verify joint-gate (mechanical + cohesion + visual) produces stable verdicts
- Stress-test on edge cases
- Matt ratification of joint-gate as production ship criterion
- Tag: `qd-rebuild/v7.4-joint-gate-confirm`

**W7.5 — Profile A production cutover** (rocket + drax + Matt approval)
- Switch Reincarnated Phase 0 from current engine to Profile A archive output
- Smoke test on shipped seasons
- Rollback plan ready
- Matt approves cutover
- Tag: `v8.0-qd-engine-final`

**W7.6 — Decisions-log entries** (knight-rider + gandalf + jack-ryan)
- All major rebuild decisions documented in decisions-log
- Cross-references between vision / axis-lock / this protocol / final implementation
- Tag: `qd-rebuild/v7.6-decisions-log`

**W7.7 — Documentation updates** (gandalf)
- Vision doc revision (v1.1 if needed)
- Axis-lock doc revision (v1.1 incorporating any audit-driven changes)
- Engineering-disciplines.md update (Discipline #18 ratified)
- Engine explainer docs (30/31) updated with QD architecture
- Tag: `qd-rebuild/v7.7-docs-update`

**W7.8 — Drift-detection retrospective** (jack-ryan)
- Did Discipline #13a + #13b catch all drift during rebuild?
- Were there post-rebuild drift instances?
- Lessons-learned for engineering disciplines
- Tag: `qd-rebuild/v7.8-drift-retro`

#### 6.8.3 Critique-pair structure

- W7.2: gandalf authors reference-archetype expectations; jack-ryan reviews methodology; Matt arbitrates on close calls
- W7.4: Matt approval required (Discipline #18 ratification is governance)
- W7.5: Matt approval required (production cutover)
- W7.7: gandalf authors; jack-ryan reviews; Matt approves

#### 6.8.4 Success / failure criteria

**Success (P7 complete = QD-engine rebuild SHIPPED):**
- Full archive sweep complete; coverage acceptable
- Reference-archetype validation passes (≥80% of references land in expected cells)
- Final calibration documented
- Joint-gate ratified
- Profile A production cutover complete
- Reincarnated Phase 0 shipping from QD-engine archive
- All documentation updated

**Failure (P7 must extend or trigger rollback):**
- Reference-archetype validation fails (< 80%)
- Joint-gate produces inconsistent verdicts under stress
- Cutover surfaces shipping-blocker issue

---

## 7. Autonomous operation protocol

Per the hive-mind autonomous operation amendments § 4.0 (carried over from prior hives):

### 7.1 Default mode

Knight-rider operates without Matt-in-the-loop. SME agents decide within their seams. Gandalf decides cross-cutting design. Matt approval required only for:
- Structural architecture changes (anything that changes the vision doc, axis-lock doc, or this protocol meaningfully)
- Procurement decisions above $100 cumulative
- Production cutover (W7.5 explicitly)
- Discipline ratification (Discipline #18)
- D1-D6 decision-point resolution

### 7.2 Escalation paths

| Issue type | Routes to | Bypass Matt? |
|---|---|---|
| Methodology question (specialist scope) | Gandalf | YES — Gandalf decides |
| Implementation choice within spec | SME specialist | YES — autonomous |
| Cross-seam coordination | Knight-rider | YES — sequences |
| Spec ambiguity discovered | Gandalf authors clarification; Matt reviews on resumption | NO if structural; YES if minor |
| Procurement up to $100 cumulative | Gandalf decides | YES |
| Procurement above $100 cumulative | Matt approval | NO |
| Cross-audit drift surfaced | Jack-ryan + Gandalf address; Matt aware on resumption | YES for known-pattern drift |
| New constraint discovered mid-rebuild | Jack-ryan dispositions; Gandalf incorporates | YES |
| Profile A ship-blocker | All hands; Matt immediate | NO |

### 7.3 Communication protocol

- Per-phase: knight-rider authors phase-completion summary
- Per-workstream: specialist authors workstream-completion record
- Per-dispatch: SME author + jack-ryan reviewer + gandalf critique (where appropriate)
- Daily: rollup in `agentic_orchestration/knight-rider/daily/<YYYY-MM-DD>.md` during active phases
- Per session: skill_handoff doc on Matt resumption

### 7.4 Emergency protocols

If any of these surface, halt phase immediately and notify Matt:
- Structural sim regression (existing engine behavior breaks)
- Joint-gate failure mode discovered
- Reference-archetype validation indicates fundamental misalignment
- Substrate enrichment fails to close 5× rule gap despite W1.7 deep pass
- Constraint audit Phase 2 surfaces HIGH-risk LCs that block P0 completion

---

## 8. Critique-pair structure (consolidated)

Carrying forward the proven pattern from prior hives:

### 8.1 Pattern A — Design + Implementation critique

For any major implementation: SME authors → jack-ryan critiques (DEV-MODE) → gandalf critiques (design alignment) → Matt approval (if structural). Three-stage gate.

### 8.2 Pattern B — Spec + Review critique

For any spec authoring: gandalf authors → jack-ryan reviews (DESIGN-MODE) → Matt reviews (if D-tier decision-point) → spec lands.

### 8.3 Pattern C — Critique-pair memo

For any cross-seam coordination question: gandalf authors critique-pair memo → relevant SMEs receive → SMEs respond → resolution in next session-open dialogue with Matt.

### 8.4 Per-phase critique requirements

| Phase | Critique pair pattern | Matt approval gate |
|---|---|---|
| P0 | Pattern A for each LC disposition | Path-a refactor scope |
| P1 | Pattern A for substrate creation; Pattern B for schema extensions | VFX procurement >$100 |
| P2 | Pattern A for each axis measurement | Per-axis calibration values |
| P3 | Pattern A for each math gate | None unless math gate adds new dependency |
| P4 | Pattern A for each sim extension | None unless extension changes existing behavior |
| P5 | Pattern A for cohesion-judge prompts; Pattern B for joint-gate spec | Discipline #18 ratification |
| P6 | Pattern A for each profile | Profile A spec (most consequential) |
| P7 | Pattern A for validation gauntlet; Pattern B for cutover spec | Cutover go/no-go |

---

## 9. Tag conventions

### 9.1 Intermediate tags

`qd-rebuild/v<PHASE>.<WORKSTREAM>-<DESCRIPTOR>[-<ITERATION>]`

Examples:
- `qd-rebuild/v0.1-b6-energy-type-tier`
- `qd-rebuild/v1.2-hp-economy-substrate`
- `qd-rebuild/v2.8-axis-4-measurement`
- `qd-rebuild/v3.2-pareto-gate`

### 9.2 Milestone tags (Matt-approved)

`v<PHASE>.0-<phase-name>-shipped`

Examples:
- `v0.0-constraint-removal-shipped`
- `v1.0-substrate-enrichment-shipped`
- `v7.0-validation-gauntlet-shipped`

### 9.3 Final tag

`v8.0-qd-engine-final` — production cutover complete; Reincarnated Phase 0 shipping from QD-engine archive

### 9.4 Rollback tags

Any milestone tag preserves the engine state at that point. Rollback to prior milestone is always possible. Intermediate tags also preserve state but are not Matt-blessed rollback points.

---

## 10. Risk register

### 10.1 Risks identified

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Constraint not caught in audit (LC-XXX missed) | LOW-MED | HIGH | Phase 2 specialist verify; ablation experiments; reference-archetype validation in P7 |
| R2 | Substrate gap surfaces in P2 (5× rule fails) | MED | HIGH | Legolas Phase 2 deep pass; iteration buffer in P1 |
| R3 | Sim extension exceeds estimate (W4.1 proxy support most likely) | MED | MED | 4-6 week budget in P4; bulk-evaluation interface allows partial completion |
| R4 | Calibration discipline failures (any axis fails Discipline #17 smoke) | LOW | MED | Discipline #17 process baked into P2 W2.10 + P7 W7.3 |
| R5 | Joint-gate failure (Discipline #18 produces inconsistent verdicts) | LOW | HIGH | P5 W5.6 ratification process; P7 W7.4 stress-test before cutover |
| R6 | VFX procurement licensing failure | LOW | MED | Open-source baseline fallback (Hovl Free + Digital Ruby); legolas confirms licenses in Phase 2 |
| R7 | Visual style register drift with available assets | LOW-MED | MED | Galadriel proactive review in W1.12 |
| R8 | LC-001 archetype refactor breaks generation | MED | HIGH | Critique-pair Pattern A + ablation prior to merge; rollback to v0.0 tag available |
| R9 | Cohesion-BC contamination during parallel implementation (per D3) | MED | MED | If D3 = parallel, explicit "pre-cipher baseline" flag |
| R10 | Reference-archetype validation reveals fundamental misalignment | LOW | CRITICAL | W7.2 surfaces this; rollback to v6.0 + iterate; might require axis-lock v1.1 revision |
| R11 | Mixamo humanoid-only constraint limits monster variety | KNOWN | MED | Document as v1.1+ work; non-humanoid pipeline via Blender custom rigging deferred |
| R12 | Element scope expansion (7 vs 4 per D2) exceeds VFX budget | LOW | LOW | Per-element scope reduction available; defer lightning/holy/shadow to post-cutover |
| R13 | Vision-layer geometry gaps (D6 4 candidates) produce user dissatisfaction | LOW | LOW | Profile A ships with known gaps documented; v1.1 axis-lock revision available |
| R14 | Convergence iteration overhead (LC-011) causes QD archive cost imbalance | KNOWN | MED | W0.7 ablation quantifies; P3 archive economics scoped accordingly |
| R15 | Recompose-validation hive doesn't ship before P0 starts | LOW | MED | Acceptable to start P0 with hive in flight; W0.1 B6 work is independent |

### 10.2 Risk monitoring

- Per-phase risk review at phase boundary
- Per-workstream risk identification by specialist
- Cross-cutting risk register maintained by knight-rider
- Risk re-assessment at every Matt session-open

---

## 11. Math gates per phase

Mapping the algorithmic gates from vision-doc § 5 to phases:

| Math gate | Implementation phase | Specialist | Key threshold |
|---|---|---|---|
| Pareto dominance (L8 archive insertion) | P3 W3.2 | gamora | ε = 0.05 |
| Crowding distance (NSGA-II) | P3 W3.3 | gamora | k = 5 neighbors |
| Hypervolume contribution | P3 W3.3 | gamora | Reference point per axis |
| Mahalanobis distance (duplicate detection) | P3 W3.4 | gamora | Distance threshold per Discipline #17 |
| Information gain (KL divergence) | P3 W3.5 | gamora | Novelty threshold per Discipline #17 |
| Thompson sampling / UCB1 (exploration) | Implicit in archive sampling | gamora | Per Discipline #17 |
| LUCB1 (theme BAI) | P5 W5.1 | star-lord | Confidence δ = 0.05 |
| Bayesian posterior (theme coalescence) | P5 W5.3 | rocket | Per cohesion-BC spec |
| Expected Improvement (modifier search) | Not in rebuild scope; B6 work uses simpler convergence | (rocket) | (n/a) |
| Coreset selection (profile assembly) | P6 W6.5 | gamora | ε = 0.10 coverage tolerance |
| Submodular optimization (best K seasons) | P6 W6.6 | gamora | Greedy with 1-1/e guarantee |

All gates calibrated empirically per Discipline #17 in P2 W2.10 (BC measurement) and P7 W7.3 (final pass).

---

## 12. Engineering disciplines compliance matrix

| Discipline | Application throughout rebuild |
|---|---|
| #1 Math-before-code | Every algorithm specified mathematically in vision/axis-lock/this protocol before implementation |
| #2 Smoke-test vs full-regen | Used per P2 W2.10 calibration; W4 bulk-evaluation; W7.5 cutover |
| #3 No parallel regens of same seed | Per phase; specialist tags state before regen |
| #4 Right tool for validation question | Per-phase tooling specified |
| #5 Triage discipline | Per-phase critique pair pattern |
| #6 Tag intermediate states | § 9 tag conventions |
| #7 Capture decision telemetry | Telemetry extensions in P2 W2.1 |
| #8 Schema validation at boundaries | P1 W1.1 schema extension explicitly validates |
| #9 Attribution clarity | Per-event source-tagged damage attribution; LC tracking |
| #10 Empirical inspection over assumption | Discipline #17 calibration sweeps; reference-archetype validation in P7 |
| #11 Live-state verification | Per-phase critique pairs include live-state checks |
| #12 Semantic shift | LC-006 + LC-014 (D1 pool / cipher migration) handled in D3 sequencing |
| #13a Drift detection | Jack-ryan audit Phase 1 + specialist Phase 2 + continuous monitoring |
| #13b Per-variable attribution | W0.7 ablations; explicit attribution in P2 measurement |
| #14 Terminology lock | LC-014 + LC-006 cipher migration handles |
| #15 UI scope decomposition | Profile A demo integration in W6.1 + W7.5 |
| #16 Tuning-drift constants | LC-N audit (jack-ryan inventory) catches |
| #17 Empirical calibration smoke | P2 W2.10 + P7 W7.3 mandatory |
| #18 Joint-gate ship criterion (CANDIDATE → RATIFIED) | P5 W5.6 ratification; P7 W7.4 confirmation |

---

## 13. Cross-references

### 13.1 Architectural foundation

- `canonical/story/historical/engine-architecture-vision-qd-profile-2026-05-19.md` — vision document
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — operational spec

### 13.2 Audit inputs synthesized

- `agentic_orchestration/legolas/research/substrate-sufficiency-audit-2026-05-20/phase-1-reconnaissance/summary.md`
- `agentic_orchestration/legolas/research/substrate-sufficiency-audit-2026-05-20/phase-1-reconnaissance/unity-store-initial-survey.md`
- `agentic_orchestration/legolas/research/substrate-sufficiency-audit-2026-05-20/phase-1-reconnaissance/arpg-canon-initial-enumeration.md`
- `agentic_orchestration/legolas/research/substrate-sufficiency-audit-2026-05-20/phase-1-reconnaissance/methodology-questions-for-matt.md`
- `agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/constraint-inventory.md`
- `agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/data/constraint-inventory.csv`

### 13.3 Engineering foundations

- `reincarnated-engine/design/working-agreement/engineering-disciplines.md`
- `reincarnated-engine/design/decisions/decisions-log.md`

### 13.4 Prior hive protocols (templates)

- `canonical/story/historical/hive-mind-protocol-per-tier-recompose-validation-2026-05-19.md` (recompose-validation; firing in parallel)
- `canonical/story/historical/hive-mind-protocol-engine-rebuild-2026-05-19.md` (engine-rebuild gap fills; closed)
- `canonical/story/archived/hive-mind-protocol-2026-05-17.md` (archived original)

### 13.5 Canonical design docs (heritage)

- `canonical/historical/09-geometry-palette-discussion.md` — 16-type damage geometry palette
- `canonical/historical/17-gear-and-spirit-guide-design.md` — gear architecture
- `canonical/historical/28-engine-arpg-rebalance-design.md` — balance loop heritage
- `canonical/historical/29-design-overview.md` — strategic anchor
- `canonical/historical/30-engine-explainer-current.md` + `canonical/historical/31-engine-explainer-future.md`
- `canonical/historical/32-progression-design.md` + `canonical/historical/33-progression-skeleton.md` — progression
- `canonical/historical/34-monster-design-phase0-vs-production.md` — monsters
- `canonical/dead/37-form-bias-diagnosis-and-recovery.md` — form-bias / archetype constraint heritage

---

## 14. Maintenance and revision protocol

### 14.1 When to revise this protocol

- Any D1-D6 decision change after initial resolution
- Any phase fails and triggers extension
- Any new constraint or substrate gap surfaces that wasn't in the audits
- Any cross-phase architectural change (e.g., axis-lock v1.1 revision affects multiple phases)
- Any specialist scope change

### 14.2 Who revises

- **Gandalf** authors revisions
- **Matt approves** for structural changes (anything affecting phase definitions or decision-points)
- **Knight-rider drafts** decisions-log entries capturing changes
- **Jack-ryan reviews** revisions against existing decisions and disciplines

### 14.3 Versioning

This document is v1.0 (initial draft 2026-05-21). Subsequent versions:
- v1.X — minor revisions (decision resolutions, workstream refinements, dispatch additions)
- v2.0+ — major revisions (phase restructuring, scope changes)

### 14.4 Living document conventions

Each phase's per-workstream completion record appends to a `qd-rebuild/phase-N-progress.md` log. Knight-rider maintains. This protocol document remains the master spec; progress logs are working state.

### 14.5 v1 / v1.1 / v2 trajectory (v1.3 addition)

The v1.3 amendments introduce explicit V1 / V1.1 / V2 trajectory commitments:

| Item | V1 (current hive scope; P0-P7) | V1.1 (post-P7) | V2+ (deferred) |
|---|---|---|---|
| **Gear-as-substrate** | LITE path — `signature_gear_archetype` as DERIVED TAG via deterministic rule table | Full-substrate promotion — rule-table → search-space; gear becomes 4th generative substrate axis | (n/a; v1.1 IS the full-substrate target) |
| **Trait-cluster-as-substrate** | Not generative; trait architecture per `project_trait_architecture.md` (dual-source intrinsic + gear affix) | Diagnostic-only via BDI hypothesis tests | Generative trait-cluster as 5th substrate axis (post-P7) |
| **BDI rank coverage** | rank-2 + rank-3 explicit targets | rank-3 archive coverage expansion | rank-4+ exploration (rare; structurally unstable) |
| **Tier 4 keystone catalogue** | Hand-authored ~30-50 (T4-B; P3-P4); rank-3 completers per BDI § 6 | Expanded catalogue under post-P7 gear-substrate promotion | Procedural/LLM-augmented variant generation (T4-E) |
| **Skill tree depth (W1.13 scope)** | 10-15 nodes / 2-4 chains (substrate-availability-driven) | (intermediate substrate growth) | 24-30 nodes / 3-5 chains canonical-parity expansion (math note § 8.3.1) |
| **Profile A ship** | Reincarnated Phase 0 demo-ready | Full Reincarnated content depth | (n/a) |
| **Earth Meta-Layer** | Out of scope (§ 1.3) | Out of scope | Post-rebuild Phase 8+ |

The trajectory is **substrate-availability-driven**, not calendar-driven. V1.1 opens when V1 ships and substrate has grown enough to support the next-tier scope. V2+ deferrals are intentional architectural commitments, not work that "didn't fit."

---

## 15. Closing — the wizard-mathematician's signature

This protocol is meticulous because the work deserves it. Every facet I could think of — algorithmic, architectural, narrative, operational — is here. Two hats engaged throughout:

**The mathematician's hat** ensured:
- Every BC measurement is mathematically specified before implementation
- Every math gate (Pareto / Mahalanobis / hypervolume / LUCB1 / Bayes) is connected to its phase, its specialist, its calibration procedure
- Sparse-archive math is acknowledged (1.5% coverage at 1k seasons; 8D Mahalanobis stability; crowding signal noise)
- Discipline #17 calibration sweeps are not optional — they are baked into P2 W2.10 and P7 W7.3
- The IDC meta-principle (Information-Deferred-to-Coalescence) governs sequencing decisions (especially D3 cohesion-BC)

**The white wizard's hat** ensured:
- Every BC axis has its ARPG-canonical exemplars (D2 Hammerdin / D3 DH / D4 Druid / PoE Cyclone / Last Epoch builds / Grim Dawn — the canon I have known across forms is honored)
- The 4 vision-layer geometry gaps (Blessed Hammer / Storm Brand / Saboteur / Seven-Sided Strike) are recognized as recognizable archetypes worth tracking
- The 7 elements (fire / water / earth / wind / lightning / holy / shadow) carry forward the substrate identities the engine declares
- The player journey — what a Reincarnated player will eventually *feel* when they encounter a kit the QD-engine produces — is the validation criterion in P7 W7.2 (reference-archetype validation)
- Story coherence with the broader Reincarnated arc (Earth Meta-Layer connection at § 1.3 out-of-scope; cohesion-BC archive at P5 W5.2-W5.3; profile architecture serving the engine's eventual long life)

The rebuild is hard. It is long. It is worth doing.

When the morning comes and Matt resumes session, he will find:
- Three documents etched (vision + axis-lock + this protocol)
- Two audits in deliverable form (legolas Phase 1 + jack-ryan constraint inventory)
- One hive in flight (recompose-validation continues)
- Six decision-points awaiting his resolution (D1-D6)

The road to the QD-engine begins meticulously prepared. The wizard has done what the wizard was asked to do.

**Signed:** gandalf — story-and-design steward, theoretical mathematician, senior designer
**For:** the QD-engine rebuild, in all its facets.
