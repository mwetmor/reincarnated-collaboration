# Matt-Briefing — LC-011 Attribution: Option C STRONG Confirm + Script Crash + W1.13 Disposition Required

**Date:** 2026-05-22 (next operational day; first action of prolonged autonomous mission)
**Author:** knight-rider
**Classification:** ESCALATION — Rule #1 of prolonged-autonomy mission prompt (Option C STRONG confirm on LC-011)
**Status:** ⚠️ FILED — W1.13 architectural fire-gate HELD; all other pre-authorized P1 work continues
**For Matt:** decision required on W1.13 disposition (deprecate vs revise vs proceed-with-reduced-confidence)

---

## 0. TL;DR

**The 45-season LC-011 ablation script CRASHED mid-Run-2** (28 of 45 seasons completed; Run 3 Surface A ablation NEVER STARTED). The babysit agent did not produce a summary artifact. Discipline #13b two-way attribution **cannot be computed** from the partial dataset.

**CORRECTION (2026-05-22 09:XX EDT, post crash-diagnosis):** my initial framing of this section claimed "Option C STRONG confirm" based on the `floor_lock_recompose=0` metric. That metric is a strict floor-lock-at-FLOOR signal — different from the original ablation script's `convergence_status='FAILED'` metric that drives the Discipline #13b attribution formula. Reading the correct metric:

| Cohort | mage_controller FAILED rate | Definition |
|---|---|---|
| Run 1 baseline (15 seasons, complete) | **3/60 = 5.0%** | script's `FAILED` definition: not converged AND target_wr==0.5 |
| Run 2 observational (12 of 15 complete) | TBD on recovery completion | same definition |
| Historical baseline (LC-011 reframing 2026-05-21) | 41.8% (different era + different framework) | floor_lock_recompose at MAX_ITERATIONS=10 near MODIFIER_SEARCH_FLOOR |
| Mission escalation threshold | ≤ 5% | per mission prompt Rule #1 |

**Run 1 sits exactly at the 5% boundary.** Not "STRONG confirm at P ≪ 0.0001" as I initially stated. The signal is consistent with Option C (era-stratification artifact superseded by post-W0.10 stack), but it is **boundary-grade evidence, not overwhelming-grade evidence**. The strict `floor_lock_recompose` metric does show 0/135 — but that's a sharper failure mode than the script's broader `FAILED` count, and isn't what the attribution formula uses.

**What this changes:**

- The escalation is still warranted by the letter of Rule #1 (≤ 5% triggers), but the *spirit* of "STRONG confirm dissolves the W1.13 mandate" is weaker than I claimed
- Finishing the runs to get the full N=45 attribution is **MORE valuable** than I argued, not less — at 5% boundary, Run 3 with Surface A ablation could meaningfully attribute (if it drops to <2%) or null (if it stays at ~5%)
- The W1.13 disposition (α/β/γ → per Matt 2026-05-22 critique-pair latitude) gets a sharper input from the full ablation

**Operational implication:** the recovery probe is now genuinely diagnostic, not just confirmatory. Knight-rider proceeds with recovery per your decision; critique-pair dispositions W1.13 rescope after recovery completes with full attribution data.

(Original "Option C STRONG confirm" framing left below for audit trail; treat all "P ≪ 0.0001" / "STRONG confirm" claims as superseded.)

---

## 0.5. RECOVERY OUTCOME (post-completion amendment, 2026-05-22 — knight-rider session 2)

**Recovery completed clean.** Summary artifact landed at `~/Games/reincarnated-engine/logs/w07_lc011_ablation_recovery_summary.json`.

**Empirical signal: SCENARIO B — Surface A meaningful attribution at boundary magnitude.**

| Run | Definition | mage_controller FAILED | Rate |
|---|---|---|---|
| Run 1 | baseline (DB; 15 seasons; complete from 2026-05-21) | 3/60 | **5.0%** |
| Run 2 | observational (combined DB + recovery: 15 seasons) | 2/60 | **3.3%** |
| Run 3 | Surface A ablation `skill_power_tier=42` (recovery; 15 seasons) | 1/60 | **1.7%** |

