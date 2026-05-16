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

**Action:** Pending engine-balance-stewardship.md Gate 3 (forthcoming session 3); may require small rocket/gamora research-pass for empirical confirmation.

**Discipline #13 instance:** YES — partial-enforcement-without-verification pattern.

### Drift-10 — D1 element-name overrides accumulating without rubric revision

**What drifted:** Per memory `project_design_intent.md` 2026-05-12 entries: multiple manual overrides accumulated on the D1 element-name pool (pall demoted; rime / miasma / shear / billow demoted; smoke reverted; cloud promoted; etc.). The rubric (`d1_total` scoring) was decoupled from operational filter (`d1_status`) — multiple overrides accumulated WITHOUT the rubric being revised to capture the patterns.

**How caught:** Matt's 2026-05-12 ongoing observation; documented in memory.

**Enforcement gap:** the rubric should reflect the project's actual judgment criteria. Override-accumulation-without-rubric-revision = the rubric is no longer canonical reference; the rubric AND the operational filter have drifted apart.

**Action:** memory notes capture the drift; rubric work (e.g., `vocabulary_commonness` sub-property; `slot_unambiguous` check) named as future work. Doc 37 § 7 superseded the curated-pool approach under cipher architecture; the drift is rendered moot by the architecture shift but remains as historical evidence of the pattern.

**Discipline #13 instance:** YES — historical instance; renders the pattern empirical not hypothetical (this is one of doc 37 § 9.1's named empirical-instance examples).

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

Different drifts have different severities. Should this audit explicitly tier instances (high-severity-form-bias; mid-severity-Fate-substrate; low-severity-pet-overreach)? My instinct: **categorical-only**; quantitative-severity-scoring tempts Goodhart's law. The current pattern-naming (P1-P5) captures severity implicitly via pattern type.

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
3. Identify if it matches an existing pattern (P1-P5) or surfaces a new pattern.
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
