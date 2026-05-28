# DISPATCH — jack-ryan Gate-5 Architectural Disposition — 8th Scaffold-Drift Case (Boss-KPM Damage Formula Gap)

**Authored:** 2026-05-28
**Author:** knight-rider (Cycle 14 hive-mind state orchestrator)
**Recipient:** jack-ryan (DESIGN-MODE — architectural disposition)
**Pattern:** Pattern B (long-form architectural analysis → 4-6 options ranked → recommendation → file to qa/pending/)
**Status:** PENDING — fires immediately on receipt
**Precedent:** Gate-3 SC7-F1 disposition (`qa/pending/2026-05-28-sc7-f1-gate-3-disposition.md`) + Gate-4 7th-case disposition (`qa/pending/2026-05-28-7th-scaffold-drift-cross-class-dps-gate-4-disposition.md`)

---

## 0. AUTHORITY + GATE INVOCATION

**Matt D2 re-evaluation hook from Gate-4 ratification:** *"Re-evaluation hook: if Track 1 surfaces 8th case materially extending scope, Matt re-evaluates."*

**Trigger condition: MET.** Gamora Option F Track 1 close (engine `f704599` + tag `gamora/v2.0-option-f-track-1-per-damage-path-bands-1` + meta `1a2b5a3`) returned **acceptance FAIL (3/18 emit; ≥12/18 required)** + invoked **Discipline #44 framing-refusal** surfacing the 8th scaffold-drift case.

**Per established cadence (SC7-F1 Gate-3 → Matt Pattern-B ratification; 7th-case Gate-4 → Matt Pattern-B ratification):** KR fires jack-ryan Gate-5 architectural disposition BEFORE surfacing options package to Matt.

**Acceptance:** disposition filed to `agentic_orchestration/qa/pending/2026-05-28-8th-scaffold-drift-boss-kpm-damage-gap-gate-5-disposition.md` per Gate-3/Gate-4 doc template.

---

## 1. SCOPE — what jack-ryan analyzes

Architectural disposition over the 8th scaffold-drift case. Specifically:

### 1.1 Two framings, both load-bearing

**Surface framing (gamora final hand-back line):**
> STR/DEX physical kits produce boss KPM=0 because `base_physical_damage_l50` (SC-6b) is uncalibrated against boss HP targets. INT/WIS-faith bands empirically grounded (82.192 INT-magical median; 75.949 WIS-faith median). STR/DEX FALLBACK to prior single-cohort bands.

**Deeper framing (gamora empirical inspection during Track 1 calibration sweep):**
> Most kits — including INT/WIS kits — produce T1 REJECT at boss encounters (t2_kpm=0.0). Only `artillery_mage` has meaningful boss KPM. INT kits int_01 standard_wizard, int_03 pyromantic_caster, int_04 red_mage, int_05 arcane_familiar, WIS kit wis_01 channeling_cleric — all produce t1_kpm=0 / t2_kpm=0 at boss encounters. The INT-magical band (61.64, 102.74) is artillery_mage-outlier-driven; 13/16 band cells are FALLBACK or single-outlier-derived.

**Discipline #42 framing-audit Q1+Q3 question to jack-ryan:** are these two framings consistent? Does the surface framing UNDERSTATE the structural depth? If so, by how much, and what's the disposition consequence?

### 1.2 Root-cause depth analysis

