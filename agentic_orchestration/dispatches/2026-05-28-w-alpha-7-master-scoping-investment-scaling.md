# DISPATCH — W-α7 Master Scoping — Investment Scaling MVP Patterns 1+2 + Multi-Profile Calibration (Case 11 Resolution)

**Authored:** 2026-05-28
**Author:** knight-rider (Cycle 14 hive-mind state orchestrator)
**Recipients:** gandalf (W-α7-gandalf canonical) + rocket (W-α7-rocket P1+P2) + gamora (W-α7-gamora multi-profile calibration + BVV harness extension) + drax (W-α7-drax loadout UI) + jack-ryan (W-α7-jack-ryan canonical retirements + Gate-1 of this master)
**Pattern:** Pattern B master scoping (~7-10d sustained-intensity work; 12-17d total to v1 from Matt Gate-7 + this ratification combined)
**Status:** PENDING — fires jack-ryan Gate-1 on receipt; per-stream dispatches authored post Gate-1 PASS
**Authority:** Matt 2026-05-28 RATIFICATION — Cycle 14 architectural integrity scope expansion (CLAUDE.md engine > game > phase invocation)

---

## 0. AUTHORITY + ARCHITECTURAL FINDING

**Matt 2026-05-28 D1+D2+D3+D4 RATIFICATION** verbatim invoked CLAUDE.md orientation: *"Engine first. Game second. Phase third."*

**Architectural finding (rocket sub-agent clarification surfaced at design-dialog layer):**
- Engine has NO points-invested scaling in damage formula
- `NODE_MAX` (5 passive / 15 active / 1 T4) exposed in loadout UI but engine doesn't deliver investment-scaled mechanics
- **UI promise without engine delivery** — architectural-integrity violation at engine layer
- Cycle 14 v1 close must address per engine > game > phase precedence

**Case 11 scaffold-drift framing:** Mode A hidden drift catch at design-dialog layer (different surface than cases 1-10 which surfaced at engine empirical-execution layer). Discipline #39 framework extends Mode A to design-dialog inspection surfaces — framework operating as architected at novel layer.

**Discipline #47 design-time check satisfied via Matt RATIFICATION authority.**

---

## 1. W-α7 SCOPE

### 1.1 Three architectural commits

1. **Pattern 1 implementation** — active skill damage scaling per point. Engine seam: rocket foundation + generation (per_skill_emitter.py + damage_resolver.py). Per-point investment → measurable damage delta.
2. **Pattern 2 implementation** — passive skill effect scaling per point. Engine seam: rocket foundation + generation. Per-point passive investment → measurable effect-magnitude delta.
3. **Multi-investment-profile calibration** — Path α parity verified at multiple investment levels (low / mid / max / mixed-profile), not just W-α3 single fixed-profile. BVV harness extended for investment-profile coverage.

### 1.2 6-pattern canonical architecture (gandalf seam)

Doc captures all 6 patterns; Patterns 1+2 implemented Cycle 14; Patterns 3-6 canonical-locked for Cycle 15+ implementation:

| Pattern | Scope | Cycle |
|---|---|---|
| **1** | Active skill damage scaling per point | C14 (W-α7-rocket-P1) |
| **2** | Passive skill effect scaling per point | C14 (W-α7-rocket-P2) |
| 3 | Threshold unlocks | C15+ (canonical-locked) |
| 4 | QoL modifiers | C15+ (canonical-locked) |
| 5 | Synergy bonuses | C15+ (canonical-locked) |
| 6 | Resource economy modifiers | C15+ (canonical-locked) |

Cycle 15 design dialog scopes detailed implementation per each deferred pattern.

### 1.3 Out of scope

- Patterns 3-6 implementation (canonical-locked only; Cycle 15+ implementation)
- W-α6 per-encounter-type bands (already firing as case 9 resolution; let complete; W-α7-gamora extends architecture)
- C-Hybrid algorithm + pirate-faction sub-cluster naming + substrate-signal research (Matt D3 Gate-7 Cycle 15 scope)
- R5-Plus scrub + Phase 5 LLM naming (in-flight outside Path α)
- Spirit guide marginal value pass (Cycle 15+)

