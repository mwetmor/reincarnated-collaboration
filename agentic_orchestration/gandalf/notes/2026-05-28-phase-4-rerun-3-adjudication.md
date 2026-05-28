# Phase 4 RE-RUN-3 Adjudication — R1/R2/R3/R4 Disposition + Cycle 14 Close-Criterion

**Date:** 2026-05-28
**Author:** gandalf (story-and-design steward)
**Mode:** Pattern B sustained dialogue with Matt → adjudication record (per OP § 2 Pattern A-deep structure; Matt directly elected disposition vs sub-agent invocation)
**Status:** LOCKED — Matt sign-off this session; KR election prompt drafted; canonical anchors amended
**Authority:** Matt 2026-05-28 (this session)

**Anchor docs:**
- `agentic_orchestration/gandalf/notes/2026-05-28-mac-mini-freeze-diagnosis.md` (freeze diagnosis + Discipline #47 candidate)
- `canonical/story/c-hybrid-cell-and-curation-architecture-2026-05-28.md` (load-bearing architecture; § 1.1 + § 1.3 amended this session)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` § 4.6 (two-layer T4 architecture; D1-D6 RATIFIED)
- `canonical/51-investment-scaling-6-pattern-architecture-2026-05-28.md` § 10.8.9 (Primary EXEMPT discipline)
- `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` (BVV calibration anchor framing)
- `agentic_orchestration/cycle-14-wave-5-season-001/w-alpha-7-plus-phase-4-rerun-3-two-layer-t4-sweep-telemetry.json` (RE-RUN-3 empirical state)

---

## 0. Top-line verdict

**Phase 4 RE-RUN-3 fails 2/5 close criteria at BVV anchor (T2 zero-KPM 19 cells; T4 specialization 14/18 fail). The failure framing R1/R2/R3 surfaced by KR is partially mis-scoped against canonical architecture.** With c-hybrid 2026-05-28 architecture in hand, the correct adjudication is:

- **R1 REJECT** — tunes a SCAFFOLD-Cycle-15-RETIREMENT value on the universal-EXEMPT Primary layer
- **R2 VERIFY-BEFORE-DECIDE** — rocket Pattern-A confirms scope; likely moot under Read B
- **R3 CYCLE 14.5 HOTFIX BLOCKING CLOSE** — gamora forensic on fight-engine timing-floor + BASE under-calibration at boss/mini_boss; player-experience-critical
- **R4 CYCLE 16+ DEFERRAL** — Secondary T4 cohort-relative-peak design-intent canonically deferred to BC axis expansion per c-hybrid § 1.1 (now 5 → 10 candidate axes post-amendment this session)
- **Read B confirmed** — preserve two-layer T4 architecture; drop Secondary T4 specialization metric as Cycle 14 close-criterion gate; Secondary T4 variants ship via strip-and-ship per current generation
- **Close path: Option γ-refined** — Cycle 14 v1 MVP closes on Primary T4 + strip-and-ship Secondary + R3 hotfix complete + canonical capture of Secondary T4 full-design-intent deferral to Cycle 16+

**Critical dissent from KR preliminary read:** KR R1/R2/R3 framing conflated which T4 layer needs to behave better. R1 tunes Primary multiplier — Primary is universal-EXEMPT, so R1 cannot move T4 specialization metric regardless of value. R3 (T2 zero-KPM) is dominant, but it is NOT a T4-layer problem — it is a BASE-damage / fight-engine problem independent of T4 layer choice. Strip-and-ship rescues T4 close-criterion via Primary-EXEMPT but does NOT rescue T2.

---

## 1. Empirical state lock

### 1.1 RE-RUN-3 file verification (framing-audit Q2 — cheapest empirical refutation)

The file at `cycle-14-wave-5-season-001/w-alpha-7-plus-phase-4-rerun-3-two-layer-t4-sweep-telemetry.json` self-identifies as Phase 4 RE-RUN-3:

```
sweep_timestamp:        2026-05-28T22:20:22.756553+00:00 UTC  (= 18:20:22 EDT)
wall_time_s:            76.52
t4_engine_routing_note: "Phase 4 RE-RUN-3: Two-Layer T4 architecture
                         (gandalf v1.17 eb5bd1b + rocket v1.13 1ac272f).
                         PRIMARY T4: DIRECT_DAMAG[E AMPLIFICATION]..."
```

Architecture commits referenced are post-Matt-D1-D6-ratification (`eb5bd1b` = gandalf doc 47 § 4.6 two-layer T4 RATIFIED; `1ac272f` = rocket v1.13 impl). File mtime 18:21 matches sweep timestamp 18:20:22 + 76s wall time.

### 1.2 1.75× DDA multiplier verified active in engine code

```
src/reincarnated/simulation/damage_resolver.py:256
  DIRECT_DAMAGE_AMPLIFICATION_MULTIPLIER: float = 1.75  # SCAFFOLD (Cycle 15 RETIREMENT)
```

Wired through `t4_sim_cycling.py:1033` → `combatant.py:217 + 574` → `damage_resolver.py:248-256` with fight-context injection per `unified_calibration_loop.py:3492`. KR's claim "DDA 1.75× IS firing" empirically confirmed.

### 1.3 Critical metadata finding — the multiplier is SCAFFOLD per Discipline #40

The `# SCAFFOLD (Cycle 15 RETIREMENT)` inline comment explicitly flags 1.75× as scaffold-with-pending-decision per Discipline #40. The team has canonically noted that 1.75× is not the final value and will be retired/refined in Cycle 15. **R1 (tune 1.75× → 2.0×) is tuning a scaffold value mid-Cycle-14 to chase 5/5 pass — exactly the trap Discipline #40 was authored to prevent.**

### 1.4 Two-layer T4 architecture lock — Primary universal-EXEMPT confirmed

Per `canonical/51-investment-scaling-6-pattern-architecture-2026-05-28.md` § 10.8.9 + the RE-RUN-3 `t4_engine_routing_note`:

| Layer | Function | T4 specialization metric applies? |
|---|---|---|
| Primary T4 | DIRECT_DAMAGE_AMPLIFICATION universal 1.75× at preferred_encounter_type | EXEMPT (universal slot) |
| Secondary T4 | Per-kit variants giving cohort-relative peak identity | YES — this is where 14-18/18 fail |

Strip-and-ship 18/18 kits SHIP per Primary EXEMPT closure regardless of Secondary T4 specialization outcome.

---

## 2. Question-by-question — R1/R2/R3/R4 disposition

### R1 — DDA multiplier tune (1.75× → 2.0×): REJECT

**Architecturally moot:**
- R1 touches Primary T4 multiplier; Primary is universal-EXEMPT from T4 specialization metric (doc 51 § 10.8.9). Doubling the multiplier cannot move the T4 metric.
- 1.75× is flagged SCAFFOLD-Cycle-15-RETIREMENT in code per Discipline #40. The team has explicitly committed to retiring the value in Cycle 15. Tuning a scaffold mid-Cycle-14 is Discipline #40 violation.
- The 1.75× × 0 KPM at boss/mini_boss = 0 KPM. R1 does not rescue T2 zero-KPM either.

**KR preliminary read** ("R1 alone won't move the needle") was correct in direction but understated architectural reason. R1 is not just insufficient — it is theater.

### R2 — preferred_encounter_type assignment misalignment: VERIFY-BEFORE-DECIDE

**Open question for rocket Pattern-A query:**

Does `preferred_encounter_type` route Secondary T4 variant SELECTION at generation time, or does it only route Primary DDA TARGETING at simulation time?

| Routing scope | R2 disposition |
|---|---|
| Primary DDA targeting only | **REJECT** — Primary is universal-EXEMPT; R2 cannot move T4 specialization metric |
| Also Secondary T4 selection | **Cycle 14.5 hotfix candidate** — misaligned preferred_encounter_type would route the wrong Secondary T4 variants into cohort positions, suppressing cohort-relative peaks |

**Likely outcome under Read B:** even if R2 routes Secondary T4 selection, with Secondary T4 specialization dropped as close-gate, R2 becomes a Cycle 16+ refinement that composes with BC axis expansion. So R2 reduces to REJECT under Read B unless rocket Pattern-A surfaces an immediate player-experience consequence.

**Dispatch:** rocket Pattern-A query authored by KR in election dispatch.

### R3 — T2 zero-KPM at boss/mini_boss: CYCLE 14.5 HOTFIX BLOCKING CLOSE

**Architecture diagnosis:**

T2 zero-KPM means BASE damage produces 0 KPM at boss_with_adds + mini_boss for multiple kits (str_01 both; dex_01 elite+boss; dex_02 magic+boss+mini; int_05 all four heavy-HP types). This is **independent of T4 layer choice** — it is a BASE-damage / fight-engine architecture problem at high-HP encounters.

**Candidate root causes (for gamora forensic):**

| Sub-cause | Likely fix |
|---|---|
| Case 10 lineage (fight-engine timing-floor) | Fight-engine fight-duration cap is suppressing damage progression at high-HP encounters; raise cap or add HP-aware extension |
| BASE under-calibration for high-HP encounters | BASE damage curves are scaled to mid-HP encounters; under-deliver at high-HP types; per-encounter-class calibration needed |
| Encounter-class HP miscalibration | Boss / mini_boss HP curves are over-tuned vs BASE damage; adjust encounter-class HP rather than damage |
| Combination | Two or more above |

**Player-experience criticality:**

If Cycle 14 closes with T2 unresolved, kits enter boss_with_adds + mini_boss encounters and produce 0 KPM → bosses do not die in any reasonable simulation time. Multiple kits affected at multiple boss-class encounter types. **This is functional-broken-at-boss-content, not "imperfect specialization." Bosses are load-bearing gameplay content in any ARPG — they gate progression and provide combat peaks.**

**Dispatch:** gamora forensic on R3 sub-causes as Cycle 14.5 hotfix. Sequenced as next-dispatch under KR Mode A.

### R4 — Secondary T4 cohort-relative peaks: CYCLE 16+ DEFERRAL

**Architecture diagnosis:**

14-18/18 kits show 0 or 1 peaks in Secondary T4 across encounter types. KR's "co-elevation problem" (cohort median rises in lockstep with DDA-boosted cells; near-miss ratios 1.341 / 1.324 below 1.5× threshold) is correctly observed.

**Why Cycle 16+ deferral is the right disposition:**

- c-hybrid § 1.1 (now amended this session) canonically scopes BC axis expansion to Cycle 16+. The expanded axis set (5 → up to 15 candidates) gives each kit more dimensions for cohort-distinct peaks.
- Pre-expansion fix would commit to a Secondary T4 variant-pool refinement that the Cycle 16 expansion may supersede.
- Under Read B, Secondary T4 testing is dropped as Cycle 14 close-gate; the variants still ship via strip-and-ship; design-intent FULL delivery is canonically deferred.

**Cycle 16 entry-criterion candidate:** at expanded BC axis space, re-run Phase 4 T4 specialization metric across the wider axis set; verify Secondary T4 produces cohort-relative peaks under the expansion.

---

## 3. Per-option assessment — Read A vs Read B + Close-Option α/β/γ

### 3.1 Read A vs Read B (two-layer T4 architecture preservation)

| Read | Operational shape | Pros | Cons |
|---|---|---|---|
| A | Remove Secondary T4 from generation; kits ship Primary only | Simpler v1 MVP; explicit non-promise of Secondary | Rolls back canonically-ratified two-layer architecture (Matt D1-D6 commits `eb5bd1b` + `1ac272f`); strips Secondary T4 richness from player experience |
| **B (LOCKED)** | Preserve two-layer architecture; drop Secondary T4 testing as close-gate | No code rollback; Secondary T4 variants ship via strip-and-ship; design-intent full delivery deferred to Cycle 16 | Risk that v1 MVP players experience Secondary T4 as inconsistent peak signature (cohort-relative peaks not delivered until Cycle 16) |

**Matt elected Read B this session.** Architecturally cleaner; no rollback; richer v1 MVP.

### 3.2 Close-Option α/β/γ disposition

| Option | Shape | Disposition |
|---|---|---|
| α | Close Cycle 14 v1 MVP under amended 3/5 criterion; T4 specialization explicitly deferred to Cycle 16; T2 zero-KPM ALSO deferred | **REJECT** — T2 functional-broken-at-boss-content; cannot ship v1 MVP this way |
| β | Don't close Cycle 14; chase 5/5 PASS via Phase 4 RE-RUN-4+ at current 5-axis architecture | REJECT — chases architecturally-deferred Cycle 16 work mid-Cycle-14 |
| **γ-refined (LOCKED)** | Close Cycle 14 v1 MVP on Primary + strip-and-ship Secondary + R3 hotfix complete; canonical capture: Secondary T4 design-intent deferred to Cycle 16+ per c-hybrid § 1.1 | **ACCEPT** — clean v1 MVP closure; player-experience-functional at boss content; design-intent deferred to canonically-correct scope |

---

## 4. Ranked recommendation — final tier table

| Tier | Item | Disposition |
|---|---|---|
| **Tier 1 (must-fire blocking close)** | R3 — gamora forensic on T2 zero-KPM at boss/mini_boss | Cycle 14.5 hotfix; blocking Cycle 14 v1 MVP close |
| **Tier 2 (verify before retire)** | R2 — rocket Pattern-A query on preferred_encounter_type routing scope | Pattern-A query; ≤30 min; likely retired under Read B |
| **Tier 3 (canonical capture)** | Cycle 14 close-criterion canonical capture | Update doc 47 § 4.6 + doc 51 § 10.8.9 close-gate semantics; explicit Secondary T4 deferral to Cycle 16+ |
| **Tier 4 (operational discipline)** | Discipline #47 candidate — host-RAM-aware operational concurrency | jack-ryan canonical ratification at next QA pass; operate under R47.1-R47.5 immediately |
| **Reserve** | Three-variant naming reconciliation with KR | Verify when KR resumes; reconcile "three-variant" → "three-dimensional / BC axis expansion" if same finding |
| **Reject** | R1 — DDA multiplier tune | Architecturally moot (universal-EXEMPT + SCAFFOLD-Cycle-15-RETIREMENT) |
| **Cycle 16+ deferral** | R4 — Secondary T4 cohort-relative peaks via BC axis expansion | Canonically scoped per c-hybrid § 1.1 (now 10 candidate axes) |

---

## 5. Cycle 14 close-criterion (amended)

**Original Cycle 14 close-criterion:** 5/5 BVV PASS across all profiles.

**Amended Cycle 14 close-criterion (this adjudication):**

| Criterion | Status under amendment |
|---|---|
| T1 — DPS variance | PASS at BVV anchor (1.147×); 4/7 profiles pass; remaining 3/7 inf due to zero-division on one path |
| **T2 — zero-KPM** | **MUST PASS (gates close)** — R3 hotfix delivers this |
| T3 — saturation | PASS structural at BVV; PASS all 7 profiles |
| T4 — specialization (Secondary cohort-relative peaks) | **DROPPED AS GATE** — design-intent canonically deferred to Cycle 16+ BC axis expansion per c-hybrid § 1.1 |
| T5 — floor | PASS 0 violations at BVV; PASS all 7 profiles |

**Effective amended gate: T1 + T2 + T3 + T5 (4/4 required); T4 explicitly deferred.**

Strip-and-ship 18/18 closure remains the v1 MVP shipping mechanism; Primary T4 1.75× DDA universal-guarantee provides the universal-floor uplift at preferred_encounter_type; Secondary T4 variants ship per strip-and-ship pruning without cohort-relative peak gate.

---

## 6. Cycle 16+ deferred-commitments capture

The following items are canonically deferred to Cycle 16+ per this adjudication + c-hybrid § 1.1 (amended this session):

1. **BC axis expansion** — 5 current axes + up to 10 candidate axes (5 from original c-hybrid + 5 added this session: `damage_element_profile`, `ailment_profile`, `hit_dodge_economy`, `movement_profile`, `proxy_summon_possession_split`); legolas Mode A consultation per Discipline #18 winnows to commit set.
2. **Secondary T4 cohort-relative peak delivery** — at expanded BC axis space; re-run Phase 4 T4 specialization metric to verify peak delivery.
3. **DDA multiplier formal value** — 1.75× SCAFFOLD retired; new value derived from three-dimensional BC space empirical data.
4. **R2 preferred_encounter_type expansion** — under expanded axis space, may compose with multiple BC axes for richer encounter-class routing.
5. **Layer 2-derived velocity granularity instrumentation** — Loot velocity / Clear velocity / Movement velocity per c-hybrid § 1.3 amendment this session.

**Empirical-validation criterion for Cycle 16 entry:** legolas Mode A consultation surfaces substrate signal-to-noise per candidate axis; commit set determined before Cycle 16 wave authoring fires.

---

## 7. Sign-off

**Adjudication authority:** Matt 2026-05-28 (this Pattern B session — Read B locked; T4 specialization gate dropped; R3 hotfix blocking close acknowledged; c-hybrid § 1.1 + § 1.3 canonical amendments authorized).

**KR election:** the next-dispatch sequence flows from this adjudication via the KR election prompt drafted this session. KR enters Mode A hive-mind for Cycle 14 remainder; surfaces back to Matt at gates only (critique-pair, wave boundaries, scope-amendments, framing-audit findings, Cycle 14 close).

**Operational constraints:** R47.1-R47.5 (Discipline #47 candidate) active immediately; jack-ryan canonical-write at next QA pass.

**Discipline composition:**
- § 3.4 recognition-validate-commit: recognition (RE-RUN-3 partial-fail) → empirical validation (this adjudication) → commit (KR election dispatch)
- § 4.1 framing-audit checklist: Q1 (load-bearing framings = "Primary is universal-EXEMPT" + "Secondary T4 metric IS the cohort-peak measure"); Q2 (cheapest empirical refutation — RE-RUN-3 file verification + code grep — fired in ~120 sec); Q3 (refinement of R1/R2/R3 framing landed BEFORE downstream dispatch fired against KR's preliminary scoping)
- Discipline #40 — scaffold-value flagging caught R1 architectural mootness via in-code `# SCAFFOLD (Cycle 15 RETIREMENT)` comment

**Signed:** gandalf (story-and-design steward)
**For:** the locked R1/R2/R3/R4 disposition + Read B confirmation + Cycle 14 close-criterion amendment + Cycle 16+ deferred-commitments capture, anchoring KR's Mode A hive-mind orchestration for Cycle 14 remainder.