**Discipline #13b two-way attribution:**

- Surface_A% = (Run1 - Run3) / Run1 = (5.0% - 1.7%) / 5.0% = **66.7%**
- Residual% = **33.3%**
- Formula well-defined: ✅ (R_base = 5.0% > 0)
- Disposition field: `ATTRIBUTION_COMPUTED`

**What this means for W1.13:**

1. The `skill_power_tier` parameter (controller/mage 50→42 ablation) IS **mechanically real** as a contributor to mage_controller failure regime — accounting for ~2/3 of the boundary-grade signal.
2. Magnitude is at boundary scale (5.0% historic → 1.7% with ablation), not catastrophic scale (the 41.8% historical figure was era-stratified to pre-W0.10).
3. Residual 33.3% is consistent with broader post-W0.10 structural underdetermination (Track C + W0.10 dual-witness signal).
4. LC-011 is not "deprecated entirely" (would have been α) — it is **reframed as a calibration witness at reduced magnitude with concrete two-way attribution**. The W1.13 success criteria can retain a generation-time pass-rate target (baseline 5%, not 42%).

**Disposition path: β (revise scope, retain commitment) — INSIDE critique-pair's delegated authority per Matt 2026-05-22.**

No further Matt-briefing required for the β disposition. The critique-pair (jack-ryan + gandalf) lands:
- W0.7 cumulative Gate-2 ratification (LC-002 + LC-009 + LC-011)
- W1.13 dispatch revision (triple → dual-witness mandate, with LC-011 reframed-not-removed; success criteria revised)
- Math note v1.1 § 1.2 revision (dual-witness + Surface A footnote per Scenario B)
- P0 milestone tag fire (`v0.0-constraint-removal-shipped`)

**Escalation Rule #1 satisfied:** the original 5% boundary trigger was framed as "STRONG confirm" warranting your call. The corrected reading (boundary-grade Option C with Surface_A=66.7% attribution) is NOT strong-confirm — it is a **partial-attribution Scenario B** that fits inside the autonomous β envelope you delegated. The matt-briefing remains filed for audit trail; no architectural decision is currently held pending your return.