Identify the substrate constants and architectural seams co-implicated:
- `base_physical_damage_l50` (SC-6b: `family_baseline × amplitude_mean`, martial-heavy=177) vs. endgame boss HP scaling
- `BASE_SPELL_DAMAGE_L50` (SC-7 calibrated mult=93.8× → `{T1:28144, T2:42216, T3:60978, T4:112575}`) — calibrated against single-class single-archetype; non-artillery INT/WIS kits still fail
- Boss HP scaling (which substrate? which doc? what's the calibration history?)
- T1 REJECT threshold (`TIER_1_REJECT_THRESHOLD = 0.30`) — appropriate for the current kit-damage-vs-boss-HP regime, or itself a scaffold?
- Kit-skill-base-damage values (per-skill `base_spell_damage`, `base_physical_damage`) — substrate-carried OR derived from `base_*_damage_l50` via skill-multiplier table?

Trace which constant first introduced the boss-KPM gap (Discipline #11 empirical inspection — git blame, design-doc trail, decisions-log).

### 1.3 Discipline citations (anticipated)

- **Discipline #39** (no-synthetic-stub-as-permanent-fallback) — does STR/DEX FALLBACK to prior single-cohort bands violate? (Matt's "scaffolds get RESOLVED, not deliberately introduced" framework)
- **Discipline #40 case (c)** (canonical-lock retraction 6-step) — does the canonical doc § 3.9 FALLBACK notation already constitute a retraction-in-progress? If Gate-5 ratifies a different path, third iteration of § 3.9 needed?
- **Discipline #42** (framing-audit) — both framings carried; deeper finding materially extends scope
- **Discipline #44** (framing-refusal — gamora-invoked)
- **Discipline #13a-partition** (mechanical partition permitted) — does deeper finding affect the partition framing? (4 damage-scaling paths per doc 47 § 3 still canonical)

### 1.4 Options analysis — minimum 4, maximum 6, ranked

Each option per Gate-3/Gate-4 template:
- Title + brief description
- Scope of work (KR estimate in days; ≤1d = Cycle 14 fit; >1d = Cycle 14 risk; >2d = Cycle 15 territory)
- What it resolves (which constants; which framings)
- What it does NOT resolve (residual risk; deferred questions)
- Discipline compliance (which disciplines satisfied; which strained)
- Recommendation rank + rationale

**Suggested option seeds (jack-ryan free to add/refine/replace):**

| # | Title | Sketch | Day estimate |
|---|---|---|---|
| A | Accept FALLBACK + advance Track 2 D3-deferred to Cycle 14 | STR/DEX per-kit physical damage calibration (~0.5-1d); leaves INT/WIS deeper finding unaddressed | ~1d |
| B | Boss HP rebase against current damage population | Reduce boss HP targets to current kit damage output median (~1d); resolves population-wide T1 REJECT | ~1d |
| C | T1 REJECT threshold widen (0.30 → 0.45 or higher) | Admit more kits to single-archetype band; mask root cause; SCAFFOLD per Matt framework | ~0.25d |
| D | Per-kit damage calibration (SC-6b AND SC-7 both per-kit, not per-class) | Full per-kit boss-KPM calibration sweep across all 18 kits × 4 cohorts (~2-3d); resolves ALL framings | ~2-3d |
| E | Cycle 14 close-criterion amendment | Accept 3/18 emit + Track 1 infrastructure as Cycle 14 close; defer 8th-case full resolution to Cycle 15 | ~0.1d |
| F | Staged: B (boss HP rebase) for Cycle 14 emit → D (per-kit calibration) for Cycle 15 | Boss HP rebase produces near-term emit signal; Cycle 15 sees full per-kit calibration sweep with proper Track 2 design-call | ~1d Cycle 14 + ~3d Cycle 15 |

Jack-ryan may compose any subset or alternative.

### 1.5 Cycle 14 v1 close criterion impact

Each option's effect on:
- D9 close criteria (≥12/18 × 3 seasons emit; Gate-2 PASS; A/B filed; #41-#46 batched; v1 tag)
- D7 escalation (3-fail/season → Matt Pattern-B) — would option require D7 fire?
- D13 P1-P9 parallel framework (post Gate-2 PASS) — which options preserve the framework
- Cycle 14 close trajectory (~4-7 days at Gate-4 → new estimate per option)

### 1.6 Discipline #18 refinement compliance

Matt's Gate-4 D3 deferral honored: methodology consultation at extension hotspots fires AFTER baseline empirical signal lands. Track 1 IS baseline; Track 2 was D3-deferred to Cycle 15.

Question for jack-ryan: does the 8th-case empirical signal (Track 1 telemetry) NOW constitute the baseline that should fire Track 2 methodology consultation? Or is Track 1's failure-mode itself architectural (boss HP) rather than calibration (per-kit damage)?

---

## 2. REQUIRED READING

Substrate:
- `~/Games/reincarnated-engine/design/math/phase-7-2-layer-joint-gate-thresholds-2026-05-27.md` § 3.7-3.10 (current canonical state)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/option-f-track-1-per-damage-path-kpm-bands-2026-05-28.md` (Track 1 math note)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` § v1.38 (gate semantic change + Discipline #44 invocation record)
- `agentic_orchestration/cycle-14-wave-5-season-001/option-f-track-1-calibration-telemetry.json` (empirical sweep telemetry; **load-bearing for root-cause depth analysis**)

Precedent:
- `agentic_orchestration/qa/pending/2026-05-28-sc7-f1-gate-3-disposition.md` (Gate-3 SC7-F1 template)
- `agentic_orchestration/qa/pending/2026-05-28-7th-scaffold-drift-cross-class-dps-gate-4-disposition.md` (Gate-4 7th-case template; 6 options ranked)

Canonical context:
- `~/Games/reincarnated-collaboration/canonical/47-damage-scaling-architecture-2026-05-26.md` § 3 (4 damage-scaling paths)
- `~/Games/reincarnated-engine/design/decisions/decisions-log.md` (recent entries — SC-6b, SC-7, Phase 7 thresholds)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (Disciplines #11, #13a, #18, #39, #40, #42, #44, #45)

Matt-decisions context:
- `agentic_orchestration/cycle-14-hive-mind-state.md` § "8TH SCAFFOLD-DRIFT CASE LANDED 2026-05-28" (KR state record + Discipline #42 framing-audit)
- Matt Gate-4 D2 re-evaluation hook verbatim

Gamora hand-back full text:
- Engine commit message at `f704599`
- AGENT_STATE.md `gamora` final entry
- Track 1 dispatch file completion section (`agentic_orchestration/dispatches/2026-05-28-gamora-option-f-track-1-per-damage-path-kpm-bands.md`)

---

## 3. DELIVERABLE + ACCEPTANCE

File: `agentic_orchestration/qa/pending/2026-05-28-8th-scaffold-drift-boss-kpm-damage-gap-gate-5-disposition.md`

Structure per Gate-3/Gate-4 template:
- § 1 Trigger + scope
- § 2 Both framings (surface + deeper) — Discipline #42 framing-audit explicit
- § 3 Root-cause depth analysis (substrate constants + git/decision lineage)
- § 4 4-6 options ranked + per-option scope/discipline/recommendation
- § 5 Recommendation + rationale (jack-ryan's process-discipline preferred)
- § 6 Cycle 14 v1 close-criterion impact per option
- § 7 Open questions for Matt Pattern-B ratification

**Time estimate:** ~0.25-0.4d (Gate-3 was ~0.25d; Gate-4 was ~0.3d; this is more architecturally complex due to deeper framing surface, target ~0.3-0.4d).

**Commit + push pattern:** auto-commit per CLAUDE.md addendum (Gate-5 disposition is authorized cycle work); auto-push per Cycle 14 per-workstream push pattern (D11 precedent; jack-ryan canonical writes pushed since Discipline #45 fire).

**Critique-pair:** none required at Gate-5 authoring; KR + Matt review on receipt.

---

## 4. OUT OF SCOPE — explicit

- **Do not implement any option.** Options are for Matt Pattern-B ratification, not jack-ryan execution.
- **Do not amend Track 1 math note or canonical doc § 3.9.** Both stand as-authored until Matt ratifies a path forward (Discipline #40 case (c) would fire on ratification, not now).
- **Do not retract or revise gamora's empirical telemetry.** Sweep data is empirical ground-truth; jack-ryan analyzes, does not re-run.
- **Do not pre-empt Matt's D2 re-evaluation.** Filed disposition is INPUT to Matt's decision, not the decision itself.
- **No code review.** This is architectural disposition, not Gate-2.

---

## 5. URGENCY

**Cycle 14 v1 close trajectory blocks pending this disposition + Matt Pattern-B ratification.** Wave 5 cascade cannot resume; D13 P1-P9 parallel framework cannot fire; v1 tag (`v1-cycle-14-no-classes-substrate-led`) cannot land.

Fire ASAP. Per established precedent, KR will surface options package to Matt immediately on jack-ryan return.

---

**KR signature:** authored per Matt 2026-05-28 D2 re-evaluation hook + SC7-F1/Gate-4 precedent + Discipline #42 framing-audit surfacing deeper finding. Fires jack-ryan as sub-agent per hive-mind decision-routing (process-gate seam owner). Matt as LAST-RESORT escalation per Matt 2026-05-23 directive — Gate-5 disposition input lands first.