---

## 2. WORK-STREAM DECOMPOSITION + SEQUENCING

### 2.1 W-α7-gandalf canonical FIRST (load-bearing)

**Owner:** gandalf (design seam; canonical-story author)
**Scope:** new canonical doc at `canonical/<NN>-investment-scaling-6-pattern-architecture-2026-05-28.md` (suggested 51)
**Effort:** ~1-2d
**Required sections:**
- Authority + provenance (Matt 2026-05-28 RATIFICATION; CLAUDE.md engine>game>phase invocation; case 11 framing)
- Architectural-integrity argument (UI promise without engine delivery)
- 6-pattern enumeration + per-pattern conceptual scope
- Patterns 1+2 detailed semantics for W-α7-rocket implementation (active skill scaling formula intent; passive skill scaling formula intent)
- Patterns 3-6 canonical-locked stubs for Cycle 15+ implementation
- Multi-investment-profile calibration framing (Path α parity at low / mid / max / mixed profiles)
- Cross-references: doc 50 (bounded-viability), doc 47 § 3 (damage scaling paths), `NODE_MAX` source location for loadout UI integration

**Cross-references to update:** 00-ground-state.md (first-reads + currents); 02-roadmap.md (Path α + Cycle 14 v1 trajectory updated; Patterns 3-6 Cycle 15+ commit).

**Tag:** `gandalf/v1.14-w-alpha-7-investment-scaling-canonical-1` (seam discretion).

### 2.2 W-α7-rocket-P1 + W-α7-rocket-P2 parallel post W-α7-gandalf lock

**W-α7-rocket-P1 — Pattern 1 active skill damage scaling:**
- **Owner:** rocket (foundation + generation seam; per_skill_emitter.py + damage_resolver.py touched)
- **Scope:** active skill damage = `base_damage × (1 + scaling_coefficient × points_invested)` (formula structure subject to gandalf canonical lock at W-α7-gandalf § 1.2; rocket seam discretion on coefficient calibration)
- **Effort:** ~2-3d (math note + implementation + integration test)
- **Math note** at `~/Games/reincarnated-engine/src/reincarnated/generation/math/w-alpha-7-pattern-1-active-scaling-2026-05-28.md` per Discipline #1
- **MIGRATION.md** within generation seam (foundation/element/anchor touches if needed)
- **Tag:** `rocket/v1.9-w-alpha-7-pattern-1-active-scaling-1`

**W-α7-rocket-P2 — Pattern 2 passive skill effect scaling:**
- **Owner:** rocket (foundation + generation seam)
- **Scope:** passive skill effect magnitude = `base_effect × (1 + scaling_coefficient × points_invested)` (formula structure per gandalf canonical lock; rocket seam discretion on coefficient calibration)
- **Effort:** ~2-3d parallel with P1
- **Math note** + MIGRATION.md
- **Tag:** `rocket/v1.10-w-alpha-7-pattern-2-passive-scaling-1`

**Cross-stream coordination:**
- W-α7-rocket-P1 + P2 may share infrastructure (point-investment lookup + scaling formula utilities); rocket seam decides decomposition
- Each commits independently; tag per pattern

### 2.3 W-α7-gamora multi-profile calibration sequential after rocket P1+P2 lands

**Owner:** gamora (simulation seam; extends unified_calibration_loop.py + bounded_viability_validation.py)
**Scope:**
- Multi-investment-profile calibration: Path α parity verified at 4 profiles (low / mid / max / mixed-profile per gandalf canonical lock; gamora seam discretion on specific profile definitions)
- BVV harness extended for investment-profile coverage: per-profile compound_pass verification; new `investment_profile` parameter
- Sensitivity analysis: scaling coefficient values from rocket P1+P2 vs Target 1 ≤1.5× variance preserved across profiles
- Reuse W-α3 Phase 2 + W-α6 (if complete) calibration architecture