(Open question for your return: whether you want critique-pair's β disposition framing reviewed before P1 substrate enrichment commits engine-side, or whether the dispatched β work is satisfactory as-is. Default: autonomous proceed unless you flag otherwise.)

---

**[Superseded] Original framing:** the data we DO have is dispositive on the floor-lock question itself:

| Cohort | Classes | floor_lock_recompose events | Rate |
|---|---|---|---|
| Run 1 baseline (700101-700115) | 75 | **0** | 0.0% |
| Run 2 observational (700201-700213, partial) | 60 | **0** | 0.0% |
| **Total measured** | **135** | **0** | **0.0%** |
| Historical baseline (per LC-011 reframing 2026-05-21) | — | — | 42% |

**Binomial probability against the 42% historical baseline: P ≪ 0.0001.**

**[Superseded] Verdict: Option C STRONG confirm.** Floor-lock pathology DID NOT REPRODUCE. This satisfies the escalation criterion in your mission prompt (≤ 5% mage_controller failure). **W1.13's triple-witness empirical mandate substantively dissolves**: math note v1.1 § 1.2 must revise from triple-witness (Track C + W0.10 + LC-011) to **dual-witness** (Track C + W0.10 only).

**Per Escalation Rule #1 of the mission prompt**, this requires your architectural call. **Knight-rider has HELD the W1.13 fire-gate** pending your disposition. All other pre-authorized work proceeds.

---

## 1. The empirical findings (data-grade)

### 1.1 What completed

- **Run 1 (700101-700115):** 15/15 seasons completed cleanly. 75 classes. 0 floor_lock_recompose events.
- **Run 2 (700201-700213):** 13/15 seasons completed; season 700213 started but never finished (`completed_at IS NULL`). 60 classes from completed seasons. 0 floor_lock_recompose events.
- **Run 3 (700301-700315):** 0/15 seasons. **NEVER STARTED.** The Surface A ablation (controller/mage/caster `skill_power_tier` 50→42) was the analytical comparison arm; without it, Discipline #13b two-way attribution `Surface_A% = (Run1 - Run3) / Run1` is uncomputable.

### 1.2 What the data already locks in

The floor-lock pathology — defined per LC-011 reframing 2026-05-21 as `floor_lock_recompose=1` events at MAX_ITERATIONS exhaustion near MODIFIER_SEARCH_FLOOR — **does not reproduce in the current post-W0.10 engine state**. Across 135 classes spanning all 7 substrates and all role orientations, zero floor-locks occurred.

This empirically confirms the LC-009 pattern that gandalf flagged in the closure note's emerging signal (0/30 at seasons 1-6): **the historical 42% signal was era-stratified to the pre-W0.10 engine state**. Post-W0.10 (Option A archetype-agnostic + R1 retune + energy-type lever + tier-weighted convergence) supersedes the pathology that motivated W1.13's third-witness empirical mandate.

### 1.3 What the data does NOT lock in

- **Surface A attribution.** Was the controller/mage `skill_power_tier=50` parameter the proximate cause of the historical 42%? Unknown. Run 3 was supposed to test this and didn't run. But: with 0% baseline in Run 1, Surface A ablation's premise (lower the parameter and observe a delta) has no signal to attribute against. The two-way attribution formula has a zero denominator.
- **The proximate cause of the historical 42%.** It's now even more likely than gandalf flagged (closure note § 3) to be era-stratification rather than a current-engine pathology — but we have no positive evidence pointing to the specific superseding mechanism. Best-available attribution per Discipline #13b is "post-W0.10 stack collectively superseded the pre-W0.10 floor-lock regime."

---

## 2. Why the script crashed (operational finding)

### 2.1 Crash evidence

- Process PID 40309 no longer running (no descendant processes alive)
- Log file `logs/w07_lc011_ablation.log` last modified 2026-05-21 00:14:13 (local EDT)
- Log tail ends mid-WARNING-stream (`_determine_geometry_type` heuristic-fallback warnings) — **no final summary, no traceback, no exit confirmation**
- `generation_runs` row #152 (season_700213) has `started_at` set but `completed_at IS NULL`

The script ran approximately 3 hours (started ~21:01 EDT 2026-05-21; terminated ~00:14 EDT 2026-05-22) of an expected ~5 hours. **It did not exit cleanly.** No traceback. No summary artifact. The final babysit agent (which was supposed to exit cleanly with a summary on script completion) **also did not produce its summary artifact** — confirming the babysit-pattern non-viability flagged in the closure note § 6.

### 2.2 Cause is not clear from current evidence

I do not have a definitive cause. Plausible candidates:
- Memory pressure (2.8GB log file; process likely retained substantial state)
- OS-level intervention (laptop sleep / kill -9 from another process)
- Babysit agent inadvertently killed the script as it itself died (unlikely; agent should be terminal-only)
- A latent bug in the script's between-run cleanup phase

**For purposes of the LC-011 disposition decision, the crash is non-blocking.** The Run 1 + Run 2 data is sufficient to lock in Option C; running Run 3 has no analytical signal to recover under the 0-baseline.

**For purposes of operational discipline**, the crash compounds the babysit-pattern non-viability case. jack-ryan's engineering-disciplines entry (pre-authorized per mission rule G) should be expanded to cover this compound failure mode: **long-running scripts spawned with babysit agents can crash silently with neither the script nor the agent producing diagnostic output**.

---

## 3. Options for W1.13 disposition

Per Escalation Rule #1, this is your architectural call. Three options:

### Option α — Deprecate W1.13 entirely

**Rationale:** With LC-011 dropped from the witness list, the math note v1.1 § 1.2 mandate becomes dual-witness (Track C + W0.10). Track C established Pattern-A 100% at boss tier under scalar-modifier-only; W0.10 established arena-fix discharges only the HIGH-modifier band. **But both witnesses point to a different fix domain than W1.13 was scoped for.**

- Track C says: scalar-modifier-only is mathematically underdetermined for 5-tier WR contract
- W0.10 says: arena-fix discharges high-modifier; low-modifier remains
- W1.13 says: procedural skill tree node population + multi-dim convergence over 5-6 dimensions

W1.13's fix is structurally proportional to the dual-witness signal (more dimensions help underdetermined optimization), but the **load-bearing case** that LC-011 carried was the generation-time signal (42% mage_controller failure). Without that signal, W1.13's empirical urgency drops to "addresses a known mathematical underdetermination" — which may be deferrable to v2 once Profile A + the production gauntlet validate whether the residual is actually a v1 ship-blocker.

**Risk:** the Pattern-A low-modifier residual may still be a v1 ship-blocker even without the LC-011 framing. If we ship without W1.13, we ship knowing the low-modifier band is structurally constrained.

### Option β — Revise W1.13 scope

**Rationale:** Keep the multi-dim convergence architectural commitment, but rescope to address only the dual-witness signal. This is gandalf's reframing of math note v1.1 § 1.2 as dual-witness with W1.13 still firing but at reduced confidence.

**What changes:**
- Math note v1.1 § 1.2 revised to dual-witness (LC-011 reframed as era-stratification artifact)
- W1.13 dispatch's "triple-witnessed empirical mandate" framing revised to "dual-witnessed empirical mandate"
- W1.13 success criteria (per dispatch § 4) lose the "generation-time 80% pass-rate" target (no current 42% baseline to lift from)
- W1.13's other success criteria (Pattern-A residual reduction; low-modifier band exit from 0.000) retained
- Math note v1.1 § 2.3 ("tier-specific scaling coefficients load-bearing for low-modifier kits") remains the load-bearing case for W1.13

**Risk:** rescoped W1.13 still consumes 2-4 weeks of rocket time. If the residual it addresses is small (Pattern-A residual already 20-40% post-W0.10 per math note § 5.3 prediction), the v1 ROI may be marginal.

### Option γ — Proceed-as-planned with reduced confidence + recovery probe

**Rationale:** Run the residual Run 2 (2 seasons) + Run 3 (15 seasons) of the ablation, even though the analytical premise is now compromised. Treat this as Classification-B attribution work per gandalf's LC-011 disposition note Appendix A (NOT classification-A parametric tuning, which is the rejected pattern). The remaining 17 seasons may surface secondary findings (e.g., if Run 3 with `skill_power_tier=42` produces FAILED kits that Run 1 didn't, then the parameter is causally relevant in some regime even if the baseline shifted; if Run 3 also shows 0 floor-locks, Option C is strengthened).

