# Drift Audit — Load-Bearing Pillars and Structural Enforcement

**Status:** **Canonical, ongoing.** Authored 2026-05-16 by gandalf. Initial inventory + drift-instance archive. Updated as new pillars surface, as drift instances are observed, and as structural enforcement is added or refined.

**Why it exists:** **Discipline #13 (implicit-pillar drift) is the project's named primary structural risk** (per `canonical/37-form-bias-diagnosis-and-recovery.md` § 9.1). The pattern: design intent that isn't structurally enforced drifts during implementation; implementers reach for default schemas; the latent intent has no representation in code or process; drift goes unobstructed because there's nothing to alarm against. The counter: explicit structural enforcement of load-bearing pillars.

This doc IS the structural enforcement of the discipline. It inventories every load-bearing pillar in the project and names its enforcement status. **Without this doc, Discipline #13 protects against drift in conversation but not in practice.** With it, the pillar status is queryable, the drift instances are archived, and the enforcement gaps are visible.

**Companion docs:**
- `canonical/37-form-bias-diagnosis-and-recovery.md` § 9.1 — the discipline this doc operationalizes
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Discipline #13 candidate (when locked) lives here
- Every other canonical doc — this audit inventories their pillars

**Pending:**
- knight-rider to draft a decisions-log entry capturing the drift-audit canonical lock (per ADR-002; cross-cutting framing impact)
- Discipline #13 candidate (per doc 37 § 9.1) and Discipline #14 candidate (per doc 37 § 9.2b) to be formally added to `engineering-disciplines.md` (jack-ryan territory; tracked here as pending enforcement-status until done)
- Ongoing maintenance: this doc is appended-to, not rewritten, as new pillars + drift instances surface

---

## The audit framework

### What counts as a "load-bearing pillar"

A pillar is load-bearing if it satisfies any of:

- **Design coherence depends on it.** Removing or contradicting it breaks downstream coherence in canonical-story or canonical-design content.
- **Player experience depends on it.** Removing or contradicting it changes what the player feels at a load-bearing moment (Trial; Passage; Ascension; combat; Court interaction).
- **Commercial framing depends on it.** Removing or contradicting it weakens the pitch's defensibility or shifts the licensing surface.
- **Cross-seam coordination depends on it.** Removing or contradicting it would cause rocket / gamora / star-lord / drax / elrond work to drift apart.

