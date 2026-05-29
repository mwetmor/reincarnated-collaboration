# DISPATCH — Rocket Cycle 14 A2-1 Step 4 (A2-1 RE-FIRE Production Cascade — Post Step 1 KPM Recalibration + Step 2 FACTION_VISIBILITY Flip)

**Authored:** 2026-05-29 (Mode A Phase A2 cascade RESUMPTION; resolution plan § 1 Step 4)
**Author:** knight-rider (Cycle 14 Mode A hive-mind orchestrator)
**Recipient:** rocket (kit emission primary; orchestration lead) + star-lord in-process (LLM cost guard $50 soft cap; surfaces at projection approach) + gamora in-process (simulation; phase7_bridge + ENCOUNTER_COHORT_KPM_BAND)
**Pattern:** Pattern B sustained-execution (full production cascade Phase 2-7 with REAL LLM calls); ~1d wall-clock per resolution plan § 1 Step 4
**Expected effort:** ~few hours to ~1d wall-clock (prior A2-1 RE-FIRE INTERIM ran in 25.1s sans LLM; this fires REAL Wave A + F-C + Wave B LLM; expect ~10-60 min pipeline wall + LLM phase time)
**Status:** PENDING — fires on receipt
**Authority:** Matt 2026-05-28 Phase A2 cascade authorization (Gate (a) + Gate (b) $50 soft cap + Gate (c) A2-1→A2-7 CONFIRMED) + Matt 2026-05-29 resolution plan § 1 Step 4 ratification (Step 3 jack-ryan PASS-with-INFO cleared Step 4 fire) + Pattern E pre-authorization for A2-2 Gate-2 post this dispatch + hive-mind decision-routing + R48.4 single-seam (jack-ryan released post Step 3 PASS-with-INFO; rocket+star-lord+gamora in-process orchestration)

---

## 0. CONTEXT (read first — 3 min)

### 0.1 Cascade-resumption lineage (full Step 1 → Step 4 chain)