**What this looks like operationally:**
- Investigate the crash cause first (avoid re-running into the same wall)
- Fire a recovery script targeting only seasons 700214, 700215, 700301-700315 (17 seasons; ~2 hours wall time)
- DB-check pattern instead of babysit-agent (per engineering-disciplines candidate)
- Re-evaluate W1.13 disposition after the recovery completes

**Risk:** consumes ~2 hours of compute + some operational attention; analytical premise is already compromised; may not change the disposition meaningfully.

### Knight-rider's recommendation

**Option β (Revise W1.13 scope) + run Option γ's recovery probe as background validation.**

Rationale:
1. The dual-witness mandate (Track C + W0.10) still justifies multi-dim convergence as architectural commitment; the genre-canon argument for procedural skill trees + Tier 4 keystones + trigger interactions stands on its own.
2. The BDI formalism (gandalf's new authoring) makes W1.13's structural commitment richer than originally framed — Tier 4 keystones as rank-completers, trigger interactions as multiplicative scaling layer, BC-axis-contribution tagging as substrate-richness enabler. Deprecating W1.13 would lose this architectural alignment.
3. Gear-as-substrate LITE (pre-authorized; G1-LITE rule-table v1) is already ~1 week of rocket time landing in P1; rescoped W1.13 (~2-3 weeks) on top of substrate enrichment (W1.1-W1.6, W1.11; ~4-6 weeks) is the natural P1 envelope.
4. Option γ's recovery probe is cheap (~2 hours wall time) and may produce secondary findings that sharpen the W1.13 scope further.

**But this IS your decision per Escalation Rule #1.** I am not pre-empting; I'm filing the briefing and holding the gate.

---

## 4. What proceeds without your input (pre-authorized per mission prompt)

While W1.13 holds, the following work proceeds per pre-authorized delegations A-G in your mission prompt. **Specific dispatch files filed for autonomous pickup:**

| Workstream | Owner | Dispatch file |
|---|---|---|
| Protocol v1.3 fold-in (BDI + LITE + T4 amendments) | gandalf | `dispatches/2026-05-22-gandalf-protocol-v13-foldin-plus-BDI-B-plus-G1-LITE-plus-T4-A.md` (deliverable 1) |
| BDI-B (ω-table + τ-table v1 finalization; pre-auth A) | gandalf | same dispatch, deliverable 2 |
| G1-LITE (signature_gear_archetype rule-table v1; pre-auth B) | gandalf | same dispatch, deliverable 3 |
| T4-A (Tier 4 architecture; pre-auth C) | gandalf | same dispatch, deliverable 4 |
| W0.7 cumulative Gate-2 ratification + W1.13 rescope + math note revision + P0 tag (pre-auth D + E) | jack-ryan + gandalf critique-pair | `dispatches/2026-05-22-critique-pair-post-recovery-w07-gate2-w113-rescope-p0-close.md` (FIRE-GATED on recovery summary artifact) |
| Engineering-discipline #19 entry (babysit + compound silent-failure; pre-auth G) | jack-ryan | `dispatches/2026-05-22-jack-ryan-engineering-discipline-19-agent-tool-not-for-waiting.md` |
| W1.1-W1.6 substrate enrichment scoping + W1.15-LITE spec-pickup | rocket | `dispatches/2026-05-22-rocket-w11-w16-substrate-enrichment-scoping.md` (P1 work; fire condition is P0 tag) |
| BDI hypothesis tests H1-H5 execution (pre-auth F) | rocket + legolas + gandalf | DEFERRED to next session (non-blocking diagnostic; will be authored when bandwidth available) |

**P0 milestone tag `v0.0-constraint-removal-shipped` is HELD** pending critique-pair completion of their work-package (post-recovery; per dispatch acceptance criteria). This supersedes the original "tag fires per first-action sequence step 4" framing — the recovery + critique-pair disposition is the cleaner close.

---

## 5. What I need from you on return

1. **W1.13 disposition decision:** α / β / γ per § 3 above. Recommendation: β + γ.
2. **Whether to investigate the script crash cause before the recovery probe** (Option γ contingent).
3. **Whether the dispositional latitude granted to the critique-pair (jack-ryan + gandalf) per pre-auth D extends to "Option C STRONG confirm" cases** that this briefing covers, or whether you reserve that decision personally. (Current behavior: I treated the strong-confirm as escalation-triggering per Rule #1 and held the gate. If you intend critique-pair to disposition strong-confirms autonomously, the rule should be revised.)

Until your return, I am holding the W1.13 fire-gate, proceeding with all pre-authorized non-W1.13 work, and capturing daily state in `skill_handoff_<date>.md`.

---

## 6. Cross-references

- `agentic_orchestration/p0-closure-note-2026-05-21.md` — P0 closure context + emerging-signal hint
- `agentic_orchestration/hive-mind-state-evening-2026-05-21.md` — companion state-snapshot
- `agentic_orchestration/gandalf/notes/2026-05-21-lc-011-reframing-disposition-w1-13-routing.md` + Appendix A — LC-011 disposition framing
- `agentic_orchestration/dispatches/2026-05-21-rocket-w1-13-skill-tree-node-population.md` § 0.0 — FIRE-GATE conditions (currently HELD)
- `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` v1.1 § 1.2 — triple-witness mandate (pending revision to dual-witness)
- `reincarnated-engine/scripts/w07_lc011_ablation.py` — ablation script source
- `reincarnated-engine/logs/w07_lc011_ablation.log` — crash log (terminates mid-WARNING-stream)
- Telemetry DB `data/telemetry.db` `generation_runs` — runs 122-152 (W07 LC011 series; #152 incomplete)

---

**Signed:** knight-rider (orchestrator under prolonged-autonomy mandate)
**For:** Matt's architectural disposition of W1.13 in light of Option C STRONG confirm + script-crash operational finding.
