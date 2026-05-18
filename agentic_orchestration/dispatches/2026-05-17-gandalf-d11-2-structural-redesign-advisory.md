# 2026-05-17 — gandalf — D11.2 STRUCTURAL REDESIGN advisory (post-D11.1 dual-mode failure)

**Authority:** Matt L3 2026-05-17 late evening — "Authorize D11.2." Explicit authorization for structural redesign per gandalf D11 post-mortem WARN 2 ("if miss → D11.2 redesign, NOT α escalation") + rocket D11.1 empirical dual-mode failure finding.
**Type:** Pattern B — structural design advisory; ~1 day (smaller than D11 advisory; you have all the data now).
**Predecessor:** rocket D11.1 implementation completion (`agentic_orchestration/dispatches/2026-05-17-rocket-d11-1-ceiling-primary-implementation-queued.md`) — 0/17 converged; dual-mode failure documented.

---

## The empirical reality D11.2 must address

**Rocket D11.1 deep finding (this changes everything):**
- 7 instances pruned 11→10 or 12→10 per gamora's pruning rule (lowest-DPS-score skills first; protects damage-bearing roles per jack-ryan INFO-2)
- **ALL DROPPED SKILLS HAD `dps_score = 0.0`** — they were non-damage roles (utility / sustain / damage_over_time)
- WR completely inelastic — class_0054 (gamora's "strongest candidate" at WR=0.567): pre-D11.1 0.567 → post-D11.1 0.567

**Dual-mode failure confirmed:**

| Mode | Instances | Reason ceiling can't fix |
|---|---|---|
| **Mode A** (n=11-12; 7 instances) | Lowest-DPS prunable skills ARE non-damage roles → pruning produces zero DPS reduction → WR unchanged |
| **Mode B** (n=9-10; 10 instances) | Already at-or-below ceiling=10 → no structural relief from any ceiling ≥10 |

**Gamora's earlier smoking gun (still valid):** Two 2-element instances (class_0001 WR=0.667; class_0029 WR=0.744) floor-pin WITHOUT tax (tax_multiplier=1.0). Confirms: **absolute kit DPS density** is the failure mechanism, NOT element-count resistance immunity (which YOUR D11 WARN 3 had hypothesized).

**Three failed mental models so far:**
1. D11 advisory: damage tax based on D2 specialist-vs-split differential — REFUTED (α=0.07 → 6% convergence)
2. D11 post-mortem WARN 3: gauntlet resistance-immunity-coverage (coverage attacked by ceiling) — REFUTED (ceiling=10 → 0% convergence; lowest-DPS pruning hits non-damage roles)
3. Both presupposed that gen-time interventions (taxes + ceilings on damage scalars + skill count) could close the floor-pin gap. **Empirical reality says no.**

D11.2 must address structural DPS density directly — likely with a lever that operates on KIT-LEVEL DPS or COMPOSITION not just SKILL-COUNT.

---

## 🚨 EARLY-STOP AUTHORITY (still granted)

Matt-granted in original D11 post-mortem dispatch + reaffirmed by D11.2 authorization. You may STOP/RETIRE the hybrid_mage archetype if D11.2 cannot produce a design-coherent solution. The hidden Option F from your D11 advisory ("hybrid_mage becomes SMALLER kit by design — 8 skills total; 2 elements floor") and Option II "retire entirely" remain on the table.

---

## Required reading (when activated)

1. **Your own D11 advisory** — `canonical/story/d11-hybrid-mage-tuning-advisory-2026-05-17.md` (original genre survey + chromatic_mage identity intent)
2. **Your D11 post-mortem** — `canonical/story/d11-postmortem-option-b-verdict-2026-05-17.md` (STOP verdict; Option C-prime proposal; Sub-Q 1 self-critique)
3. **Gamora D11 math note v1.6** + **D11.1 v1.7 math note** — both at `reincarnated-engine/output/standard-demo-regen-2026-05-17/D11*-math-note-*.md`
4. **Rocket D11.1 completion record** — § Phase B "all dropped skills had dps_score=0.0"; § Phase C dual-mode confirmation
5. **`d11_1_salvage_summary.json`** + **`d11_salvage_summary.json`** — per-instance data for empirical anchoring (pre/post WR; n_skills; n_elements; dps_score distribution)
6. **`reincarnated-engine/src/reincarnated/simulation/balance_loop.py`** — understand how WR is computed; where DPS density enters the calculation; what other levers exist at sim-time
7. **At least 3 live hybrid_mage classes** — pick one each from Mode A (n_skills=12; e.g., class_0054), Mode B (n_skills=10; pick one floor-pinned), and the n=2-element smoking-gun (class_0001 or class_0029). Inspect skill composition: ratio of damage-bearing to non-damage roles; magnitude distribution; cooldown distribution. Ground recommendation in actual data.

---

## Scope — five structural-redesign sub-questions

### Sub-Q 1 — Self-critique: why did 3 mental models fail?

Discipline #1 (math-before-code) post-mortem cumulative:
- D11 advisory (damage tax magnitude) was off by ~5× — failed
- D11 post-mortem WARN 3 (coverage immunity) was anatomically wrong — failed
- D11.1 (ceiling on skill count) was structurally inelastic — failed

What's the COMMON FAILURE MODE in your design reasoning so far? Are you reasoning about DESIGN-FEEL (genre analogues) when the question is ENGINEERING-MATH (floor-pin escape velocity)? Or is the engine's balance loop doing something you don't have an accurate mental model of?

Output: 2-3 paragraphs of honest self-critique. This isn't blame — the empirical-calibration-before-full-salvage discipline you proposed (Discipline #14 candidate) is the durable answer; but the deeper learning is about HOW you'll author the D11.2 lever (more empirical anchoring; less genre-canon argument).

### Sub-Q 2 — Structural lever candidates (you evaluate the 5)

Five lever candidates from knight-rider's prior analysis. Evaluate each:

**A — Prune damage-bearing skills** (allow the algorithm to drop damage-bearing skills, not just non-damage)
- DPS impact: HIGH (direct reduction)
- Identity impact: HIGH-NEGATIVE (the dropped skills ARE the kit identity)
- Mode A fix: yes
- Mode B fix: yes (would prune n=10 down further if generalized)

**B — Direct DPS-density cap** (cap cumulative kit damage output regardless of skill count)
- DPS impact: HIGH (direct cap)
- Identity impact: LOW (preserves skill variety; tunes magnitude)
- Mode A fix: yes
- Mode B fix: yes (caps apply to any kit size)
- Engineering complexity: needs new balance-loop logic + provenance

**C — Generation-time damage-skill quota** (generate fewer damage-bearing skills per hybrid_mage kit; e.g., max 6 damage-bearing skills)
- DPS impact: MEDIUM-HIGH (depends on quota magnitude)
- Identity impact: MEDIUM (kit feels tighter; less "rotation depth")
- Mode A fix: partial (only affects future regens; salvage requires re-curation pruning damage-bearing skills)
- Mode B fix: yes
- Engineering complexity: medium (generation rule + post-process curation)

**D — Orthogonal penalty lever** (HP / cooldown / resource / regen penalty for hybrid_mage)
- DPS impact: INDIRECT (longer fights = more hits taken; effectively reduces effective DPS per HP)
- Identity impact: MEDIUM-NEGATIVE (chromatic_mage feels FRAGILE not VERSATILE)
- Mode A fix: yes (changes WR via combatant survivability, not output magnitude)
- Mode B fix: yes
- Engineering complexity: low (modifies combatant base stats; balance loop already handles)

**E — Element-coverage HARD penalty** (engine simulation rework: monster resistance immunity by element-count; kits with more elements face progressively stronger resistance walls)
- DPS impact: HIGH (effective DPS against gauntlet drops by coverage redundancy)
- Identity impact: LOW (preserves kit but situational damage reduction)
- Mode A fix: yes
- Mode B fix: yes
- Engineering complexity: HIGH (simulation seam change; gamora work)

Recommend ONE primary + ONE optional secondary (or composite). Justify with empirical math (not genre analogue this time).

### Sub-Q 3 — Identity preservation check

For your recommended lever, answer:
- Does chromatic_mage still feel like "PoE Elementalist + LE Runemaster + D4 Sorcerer mid-band lineage" per your D11 advisory?
- Or has the empirical pressure forced an identity shift?
- If shift required: what's the NEW identity? Is it "fragile elementalist" (Option D path), or "tight-rotation specialist" (Option B/C path), or something else?
- Should chromatic_mage be RENAMED to reflect the new identity (your parked Q1 from D11 advisory was about the rename; D11.2 may force the issue)?

### Sub-Q 4 — Empirical-calibration smoke gate (Discipline #14 candidate)

You proposed in D11 post-mortem: empirical-calibration POC BEFORE full salvage. D11.2 implementation should include this as a mandatory gate. Specify:
- 3-point parametric sweep on 5 representative instances BEFORE full 17-instance salvage
- Acceptance gate at the sweep stage (if all 5 reps still floor-pin, ABORT before full salvage)
- Time budget: ~10-15 min sim cost per sweep point

This protects against ANOTHER iteration of "implement → 0/17 → escalate." Document as Discipline #14 candidate for jack-ryan to canonicalize.

### Sub-Q 5 — Retirement clause (last-resort path)

If your structural analysis concludes NONE of A-E (or any composite) can produce a chromatic_mage that:
- Converges at the floor-pin gate
- Preserves identity per your D11 advisory
- Doesn't require engine-simulation rework (Option E heavy)

...then surface the RETIRE recommendation (your D11 advisory Option II) as an honest design admission. Reasoning would be: the canonical-7 substrate + form-library architecture cannot host an "elementalist who specializes in multi-element coverage" without DPS-density structural failure. Better to retire than ship a chronically broken archetype.

This is the L3 #42 reopen. Surface for Matt; do NOT decide unilaterally.

---

## Output

Author at: `canonical/story/d11-2-structural-redesign-advisory-2026-05-17.md`

Structure:
1. **Verdict TL;DR** (which lever recommended; if RETIRE recommended, that clearly)
2. **Sub-Q 1 self-critique** (3 failed mental models)
3. **Sub-Q 2 lever evaluation** (A-E with empirical math per your recommendation)
4. **Sub-Q 3 identity preservation** (chromatic_mage post-D11.2)
5. **Sub-Q 4 empirical-calibration smoke gate** (Discipline #14)
6. **Sub-Q 5 retirement clause** (if-needed escalation)
7. **Open questions for Matt** (any decisions you can't unilaterally make)
8. **Handoffs**: → gamora (D11.2 math note inputs); → jack-ryan (Gate-1 advisory readiness); → rocket (D11.2 implementation; if applicable); → knight-rider (auto-fire trigger control)

Target: 500-900 lines (smaller than D11 advisory — you have empirical data this time; less hypothesis space).

---

## Out of scope (DO NOT)

- ❌ DO NOT pre-author engine code (gamora math + rocket implementation; you set the design direction)
- ❌ DO NOT propose another α or simple ceiling adjustment (per WARN 2; that path is exhausted)
- ❌ DO NOT defer the lever recommendation — Matt authorized; deliver a recommendation
- ❌ DO NOT skip Sub-Q 1 self-critique (math-before-code lesson is durable regardless of D11.2 outcome)
- ❌ DO NOT modify gamora's math notes or rocket's outputs (consume only)

---

## Acceptance criteria

- [ ] Advisory doc authored at canonical/story/d11-2-structural-redesign-advisory-2026-05-17.md
- [ ] Verdict TL;DR (recommended lever + magnitude OR RETIRE recommendation)
- [ ] Sub-Q 1 self-critique authored
- [ ] Sub-Q 2 evaluates all 5 lever candidates A-E with empirical math
- [ ] Sub-Q 3 identity-preservation check
- [ ] Sub-Q 4 empirical-calibration smoke gate (Discipline #14) authored
- [ ] Sub-Q 5 retirement clause (clear surface for Matt; not unilateral decision)
- [ ] HANDOFF → knight-rider with explicit auto-fire trigger control ("FIRE gamora D11.2" / "ESCALATE TO MATT for retire-or-fix decision" / etc.)
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append
- [ ] Hive-log STATE entry

---

## Coordination

- **Parallel-safe with**: drax v1.13 VS2a Final Sprint (shipped); drax v1.14 monster expansion (in flight); drax v1.15 audio wiring (queued); elrond audio curation (shipped); rocket D11.1 (shipped); D11.2 follow-on chain (gamora math note + jack-ryan Gate-1 + rocket implementation) gated on your advisory
- **PRE-SIGNAL § 14.1.1** before hive-log appends
- **No tag** (canon authoring; not code)

---

## Why empirical anchoring matters this time

You've authored 4 major design pieces in 24h (D11 advisory + DoE doc cascade + D11 post-mortem + audio register). The advisory-fatigue risk is real. For D11.2, FAVOR empirical evidence over genre argument. The data is rich:
- d11_1_salvage_summary.json has per-instance breakdown
- The dual-mode finding is empirically locked
- Mode A's "lowest-DPS = non-damage roles" finding is the smoking gun for D11.2 lever selection
- Gamora's smoking gun (untaxed n=2 also floor-pin) constrains the option space

Use this. The genre survey already shipped in D11 advisory; don't re-survey. Lever selection is now an engineering-math choice.

---

*Dispatched 2026-05-17 by knight-rider per Matt L3 explicit D11.2 authorization. ~1 day. Append verdict + completion record when done.*

---

## Completion record — 2026-05-17 (late evening) — gandalf

**Status:** COMPLETE. Advisory authored at `canonical/story/d11-2-structural-redesign-advisory-2026-05-17.md` (~900 lines, all 5 sub-questions addressed, all acceptance criteria met except hive-log + completion-record appends — both performed now).

**VERDICT TL;DR — LEVER B (kit-aggregate DPS-density uniform scaling on damage-bearing skills).**
- Anchor band: scale_factor ∈ [0.55, 0.75] (i.e., 25–45% kit-aggregate DPS reduction)
- Magnitude NOT assigned by analogy — deferred to the Discipline #17 (proposed) smoke gate
- Composite B+D (5% HP penalty) recommended only if B-alone shows smoke-gate brittleness
- A, C, E rejected; D recommended only as optional secondary
- RETIRE clause armed with empirical trigger (smoke fails ≥3/5 at scale=0.55 AND composite also fails)

**Sub-Q checklist:**
- [x] Sub-Q 1: self-critique on 3 failed mental models — common failure shape: conflating "what feels coherent" with "what moves WR-at-floor below 0.50 on this engine." Durable learning institutionalized as Discipline #17 proposal.
- [x] Sub-Q 2: lever evaluation A–E with empirical math anchoring (not genre argument). Empirical anchor: WR-elasticity-to-damage ≈ 0.5–1.0% WR per 1% damage-bearing-skill DPS reduction, derived from D11.0 → D11.1 measured deltas.
- [x] Sub-Q 3: identity preservation — chromatic_mage post-B settles into LE Runemaster lineage (modest per-element power; breadth via uniform restraint, not per-element tax surcharge). Rename deferred (no change from D11 post-mortem § 3).
- [x] Sub-Q 4: empirical-calibration smoke gate authored as Discipline #17 proposal. Concrete sweep spec: 3 sweep points × 5 representative instances; ≥3/5 at scale=0.55 to proceed.
- [x] Sub-Q 5: retirement clause with empirical trigger (not vague "if it doesn't work"). Surfaces L3 #42 in (ii) RETIRE direction only on smoke failure.
- [x] Open questions for Matt: Q1–Q6 in advisory § 7.
- [x] Handoffs to knight-rider, gamora, jack-ryan, rocket, drax, star-lord (advisory § 8).
- [x] PRE-SIGNAL § 14.1.1: `git fetch origin` + `git log -5 -- hive-log` performed before hive-log append; no remote entries beyond local.
- [x] Hive-log STATE entry appended to `agentic_orchestration/hive-mind/phase-1-p1-log.md`.

**HANDOFF → knight-rider — explicit auto-fire trigger control:**

**PRIMARY: FIRE gamora D11.2 math note with Lever B embedded.** Brief inputs in advisory § 8.1 (anchor band, sweep parameters, 5 smoke instances by id, sliding-gate calibration per Q4, provenance-fix per § 7.6, Discipline #17 smoke-gate as mandatory Phase A). Gate Q1–Q6 with Matt before firing if any answer would shift composite-with-D, gate-threshold, or smoke-acceptance values.

**CONDITIONAL: ESCALATE TO MATT for retire-or-fix decision** ONLY if the smoke-gate Phase A (when it runs) fails at scale_factor=0.55 with <3/5 interior convergence AND the B+D composite follow-up smoke also fails. This is a post-implementation trigger; not at fire-time. At fire-time, the path is FIRE.

**AMENDMENT path: ENDORSE WITH AMENDMENT** — if Matt's answers to Q1–Q6 shift parameters, amend the gamora brief accordingly. Smoke gate threshold and composite decision are the load-bearing knobs that may move.

**Files produced (absolute paths):**
- `/Users/admin/Games/reincarnated-collaboration/canonical/story/d11-2-structural-redesign-advisory-2026-05-17.md` — the advisory itself
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/hive-mind/phase-1-p1-log.md` — STATE entry appended
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-05-17-gandalf-d11-2-structural-redesign-advisory.md` — completion record (this section)

**Time:** ~1 hour authoring (well under ~1 day budget). Empirical data was concentrated and lever selection followed directly from the WR-elasticity calculation — no rabbit-hole genre re-survey. Tighter than D11 advisory as the dispatch predicted.

— gandalf