| # | Dispatch / event | Status |
|---|---|---|
| A2-1 (INTERIM) | `2026-05-29-rocket-cycle-14-wave-5-season-001-production-fire.md` | ❌ INTERIM FAIL (0/18 emit; cross-seam import bug blocked Phase 7) — collab `26d4baa` |
| A2-1-FIX | `2026-05-29-gamora-cycle-14-a2-1-fix-phase7-bridge-import.md` | ✅ CLOSED (phase7_bridge absolute imports + quality-vector ID fix) — engine `b0ed9fd` + tag `gamora/v2.12-a2-1-fix-phase7-bridge-imports-1` |
| A2-1 (RE-FIRE attempt 1) | `2026-05-29-rocket-cycle-14-a2-1-refire-post-phase7-bridge-fix.md` | ❌ MATERIAL FAIL (Concern #1 KPM gap + Concern #2 Phase 5 placeholder) — collab `9f9ed28` + engine `c8586e4` |
| Resolution plan ratification | Matt in-session 2026-05-29 | Path A + Path D ratified |
| A2-1 Step 1 (gamora KPM recalibration) | `2026-05-29-gamora-cycle-14-a2-1-step-1-synthetic-kit-kpm-recalibration.md` | ✅ COMPLETE — 18/18 PASS per-bc_cell_id table; engine `8715f10` + tag `gamora/v2.13-a2-1-step-1-synthetic-kit-kpm-recalibration-1` |
| A2-1 Step 2 (rocket FACTION_VISIBILITY flip) | `2026-05-29-rocket-cycle-14-a2-1-step-2-faction-visibility-flip.md` | ✅ COMPLETE — all 5 edits + Disc #11 audit clean; engine `5d69291` + tag `rocket/v1.1-a2-1-step-2-faction-visibility-visible-1` |
| A2-1 Step 3 (jack-ryan Gate-2 Pattern E) | `2026-05-29-jack-ryan-cycle-14-a2-1-step-3-gate-2-pattern-e-review.md` | ✅ PASS-with-INFO — 3 INFOs all deferred per resolution plan § 4; cascade fires; collab `b22cc79` |
| **A2-1 Step 4 (THIS DISPATCH — A2-1 RE-FIRE attempt 2)** | this dispatch | ⏳ PENDING — production cascade fire with BOTH fixes applied |

### 0.2 What Step 1 + Step 2 + Step 3 deliver to Step 4 (KR-verified)

**Step 1 architectural precondition:** Phase7SyntheticKit now uses per-bc_cell_id magnitude table (18 entries; 60k-254k range; fallback 100k). Sweep PROVED 18/18 in-band coverage at W-α6 ENCOUNTER_COHORT_KPM_BAND. Expected Step 4 Phase 7 mechanical gate: synthetic kits PASS T1 gauntlet at the bc_cell-assigned (enc_type, cohort) cells.

**Step 2 architectural precondition:** `FACTION_VISIBILITY="visible"` at orchestrator → `should_fire_wave_a()` returns True → Wave A (faction LLM) + F-C (inter-faction relationships) + Wave B (per-kit identity LLM) ALL FIRE. Expected Step 4 Phase 5: real LLM-generated `ExportFactionCluster` records with `faction_label_canonical`; real `ExportFactionRelationship` records; real `cohesion_judge_confidence` scores fed to Phase 7 cohesion gate.

**Step 3 Gate-2 PASS-with-INFO disposition:** cascade fires. Pattern E pre-authorization invoked. 3 INFOs are deferred:
- INFO-1: calibration scope residual (synthetic-kit single-skill vs full-kit band derivation; resolved architecturally via viable_cohorts filtering at math note § 3); carry-forward to A2-6
- INFO-2: consumer-side default at `phase5_orchestrator.py:193` still "invisible" (benign — orchestrator overrides at line 835); defer to Matt re-engage per resolution plan § 4
- INFO-3: Disc #40 + Disc #42a Instance-5 deferred per resolution plan § 4

### 0.3 What this dispatch fires

**Re-fire the SAME Wave 5 season_001 PRODUCTION cascade as the prior A2-1 RE-FIRE attempt 1, with BOTH Step 1 + Step 2 fixes applied.** Engine HEAD at `3b69dad` (post-Step-2); production pipeline now expected functional through Phase 7 with REAL LLM cohesion judge exercised.

Pipeline (engine `~/Games/reincarnated-engine/`; same orchestration as prior A2-1 RE-FIRE attempt 1):

1. **Phase 2** — kit candidate generation (12 skills × 3 chains × 4 tiers; substrate weapon binding per SC-6b enrichment)
2. **Phase 3** — gauntlet simulation (R3-prime band lower-bound + T1 base-context amendment active; quality-vector derivation meaningful post bundled fix from A2-1-FIX)
3. **Phase 4** — archive insertion to `kit_archive.db`
4. **Phase 5** — **cohesion judge LLM FIRES FOR REAL** (Wave A + F-C + Wave B per Step 2 flag flip; star-lord cost guard enforces $50 soft cap projection)
5. **Phase 7** — acceptance gate (≥12/18 kits emit threshold; **synthetic_kit KPM in-band** per Step 1 per-bc_cell_id table; cohesion_judge_confidence ≥ 0.75 threshold per scaffold-current Phase 7 gate)

### 0.4 Disc #42a framing-audit at dispatch consumption

KR's authoring applied Q1-Q6. Rocket should re-apply at consumption:

- **Q1 — load-bearing framing assumption:** "Step 1 (per-bc_cell_id magnitude table) + Step 2 (FACTION_VISIBILITY=visible) are the two architectural preconditions sufficient for A2-1 RE-FIRE to produce ≥12/18 emit AFTER real-LLM cohesion judge exclusions at the W-α6-calibrated Phase 7 acceptance gate; D9 ratified close-criterion intended to measure this."
- **Q2 — refutation evidence in scope:** Step 4 production cascade IS the refutation evidence; observed Phase 7 emit count + LLM exclusion count + cohesion judge confidence distribution + LLM cost cumulative
- **Q3 — refutation surface-able cheaply:** yes — full pipeline ~10-60 min wall-clock; LLM cost expected ~$5-20 (first production fire establishes empirical baseline)
- **Q4 — measurement context match:** Step 4 fires the full production cascade with Step 1 + Step 2 architectural fixes active; the gate is calibrated against D9 ratified close-criterion (≥12/18 per-season)
- **Q5 — calibration scope match:** synthetic-kit in-band coverage proved at Step 1 sweep matches the calibration scope (per-bc_cell_id viable_cohorts); Step 4 verifies empirically end-to-end
- **Q6 — semantic stability of "≥12/18 emit at Phase 7 acceptance":** ≥12/18 IS the D9 ratified criterion AFTER LLM exclusions. Phase 3 13/18 WR-bracket PASS is informational PROXY only. Rocket attestation in completion record MUST cite Phase 7 result (not Phase 3 proxy) for the architectural validation claim. **Q6 vigilance flag forward** (per prior A2-1 RE-FIRE attempt 1 attestation-discipline pattern).

If any framing refutes, SURFACE TO KR before pipeline fire.

### 0.5 Disc #40 cohesion-threshold WARN-watch (capture-and-watch per resolution plan § 3)

Phase 7 cohesion gate threshold `cohesion_judge_confidence >= 0.75` is scaffold-calibrated (NEVER empirically validated against real LLM scores; this is the FIRST production fire that produces real scores). Star-lord telemetry must capture per-kit `cohesion_judge_confidence` distribution.

**Surface protocol (per resolution plan § 3):**
- Systematic under-0.75 pattern observed across A2-1 RE-FIRE kits → SURFACE TO KR via interim completion-record append (Pattern B design call for Matt re-engage; do NOT halt cascade for scattered under-0.75)
- Scattered under-0.75 (a few kits below threshold) → capture-and-watch; treat as scaffold-discovery; do NOT escalate
- All scores above 0.75 → clean signal; capture as baseline data point

### 0.6 D13 parallel-fire authorization activates POST A2-2 (NOT this Step 4)

Per resolution plan § 1.5: D13 P1-P9 parallel-fire activates AFTER A2-2 (jack-ryan Gate-2 PASS on this Step 4 produces season_001 PASS). Step 4 itself fires under R48.4 single-seam — rocket+star-lord+gamora in-process orchestration is NOT parallel sub-agent fan-out; it's one rocket-led pipeline with in-process dependencies.

---

## 1. THE TASK

**Re-fire Wave 5 season_001 PRODUCTION cascade end-to-end against current engine state (HEAD at `3b69dad`). Both Step 1 KPM recalibration + Step 2 FACTION_VISIBILITY flip MUST be active in the pipeline.**

### 1.1 Pre-flight (REQUIRED before pipeline fire)

1. **Disc #48 R48.5 vm_stat check:** confirm > 1 GB free + reclaimable (KR pre-flight at Step 4 entry showed ~2.83 GB available; production cascade is heavier — verify still holds at the moment of fire)
2. **Disc #48 R48.4 single-seam confirm:** jack-ryan sub-agent released post Step 3 PASS-with-INFO; rocket+star-lord+gamora in-process pipeline (NOT parallel sub-agents)
3. **Engine state confirm:** HEAD at `3b69dad` (rocket Step 2 AGENT_STATE checkpoint); Step 1 + Step 2 commits + tags intact:
   - `8715f10` gamora Step 1 (PHASE7_SYNTHETIC_KIT_MAGNITUDE_TABLE 18-entry + assert + fallback at phase7_bridge.py:129-162; magnitude lookup at line 251)
   - `685b362` gamora Step 1 AGENT_STATE
   - `5d69291` rocket Step 2 (FACTION_VISIBILITY="visible" at line 89; assert updated at 1264-1265)
   - `3b69dad` rocket Step 2 AGENT_STATE
4. **Verify both fixes landed:**
   - `python3 -c "from reincarnated.simulation.phase7_bridge import PHASE7_SYNTHETIC_KIT_MAGNITUDE_TABLE; assert len(PHASE7_SYNTHETIC_KIT_MAGNITUDE_TABLE) == 18; print('Step 1 smoke PASS: ' + str(len(PHASE7_SYNTHETIC_KIT_MAGNITUDE_TABLE)) + ' entries')"`
   - `python3 -c "from reincarnated.simulation.wave5_season_orchestrator import FACTION_VISIBILITY; assert FACTION_VISIBILITY == 'visible'; print('Step 2 smoke PASS: FACTION_VISIBILITY = ' + FACTION_VISIBILITY)"`
5. **Star-lord LLM cost guard active:** verify cost-tracking wired + projects against $50 soft cap (this re-fire IS the FIRST real LLM spend; pay attention to per-call cost capture)
6. **Prior A2-1 RE-FIRE attempt 1 phase outputs:** existing `phase2_*` / `phase3_*` / `phase4_*` / `phase5_*` / `phase7_*` JSONs in season-001 dir are from the FAIL run (committed `9f9ed28`). Rocket's call: archive to subdir (e.g., `a2-1-refire-1-fail-pre-step1-step2/`) for clarity, OR overwrite (FAIL state preserved in git history regardless)
7. **kit_archive.db:** present at `cycle-14-wave-5-season-001/kit_archive.db`. A2-1 RE-FIRE attempt 1 added 18 ACCEPTED kits. Rocket's call: clear and re-populate (recommended for clean re-fire) OR append (complicates A2-2 Gate-2 review; recommend clear-and-re-populate)

### 1.2 Pipeline fire

Run the full season_001 production pipeline (same orchestration as prior A2-1 RE-FIRE attempt 1):
- Phase 2 → kit candidate gen
- Phase 3 → gauntlet sim (quality vectors meaningful post bundled fix)
- Phase 4 → archive insert
- Phase 5 → **cohesion judge LLM CALLS FIRE FOR REAL (Wave A + F-C + Wave B; star-lord cost guard projects + emits)**
- Phase 7 → acceptance gate (synthetic_kit KPM in-band per Step 1 per-bc_cell_id table; cohesion_judge_confidence ≥ 0.75 per scaffold threshold)

**LLM cost guard surface conditions (star-lord in-process):**
- Track per-LLM-call cost cumulative across season_001
- Project cumulative cost for season_001 + extrapolate to 3-season cascade
- **If projected approach hits $50 across all 3 seasons → SURFACE TO KR via interim completion-record append** (cascade decision: continue / pause / Matt cap-extension)
- **Hard-halt threshold:** projected > $60 (20% overshoot) → halt cascade + SURFACE IMMEDIATELY

This is the FIRST production fire that meaningfully spends LLM budget. The cost projection captured at A2-1 RE-FIRE attempt 2 close becomes the EMPIRICAL baseline for 3-season cascade projection accuracy.

**Cohesion-threshold WARN-watch (per resolution plan § 3; Disc #40 capture-and-watch):**
- Capture per-kit `cohesion_judge_confidence` score distribution in Phase 7 verdict log
- Surface to KR IF systematic under-0.75 pattern observed (NOT scattered) → Pattern B design call deferred to Matt re-engage; do NOT halt cascade

### 1.3 Output telemetry

Same shape as prior A2-1 RE-FIRE attempt 1 (per § 1.3 of that dispatch). Phase 5 cohesion-judge LLM telemetry per SC-3 PRIMARY (Structured Output with Layer Tags). Cross-Character Diversity Audit per SC-3 DETECTION (informational). Phase 7 verdict log captures per-kit cohesion_judge_confidence distribution.

Required telemetry artifacts (mirrors prior A2-1 RE-FIRE attempt 1 paths):
- `agentic_orchestration/cycle-14-wave-5-season-001/phase2_kit_candidates.json` (overwrite OR archive prior)
- `agentic_orchestration/cycle-14-wave-5-season-001/phase3_gauntlet_results.json`
- `agentic_orchestration/cycle-14-wave-5-season-001/phase3_pm1_clustering.json`
- `agentic_orchestration/cycle-14-wave-5-season-001/phase3_quality_vectors.json`
- `agentic_orchestration/cycle-14-wave-5-season-001/phase4_archive_insertion.json`
- `agentic_orchestration/cycle-14-wave-5-season-001/phase5_faction_clusters.json` (now LLM-derived, not placeholder)
- `agentic_orchestration/cycle-14-wave-5-season-001/phase5_faction_relationships.json` (now populated, not empty)
- `agentic_orchestration/cycle-14-wave-5-season-001/phase7_season_summary.json` (target ≥12/18 shipped_worthy)
- `agentic_orchestration/cycle-14-wave-5-season-001/season_summary.json`
- `agentic_orchestration/cycle-14-wave-5-season-001/kit_archive.db` (cleared + re-populated)
- Prior A2-1 RE-FIRE attempt 1 outputs archived to `a2-1-refire-1-fail-pre-step1-step2/` subdir (rocket's call on naming)

### 1.4 Acceptance criterion (D9 ratified per-season; resolution plan § 1 Step 4)

- ✅ **≥12/18 kits emit** at Phase 7 acceptance (THIS IS THE D9 RATIFIED THRESHOLD)
- ✅ Phase 7 emit count explicitly cited (NOT Phase 3 13/18 proxy) — Disc #42a Q6 vigilance flag forward
- ✅ Phase 5 cohesion judge LLM exclusion count explicitly cited
- ✅ Phase 5 ExportFactionCluster + ExportFactionRelationship records populated with REAL LLM output (not placeholders)
- ✅ LLM cost cumulative captured + extrapolation to 3-season projection (within $50 soft cap)
- ✅ Per-kit `cohesion_judge_confidence` distribution captured in Phase 7 verdict log
- ✅ Disc #11 grep `synthetic_mode` ZERO functional code (re-verify; sanity from Step 1 + Step 2 work intact)
- ✅ Cross-seam round-trip (production cascade IS the round-trip)
- ✅ Tag: `rocket/v1.2-a2-1-refire-2-season-001-{pass|fail}-{emit_count}` (or seam convention; emit count in tag for clarity)
- ✅ Auto-commit per CLAUDE.md addendum 2026-05-25
- ✅ Do NOT push — KR fires push after Step 5 A2-2 Gate-2 PASS per per-workstream pattern

### 1.5 Completion-record format (append to this dispatch)

Append a `## Completion record` section with:

1. **VERDICT** — single line: "A2-1 RE-FIRE attempt 2 season_001 production ≥12/18 emit at Phase 7 acceptance — PASS (Phase 7 emit count: X/18; LLM exclusions: Y; LLM cost: $Z)" OR "FAIL with diagnosis + framing-audit Q1/Q2/Q3 applied"
2. **Phase 7 emit count** — explicit X/18 figure (D9 ratified validation gate)
3. **Phase 5 LLM cohesion judge** — per-kit cohesion verdict (PASS / EXCLUDED + reasoning excerpts); total LLM cost; cost projection to 3-season
4. **Phase 5 Wave A + F-C + Wave B exercised** — ExportFactionCluster + ExportFactionRelationship counts; LLM-derived labels samples; INFO-2 consumer-side default did NOT block exercise (confirms benign disposition)
5. **Per-kit cohesion_judge_confidence distribution** — score table or histogram; WARN-watch surface if systematic under-0.75
6. **Phase 3 gauntlet sim** — informational proxy (WR-bracket PASS count + quality-vector distribution)
7. **Synthetic-kit Phase 7 KPM coverage** — per-kit observed KPM vs ENCOUNTER_COHORT_KPM_BAND (confirms Step 1 architecture empirically end-to-end)
8. **AI-tell detection sub-audit** — Cross-Character Diversity per SC-3 DETECTION
9. **Disc #11 grep verification** — `synthetic_mode` ZERO functional code (re-confirm)
10. **Telemetry output paths** — all written JSON files + archived prior outputs subdir
11. **Engine + collab commits + tag** — rocket commits + tag with emit count
12. **Disc #42a framing-audit self-verification** — Q1-Q6 at completion (meta-observation 5; verify artifact against report)
13. **Disc #42a Q6 vigilance forward** — confirm attestation cites Phase 7 result (not Phase 3 proxy)
14. **Star-lord LLM cost guard report** — per-Phase cost breakdown + 3-season projection + $50 soft cap status
15. **Any anomalies surfaced** during pipeline fire

---

## 2. CROSS-SEAM CONTRACT CHANGE? (Principle 6)

**No** — production cascade fire; no code change. Cross-seam round-trip: rocket → gamora → star-lord → phase7 (synthetic kit construction at phase7_bridge consumed by gauntlet_sim).

---

## 3. QUALITY CRITERION (KR OP § 3.11)

**Game-quality goal:** empirically validate Cycle 14 v1 architecture at the Phase 7 acceptance layer (post-LLM cohesion judge) AND establish empirical LLM cost baseline for 3-season cascade projection. This is the FIRST production fire that exercises the full cascade through real LLM cohesion judge AND phase 7 emit acceptance under W-α6-calibrated KPM bands + per-bc_cell_id synthetic kit magnitudes — the architectural validation gate Cycle 14 v1 was designed to satisfy.

**Refutation conditions:**
- Phase 7 emit < 12/18 — refute = full pipeline re-fire produces empirical signal; Step 1 + Step 2 fixes empirically verified by Step 3 jack-ryan Gate-2; FAIL would surface a THIRD architectural concern distinct from Concerns #1 + #2 → SURFACE IMMEDIATELY per resolution plan § 3 A2-1 RE-FIRE second-material-fail clause (Matt election; no re-fire loop)
- LLM cost > $60 hard-halt → SURFACE IMMEDIATELY + halt
- LLM cost projection toward $50 across 3 seasons → SURFACE for Matt cap-extension election
- Cohesion-threshold systematic under-0.75 pattern → SURFACE for Pattern B design call (do NOT halt cascade)
- Dispatch framing pre-commits to a decision Matt has not ratified — NO (Step 4 fires per resolution plan § 1 Step 4 + Step 3 PASS unblock)

If any refutation condition triggers, SURFACE TO KR before continuing.

---

## 4. OUT OF SCOPE

- ❌ Any engine code change (Step 1 + Step 2 architecture is locked; this is re-fire of fixed code)
- ❌ Path α architectural amendment
- ❌ Two-layer T4 architectural amendment
- ❌ Cycle 16+ BC axis expansion impl
- ❌ Doc 48 class-roster A/B comparison execution (A2-5 scope; gandalf)
- ❌ Disciplines #41/#44/#45/#46 batched canonical-write (A2-6 scope; jack-ryan)
- ❌ Cross-season (A2-3/A2-4) production fire (this is season_001 only; A2-3 + A2-4 fire after A2-2 PASS)
- ❌ Jack-ryan Gate-2 review (A2-2; fires after this dispatch closes; Pattern E pre-authorized)
- ❌ Matt v1 tag ratification (A2-7)
- ❌ Phase 7 cohesion-judge-threshold recalibration (scaffold-flag; capture-and-watch only)
- ❌ FACTION_VISIBILITY re-amendment (Step 2 locked Cycle 14 v1 default)
- ❌ Phase7SyntheticKit magnitude re-amendment (Step 1 per-bc_cell_id table locked)
- ❌ ENCOUNTER_COHORT_KPM_BAND amendment (W-α6 canonical authority preserved)
- ❌ Player-facing faction-architecture commitments (deferred recognition record stands)
- ❌ Disc #42a Instance-5 + Disc #40 canonical writes (deferred to Matt re-engage)
- ❌ Decisions-log canonical writes (jack-ryan owns; deferred)
- ❌ Pushing without KR coordination
- ❌ Parallel sub-agent fan-out under R48.4 (rocket+star-lord+gamora in-process pipeline IS R48.4-compliant)
- ❌ D13 P1-P9 parallel-fire (activates POST A2-2; not this Step 4)

---

## 5. RISKS + COMPLICATIONS

- **LLM cost projection accuracy:** this is the first run that meaningfully spends LLM budget. The cost-per-season projection is OBSERVED here; extrapolation to 3-season may surface the $50 cap concern. If season_001 alone costs > $17 (1/3 of cap), 3-season is at risk. Star-lord cost guard surfaces at projection approach.
- **Phase 5 LLM verdict-vs-AI-tell tradeoff (untested at production scale):** SC-3 PRIMARY Pattern B Structured Output with Layer Tags has been research-validated but NOT exercised at production scale in this seam. May surface LLM-call-failure modes or unexpected exclusion patterns.
- **Phase 7 emit < 12/18 even with both fixes:** if LLM exclusions are aggressive (e.g., 7-8 exclusions) OR cohesion_judge_confidence systematically below threshold, Phase 7 could fall below 12/18. SURFACE IMMEDIATELY with diagnosis (resolution plan § 3 second-material-fail clause; routes to Matt without re-fire loop).
- **Cohesion threshold scaffold pressure:** the 0.75 threshold is scaffold-calibrated; first empirical data point produced here. Capture-and-watch per resolution plan § 3.
- **Phase 3 WR-bracket regression post Step 1/2:** Step 1 changes phase7_bridge (synthetic kit construction); Step 2 changes orchestrator flag (Phase 5 invocation). Neither touches Phase 3 gauntlet sim. WR-bracket count expected stable at 13/18. If it shifts, surface (would indicate test-coverage gap).
- **Disc #48 R48.5 mid-run RAM pressure:** if vm_stat < 500 MB available mid-run, pause + SURFACE. Production cascade is heavier than Step 1/2/3; watch RAM closely.
- **Disc #42a Q6 attestation discipline:** rocket MUST cite Phase 7 result (not Phase 3 proxy) for architectural validation claim. Self-audit at completion record authoring (per prior A2-1 RE-FIRE attempt 1 attestation pattern).

---

## 6. URGENCY + SEQUENCING

**Fires under R48.4 single-seam (rocket+star-lord+gamora in-process orchestration; jack-ryan released post Step 3).** Step 5 (jack-ryan + gandalf Pattern E autonomous Gate-2 = A2-2) fires AFTER this dispatch closes.

Per resolution plan § 2: total wall-clock estimate to A2-1 RE-FIRE PASS is ~1d production. Cumulative through Step 4 close: ~1d + 3h. Cascade then proceeds to A2-2 → A2-3 (season_002) → A2-4 (season_003) → A2-5 (A/B) → A2-6 (disciplines batch) → A2-7 (Matt v1 tag).

A2-1 RE-FIRE attempt 2 PASS → KR fires A2-2 (jack-ryan + gandalf Pattern E autonomous-pair Gate-2 on season_001 production output).

A2-1 RE-FIRE attempt 2 FAIL → SURFACE IMMEDIATELY per resolution plan § 3 second-material-fail clause (Matt election; no re-fire loop).

---

## 7. SURFACING-TO-KR PROTOCOL

Append completion record (interim OR final) at any of:

- ✅ Season_001 ≥12/18 emit at Phase 7 + LLM cost within season-budget → normal close (KR fires A2-2)
- 🚨 Phase 7 emit < 12/18 → SURFACE IMMEDIATELY per resolution plan § 3 second-material-fail clause (Matt election; no re-fire loop)
- 🚨 LLM cost projection approach $50 cumulative across 3 seasons → SURFACE for Matt cap-extension election
- 🚨 LLM cost hard-halt $60 overshoot → SURFACE IMMEDIATELY + halt
- ⚠️ Cohesion-threshold systematic under-0.75 pattern → SURFACE for Pattern B design call (do NOT halt cascade; INFO-class)
- ⚠️ Disc #11 grep returns `synthetic_mode` functional code → SURFACE IMMEDIATELY (regression from Step 1/2)
- ⚠️ Disc #48 R48.5 mid-run RAM pressure (< 500 MB) → pause + SURFACE
- ⚠️ Disc #42a framing-audit refutes pre-imposed assumption → SURFACE IMMEDIATELY before continuing
- 🚨 Substantial unexpected failure mode → SURFACE IMMEDIATELY

---

## 8. REFERENCES

- `agentic_orchestration/gandalf/notes/2026-05-29-concern-1-and-2-resolution-plan.md` § 1 Step 4 + § 3 surface conditions
- `agentic_orchestration/dispatches/2026-05-29-gamora-cycle-14-a2-1-step-1-synthetic-kit-kpm-recalibration.md` § Completion record (Step 1 architectural precondition)
- `agentic_orchestration/dispatches/2026-05-29-rocket-cycle-14-a2-1-step-2-faction-visibility-flip.md` § Completion record (Step 2 architectural precondition)
- `agentic_orchestration/dispatches/2026-05-29-jack-ryan-cycle-14-a2-1-step-3-gate-2-pattern-e-review.md` § Completion record (Step 3 Pattern E PASS-with-INFO)
- `agentic_orchestration/qa/pending/2026-05-29-a2-1-step-3-gate-2-pattern-e-step-1-plus-step-2-review.md` — Step 3 finding-file (3 INFOs deferred)
- `agentic_orchestration/dispatches/2026-05-29-rocket-cycle-14-a2-1-refire-post-phase7-bridge-fix.md` — prior A2-1 RE-FIRE attempt 1 FAIL (pattern reference for this dispatch's structure; FAIL record for archival)
- `agentic_orchestration/cycle-14-path-alpha-v1-closure-record-2026-05-28.md` — Phase A1 closure record + Pattern E pre-authorization
- `agentic_orchestration/cycle-14-hive-mind-state.md` — Wave 5 state (cascade resumption in-flight; Step 4 firing)
- `agentic_orchestration/research/2026-05-27-cycle-14-sc-3-cohesion-judge-llm-architecture.md` — SC-3 PRIMARY pattern + DETECTION
- `~/Games/reincarnated-engine/src/reincarnated/simulation/phase7_bridge.py` — Step 1 impl (PHASE7_SYNTHETIC_KIT_MAGNITUDE_TABLE)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/wave5_season_orchestrator.py` — Step 2 impl (FACTION_VISIBILITY="visible")
- `~/Games/reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py:206` — ENCOUNTER_COHORT_KPM_BAND
- `~/Games/reincarnated-engine/src/reincarnated/llm/phase5_orchestrator.py` — Phase 5 LLM consumer
- `~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` § v1.57 — Step 1 migration record
- `~/Games/reincarnated-engine/design/decisions/decisions-log.md` line 3536 — D9 ratified close-criterion LOCKED
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disc #11/#18/#21/#22/#39/#40/#42a/#43/#48 active
- Engine HEAD: `3b69dad` (rocket Step 2 AGENT_STATE); Step 1 + Step 2 tags both intact

---

**KR signature:** authored per Phase A2 cascade RESUMPTION authorization + Step 3 PASS-with-INFO Pattern E fire-and-continue + R48.4 single-seam (jack-ryan released post Step 3; rocket+star-lord+gamora in-process pipeline) + Disc #42a meta-observation 5 self-vigilance (Step 1 + Step 2 + Step 3 work-products verified at engine HEAD `3b69dad`; Step 3 finding-file at qa/pending/ 26,888 bytes verified on-disk; Pattern E PASS-with-INFO disposition explicit) + auto-commit per CLAUDE.md addendum 2026-05-25 + Disc #42a Q6 vigilance flag forward (attestation MUST cite Phase 7 result, not Phase 3 proxy; per prior A2-1 RE-FIRE attempt 1 attestation-discipline pattern).

This dispatch is the cheapest empirical refutation of "do Step 1 (per-bc_cell_id magnitude table) + Step 2 (FACTION_VISIBILITY=visible) together unblock A2-1 RE-FIRE to produce ≥12/18 emit at Phase 7 acceptance AFTER real-LLM cohesion judge exclusions under D9 ratified close-criterion?" — re-fire of season_001 production cascade with both fixes landed (~10-60 min wall + LLM phase; first real LLM spend establishes empirical baseline for 3-season cascade projection).

A2-1 RE-FIRE attempt 2 PASS = Cycle 14 v1 architecture empirically validated at Phase 7 acceptance layer + unblocks A2-2 Gate-2 (Pattern E autonomous critique-pair = jack-ryan + gandalf) → cascade continues through A2-3 + A2-4 + A2-5 + A2-6 toward A2-7 Matt v1 tag ratification.