**Effort:** ~2-3d sequential after rocket P1+P2 close
**Math note** at `~/Games/reincarnated-engine/src/reincarnated/simulation/math/w-alpha-7-multi-investment-profile-calibration-2026-05-28.md`
**MIGRATION.md** § v1.45 (or next available; coordinate with rocket P1+P2 commits)
**Tag:** `gamora/v2.9-w-alpha-7-multi-profile-calibration-1`

### 2.4 W-α7-drax loadout UI update parallel with W-α7-gamora

**Owner:** drax (loadout + demo seam)
**Scope:**
- NODE_MAX surfaces (5 passive / 15 active / 1 T4) become mechanically meaningful in loadout UI
- Each skill point visibly affects kit performance preview
- UI integration with engine investment-scaling output
- May surface Discipline #47 design-time check considerations if UI affects bounded-viability presentation

**Effort:** ~1-2d parallel with W-α7-gamora (gates on rocket P1+P2 engine landing, not gamora calibration)
**Tag:** `drax/v1.X-w-alpha-7-loadout-investment-scaling-ui-1`

### 2.5 W-α7-jack-ryan canonical retirements parallel throughout

**Owner:** jack-ryan (canonical-write seam)
**Scope:**
- Decisions-log entries: case 11 RATIFICATION + W-α7 Patterns 1+2 architectural commit + Patterns 3-6 Cycle 15+ canonical-lock
- Possible new discipline candidate: engine-game-phase orientation as inspection discipline (catches UI-promise-without-engine-delivery patterns); jack-ryan seam discretion on whether new discipline #48 OR extension of #47 OR doc-51-only canonical authority
- Cross-reference audit: case 11 Mode A design-dialog layer extension of Discipline #39 framework

**Effort:** ~0.5d parallel
**Tag:** `jack-ryan/v1.9-w-alpha-7-canonical-retirements-1`

### 2.6 Bundle Gate-2 + Wave 5 RE-FIRE post all streams

**Bundle Gate-2 (jack-ryan; ~0.25d):** full cross-stream coherence + Discipline #47 enforcement + decisions-log entry
**Wave 5 RE-FIRE (gamora; ~3-5d):** full production season under composite engine state (Path α + Option B per-encounter bands + W-α7 investment scaling + R5-Plus scrub + Phase 5 LLM naming)

---

## 3. CYCLE 14 V1 CLOSE TRAJECTORY

| Phase | Effort | Calendar |
|---|---|---|
| W-α6 (currently firing) per-encounter-type bands | ~2-4d | Days 0-4 |
| W-α7-gandalf canonical | ~1-2d | Days 4-6 |
| W-α7-rocket P1 + P2 parallel | ~2-3d | Days 6-9 |
| W-α7-gamora multi-profile + W-α7-drax UI parallel | ~2-3d | Days 9-12 |
| W-α7-jack-ryan canonical retirements (parallel throughout) | ~0.5d | Days 4-12 |
| Bundle Gate-2 | ~0.25d | Day 12 |
| Wave 5 RE-FIRE | ~3-5d | Days 12-17 |
| Matt v1 ratification | <0.1d | Day 17 |

**Realistic estimate: ~12-17d total from this ratification + Gate-7 Option B ratification.** Within Path α 4-6 week budget; **at upper end of sustained-intensity threshold** per Matt's acknowledgment.

---

## 4. GATE-1 ACCEPTANCE CRITERIA (jack-ryan DESIGN-MODE)

Concerns to surface or rule out:

- **W-α7-gandalf canonical content adequacy** — does proposed canonical doc capture Patterns 1+2 detailed semantics enough for downstream W-α7-rocket implementation to commit cleanly without re-litigating?
- **W-α7-rocket P1 + P2 parallel-vs-sequential** — formula structures may share infrastructure; rocket seam discretion on internal decomposition. Acceptable framing?
- **W-α7-gamora sequential dependency on rocket** — calibration cannot fire until P1+P2 engine implementations land. Cross-stream signal coordination adequate?
- **W-α7-drax UI gate on rocket engine landing** — UI work doesn't need gamora calibration, but does need rocket P1+P2 to produce investment-scaled mechanics. Coordination signal adequate?
- **W-α7-gamora multi-profile coverage** — 4 profiles (low / mid / max / mixed) per gandalf canonical lock OR rocket seam discretion? Verify load-bearing source.
- **W-α6 in-flight coordination** — does W-α7 architecturally absorb W-α6 (multi-profile calibration subsumes per-encounter bands at fixed-profile)? Or do both architectures compose cleanly?
- **Case 11 Mode A extension of Discipline #39 framework** — design-dialog inspection layer is novel; does framework extension warrant explicit canonical write in W-α7-jack-ryan W-α5c-equivalent OR doc-51 sufficient?
- **Wave 5 RE-FIRE composition note** — Matt D4 (Gate-7) flagged Path α + Option B + R5-Plus + Phase 5 LLM naming integration. Investment scaling now adds another composition vector. Adequate framing?
- **Drax workstream revival coordination** — drax has been DEFERRED through Path α; loadout work re-fires under W-α7-drax. Communication mechanism adequate?
- **Discipline candidate decision (W-α7-jack-ryan)** — engine-game-phase orientation inspection discipline. New #48 vs #47 extension vs doc-51-only — jack-ryan seam discretion. Frame appropriately?

Return form: PASS / PASS-WITH-AMENDMENTS / BLOCK. If amendments, list in-place edits before per-stream dispatches fire.

Time budget: ~15-20 min (master scoping breadth + multi-stream coordination).

Return: PASS verdict + per-stream verdicts + bundle coordination verdict + rationale + recommendation on case 11 Mode A canonical extension framing.

---

## 5. RISKS + COMPLICATIONS

- **Sustained-intensity threshold (Matt acknowledged).** ~12-17d total Cycle 14 v1; upper bound of 6-week budget. Re-evaluation hook applies if scope expands further (Matt Path α framing).
- **Case 12+ probability rising.** Path α has surfaced cases 8/9/(probable 10)/11 in single session. Each architectural absorption increases surface area; framework Mode A extension expected.
- **W-α7-rocket cross-pattern coordination.** P1 + P2 may share infrastructure; rocket seam decomposition could introduce Pattern 1 + Pattern 2 inter-dependency.
- **Drax workstream revival.** ~1.5-2hr of Path α elapsed where drax was DEFERRED; W-α7-drax revives; deferred sample-data wiring + image pipeline + Court accumulation now re-sequenced with investment-aware UI.
- **Pre-fire resource projection (Discipline #1.1).** W-α7-gamora multi-profile calibration is highest-compute stream; project sweep × 4 profiles × 24 cells = 96 cells (4× W-α6 scope). Wall-time + memory projection in math note.

---

## 6. URGENCY

**Cycle 14 v1 close trajectory ~12-17 days from this ratification.** Architectural-integrity precedence per CLAUDE.md engine > game > phase mandates closure within cycle.

Fire jack-ryan Gate-1 review ASAP. Per-stream dispatches author + parallel fan-out post Gate-1 PASS + W-α6 completion + W-α7-gandalf canonical lock.

---

**KR signature:** authored per Matt 2026-05-28 D1+D2+D3+D4 RATIFICATION + CLAUDE.md engine>game>phase invocation + case 11 Mode A design-dialog framing per Discipline #39 framework extension. Five-seam coordination (gandalf + rocket + gamora + drax + jack-ryan) parallel fan-out post canonical lock. Q10 quality > timeline drives; architectural integrity preserves canonical-doc-50 design directive at engine layer.