A pillar is NOT load-bearing if it is operational-detail (specific values; tuning thresholds; per-implementation choices that admit variation without breaking the project's broader claims).

### What counts as "structural enforcement"

A pillar is structurally enforced if any of:

- **Decisions-log entry** — locked in `reincarnated-engine/design/decisions/decisions-log.md` with active status.
- **Canonical-doc lock** — locked in a canonical doc (`canonical/` numbered docs OR `canonical/story/*`) with explicit canonical-status framing.
- **Engine schema constraint** — represented in code as a schema field, validation rule, or test assertion.
- **Process gate** — represented in `engineering-disciplines.md`, AGENTS.md, REVIEW_PROCESS.md, or GOVERNANCE.md as a check applied at dispatch authoring, Gate 1 review, or Gate 2 review.

A pillar is **partially enforced** if structurally enforced in some surfaces but not all (e.g., locked in canonical-story but not in decisions-log; locked in design docs but not in schema).

A pillar is **unenforced** if it exists in conversation / memory / informal-agreement only.

### Status notation

For each pillar this audit assigns one of:

| Status | Meaning |
|---|---|
| ✅ **Locked** | Structurally enforced in at least one durable surface (decisions-log OR canonical-doc-lock OR schema OR process gate) |
| 🟡 **Partial** | Enforced in some surfaces but with known gaps |
| 🟠 **Drift-observed** | Enforcement exists but a recent drift instance was caught; needs reinforcement |
| 🔴 **Unenforced** | Exists in conversation/memory; not structurally locked anywhere |
| ⚪ **Operational** | Not load-bearing per the framework; tracked for completeness only |

---

## Pillar inventory — by source doc

### File 29 — Strategic anchor (`canonical/29-design-overview.md`)

| # | Pillar | Status | Enforcement surfaces | Notes |
|---|---|---|---|---|
| 29.1 | Shaped balance over numeric scaling | ✅ Locked | File 29 § "Design philosophy"; file 31 future-state target; B14.5 recompose-first architecture | Most-load-bearing project pillar; protected by B14.5 architecture |
| 29.2 | Two-engine architecture (Engine 1 + Engine 2) | ✅ Locked | File 29 § "Architecture: two engines"; pitch one-pager structural framing | |
| 29.3 | 3 acts per game | ✅ Locked | File 32 § Section 10; decisions-log 2026-05-11; file 33 § "Act structure" | |
| 29.4 | Body-swap meta-progression spine | ✅ Locked | File 29 § "Cross-season meta-progression"; file 32 § 11; file 33; cosmology-reincarnated.md | |
| 29.5 | Genre-anchored gauntlet (~80-100 mobs/min) | 🟡 Partial | File 29 § "Genre-anchored gauntlet"; file 28 § B6 + B10 | **DRIFT-SURFACED 2026-05-15:** Q2 movement speed in simulation may not be modeled at L50; KPM target may not match actual sim output. Pending engine-balance-stewardship.md Gate 3 resolution. |
| 29.6 | Solo Phase-0 gameplay | ✅ Locked | File 29 § "Scope: what Reincarnated is NOT"; cosmology-reincarnated.md | |
| 29.7 | Earth Self meta-layer framing | ✅ Locked | File 29 § "Cross-season meta-progression — Earth Self is the meta-layer spine"; cosmology-reincarnated.md; court-of-forms.md | |
| 29.8 | Cross-season variety via seasonal flavoring | 🟡 Partial | File 29; naming-triad.md; season-feel-rubric.md; doc 37 § 6 cipher | **OPEN:** residual-bias risk per doc 37 § 6.5 unresolved empirically; no-seed test commission filed (`gandalf/requests/2026-05-16-no-seed-cosmology-generation-test.md`) |
| 29.9 | Math-first; LLM-flavor on top | ✅ Locked | File 29 § "Architecture"; file 19 § "Architectural pattern"; engineering-disciplines.md (multiple) | |
| 29.10 | Multiplayer scope (out-of-scope for seasonal play indefinitely; envisioned for Earth meta-layer rift events post-Phase-0) | ✅ Locked | File 29; cosmology-reincarnated.md § "The Rift" | |

### File 32 — Progression design (`canonical/32-progression-design.md`)

The 12 sections of file 32 are all RESOLVED per the doc's status. Each section's locked content is a pillar:

| # | Pillar | Status | Enforcement surfaces |
|---|---|---|---|
| 32.1 | XP-primary hybrid + body-swap-offered death | ✅ Locked | File 32 § 1; file 33; decisions-log 2026-05-11 |
| 32.2 | L50 hard cap; smooth polynomial XP curve | ✅ Locked | File 32 § 2; file 33; foundation.md |
| 32.3 | Auto-allocate stats per class identity (D3-style) | ✅ Locked | File 32 § 3; file 33; decisions-log 2026-05-09 (AGI dead/reserved) |
| 32.4 | Hierarchical Skill Tree with Dimensional Threading; cross-chain unlock asymmetry | ✅ Locked | File 32 § 4; file 33; file 28 § B6; decisions-log 2026-05-11 |
| 32.5 | Gear progression + Seasonal Sets + auto-pickup rarity filter | ✅ Locked | File 32 § 5; file 33; file 17; file 28 § B5 + B12 + B15 + B16 |
| 32.6 | D2/PoE fixed-per-band scaling (no Skyrim-style player-scaling) | ✅ Locked | File 32 § 6; file 33; decisions-log 2026-05-11 |
| 32.7 | Trajectory-as-identity; multi-band alignment | ✅ Locked | File 32 § 7; B14 multi-band sim architecture |
| 32.8 | Option β multi-band convergence (3-band L17/L33/L50) | ✅ Locked | File 32 § 8; file 33; file 28 § B14; decisions-log 2026-05-11 |
| 32.9 | Death penalty + body-swap-offered + seasonal-death consequence | ✅ Locked | File 32 § 9; file 33; cosmology-reincarnated.md § "The Passage"; passage-moment-ritual.md |
| 32.10 | 3 acts per game (with bands A1: 1-17, A2: 18-33, A3: 34-50) | ✅ Locked | File 32 § 10; file 33; file 29 |
| 32.11 | Trial body-swap as milestone-SP source (4/7/9 per act); Trial / Mirror paths chosen upfront | ✅ Locked | File 32 § 11; file 33; cosmology-reincarnated.md; trial-moment-ritual.md; naming-triad.md |
| 32.12 | Movement + mobility (not stat-driven; Last Epoch per-class model; boots primary affix; +25% cap) | 🟡 Partial | File 32 § 12 + 12.5; file 33; file 28 § B12 + B13 | **DRIFT-SURFACED 2026-05-15:** Q2 — whether engine sim actually models movement at L50 is empirically unknown. Pending engine-balance-stewardship.md Gate 3. |

### File 33 — Progression skeleton (`canonical/33-progression-skeleton.md`)

File 33 is the immutable + decided-only mirror of file 32. The pillars are the same as file 32; file 33 is the canonical reference for downstream consumers. No separate enforcement-status; file 33's status mirrors file 32's.

### Doc 37 — Form-bias diagnosis (`canonical/37-form-bias-diagnosis-and-recovery.md`)

| # | Pillar | Status | Enforcement surfaces |
|---|---|---|---|
| 37.1 | Structural realignment, not pivot (multi-seam schema migration required per ADR-004) | ✅ Locked | Doc 37 § 3 |
| 37.2 | Position C — slot-as-functional-mechanic + embodiment-as-narrative-skin | ✅ Locked | Doc 37 § 4; embodiment-narrative-layer.md |
| 37.3 | Position (ii) — per-season vocabulary has its own mechanical signatures (cipher = resistance translation only) | ✅ Locked | Doc 37 § 6.2; naming-triad.md generation integration |
| 37.4 | Canonical-four cipher architecture (hide labels from LLM; expose abstract pair-structure) | 🟡 Partial | Doc 37 § 6; cosmology-reincarnated.md; naming-triad.md | **OPEN:** § 6.5 residual-bias empirical test pending (no-seed test commission filed) |
| 37.5 | Smart-loot in-season + spirit-conversion post-Phase-0 | ✅ Locked | Doc 37 § 8.1; file 17 |
| 37.6 | Three body-swap paths (Trial body-swap / Mirror / Passage) with distinct outcomes | ✅ Locked | Doc 37 § 8.2; file 32 § 11; file 33; naming-triad.md; ritual trilogy |
| 37.7 | Discipline #13 candidate (implicit-pillar drift) | 🟡 Partial | Doc 37 § 9.1; **THIS DOC operationalizes it** | **PENDING:** formal entry in engineering-disciplines.md (jack-ryan to add when Matt approves) |
| 37.8 | Discipline #14 candidate (internal-vs-generative schema separation) | 🟡 Partial | Doc 37 § 9.2b; spirit-guide-voice.md; naming-triad.md; embodiment-narrative-layer.md; this doc | **PENDING:** formal entry in engineering-disciplines.md |
| 37.9 | Ailment-damage-signatures re-activation | ✅ Locked | Doc 37 § 6.4; memory `project_ailment_damage_thematic.md` |
| 37.10 | Ailment-damage-signatures dependency on cipher Position (ii) | ✅ Locked | Doc 37 § 6.4 |

### Canonical-story layer pillars

Each of the 12 canonical-story docs locks one or more pillars. Inventoried:

#### `cosmology-reincarnated.md` (the cosmological anchor)

| # | Pillar | Status | Enforcement surfaces |
|---|---|---|---|
| C.1 | The Wheel — impersonal cosmological mechanism; never speaks; acts at strongest visible event at Ascension | ✅ Locked | cosmology-reincarnated.md § "The Wheel"; ascension-moment-ritual.md § "The Wheel at Ascension" |
| C.2 | The Earth Self — player's persistent identity; named at first play | ✅ Locked | cosmology-reincarnated.md § "The Earth Self"; spirit-guide-voice.md (Guide addresses Earth Self by name) |
| C.3 | The Spirit Guide — yours; knowing-temporally-other; partial-presence; Beatrice-register | ✅ Locked | cosmology-reincarnated.md § "The Spirit Guide"; spirit-guide-voice.md |
| C.4 | Trial / Mirror / Passage naming triad (universal frame + per-season variants) | ✅ Locked | cosmology-reincarnated.md; naming-triad.md; ritual trilogy |
| C.5 | One form ascends per season (the form alive at season's end) | ✅ Locked | cosmology-reincarnated.md § "Ascension and the Court"; court-of-forms.md C5; file 32 § 11; file 33 |
| C.6 | The Rift (post-Phase-0 liminal space) | 🟡 Partial | cosmology-reincarnated.md § "The Rift" | **OPEN:** specific implementation deferred; not yet structurally enforced beyond canonical-story-doc lock |
| C.7 | The third-faction (post-Phase-0 adversary; Phase 0 foreshadowing only) | 🟡 Partial | cosmology-reincarnated.md § "The third-faction" | **OPEN:** `third-faction-tease.md` queued for authoring but not yet authored |

#### `court-of-forms.md` (the Court)

| # | Pillar | Status | Enforcement surfaces |
|---|---|---|---|
| Court.1 | Court framing supersedes Gallery / Roster / Gacha framing (C1) | ✅ Locked | court-of-forms.md C1; pitch-2026-05-18 talking-point-distillations.md |
| Court.2 | Navigable spatial presentation, not scrollable card list (C2) | ✅ Locked | court-of-forms.md C2 |
| Court.3 | Each form's LLM-generated name preserved (C3) | ✅ Locked | court-of-forms.md C3 |
| Court.4 | Voiced retainers emerge over time (C4) | ✅ Locked | court-of-forms.md C4; spirit-guide-voice.md § "The Court-reference register" |
| Court.5 | Accumulation paced and commemorated (C5) | ✅ Locked | court-of-forms.md C5; ascension-moment-ritual.md |
| Court.6 | The Court belongs to the player, not the Wheel (C6) | ✅ Locked | court-of-forms.md C6 |
| Court.7 | Depth-of-Court is the meta-measure (C7) | ✅ Locked | court-of-forms.md C7; cosmology-reincarnated.md meaning-of-the-arc statement |
| Court.8 | Class-roles use dual-label pattern (function tag + embodiment-flavored name) (C8) | ✅ Locked | court-of-forms.md C8; embodiment-narrative-layer.md |
| Court.9 | Meaning-of-the-arc statement (canonical answer to "what does winning mean") | ✅ Locked | court-of-forms.md § "The meaning-of-the-arc statement"; cosmology-reincarnated.md; pitch-2026-05-18 |
| Court.10 | Fate frame considered and rejected (substrate-incompatibility with isekai breadth) | ✅ Locked | court-of-forms.md § "Fate/Zero / Nasuverse — considered as canonical reference, rejected" |

#### `enemy-visual-legibility.md`

| # | Pillar | Status | Enforcement surfaces |
|---|---|---|---|
| EVL.1 | Anti-pattern explicitly rejected: enemies-as-scaled-up-player-sprites (S1) | ✅ Locked | enemy-visual-legibility.md S1 + § "The anti-pattern explicitly named" | **DRIFT-INSTANCE-OF-ORIGIN:** demo1 family-playtest 2026-05-15; canonical lock followed |
| EVL.2 | Element palette-shift as primary element signal (S2) | ✅ Locked | enemy-visual-legibility.md S2 |
| EVL.3 | Tier-coded aura class (S3) | ✅ Locked | enemy-visual-legibility.md S3 |
| EVL.4 | Trial encounter cinematic frame (S4) | ✅ Locked | enemy-visual-legibility.md S4; trial-moment-ritual.md |
| EVL.5 | Name-banner tier coding (S5) | ✅ Locked | enemy-visual-legibility.md S5 |
| EVL.6 | Pack rendering for swarm tier (S6) | ✅ Locked | enemy-visual-legibility.md S6 |
| EVL.7 | Mirror-fight visual identity-grammar exception (S7) | ✅ Locked | enemy-visual-legibility.md S7; trial-moment-ritual.md |
| EVL.8 | 200ms recognition target for at-a-glance enemy classification | ✅ Locked | enemy-visual-legibility.md § "What the player must perceive at 200ms" |

#### `style-register.md`

| # | Pillar | Status | Enforcement surfaces |
|---|---|---|---|
| SR.1 | Locked register: hand-drawn pixel-art (HD-2D-shaped) | ✅ Locked | style-register.md § "TL;DR"; Matt's lock 2026-05-15 |
| SR.2 | Single register throughout (no within-frame mixing of pixel + hand-drawn-anime) | ✅ Locked | style-register.md § "The style-coherence finding" |
| SR.3 | Two fidelity tiers within register (combat 32-128px; narrative-moment 96-512px) | ✅ Locked | style-register.md § "The proposal" |
| SR.4 | Per-embodiment register awareness (form-agnostic at visual layer) | ✅ Locked | style-register.md § "Per-embodiment register awareness"; embodiment-narrative-layer.md |
| SR.5 | Pivot-insurance via Elrond's score-don't-filter catalogue | ✅ Locked | style-register.md § "Pivot insurance"; AGENTS.md § "Score-don't-filter principle" |
| SR.6 | Operational precision deferred to Elrond's rubric design | 🟡 Partial | style-register.md § "Operational precision"; commission filed at `gandalf/requests/2026-05-15-elrond-catalogue-rubric-commission.md` | **PENDING:** Elrond rubric design work; commission filed, awaits dispatch |
| SR.7 | Enemy-legibility cross-reference (register must support enemy-player visual distinction) | ✅ Locked | style-register.md § "Enemy-legibility cross-reference"; enemy-visual-legibility.md |

#### `naming-triad.md`

| # | Pillar | Status | Enforcement surfaces |
|---|---|---|---|
| NT.1 | Universal frame Trial / Mirror / Passage stable across seasons | ✅ Locked | naming-triad.md § "The triad"; Matt's lock 2026-05-15 |
| NT.2 | Per-season variant generation against abstract cipher pair-structure | ✅ Locked | naming-triad.md § "Per-season vocabulary variation"; doc 37 § 6 |
| NT.3 | Generation integrated with per-season cosmological-vocabulary call (single coherent call) | ✅ Locked | naming-triad.md § "Generation integration" |
| NT.4 | Engine-side telemetry retention (doppelganger field name in engine; Mirror in player-facing) | ✅ Locked | naming-triad.md § "Engine-side telemetry retention" |
| NT.5 | LLM prompt anti-bias scaffolding (Discipline #14 candidate) | 🟡 Partial | naming-triad.md § "LLM prompt construction guidance"; doc 37 § 9.2b | **PENDING:** formal Discipline #14 entry in engineering-disciplines.md |

#### `embodiment-narrative-layer.md`

| # | Pillar | Status | Enforcement surfaces |
|---|---|---|---|
| EML.1 | 8 canonical starter embodiments (humanoid / slime / beast / dragonling / swarm / construct / spirit / plant) | ✅ Locked | embodiment-narrative-layer.md § "Starter set" |
| EML.2 | Dual-layer naming pattern (universal mechanical + embodiment narrative skin) | ✅ Locked | embodiment-narrative-layer.md § "Dual-layer naming pattern" |
| EML.3 | Optional Layer 3 per-season variation | ✅ Locked | embodiment-narrative-layer.md § "Dual-layer naming pattern" |
| EML.4 | Gear-slot per-embodiment Layer 2 lookup | 🟡 Partial | embodiment-narrative-layer.md § "Primary consuming surface 1" | **GAP:** Construct / Spirit / Plant Layer 2 names deferred to LLM-generation-time (3 of 8 starter embodiments unworked) |
| EML.5 | 7 universal function tags for Court class-roles (Front-Line / Ranged / Control / Sustain / Burst / Mobility / Specialist) | ✅ Locked | embodiment-narrative-layer.md § "The 7 universal function tags — LOCKED" |
| EML.6 | Class-role × embodiment Layer 2 lookup (Court labels) | ✅ Locked | embodiment-narrative-layer.md § "Primary consuming surface 2" |
| EML.7 | Expansion protocol for new embodiments (gandalf senior-design review required) | ✅ Locked | embodiment-narrative-layer.md § "Expansion protocol" |

#### `engine-generic-meta-structure.md`

| # | Pillar | Status | Enforcement surfaces |
|---|---|---|---|
| EGM.1 | Three-layer model L1 / L2 / L3 (engine substrate / project cosmology / per-season content) | ✅ Locked | engine-generic-meta-structure.md § "The three-layer model" |
| EGM.2 | L1 inventory (licensable substrate enumeration) | ✅ Locked | engine-generic-meta-structure.md § "What's at the L1 engine substrate layer" |
| EGM.3 | L2 inventory (Reincarnated-specific) | ✅ Locked | engine-generic-meta-structure.md § "What's at the L2 Reincarnated cosmology layer" |
| EGM.4 | Configuration points (what a licensee can customize) | ✅ Locked | engine-generic-meta-structure.md § "What a licensee configures at instantiation" |

#### Ritual trilogy (`trial-moment-ritual.md` / `passage-moment-ritual.md` / `ascension-moment-ritual.md`)

| # | Pillar | Status | Enforcement surfaces |
|---|---|---|---|
| Trial.1 | Six-phase Trial ritual structure (Approach / Threshold / Choice / Transition / Fight / Resolution) | ✅ Locked | trial-moment-ritual.md |
| Trial.2 | Two Spirit Guide voice lines per Trial (Phase 2 + Phase 6); silent at Phase 3 choice + during Phase 5 fight | ✅ Locked | trial-moment-ritual.md; spirit-guide-voice.md |
| Trial.3 | Path locked irrevocably at Phase 3 commit; no mid-fight switch | ✅ Locked | trial-moment-ritual.md § Phase 3; file 32 § 11 |
| Trial.4 | Mirror-fight rendering exception (player sprite + recognition cues) | ✅ Locked | trial-moment-ritual.md § Phase 5; enemy-visual-legibility.md S7 |
| Passage.1 | Six-phase Passage ritual structure (Death-approach / Threshold / Choice / Transition / Settling / Aftermath) | ✅ Locked | passage-moment-ritual.md |
| Passage.2 | Spirit Guide CONSPICUOUSLY ABSENT at Phases 2-4 (threshold + choice + transition) | ✅ Locked | passage-moment-ritual.md § "The Spirit Guide's absence — load-bearing canonical detail"; spirit-guide-voice.md |
| Passage.3 | One Spirit Guide voice line at Phase 5; canonical exclusion of Passage Phases 2-4 from Spirit Guide speech surface | ✅ Locked | passage-moment-ritual.md; spirit-guide-voice.md Trigger Gate-1 question |
| Passage.4 | Three pool-state sub-cases (≥2 / =1 / =0) + Trial-death sub-case | ✅ Locked | passage-moment-ritual.md § "Pool-state sub-cases"; file 33 |
| Passage.5 | Embodiment-specific death-language (Phase 2 + Phase 4 consume embodiment-narrative-layer.md) | ✅ Locked | passage-moment-ritual.md; embodiment-narrative-layer.md § "Injury / death vocabulary" |
| Ascension.1 | Six-phase Ascension ritual structure (Approach / Threshold / Event / Reception / Settling / Threshold-to-next) | ✅ Locked | ascension-moment-ritual.md |
| Ascension.2 | Three Spirit Guide voice lines at Ascension (voice climax) | ✅ Locked | ascension-moment-ritual.md; spirit-guide-voice.md |
| Ascension.3 | Earth Self register at Ascension (NOT seasonal vocabulary; canonical commitment) | ✅ Locked | ascension-moment-ritual.md § "Canonical commitment — Earth Self register" |
| Ascension.4 | Wheel's strongest visible cosmological event at Phase 3 | ✅ Locked | ascension-moment-ritual.md § "The Wheel at Ascension" |
| Ascension.5 | First-Ascension special framing (Court's birth) | ✅ Locked | ascension-moment-ritual.md § "Special cases" |

#### `spirit-guide-voice.md`

| # | Pillar | Status | Enforcement surfaces |
|---|---|---|---|
| SGV.1 | Locked register: Beatrice from Re:Zero (with named Reincarnated-specific adaptations) | ✅ Locked | spirit-guide-voice.md § "The locked register" |
| SGV.2 | Voice arc across season (reserved → warmed → companion) | ✅ Locked | spirit-guide-voice.md § "The voice arc across a season" |
| SGV.3 | Voice across seasons (relationship resets-but-persists) | ✅ Locked | spirit-guide-voice.md § "The voice across seasons" |
| SGV.4 | Twelve anti-patterns explicitly named | ✅ Locked | spirit-guide-voice.md § "Anti-patterns explicitly named" |
| SGV.5 | Constant-across-body-swap principle (Guide refers to form as "what player wears," not "what player is") | ✅ Locked | spirit-guide-voice.md § "The constant-across-body-swap principle in voice" |
| SGV.6 | Court-reference register (sparing cross-season Court-member references) | ✅ Locked | spirit-guide-voice.md § "The Court-reference register" |
| SGV.7 | Categorical-language integration (S/S/M/S/D translated into voice) | ✅ Locked | spirit-guide-voice.md § "The categorical-language integration" |
| SGV.8 | Canonical silences (Passage Phases 2-4; combat; Trial Phase 3 choice; literal future-state) | ✅ Locked | spirit-guide-voice.md § "What the Guide does NOT speak about" |

#### `season-feel-rubric.md`

| # | Pillar | Status | Enforcement surfaces |
|---|---|---|---|
| SFR.1 | 10 dimensions that must cohere (D1-D10) | ✅ Locked | season-feel-rubric.md § "The rubric — ten dimensions" |
| SFR.2 | Cross-season distinctiveness vs cross-season recognizability balance | ✅ Locked | season-feel-rubric.md § "Cross-season distinctiveness vs cross-season recognizability" |
| SFR.3 | Reverse-validation methodology (two variants: seeded + no-seed) | ✅ Locked | season-feel-rubric.md § "Reverse-validation"; commission filed for Variant 2 experiment |
| SFR.4 | Failure modes named (cross-dimensional flatness; genre-default leakage; cross-season homogeneity; consumer-mismatch; player-experience flatness) | ✅ Locked | season-feel-rubric.md § "Failure modes to protect against" |

---

## Drift instances observed and archived

Each entry: what drifted; how it was caught; what structural-enforcement gap allowed the drift; what was done.

### Drift-1 — Form-bias diagnosis (the foundational instance)

**What drifted:** Humanoid-default form throughout the engine's categorical axes — gear, class, weapons, wears, attribute system. Despite the project being literally named "Reincarnated" and the isekai-genre commitment, the engine produced humanoid-only forms across all 5 production seasons + Yomi.

**How caught:** Matt's 2026-05-14 design session; surfaced in doc 37.

**Enforcement gap:** the latent intent ("non-humanoid forms in an isekai project") existed in conversation + project naming but had NO structural enforcement. No schema constraint admitted non-humanoid; no Gate-1 check asked "does this generation produce embodiment variety?"; no decisions-log entry locked the breadth-of-form requirement.

**Action:** Doc 37 authored; Position C locked (slot-as-functional-mechanic + embodiment-as-narrative-skin); embodiment-narrative-layer.md authored locking 8 canonical embodiments + expansion protocol; Discipline #13 candidate surfaced from this exact instance.

**Discipline #13 instance:** **YES — this is the foundational instance the discipline was named for.**

### Drift-2 — Pet system at story-pillar weight (caught in dialogue)

**What drifted:** gandalf Phase 2 § 1.9 recommendation to promote the pet system from memory-note to canonical-story design intent. The Spirit Guide already occupies the emotional-anchor-through-transformation slot; adding the pet to the same slot would split the relationship's center.

**How caught:** Matt's 2026-05-15 dialogue pushback (*"I am not sure this has value in the story, let's discuss"*).

**Enforcement gap:** no structural enforcement against gandalf's own design-conversation drift toward redundant emotional-anchor proposals.

**Action:** gandalf walked back the recommendation; the Spirit Guide retains the emotional-anchor-through-transformation slot uncontested.

**Discipline #13 instance:** PARTIAL — caught before reaching canonical-story; surfaced the value of dialogue-stage critique in protecting the design layer.

### Drift-3 — Fate substrate (caught in dialogue)

**What drifted:** gandalf design proposal to use Fate/Zero / Nasuverse framing as canonical reference for the Court. The Fate frame's humanoid-locked substrate (Throne of Heroes = repository of human historical/mythical figures) would have re-imported the bias doc 37 was meant to remove.

**How caught:** Matt's 2026-05-15 dialogue pushback (*"A slime or cat-human-slave or dragonling has no place at the throne but deserves a spot at the court. Let's leave off the fate explicit ties"*).

**Enforcement gap:** the form-bias work (doc 37) was named conceptually but applied unevenly during dialogue — gandalf reached for Fate framing without auditing its substrate-compatibility against the project's isekai commitment.

**Action:** Fate frame rejected as canonical reference; retained as design-conversation lens. court-of-forms.md amended with explicit decision-archaeology note. Class-role labels reworked from humanoid-coded (Knight / Berserker / Archer / etc.) to dual-label pattern (function tag + embodiment-flavored name).

**Discipline #13 instance:** **YES — Matt applied Discipline #13 in real time against gandalf's own drift.** This is the discipline working as designed.

### Drift-4 — Style-register Phase-1 onboarding miss

**What drifted:** gandalf agent definition explicitly names `canonical/story/style-register.md` as gandalf's owned senior-design call to surface during Phase-1 onboarding. Gandalf missed it in Phase 1 + Phase 2; the visual-presentation substrate stayed unaddressed.

**How caught:** Matt's 2026-05-15 question (*"Where does canonical/story/style-register.md sit in your queue? ... is that intentional (sequencing) or an oversight?"*).

**Enforcement gap:** the agent definition itself was the structural enforcement; gandalf's reading-pass missed it. No second-pass check ensured all owned items were inventoried.

**Action:** style-register.md authored 2026-05-15; canonical lock applied; Elrond catalogue-rubric commission filed.

**Discipline #13 instance:** YES — a gap-in-personal-onboarding instance. The discipline's *"verify each pillar has structural enforcement"* applies to the agent's own ownership claims.

### Drift-5 — Enemy-visual-legibility canonical gap

**What drifted:** demo1 family-playtest finding (enemies rendered as scaled-up player sprites) was a real player-experience failure that had no canonical-design-intent counter. The locked design assumed enemy distinctiveness; the implementation reused player sprites.

**How caught:** Matt's 2026-05-15 commission (*"Enemy Monsters need to have enough context (text, color) to map them to pixel files. In the demo, the enemies looked the same as player combatants (but made larger). This was really poor experience"*).

**Enforcement gap:** no canonical-design-intent doc named the player-perception requirement; no engine-emit field forced the visual distinction; no Gate-1 check on dispatches.

**Action:** enemy-visual-legibility.md authored 2026-05-15 with 7 structural commitments S1-S7; anti-pattern (enemies-as-scaled-up-player-sprites) explicitly rejected canonical; cross-references to style-register.md added.

**Discipline #13 instance:** YES — the design intent ("enemies must be visually distinct from player") existed in implicit-understanding but never structurally enforced.

### Drift-6 — Style-register categories not operationally precise

**What drifted:** gandalf authored style-register.md with categorical register names (retro pixel-art / hand-drawn pixel-art / vector / hand-drawn-2D anime / HD raster) that work for design conversation but are subjective at the cataloguing layer. Two curators tagging the same asset could legitimately classify it differently.

**How caught:** Matt's 2026-05-15 question (*"Do you feel the values that you provided for the pixel/2D/VFX categories will be precise enough for Elrond and Legolas to score within their schema and select for/against without issue or confusion?"*).

**Enforcement gap:** gandalf authored at design-conversation register; operational-rigor for catalogue schema is Elrond's territory but the boundary wasn't explicit.

**Action:** style-register.md amended with Operational Precision section deferring rubric to Elrond; commission filed at `gandalf/requests/2026-05-15-elrond-catalogue-rubric-commission.md` with six-axis proposal as gandalf's input.

**Discipline #13 instance:** YES — pattern of "authored at canonical-design-conversation register without verifying operational-rigor consumers."

### Drift-7 — View A/B/C AOE-philosophy unanalyzed-as-system

**What drifted:** The engine's AOE-vs-pack behavior is governed by THREE parameters (`math_model.py` damage-reduction; `role_constraints.py` ; `damage_resolver.py` AOE multiplier). These have NEVER been analyzed as a joint system. Jack-ryan Gate 1 finding 2026-05-15: empirically the system reads as View A (compound — 0.6× per-hit reduction overwhelmed by lower energy cost + shorter cooldown + N=8× pack multiplier), but no canonical lock exists.

**How caught:** Jack-ryan Gate 1 review on B10.4 work surfaced the unanalyzed-system pattern.

**Enforcement gap:** no canonical-design-intent doc named the AOE-philosophy lock; the three parameters drifted independently into an emergent state nobody analyzed.

**Action:** engine-balance-stewardship.md commission filed (`agentic_orchestration/dispatches/2026-05-16-gandalf-engine-balance-stewardship.md`); pending gandalf authoring (session 3 of three). View A/B/C lock pending; decisions-log entry pending.

**Discipline #13 instance:** YES — multi-parameter system drifting without joint-analysis is a clear instance.

### Drift-8 — Q1 divergence floor/ceiling never operationalized

**What drifted:** Matt's Q1 articulation 2026-05-15 (class-divergence-above-a-floor + below-a-ceiling + experienced-cost-parity) names a multi-dimensional constraint the convergence framework doesn't currently target. Single-number win-rate aggregation has been the substrate; the multi-dimensional framing was implicit-in-conversation but never operationalized.

**How caught:** Matt's 2026-05-15 Q1 articulation surfaced the implicit-pillar.

**Enforcement gap:** the design intent (class-distinctiveness + playable-floor) existed in conversation but had no operational measurement framework.

**Action:** Pending engine-balance-stewardship.md Gate 2 (forthcoming session 3).

**Discipline #13 instance:** YES.

### Drift-9 — Q2 movement speed in simulation empirically unknown

**What drifted:** Engine 1 claims to balance against L50 endgame (file 29). Whether the simulation models movement at L50 endgame speed (or at L1 baseline, or not at all) is empirically unknown. Matt's 2026-05-15 Q2 surfaced this as a measurement gap.

**How caught:** Matt's 2026-05-15 Q2 question.

**Enforcement gap:** the file-29-claim ("engine balances against L50 endgame") was structurally locked at the LEVEL layer but not at the MOVEMENT layer. No verification that ALL endgame-state parameters are modeled at endgame values.

**Action:** Pending engine-balance-stewardship.md Gate 3 (forthcoming session 3); may require small rocket/gamora research-pass for empirical confirmation. **2026-05-16 Day-4 amendment:** Resolved via Matt verdict reversal at Day 4 close — **Option B (end-game-anchored: player 8.0 m/s; trash 5.75 m/s; fast-archetype 7.5 m/s; AI_SPEED_MULTIPLIER 0.719) is the operative resolution.** Both the baseline-anchor portion AND the full Gate-3b sim-consumption portion are now VS2a-gating (per `engine-balance-stewardship.md` § Gate 3 Rec 3b Day-4 close update + `canonical/story/movement-speed-baseline.md` § "Verdict Reversal 2026-05-16"). The earlier Option A (mid-game 7.5 m/s; AI_SPEED_MULTIPLIER 0.767) is superseded.

**Discipline #13 instance:** YES — partial-enforcement-without-verification pattern.

### Drift-10 — D1 element-name overrides accumulating without rubric revision

**What drifted:** Per memory `project_design_intent.md` 2026-05-12 entries: multiple manual overrides accumulated on the D1 element-name pool (pall demoted; rime / miasma / shear / billow demoted; smoke reverted; cloud promoted; etc.). The rubric (`d1_total` scoring) was decoupled from operational filter (`d1_status`) — multiple overrides accumulated WITHOUT the rubric being revised to capture the patterns.

**How caught:** Matt's 2026-05-12 ongoing observation; documented in memory.

**Enforcement gap:** the rubric should reflect the project's actual judgment criteria. Override-accumulation-without-rubric-revision = the rubric is no longer canonical reference; the rubric AND the operational filter have drifted apart.

**Action:** memory notes capture the drift; rubric work (e.g., `vocabulary_commonness` sub-property; `slot_unambiguous` check) named as future work. Doc 37 § 7 superseded the curated-pool approach under cipher architecture; the drift is rendered moot by the architecture shift but remains as historical evidence of the pattern.

**Discipline #13 instance:** YES — historical instance; renders the pattern empirical not hypothetical (this is one of doc 37 § 9.1's named empirical-instance examples).

### Drift-11 — Load-bearing dimension deferred to "later" until "later" gated near-term ship (two instances 2026-05-16)

**What drifted:** Two scoping decisions made earlier in the project deferred load-bearing dimensions of player experience to later milestones — and "later" turned out to be after the deferred dimension started gating the next near-term ship. Both surfaced in Matt's 2026-05-16 dialogue within hours of each other; both required Matt's direct catch.

**Instance A — Movement-speed baseline.** B12 (*movement speed + boots + gear slot audit*) was scoped to Stage A2 in `canonical/16-project-roadmap.md` § Stage A2 and explicitly deferred out of VS2a (*"not visually load-bearing for VS2a"*). The full B12 scope (gear slots, +% MS affixes, hard-cap design) is legitimate Stage A2 work — but the BASELINE ANCHOR portion (what speed is the player actually moving at?) was implicitly bundled into the deferred scope. Demo VS2a cannot ship with hand-tuned px/s placeholders that don't match a defensible design baseline; the baseline-anchor decision is upstream of VS2a, not downstream. Resolution: `canonical/story/movement-speed-baseline.md` authored same day; B12 split into baseline subset (VS2a scope) + full audit (Stage A2 scope); decisions-log entry queued. **2026-05-16 Day-4 amendment:** The Day-4 verdict reversal sharpened this further — not only the baseline-anchor subset but also the **full Gate-3b sim-consumption portion** (engine consumes end-game-anchored MS values; kiting modeling; AI_SPEED_MULTIPLIER 0.719 wired into convergence-loop telemetry) is **also in VS2a scope**, not a "tightly-following post-VS2a ticket" as the morning framing had it. Matt: *"No point playing a game which is not ran through the sim."* The implicit-deferral pattern bit twice on this same instance — first the baseline-anchor subset (caught earlier in the day); then the sim-consumption subset (caught at Day-4 close evening). Both are now VS2a-gating. The pattern's lesson sharpens: when a deferred milestone surfaces ONE upstream-of-near-term-ship dependency, sweep the rest of the deferred milestone for sibling dependencies in the same session — they tend to cluster, not surface in isolation.

**Instance B — Geometry × element VFX coverage.** The substrate-realignment / `form-bias-cadence-strategy.md` work was scoped around two catalogue axes — element/substrate (fire/void/necrotic/crystal/etc.) + embodiment (warrior/mage/rogue narrative skin). The GEOMETRY axis (impact_burst / projectile / beam / cone / ground_slam / aura / nova / ring / chain / whirlwind / dash_attack / etc.) was implicitly assumed addressable at integration time. B11 (geometry palette 16 → 25; VS2a-gating) drives drax to integrate 9 new geometries × N elements; without geometry-coverage extracted from vendor catalogues, drax integration faces zero-coverage cells with no defensible fallback. Resolution: `agentic_orchestration/gandalf/requests/2026-05-16-geometry-vfx-coverage-investigation-b11-gating.md` filed same day; B11 demo integration phase HELD pending Elrond rubric + gandalf gap-severity assessment.

**How caught:** Matt direct catch 2026-05-16, both within the same dialogue session. Movement-speed surfaced first (Matt: *"I don't want to ship demo VS2a without this"*); geometry-coverage surfaced ~1 hour later (Matt: *"we have scoped alot of work in mapping embodiment categories and elements from JSON to 2D/VFX packages, but have we investigated the skills geometries themselves?"*). Neither was flagged by gandalf at the earlier scoping moments — both flowed through gandalf-authored scoping docs (form-bias-cadence-strategy; B12 deferral) and were missed.

**Enforcement gap:** When scoping a deferred milestone or a multi-axis workstream, no structural check existed for *"is any load-bearing portion of this milestone actually upstream of the near-term ship?"* The form-bias-cadence-strategy scoping named element + embodiment as the catalogue axes; geometry was treated as implicit (verifiable-at-integration-time). The roadmap B12 entry bundled "movement speed + boots + gear slots" as one atomic deferrable unit; the baseline-vs-gear-economy split was treated as implicit. Both implicit assumptions were structurally correct AT SCOPING TIME and operationally wrong AT NEAR-TERM-SHIP TIME.

**Action:** Both instances resolved same-day with operational fixes (see canonical docs above). Pattern P6 named below for future prevention. **Specific forward audit recommended:** sweep current scoped-but-not-yet-active milestones (VS2b Substrate Realignment; Stage A2 B-series; Stage A3+ work) for similar implicit-axis assumptions before they recur.

**Discipline #13 instance:** YES — both instances are partial-enforcement-without-verification. The deferral decisions did not verify that no near-term ship would surface a dependency on the deferred portion. This is the same enforcement-gap shape as Drift-7/8/9, applied to scoping decisions rather than design pillars.

### Drift-12 — Test scaffolding masks production defect (gamora V2.1 emission gap)

**What drifted:** Star-lord's v2.1 telemetry smoke test (`reincarnated-engine/tests/test_telemetry_v21.py` lines 605-606) injected synthetic `loadout_json` values into test fixtures with an explicit workaround comment in order to satisfy the recorder's input preconditions in isolation. The test confirmed the recorder correctly writes the three new V2.1 per-fight fields (`encounter_index_within_room`, `room_won`, `hp_fraction_at_encounter_start`) when those fields are present alongside a non-None `loadout_json`. The test passed.

Meanwhile, gamora's V2 sequential-room execution path in production constructed fight_log dicts with `loadout_json: None`. The star-lord recorder's `is None → continue` guard at `recorder.py` line 477 (a correct V1-era defensive guard) silently dropped every V2 fight record. **All 204,800 rows of season_001006's `class_fight_loadouts` table had NULL on the three V2.1 fields.** The full-class regen completed; nothing alarmed; the gap was only surfaced because star-lord's post-regen recovery check empirically queried the column. The fix (`gamora/v1.3-b10-v2-emission-gap-fix @ df717a8`) emits `"{}"` instead of `None`, which passes the guard. 1114 rows of fresh smoke-season data persisted post-fix (was 0 before).

**How caught:** Star-lord post-regen empirical column check 2026-05-16 (per `agentic_orchestration/qa/findings/2026-05-16-star-lord-full-regen-post-b6-v2.md`). NOT caught by either of: (a) gamora's own V2 smoke pass at the V2 dispatch's intermediate tag, (b) star-lord's v2.1 schema smoke pass at the v2.1 dispatch's intermediate tag. Both seam-isolated smoke passes were green; the cross-seam integration path was silent.

**Enforcement gap:** the v2.1 smoke test exercised the recorder's *code path* with synthetic fixtures but did not exercise the *integration path* with production fixtures. The synthetic-injection workaround was correct as a unit test of the recorder in isolation — and the dispatch's completion record correctly notes that. But there was no cross-seam round-trip smoke test that ran V2 production fight_log dicts through the recorder end-to-end. The seam boundary between gamora's emission and star-lord's persistence had test coverage on each side and no test coverage on the boundary itself.

This is the empirical instance the Pattern P7 framing below is named for.

**Action:** Fix shipped (`df717a8`). MIGRATION.md §v1.4 + §v1.5 entries document the semantic correction. This Drift-12 entry surfaces the underlying pattern (P7) so the prevention prescription can be operationalized at future dispatch authoring.

**Cross-references:**
- Dispatch: `agentic_orchestration/dispatches/2026-05-16-gamora-v21-per-fight-emission-gap-fix.md` (full completion record at bottom)
- Star-lord findings: `agentic_orchestration/qa/findings/2026-05-16-star-lord-full-regen-post-b6-v2.md`
- Engineering disciplines #13b (commit `4259969`): same empirical instance examined at a different abstraction layer. **The relationship is non-overlapping at the discipline-vs-prevention layer:**
  - Discipline #13b frames the gamora V2.1 case as *outcome attribution opacity*: once the missing-emission symptom appeared, root-cause attribution required targeted ablation/inspection and was not derivable from the symptom alone. #13b is actionable through *empirical experiment*, not process gates.
  - Drift-12 (Pattern P7) frames the same case as *test-fixture isolation masking production-fixture divergence*: the reason the symptom appeared in production rather than in a green smoke run is that test fixtures bypassed the precondition production violated. P7 is actionable through *process gates* on test-fixture review.
  - Both true; both load-bearing; complementary rather than duplicative. #13b prescribes ablation; P7 prescribes cross-seam round-trip discipline. The same empirical case demonstrates both gaps simultaneously.
- P6 forward audit (`canonical/story/p6-forward-audit-2026-05-16.md`): the test-scaffolding pattern is structurally distinct from P6 (P6 is scoping-time axis omission; P7 is implementation-time fixture divergence). Not a P6 instance.

**Discipline #13a instance:** PARTIAL. The canonical intent ("V2 emits these three fields populated") existed in the v2.1 schema design + the V2 dispatch wire-up; the code did emit the fields. But the canonical-vs-code comparison was insufficient because the lower-level precondition (`loadout_json` non-None) was implicit. This is on the edge of #13a's "directly comparable from code" criterion — the gap was only visible by reading the recorder guard and the V2 emission together. P7 is the more precise pattern label for this instance than #13a alone.

### Drift-13 — Vendor deliverable-register confusion (CraftPix cross-product-line split)

**What drifted:** The catalogue-research vocabulary implicitly treated `vendor → style_register` as a one-to-one relationship. Tier-1 vendor sweeps and per-vendor findings docs assumed that if a vendor markets their catalogue as "pixel art," all product lines under that vendor ship pixel-art-shaped raster deliverables. CraftPix.net violates this assumption: its **VFX packs** (e.g., `craftpix-pixel-magic-effects-icons`, surfaced in the Step B Tier-1 2D VFX crawl) ship pixel-art-shaped raster (PNG/PSD, 64×64 / 128×128 / 256×256 frames) and are correctly tagged `style_register: pixel-art` in the catalogue; its **character sprite packs** (verified 2026-05-16 by the legolas character-track scout — Adventure Game Character Sprite Pack, Woman Hero Game Character Sprite, etc.) ship vector deliverables (AI / EPS / PSD layered, with explicit "vector graphics; parts of body divided into separate elements for vector editor" language on product pages). Both product lines carry CraftPix's site-wide "pixel art" marketing label; only per-product-page inspection surfaces the split.

The CraftPix catalogue file already reflects the split empirically — `craftpix/full-2026-05-16.jsonl` contains 5 `style_register: pixel-art` records and 2 `style_register: vector` records (CraftPix is presently the only Tier-1 vendor with mixed registers in its inventory). The records were tagged correctly per-product by the curators on each side; what drifted is the *implicit vocabulary assumption* that downstream consumption could safely aggregate by vendor.

**How caught:** legolas character-track Mode A scout returned 2026-05-16 (`agentic_orchestration/research/catalogue/character-track-vendor-scout-2026-05-16.md`) and flagged CraftPix as `HOLD — register mismatch` in the character-track-only context. Matt then asked the broader question — whether the per-product-line split could mislead downstream wiring (drax) or downstream register validation (gandalf), and whether the prior Step B VFX surface had been treating CraftPix as register-consistent. Cross-reference to the Step B VFX crawl confirmed: the VFX-side curator correctly identified pixel-art-shaped raster (extraction_notes explicitly say `"Not vector"`), but the abstraction-layer assumption that `vendor ⇒ register` was never explicitly stated or verified.

**Enforcement gap:** the catalogue's `style_register` field exists at the per-record (per-product) granularity already, but the catalogue's *consumption-side vocabulary* — per-vendor findings docs, per-vendor rubric notes, vendor-class HOLD/PROMOTE language, and the implicit mental model for "is CraftPix in or out?" — operated at vendor granularity. The dispatch authoring for catalogue crawls did not require `deliverable_register` (or equivalent) be inspected per product line within a vendor before vendor-class judgments were rendered. The first downstream consumer that would have surfaced this mismatch (drax wiring sourcing both VFX and character packs from CraftPix; gandalf register-validation pass) had not yet activated when the implicit assumption was forming.

**Action:** Pattern P8 named below for future prevention. The CraftPix VFX records remain valid (correct register tag); the CraftPix character records remain valid (correct register tag); no catalogue mutation required as result of this drift. Cross-seam forward actions queued (see Cross-references). NOT in scope of this drift entry: retrospective audit of all curated vendor packs (bounded to pattern documentation); CraftPix-specific catalogue re-curation (legolas + elrond own that decision); process-gate operationalization (separate decision; this entry surfaces the pattern).

**Cross-references:**
- legolas character-track scout: `agentic_orchestration/research/catalogue/character-track-vendor-scout-2026-05-16.md` (CraftPix vector finding at § Vendor 7)
- Step B 2D VFX inventory: `agentic_orchestration/research/catalogue/cross-vendor-substrate-inventory-2026-05-16.jsonl` (CraftPix VFX records correctly tagged pixel-art)
- Catalogue empirical evidence: `agentic_orchestration/research/catalogue/craftpix/full-2026-05-16.jsonl` (mixed-register vendor confirmed; 5 pixel-art + 2 vector records)
- Forward cross-seam actions (queued, not part of this drift entry's commission scope):
  - **legolas:** future Mode B catalogue dispatches should record per-product-line `deliverable_register` explicitly (not aggregate by vendor) — small persona-rule extension; knight-rider to route if Prevention (a) is selected
  - **elrond:** catalogue.db schema may need amendment to ensure register is enforced per-record (not per-vendor) and to expose a vendor-level "register-mixed: yes/no" flag at query time; flag for future elrond data-architecture decision
  - **drax:** downstream dispatches that source from a vendor across multiple product lines (VFX + characters from the same vendor) must check `style_register` at the per-pack level, not at the vendor level
- Style-register doc (consumption-time filter layer): `canonical/story/style-register.md`
- NOT cross-referenced (different abstraction layer; verified non-relevant): grouping-layer vocabulary spec

**Discipline #13 instance:** YES — instance of "implicit-pillar drift" applied to the catalogue-research vocabulary layer. The pillar `vendor catalogue inspection records register at the per-deliverable granularity that matches downstream-consumption granularity` was implicit and not structurally enforced. The drift was caught at the moment the first cross-product-line consumer (legolas character scout reading prior VFX work) ran the inspection — earlier than downstream wiring or register-validation would have caught it, which is the desired catch-cadence.

### Drift-14 — Per-season vocabulary pool scored on D1 rubric but not against VFX-catalogue-mapping coherence

**What drifted:** The 156-entry seasonal-element pool (`data/seasonal_elements/pool.json`) was scored Stage A1 (commit `98f1e3f`, 2026-05-12) against the **D1 rubric** — 5 properties × 2 points + Genre Precedent +1 bonus, totaling ~11 max score. The 5 properties scored entries against *conceptual visualizability* (can a player picture it), *fantasy-heroic* (does it read genre-appropriate), *genre precedent* (does it appear in shipped ARPG canon), *common vocabulary* (does an average player know the word), and one or two related properties. **What D1 rubric did NOT score:** whether each entry maps cleanly to our actual 2D elemental / VFX catalogue (Pimen GREEN list + CreativeKind palette-shift coverage). Those are two different questions — the rubric answered the first; the second was implicit-deferred.

The cipher migration architecture (per `canonical/37-form-bias-diagnosis-and-recovery.md` § 6 + `canonical/story/form-bias-cadence-strategy.md` § 7.2) commits to: **L1 substrate (canonical-four) drives VFX; L3 per-season vocabulary drives player-visible labels.** This works elegantly *only if* L3 vocabulary entries are conceptually VFX-coherent with their canonical slot. Concrete failure mode: a season selects `throne` (earth-allow-list, D1 total=11 — top score) as the earth-slot substance; sim emits earth-canonical skills; demo renders earth-canonical VFX (stone particles, mineral debris); player-visible label reads "throne strike" or "throne aura." The mismatch between *vocabulary suggesting royal-conceptual imagery* and *VFX rendering as stone particles* produces cognitive dissonance.

The drift is structural across both tiers:
- **Allow-list tier (81 entries; supposedly clean):** includes entries with real VFX-mapping ambiguity — `throne` (conceptual, not substance); `blood` (red liquid; canonical water VFX is blue/cyan); `mercury` (silver liquid); `bone / marrow / chitin / claw / horn / scale / thorn / tooth / husk / shell` (biological-organic, distinct visual register from mineral earth); `pearl` (white reflective, palette-shift water possible but unusual).
- **Quarantine tier (35 entries):** disproportionately contains entries that cannot map at all — wind-quarantine `whisper / hum / sigh / thrum / breath / exhalation / whistle` are *auditory*, not visual; water-quarantine `honey / jelly / milk / nectar / sap / sweat / tear / lather / suds` are specific liquid types requiring custom VFX not palette-shifts; earth-quarantine `threshold / flower / petal` are abstract or non-mineral. The D1 rubric correctly demoted these on visualizability scoring, but the demotion is correlated-with-VFX-incoherence rather than caused-by-it.

**How caught:** Matt direct catch 2026-05-17 Day 4 evening (immediately following gandalf's element-pool diff response): *"Based on this, it seems that we have not filtered those elements which will not map cleanly to our 2D elemental/VFX catalogue out of scope. Is this true? Is there still a gap here for VS2a demo?"* — caught by reading the diff output, not by structural enforcement.

**Enforcement gap:** D1 rubric is structurally enforced (scoring methodology codified at commit `98f1e3f`; selector consumes scores at `element/selector.py`). VFX-catalogue-mapping coherence scoring does NOT exist as a structural enforcement. When the D1 rubric was authored at Stage A1, the VFX catalogue (Pimen, CreativeKind) had not yet been crawled — VFX coverage was unknown. The rubric was authored against what was knowable then; the rubric extension that bridges to VFX coverage was not added when the catalogue work returned (Step B Tier-1 crawl 2026-05-16 + Pimen viability gate PASS).

**This is a Pattern P6 instance.** Load-bearing dimension (VFX-catalogue-mapping coherence) deferred to a later milestone (Stage 3 cipher migration ship) that becomes upstream of a near-term ship (VS2b). Same shape as Drift-11 movement-speed-baseline and geometry-vfx-coverage instances — and same fix shape (explicit rubric extension + bounded audit pass + closes before the ship the deferred dimension gates).

**Is this VS2a-gating? YES — Matt verdict reversal 2026-05-17 (Day 4 evening into Day 5 close).** Initial gandalf framing (immediately following the Drift-14 surfacing) was "pre-VS2b-ship gap, not VS2a-blocking" — pre-Stage-3 cipher migration the LLM still sees canonical-four labels and per-season vocabulary doesn't yet drive player-visible surface end-to-end, so the gap is technically camouflaged at VS2a. Matt's pushback (verbatim): *"I really don't want to ship any more canonically biased seasonal themes."*

The pushback is sharper than the initial framing. **The D1 rubric, as currently scored, has a structural canonical-four bias baked in.** Allow-list tier composition: fire allow-list (20) is dominated by canonically-fire substances; wind allow-list (14) by canonically-wind weather; water allow-list (14) by canonically-water; earth allow-list (33) by canonically-earth-mineral. **The non-canonical-but-VFX-coherent entries** (biological-earth materials; specific liquids; alternative-element-form substances) are mixed into quarantine/eligible tiers alongside the genuinely-VFX-incoherent ones (auditory, textural, abstract). The rubric pushes the selector toward canonical-four conformity even while claiming to enable per-season variety. **This is itself a form-bias instance** — the rubric structurally undermines what Substrate Realignment Stage 1 (embodiment-axis additive; shipped today) was supposed to enable at the player-facing per-season-vocabulary surface.

VS2a regen will happen anyway as part of the end-game-anchored MS values + form-bias Stage 1+2 fields + Stage B export-DTO fix + B6 main + chierit characters landing. Drift-14 closure folds into that same regen cycle. **Incremental cost vs benefit:** ~1.5-2 days work (legolas Track A + gandalf Track B) closes a Substrate Realignment Stage 1 player-facing completion gate — that's cheap insurance against shipping VS2a with the same canonical bias the project just architecturally committed to closing.

VS2a end-game-anchored playtest framing (per Day-4 verdict reversal) is balance state for sim+demo coherence. Drift-14 closure is **vocabulary state** for player-experience canonical-bias-closure. Both are needed for VS2a to ship cleanly.

**Action:**
- Drift-14 entry archived here (this section).
- Gap-closure commission filed at `agentic_orchestration/gandalf/requests/2026-05-17-pool-vfx-catalogue-mapping-audit.md` — legolas Mode A catalogue audit (Pimen + CreativeKind VFX coverage at concept level — which substance-types render coherently with palette-shift; which require custom VFX work; which can't map without bespoke commission) + gandalf re-scoring pass (add `vfx_catalogue_mapping_clean` property to D1 rubric; score pool against catalogue coverage; produce culled pool for VS2b cipher migration ship). Bounded scope ~1-2 days combined.
- Forward discipline candidate (D15-candidate territory per P6 forward audit § sub-pattern naming): "Pool-vs-catalogue mapping must be scored at pool-introduction time, not deferred to ship-time." Surface to next jack-ryan engineering-disciplines pass alongside R11(b) + Pattern P7 silent-drop cluster + Drift-11 sibling-cluster-sweep lesson.

**Cross-references:**
- Source pool: `reincarnated-engine/data/seasonal_elements/pool.json` (current state — 156 entries; 81 allow-list / 40 eligible / 35 quarantine)
- D1 rubric methodology: Stage A1 commit `98f1e3f` (rubric scored + selector filter + Phase C scoring)
- Cipher migration architecture: `canonical/37-form-bias-diagnosis-and-recovery.md` § 6 + `canonical/story/form-bias-cadence-strategy.md` § 7.2
- VFX catalogue coverage: `agentic_orchestration/research/catalogue/cross-vendor-substrate-inventory-2026-05-16.jsonl` (Step B Tier-1 inventory) + Pimen viability-gate PASS findings + `canonical/story/geometry-vfx-coverage-assessment.md`
- P6 forward audit pattern: `canonical/story/p6-forward-audit-2026-05-16.md`
- Sibling drift instances (also P6): Drift-11 instance A (movement-speed-baseline) + Drift-11 instance B (geometry × element VFX coverage) — both 2026-05-16 catch

**Discipline #13 instance:** YES — instance of "implicit-pillar drift" applied to the pool-rubric-vs-catalogue-coverage layer. The implicit pillar `pool vocabulary entries are scored against ALL downstream-consumption requirements at scoring time, not just against conceptual visualizability` was never explicitly stated and not structurally enforced. The drift surfaces at the moment the first downstream consumer that depends on VFX coherence (Stage 3 cipher migration → VS2b ship) starts looking upstream — caught one step earlier than downstream-consumer-activation time, which is the desired catch-cadence per the P6 forward-audit prescription.

### Drift-15 — Environment tileset / wall / prop sourcing implicit-deferred without being named as a deferred axis (P6 instance)

**What drifted:** The catalogue research workstream (Step B Tier-1 inventory + per-vendor scouts; 2026-05-16) explicitly scoped TWO visual axes — **VFX** (Pimen GREEN-list + CreativeKind) and **characters** (chierit Elementals + CreativeKind monster sprites). The THIRD axis — **environment assets (floor tiles + wall tiles + props / scenery objects)** — was implicit-deferred without being named as a deferred axis. No catalogue dispatch authored a sweep for environmental tilesets; no canonical-doc named environment as a separate sourcing track; no forward-flag captured "environment is out of Step-B-Tier-1 scope; needs separate sweep at named ship-gate."

The room/hallway arena topology drax shipped 2026-05-16 (commit `5463be8`; `canonical/story/arena-room-hallway-system.md`) committed VS2a to Diablo/PoE-style single-camera ARPG framing where environmental visual identity is load-bearing per genre canon (D2 per-act tilesets; D3/D4 per-zone visual identity; PoE per-map tile families; Hades per-region chamber visuals; Octopath/Sea of Stars/Eiyuden HD-2D environmental detail — all treat environment art as foundational, not decorative). Demo v1 shipped with geometrically-drawn placeholders for walls + "random seasonal structures on the ground"; family-playtest signal flagged geometric walls + random-structures as known-low-quality + geometric floor tiles as merely acceptable.

VS2a is therefore being shaped to ship multiple ARPG-genre + HD-2D-register commitments — end-game-anchored MS values (sim+demo coherent), Path A-prime ARPG-scale sprites (chierit 2.5×; monsters at genre-scale), pool VFX-mapping closure (canonical-bias-clean per-season vocabulary), room/hallway topology (Diablo/PoE single-camera framing) — alongside **geometric environmental placeholders** that contradict every other commitment. Structural incoherence.

**How caught:** Matt direct catch 2026-05-17 Day 5 by reference to demo v1 empirical signal: *"In the demo v1, one of the worst parts of it was the geometrically drawn 'random seasonal structures on the ground' and the geometrically drawn walls. The geometrically drawn floor tiles weren't too bad, but they weren't amazing either... I was wondering if we may have any wall, floor or object shapes which could be mapped to fit each season of the demo VS2a? And if not, would it make sense for legolas to look for anything that might match to our static dimensions of floors/walls? This could REALLY make the difference in the demo."*

**Enforcement gap:** Step B Tier-1 catalogue commission and per-vendor scout dispatches all named VFX + character axes explicitly; none named environment as a deferred-but-needed axis. The implicit assumption was that demo1's existing geometric environment rendering would carry forward into VS2a — that assumption was structurally wrong against the room/hallway topology commitment + the ARPG-register + HD-2D-style commitments shipping in parallel. No structural check on "are all load-bearing visual axes (VFX + characters + environment + UI + audio) explicitly enumerated at scoping time and either in-scope or named-deferred?"

**This is the FOURTH P6 instance** (alongside Drift-11A movement-speed, Drift-11B geometry × element VFX coverage, Drift-14 pool VFX-mapping). The pattern is now empirically robust at four sibling instances within ~24 hours of each other:

| Instance | Implicit-deferred dimension | Surfaced as gating | Catch source |
|---|---|---|---|
| Drift-11A | Movement-speed baseline (B12 deferral) | VS2a-gating | Matt direct 2026-05-16 |
| Drift-11B | Geometry × element VFX coverage | B11-gating | Matt direct 2026-05-16 |
| Drift-14 | Pool VFX-mapping coherence | VS2a-gating | Matt direct 2026-05-17 |
| **Drift-15** | **Environment tileset / wall / prop sourcing** | **VS2a-gating (recommended)** | **Matt direct 2026-05-17** |

**The pattern has crossed from "occasional drift" to "load-bearing systematic gap in scoping discipline."** Every catalogue / scoping commission authored to date has surfaced at least one implicit-deferred dimension at near-term-ship-gate time. The prevention prescription from Drift-11 sibling-cluster-sweep ("when one instance surfaces, sweep the rest of the deferred milestone for sibling dependencies in the same session") is correct but reactive. Forward prescription should be: at scoping time, enumerate ALL load-bearing visual axes (VFX + characters + environment + UI + audio) and explicitly state which are in-scope vs deferred-with-named-ship-gate. This is candidate D16 territory ("Multi-axis-catalogue-scoping requires explicit axis-enumeration at scoping time").

**Action:**
- Drift-15 entry archived here (this section).
- Gap-closure commission filed at `agentic_orchestration/gandalf/requests/2026-05-17-environment-tileset-catalogue-sweep-and-vs2a-selection.md` — legolas Mode B environment-tileset catalogue sweep (Track A) + gandalf per-season environmental-theming framework (Track B) + Matt VS2a pack selection (Track C) + downstream drax integration dispatch (Track D; separately authored by knight-rider).
- VS2a-gating reclassification recommended (same logic as Drift-14).
- Forward discipline candidate D16: "Multi-axis-catalogue-scoping requires explicit axis-enumeration at scoping time" — surface to next jack-ryan engineering-disciplines pass alongside D14, D15, R11(b), Pattern P7 cluster, Drift-11 sibling-cluster-sweep lesson. Disciplinary cluster is now 6 items — strong empirical basis for a coordinated jack-ryan pass when capacity allows.

**Cross-references:**
- Commission: `agentic_orchestration/gandalf/requests/2026-05-17-environment-tileset-catalogue-sweep-and-vs2a-selection.md`
- Sibling P6 instances: Drift-11A + Drift-11B + Drift-14 (above)
- Arena topology commit: `canonical/story/arena-room-hallway-system.md` (drax v0.12 — the room/hallway topology that surfaces environment as load-bearing)
- Style register: `canonical/story/style-register.md` (Candidate B HD-2D-pixel-art register — the register environment assets must honor)
- Forward audit: `canonical/story/p6-forward-audit-2026-05-16.md` — pattern naming basis; should be amended to add Drift-15 sub-pattern if a P6-doc-amendment pass happens later

**Discipline #13 instance:** YES — instance of "implicit-pillar drift" applied to the catalogue-scoping-vocabulary layer. The implicit pillar `multi-axis catalogue scoping enumerates ALL load-bearing visual axes at scoping time, with deferred axes explicitly named and ship-gated` was never stated and not structurally enforced. Same shape as Drift-13 (vendor-mixed-register at consumption granularity) applied at one level higher (scoping granularity vs consumption granularity).

---

## Cross-cutting drift patterns

Several drift instances above share common pattern-shapes. Naming the patterns helps future prevention:

### Pattern P1 — Design intent in conversation but not in code/schema/process

Examples: Drift-1 (form-bias); Drift-5 (enemy-legibility); Drift-7 (View A/B/C); Drift-8 (Q1 divergence). Pattern: project agrees in conversation; implementation drifts because nothing structurally alarms.

**Prevention:** every canonical conversation that locks a design intent should produce at minimum a decisions-log entry; if cross-seam, a canonical-doc lock; if cross-seam AND implementation-load-bearing, a Gate-1 check at dispatch authoring.

### Pattern P2 — Categorical-design-conversation register not bridged to operational-rigor register

Examples: Drift-6 (style-register categories); Drift-9 (movement-speed at-which-level); SR.6 (operational-precision-deferred-to-Elrond). Pattern: gandalf-or-Matt-authors-at-canonical-design-register; downstream consumers need operational-rigor; gap not noticed at authoring time.

**Prevention:** canonical-design-doc authoring should explicitly name downstream operational consumers and bridge the registers — either by authoring the operational-rigor in the same doc, or by explicitly commissioning the operational-rigor work to the appropriate steward (Elrond for data schemas; star-lord for prompt templates; etc.).

### Pattern P3 — gandalf design-conversation overreach (caught by Matt)

Examples: Drift-2 (pet system); Drift-3 (Fate substrate). Pattern: gandalf proposes design moves that work in canonical-design-register but conflict with existing project commitments; Matt catches in dialogue.

**Prevention:** gandalf should self-audit proposed design moves against existing canonical-locks before surfacing. The fact that Matt has caught this twice in one session (2026-05-15) is positive evidence the dialogue-stage critique works; the cost-of-correction-at-dialogue is much lower than cost-of-correction-after-canonical-lock.

### Pattern P4 — gandalf agent-definition ownership miss

Example: Drift-4 (style-register Phase-1 onboarding miss). Pattern: agent definition names ownership; agent's onboarding pass misses it.

**Prevention:** agent's onboarding-completion should produce an explicit ownership-inventory check against the agent definition. Phase-2 deliverable amendment recommended (see § "Recommendations for closing gaps" below).

### Pattern P5 — Multi-parameter system drift without joint analysis

Example: Drift-7 (View A/B/C). Pattern: multiple parameters individually tuned over time; the joint-system behavior emerges without anyone analyzing it as a system.

**Prevention:** any system governed by ≥3 parameters that interact mechanically should have an explicit canonical-design-doc naming the joint-behavior intent. Otherwise the emergence is drift.

### Pattern P6 — Load-bearing dimension deferred to "later" until "later" gates near-term ship

Example: Drift-11 (both instances — movement-speed baseline; geometry × element VFX coverage). Pattern: a scoping decision defers a complex multi-part workstream (B12 = baseline + gear economy; substrate-realignment = element + embodiment + ?...geometry?) to a later milestone. The deferred workstream is treated as atomic. A near-term ship downstream surfaces that some *portion* of the deferred workstream is actually upstream of the near-term ship — and the implicit-atomic-deferral was wrong.

This pattern is distinct from P1 (design intent in conversation but not code) because the dimensions WERE in the code/plan; the scoping decision just placed them wrongly in time. It's distinct from P5 (multi-parameter system drift) because the issue is not joint-emergence of tuned parameters but rather omission of an axis from the scoping conversation.

**Prevention:** when scoping a deferred milestone OR a multi-axis workstream:

1. **Decompose the milestone/workstream into its constituent dimensions** before deferring. Name each dimension explicitly. The B12 deferral named "movement speed + boots + gear slot audit" as one unit; if it had been decomposed into (a) baseline anchor, (b) gear-slot architecture, (c) MS affix economy, (d) hard-cap design, the baseline-anchor-vs-VS2a gating would have been visible at scoping time.
2. **For each dimension, ask:** *"is there a near-term ship between now and this milestone where this dimension becomes load-bearing?"* If yes, split that dimension out of the deferred scope and promote to the near-term-relevant scope.
3. **Catalogue/categorical workstreams are particularly vulnerable** because the constituent dimensions are not always all named at scoping time. The substrate-realignment scoping named element + embodiment but did not exhaustively enumerate "what other axes does a VFX library vary along?" — geometry was implicit-assumed. Catalogue workstreams should enumerate dimensions exhaustively (or explicitly name "all other axes are scoped post-hoc with this acknowledged risk").

**Forward audit triggered by Drift-11:** sweep current scoped-but-not-yet-active milestones for similar implicit-axis assumptions:

- **VS2b Substrate Realignment** — locked axes are element + embodiment. Other axes that may be upstream of VS2b-target ships? Animation style register; VFX motion conventions; color palette per element; canvas-size discipline per substrate; frame-rate conventions; loop-vs-one-shot structural patterns
- **Future Stage-A2 B-series work** — each B-item should be decomposed into constituent dimensions; each dimension audited for near-term-gating before locking the Stage-A2 atomic scope
- **VS2b Pimen full integration** — full integration may surface dimensions the first-Pimen-integration in VS2a didn't expose; recommend dimension-audit at VS2b authoring

This forward audit is gandalf scope; recommend single sweep-and-file pass within next 2 weeks before VS2b work activates.

### Pattern P7 — Test scaffolding masks production defect

Example: Drift-12 (gamora V2.1 emission gap; star-lord v2.1 smoke synthetic `loadout_json` injection masked production V2's `None` emission). Pattern shape, in four steps:

1. **Test setup uses synthetic / workaround fixtures** to satisfy preconditions the production code under test isn't yet expected to satisfy, OR to isolate the seam under test from upstream complexity. The workaround is technically legitimate as a unit test — it does exercise the code path correctly.
2. **The workaround makes the test green.** All assertions on the seam-under-test pass.
3. **The production gap becomes invisible.** Production code in the upstream seam fails to satisfy the precondition the test workaround bypassed; downstream code drops/silently-skips/no-ops; the test suite reports green because the test exercised the code path with a manufactured precondition rather than the production-fixture precondition.
4. **Risk surface:** the test suite confirms "code paths are exercised" but cannot confirm "production fixtures reach those code paths." Cross-seam integration silently degrades; the gap surfaces only when downstream empirical verification (column query; post-regen check; production telemetry inspection) is run by someone outside the seam.

P7 is **structurally distinct** from P1 (intent never made it into code) — in P7 the code is correct and the unit test is correct; the gap is in fixture realism at the seam boundary. P7 is also distinct from P5 (multi-parameter joint behavior un-analyzed) — in P7 there's a single boundary with a single-fixture-shape mismatch, not joint-emergence.

**Why this pattern is high-risk specifically for this project:** Reincarnated's engine has six tightly-coupled seams (rocket/gamora/star-lord/drax/elrond + LLM) that communicate via fixture dicts (fight_log records; loadout dicts; telemetry events). Each seam has unit-test coverage with seam-isolated fixtures. The fixture-shape contract between seams is enforced by Python convention (dict keys) rather than by typed schema with mandatory-vs-optional-field validation. Whenever an upstream seam adds a field, the downstream seam's tests already exercise the *consumer* with synthetic shaped-correctly fixtures — and the upstream seam's tests already exercise the *producer* in isolation. The integration path is the gap; P7 is the named risk-shape for that gap.

**Prevention prescription:**

The commission surfaces four candidate prevention mechanisms. After examining each against the gamora V2.1 instance and against the project's broader test architecture:

- **(a) Workaround-annotation discipline.** Workaround comments in test setup must include a "REVIEW: is this masking a production gap?" annotation. **PARTIALLY RECOMMENDED — limited reach.** This catches the cases where the test author knows they're working around something. It does NOT catch the gamora V2.1 case, where the star-lord smoke author was correctly testing the recorder in isolation and the workaround was correctly framed — no test-author judgment failure occurred. (a) is necessary but insufficient.

- **(b) Round-trip discipline.** **PRIMARY RECOMMENDED.** At least one smoke test per cross-seam contract must use production-path fixtures end-to-end, not seam-isolated fixtures. For the V2.1 case, a smoke that ran a tiny gamora V2 room execution → recorder → DB query → field-population assertion would have caught the gap. The cost is one additional smoke per cross-seam-contract migration; the value is the integration-path coverage that seam-isolated smokes provably cannot provide.

  **Operationalization:** when star-lord or gamora ships a schema/recorder/emission change to a cross-seam contract (telemetry schema; fight_log dict shape; loadout dict shape), the dispatch's acceptance criteria must include one of: (i) a cross-seam round-trip smoke OR (ii) an explicit "round-trip-not-applicable because <reason>" justification. Knight-rider can author this as part of dispatch authoring; jack-ryan can enforce at Gate 1.

- **(c) Audit hook.** Knight-rider's quarterly review reads `# workaround` comments in test files and routes for review. **TERTIARY RECOMMENDED — long-tail catch.** Useful as a periodic sweep but does not catch the gap at dispatch authoring. Lives at the same cadence as this drift-audit's R10 periodic re-pass.

- **(d) Recorder-side fail-loud-on-silent-drop.** **STRONGLY RECOMMENDED as a complementary code-level prevention.** The deeper structural cause of the gamora V2.1 case was that `recorder.py` line 477 silently `continue`d on `loadout_json is None` — a defensive guard that swallowed an unexpected production state. Defensive-silent-skip in recorder code paths is a fixture-contract violation made invisible. Recommend: cross-seam recorders/persistors that drop input should emit a counter or log entry (debug-or-info level) on every drop, so empirical "expected N rows, got 0 rows" gaps become discoverable from the run log without requiring a post-regen DB column query. This is star-lord-seam code change, not a process gate; recommend filing as forward action when star-lord next touches recorder.py.

**Composite recommendation:** (b) at dispatch authoring + (d) at recorder code + (a) as a discipline reminder. (c) deferred to drift-audit R10 quarterly cadence.

**Forward action:** see R11 below for the operationalization route.

### Pattern P8 — Vendor deliverable-register confusion (cross-product-line register inconsistency within a single vendor)

Example: Drift-13 (CraftPix character packs ship vector; CraftPix VFX packs ship pixel-art-shaped raster; both carry the site-wide "pixel art" marketing label). Pattern shape:

1. **Vendor uses consistent surface labeling** across all product lines (marketing copy, category names, store-tier descriptions). The label suggests a single deliverable register.
2. **Actual deliverable register varies per product line** within the vendor. One product line ships register-A (e.g., pixel-art raster PNG/PSD); another product line ships register-B (e.g., vector AI/EPS) — both labeled identically on the vendor's site.
3. **Downstream consumption implicitly aggregates by vendor.** Curation rubrics, per-vendor findings docs, vendor-class HOLD/PROMOTE/INCLUDE language, and downstream wiring (drax sourcing; gandalf register-validation) treat the vendor as a single register class. Per-vendor aggregation is the natural research-economy abstraction (one license; one vendor relationship; one rubric pass) but it elides the per-product-line register split.
4. **Cross-product-line confusion is not surface-visible** until either (a) downstream consumption across multiple product lines from the same vendor surfaces the mismatch (drax integration loading a "pixel" character pack alongside a "pixel" VFX pack and finding deliverable-shape divergence), OR (b) a second curator passes the vendor under a different product-line lens (the Drift-13 instance — VFX-side curator tagged pixel-art correctly; character-side curator tagged vector correctly; the mismatch only became visible when the two passes were compared).
5. **Risk surface:** vendor sweeps and curation rubrics that aggregate by vendor (not per-product-line) inherit the vendor's marketing-label register and miss the per-deliverable register split. The catalogue's per-record `style_register` field may be correctly populated by individual curators yet still mislead consumers who reason at vendor granularity. Style-register lock (`canonical/story/style-register.md`) operates as a consumption-time filter on per-record register data — its filtering effectiveness depends on per-record register being accurate, which it is — but the *vocabulary* of vendor-class judgment in curation dispatches and findings docs is the layer that drifts.

P8 is **structurally distinct** from P1 (intent never made it into code) — in P8 the per-record data IS in the catalogue correctly; the gap is at the vocabulary/aggregation layer above the catalogue. P8 is distinct from P2 (categorical-register not bridged to operational-register) — in P8 both registers are operational; the issue is per-vendor-vs-per-product-line granularity mismatch. P8 is distinct from P5 (multi-parameter joint behavior) — in P8 there is a single attribute (register) whose granularity is wrong for the consumption layer.

**Why this pattern is high-risk specifically for this project:** Reincarnated's catalogue research is structured by vendor (legolas crawls one vendor at a time; findings-summary docs are filed per-vendor at `research/catalogue/<vendor>/`; HOLD/PROMOTE/INCLUDE decisions are commonly rendered per-vendor). The catalogue's per-record `style_register` field has the correct granularity for downstream filtering, but the human-readable vocabulary above it (and the implicit mental model of "is vendor X a pixel-art vendor or a vector vendor?") aggregates by vendor. Whenever a vendor spans multiple product lines (VFX + characters; environments + portraits; sprites + tilesets), the per-vendor aggregation will be wrong for any vendor that mixes registers. CraftPix is the surfaced empirical instance; the same vendor-class label-vs-deliverable mismatch may exist at other Tier-1+ vendors not yet inspected at the multi-product-line lens.

**Prevention prescription:**

The commission surfaces four candidate prevention mechanisms (relabeled a-d for clarity within this section). After examining each against the CraftPix instance and against the catalogue's broader research architecture:

- **(a) Per-product-line register validation in catalogue dispatches.** legolas Mode B catalogue dispatches should record `deliverable_register` (or equivalent) explicitly per product line, not implicitly aggregate to per-vendor. **PRIMARY RECOMMENDED.** The per-record `style_register` field already exists at the right granularity — what's missing is dispatch-level instruction that the field MUST be populated per product line based on per-product-page inspection, NOT inferred from the vendor's site-wide marketing label. For vendors marketing as one register where any per-product-page inspection finds a different register, the dispatch must surface a "vendor register-mixed: yes" flag in the findings-summary doc. **Operationalization:** small persona-rule extension to legolas (catalogue dispatch authoring + persona file); knight-rider to route once selected.

- **(b) Cross-vendor register-consistency audit.** Periodic audit checking labels-vs-deliverables across all curated vendors (not just CraftPix). **SECONDARY RECOMMENDED — long-tail catch.** Useful as a one-shot sweep AND as a periodic re-pass (quarterly at drift-audit R10 cadence). Cost: re-pass each curated vendor's findings-summary doc against current catalogue records and flag any vendor with mixed `style_register` values. Cheap because the data already exists; just needs aggregation-and-comparison. Recommended cadence: one-shot sweep within the next Tier-1+ catalogue review (since CraftPix is presently the only mixed-register vendor in inventory, the sweep is cheap now); then quarterly at R10.

- **(c) Engineering-discipline candidate (#15 — per-product-line register validation).** **DEFERRED to jack-ryan judgment.** Engineering-discipline codification is jack-ryan dispatch territory; this drift-audit entry surfaces the pattern but does not pre-empt jack-ryan's decision on whether (a) belongs in engineering-disciplines.md as a numbered discipline OR stays as a legolas persona-rule extension. Recommend gandalf flag to jack-ryan via the next handoff; jack-ryan decides discipline-vs-persona-rule scope.

- **(d) Schema-level enforcement at catalogue.db.** Future elrond catalogue.db schema (when materialized from JSONL crawls) should expose a vendor-level "register-mixed: yes/no" computed flag at query time, so any consumer querying by vendor sees the mixed-register state explicitly. **TERTIARY RECOMMENDED — downstream-consumption safety net.** Lives at elrond data-architecture layer; flag for future elrond decision. Does not replace (a) — (a) catches at curation; (d) catches at consumption; both layers benefit from the discipline.

**Composite recommendation:** (a) at legolas dispatch authoring + (b) as a one-shot sweep at next Tier-1+ review (then quarterly at R10) + (d) at next elrond catalogue.db schema decision. (c) deferred to jack-ryan judgment.

**Forward action:** gandalf surfaces (a) and (d) as cross-seam considerations to knight-rider for routing (legolas persona-rule extension; elrond schema flag). (b) folded into R10 quarterly cadence (this drift-audit doc's existing periodic re-pass). (c) referred to jack-ryan via next handoff.

---

## Recommendations for closing gaps

### R1 — Add Discipline #13 candidate (implicit-pillar drift) to engineering-disciplines.md

Per doc 37 § 9.1: the candidate is drafted and ready. **Pending jack-ryan formal entry + Matt approval.**

When entered, this doc cross-references engineering-disciplines.md as the formal enforcement surface.

### R2 — Add Discipline #14 candidate (internal-vs-generative schema separation) to engineering-disciplines.md

Per doc 37 § 9.2b: the candidate is drafted and ready. **Pending jack-ryan formal entry + Matt approval.**

When entered, the Trigger Gate-1 question (*"Does this LLM call template expose internal mechanical labels? If yes, refactor to expose only per-instance vocabulary"*) becomes formal enforcement.

### R3 — Author embodiment-narrative-layer.md Layer 2 lookups for Construct / Spirit / Plant

Per EML.4: 3 of 8 starter embodiments have Layer 2 names deferred to LLM-generation-time. The deferral works operationally but creates LLM-run-to-LLM-run variance. **Recommendation:** when an LLM-generated season surfaces a Construct / Spirit / Plant form with naming the player-tests find good, capture those Layer 2 names canonically. Incremental amendment to embodiment-narrative-layer.md.

### R4 — Run the no-seed cosmology test (resolve doc 37 § 6.5)

Per `gandalf/requests/2026-05-16-no-seed-cosmology-generation-test.md`. **Not urgent**, but pending capacity for rocket + star-lord scope.

### R5 — Run the Elrond catalogue-rubric commission

Per `gandalf/requests/2026-05-15-elrond-catalogue-rubric-commission.md`. **Not urgent**, but operationally upstream of any catalogue-crawl work (Legolas Mode B).

### R6 — Complete engine-balance-stewardship.md (Gates 1-3)

Per dispatch `agentic_orchestration/dispatches/2026-05-16-gandalf-engine-balance-stewardship.md`. **Scheduled as session 3 of three** in the current canonical-story sequence.

### R7 — Agent-definition ownership-inventory check (future Phase-1 onboarding standard)

Per Drift-4: gandalf Phase 1 missed style-register.md ownership. Recommendation: add to gandalf agent definition or to canonical-story authoring discipline an explicit Phase-1-completion check: *"audit agent-definition ownership clause; produce inventory of every owned item; verify each is either authored, scheduled, or explicitly deferred with rationale."*

Surfaces if any agent's onboarding misses items; protects against future Drift-4-shape gaps.

### R8 — Author third-faction-tease.md (close C.7 partial-enforcement gap)

Per work-queue item #9 (small focused doc; queued). Closes a known C.7 partial-enforcement state.

### R9 — Begin seasonal-anchor-prose-notes.md per-anchor entries

Per work-queue item #12 (long-term effort). Each authored per-anchor entry incrementally strengthens D1 cosmological-register structural-enforcement at the anchor library layer. May be accelerated significantly if the no-seed reverse-test (R4) produces tooling for reverse-derivation as seed for anchor-prose-notes.

### R11 — Operationalize Pattern P7 prevention (cross-seam round-trip + recorder fail-loud)

Per Pattern P7 prevention prescription (composite of (b) + (d) + (a)):

- **(b) Cross-seam round-trip discipline.** Knight-rider to incorporate into dispatch authoring template: when a dispatch ships a change to any cross-seam contract (telemetry schema; fight_log dict shape; loadout dict shape; export packet shape; any inter-seam fixture format), the acceptance criteria must include either (i) a cross-seam round-trip smoke that uses production-path fixtures end-to-end OR (ii) an explicit "round-trip-not-applicable because <reason>" justification. Jack-ryan Gate-1 hook: surface a check on dispatches that ship cross-seam contract changes without one of the two clauses.
- **(d) Recorder fail-loud-on-silent-drop.** Forward action for star-lord at next recorder.py touch: replace the `loadout_json is None → silently continue` pattern (and structurally similar defensive-silent-skip patterns) with a counter or log entry so empirical "expected N rows, got 0 rows" gaps surface from the run log without requiring a post-regen DB column query. This is star-lord-seam code; recommend gandalf surfaces to star-lord at next v2.x telemetry dispatch authoring time.
- **(a) Workaround annotation reminder.** Discipline reminder (lighter than a process gate) at dispatch authoring: when a dispatch's smoke acceptance includes a synthetic-fixture workaround in the test, the dispatch's completion record should note whether the workaround masks a production gap or is genuinely a unit-isolation choice. The star-lord v2.1 dispatch's completion record correctly observed the workaround was unit-isolation, so this annotation is mostly about making the question visible rather than catching new failures.

**Owner:** knight-rider for (b) as a dispatch-template amendment + jack-ryan Gate-1 hook; star-lord for (d) at next recorder touch; gandalf surfaces (a) at the next dispatch-authoring discipline review with knight-rider.

**Pending:** knight-rider + jack-ryan coordination on (b) wording; star-lord notification of (d) for next recorder.py work; (a) reminder embedded in this audit and surfaced when the next dispatch with synthetic test fixtures lands.

### R10 — Periodic drift-audit re-pass

This doc is ongoing. **Recommendation:** re-pass quarterly (or at major milestones — pre-Stage-A2 ship; pre-Stage-A3 ship; pre-pitch; etc.). Each re-pass:

- Adds new pillars surfaced since last pass
- Updates status of partial-enforcement entries (have gaps been closed?)
- Archives new drift instances observed
- Updates pattern inventory if new cross-cutting patterns emerge

---

## Open questions

These do not block the canonical lock. They surface during implementation.

### Q1 — Quantitative drift-detection metrics

Should the project have automated drift-detection (e.g., LLM-call output scanning for forbidden labels per Discipline #14; periodic canonical-vs-implementation diff)? My instinct: **partial**. Discipline #14 anti-bias scaffolding can be partially automated (prompt-template review for forbidden-label-presence). Deeper drift-detection requires human design-judgment and shouldn't be automated.

### Q2 — Audit-finding severity tiering

Different drifts have different severities. Should this audit explicitly tier instances (high-severity-form-bias; mid-severity-Fate-substrate; low-severity-pet-overreach)? My instinct: **categorical-only**; quantitative-severity-scoring tempts Goodhart's law. The current pattern-naming (P1-P7) captures severity implicitly via pattern type.

### Q3 — Audit ownership

This doc is gandalf-authored canonical. Who maintains it? My current commitment: **gandalf owns the audit's structural-enforcement-discipline aspect; knight-rider coordinates cross-agent updates; jack-ryan provides discipline-related amendments when engineering-disciplines.md evolves; rocket / gamora / star-lord / drax / elrond contribute drift-instances when they observe them in their seams.** Distributed ownership; gandalf is the structural-coherence steward.

### Q4 — Cross-project applicability

The drift-audit framework is generic. If Reincarnated's engine ever licenses, the licensee inherits L1 substrate; do they also inherit a drift-audit obligation? My instinct: **yes — the audit framework should be part of engineering-disciplines.md formal documentation, which licensees inherit as process substrate.**

### Q5 — Drift-instance-retrospective frequency

How often should the drift instances be retrospectively reviewed for new patterns? My instinct: **at quarterly re-passes per R10**; patterns accumulate slowly.

---

## What this doc DOESN'T do

- **It does not enforce drift-prevention in real-time.** That requires Gate-1 reviews, prompt-template audits, dispatch-time checks. This doc inventories; the enforcement happens in process and disciplines.
- **It does not specify quantitative metrics for pillars.** Per Q2; categorical-design-criteria are the framework.
- **It does not replace decisions-log.** Decisions-log is the lock-of-record; this doc references decisions-log entries as structural-enforcement surfaces. The audit is the inventory; decisions-log is one of the durable surfaces.
- **It does not retroactively re-litigate locked decisions.** Locked pillars remain locked; this doc inventories them, doesn't relitigate them.

---

## Cross-references

- `canonical/37-form-bias-diagnosis-and-recovery.md` § 9.1 — the discipline this doc operationalizes
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Discipline #13 + #14 candidates pending formal entry
- `canonical/29-design-overview.md` — strategic anchor; many file-29 pillars inventoried above
- `canonical/32-progression-design.md` + `canonical/33-progression-skeleton.md` — 12 progression pillars inventoried
- Every `canonical/story/*.md` doc — inventoried in their respective sections
- `agentic_orchestration/AGENTS.md` § "Authority tiers" — defines the seams that participate in drift-prevention
- `agentic_orchestration/REVIEW_PROCESS.md` — Gate 1 + Gate 2 protocols where drift-prevention enforces
- `agentic_orchestration/gandalf/requests/2026-05-15-elrond-catalogue-rubric-commission.md` — drift-related commission
- `agentic_orchestration/gandalf/requests/2026-05-16-no-seed-cosmology-generation-test.md` — drift-related commission
- `agentic_orchestration/dispatches/2026-05-16-gandalf-engine-balance-stewardship.md` — drift-related dispatch (session 3)
- Memory `project_design_intent.md` — D1 element-name override history (Drift-10 source)
- `agentic_orchestration/dispatches/2026-05-16-gamora-v21-per-fight-emission-gap-fix.md` — Drift-12 source dispatch (completion record at bottom)
- `agentic_orchestration/qa/findings/2026-05-16-star-lord-full-regen-post-b6-v2.md` — Drift-12 empirical source (star-lord post-regen column check that surfaced the gap)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 13b (commit `4259969`) — Discipline #13b cites the same gamora V2.1 instance at the outcome-attribution-opacity layer (complementary to Drift-12's test-fixture-divergence layer)

---

## Maintenance protocol

**This doc is ongoing.** Append-only structure for drift instances + status updates for enforcement state. Do not rewrite history.

### Adding a new pillar

When a new canonical-design-doc lands OR a new file-29/32/33-style strategic-anchor pillar surfaces:

1. Add the pillar to the appropriate inventory section above.
2. Assign status (✅ Locked / 🟡 Partial / 🟠 Drift-observed / 🔴 Unenforced / ⚪ Operational).
3. Enumerate enforcement surfaces.
4. Update cross-references.

### Archiving a new drift instance

When drift is observed (in dialogue, in implementation review, in family playtest):

1. Author a new entry in § "Drift instances observed and archived."
2. Name what drifted; how caught; the enforcement gap; the action taken.
3. Identify if it matches an existing pattern (P1-P7) or surfaces a new pattern.
4. If new pattern, add to § "Cross-cutting drift patterns."

### Updating enforcement status

When a partial-enforcement gap is closed (e.g., Discipline #13 lands in engineering-disciplines.md; embodiment-narrative-layer.md gains Construct/Spirit/Plant Layer 2 entries; etc.):

1. Update status from 🟡 Partial to ✅ Locked.
2. Update enforcement-surfaces entry.
3. Remove from § "Recommendations for closing gaps" if applicable.

### Periodic re-pass

Per R10: quarterly OR at major milestones, gandalf re-passes the audit:

1. Refresh pillar inventory (any new docs landed?).
2. Refresh status (any enforcement gaps closed?).
3. Archive any new drift instances.
4. Refine pattern inventory.
5. Update recommendations.

— gandalf, with Matt's standing approval on the discipline framework + ongoing maintenance commitment (2026-05-16)
