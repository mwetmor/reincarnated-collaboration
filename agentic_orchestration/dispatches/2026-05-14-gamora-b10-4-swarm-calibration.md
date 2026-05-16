# Dispatch — 2026-05-14 — gamora — B10.4 swarm calibration + cost verification

**From:** knight-rider
**To:** gamora
**Approved by:** Matt, 2026-05-14
**Estimated effort:** 2–3 hours
**Acceptance:** Swarm `eff_attr` bumped from 0 to a calibrated value (5–8 range, gamora picks with math justification); full-regen and smoke-mode wall times measured vs B10.1 baseline; decisions-log entry capturing V2 framing context; all tests pass; `v1.3-b10-4-swarm-calibration` tagged.

**Gate 1:** jack-ryan reviewed — see notes below before starting.

---

## Context

B10.2 empirical finding: swarm-pack DPS ≈ 298 at `eff_attr=0`. This is low enough that any tier-50 class with potions wins pack fights on sustain — the AOE/single-target differential is mechanical but not decisive. V1 partial AOE signal is confirmed; full differential lands in B10 V2 (sequential rooms with HP carryover). B10.4 addresses the calibration gap: bump swarm `eff_attr` so swarm encounters present a meaningful threat, and measure actual regen cost vs B10.1 estimates.

**Why this is Discipline #12 (semantic-shifting):** Changing `eff_attr` changes what "swarm encounter" means in balance history and telemetry. Any telemetry-recorded DPS values from pre-B10.4 seasons reflect eff_attr=0 swarms. Post-B10.4 seasons will reflect the calibrated value. This is a known break point — document it explicitly.

**V2 framing context to capture:** B10 V2 (sequential rooms with HP carryover) is the full multi-actor simulation. B10.4 swarm calibration is NOT V2 — it makes the current proxy encounters feel right within V1 semantics. V2 remains a separate roadmap item.

---

## Math-before-code (BLOCKING — document before any code)

### C1 — Target DPS for swarm tier at tier-50

Current: ~298 DPS (eff_attr=0). Too low — potions trivially overcome it.

**Bounding constraint (required — do not invent a target outside this bound):**
- Trash tier reference: eff_attr=40, analytical DPS ≈ 660 at tier-50
- Swarm target must satisfy: `swarm DPS / trash DPS < 0.40` (swarm must be below 40% of trash threat level)
- Document the actual ratio in your math note: `chosen swarm DPS / 660 = X%`
- Do NOT adjust trash, elite, mini-boss, or boss eff_attr — swarm only

Pick a target DPS value that:
- Threatens a class that doesn't manage potions well (a class burning through potions faster than regen should feel pack pressure)
- Remains clearly below the 0.40 ratio bound above
- Does NOT make pack fights the dominant damage source (swarm is a positioning/AOE-signal encounter, not an attrition fight)

Suggested approach: find the eff_attr where pack fight timeout occurs at roughly modifier=0.1 (instead of 0.03 as in B10.2). That creates a meaningful floor without overcorrecting.

### C2 — Specific eff_attr value (pick one, 5–8 range, with DPS math)

Document: at chosen eff_attr, what is the resulting swarm DPS? Show the calculation. Verify it's below trash tier (eff_attr=40 = ~660 DPS analytical). If the chosen value produces DPS where sustain still trivially wins, go higher within the range. If it produces DPS where swarm fights become attrition slogs, go lower.

### C3 — Telemetry / MIGRATION.md check (conditional path is explicit — follow it)

Does star-lord's telemetry record per-fight DPS values or `eff_attr` directly as a persisted field?

- **If YES** (DPS or eff_attr is written to the telemetry log or SQLite): this is a cross-seam schema change under ADR-004. **Stop. Write MIGRATION.md describing the field change and notify knight-rider before writing any implementation code.** Do not proceed past this gate until knight-rider confirms.
- **If NO** (DPS is computed at fight time, never persisted): note this explicitly in your math doc ("telemetry schema unaffected — DPS is runtime-computed, not persisted"). No MIGRATION.md needed. Proceed.

---

## Cost verification (B10.4 primary deliverable alongside calibration)

**Required order — do not invert (Discipline #2):**

1. **Run smoke-mode first** (~5 classes, 30 fights): target ≤3 min. Record actual wall time. If smoke is dramatically over target (>2× expected), STOP and diagnose before proceeding to full regen.
2. **Only if smoke is healthy — run full regen** (all 10 classes, 100 fights): target 29–34 min (B10.1 estimate). Record actual wall time.
3. **Document delta from B10.1**: did PackProxy (replacing swarm slots) change cost meaningfully vs the 29–34 min baseline? Append finding to `b10-gauntlet-analysis.md §14`.

---

## Decisions-log entry to write

After implementation, append to `decisions-log.md`. The entry must include all four of these fields — do not omit any:

- **Swarm eff_attr calibration decision**: chosen value, rationale, target DPS, swarm/trash ratio
- **V2 framing boundary** (explicit one-liner required): "B10.4 is V1 tuning only. B10 V2 (sequential rooms with HP carryover) is out of scope for this work and remains a separate roadmap item."
- **Semantic break point** (Discipline #12 — label it explicitly): "All historical swarm DPS observations prior to commit `[hash]` reflect eff_attr=0 and are not directly comparable to post-B10.4 observations at eff_attr=[chosen value]. Treat as a calibration epoch boundary."
- **Delta from V1 baseline**: what changed, what the new floor is, and what modifier threshold now triggers pack fight timeout

---

## Additional validation: trash → swarm replacement metrics

The B10.2 gauntlet replaced 6 trash-tier 1v1 slots with 6 swarm PackProxy slots. Before the decisions-log entry for this change can be approved, two metrics must be confirmed clean. Run these during the B10.4 full-regen pass and report in the completion record:

**V1 — Kills per minute:** Compare average kills per minute per class in the B10.2 gauntlet (swarm proxy slots) against B10.1 telemetry (trash slots). If kills per minute increased materially (>15% across the class pool), flag to knight-rider before tagging — this indicates the gauntlet became easier and convergence metrics are not comparable to B10.1. If flat or lower, note and proceed.

**V2 — Converged build diversity:** Compare spread of converged builds (number of distinct skill compositions at convergence) between B10.2 and B10.1 historical data. If diversity increased materially, the swarm proxy may be rewarding a wider skill set than trash encounters did — flag to knight-rider. If stable, note and proceed.

Document both findings in `b10-gauntlet-analysis.md §14` alongside cost findings. Decisions-log entry for the trash→swarm design change will be written by knight-rider after B10.4 closes, conditioned on these metrics being clean.

---

## Scope

- [ ] C1/C2: target DPS and eff_attr value documented (math-before-code)
- [ ] C3: telemetry schema check; MIGRATION.md if required
- [ ] Bump swarm `eff_attr` to chosen value in simulation constants
- [ ] Run smoke-mode first; record wall time
- [ ] Run full regen only after smoke passes; record wall time
- [ ] V1: kills per minute comparison (B10.2 vs B10.1 telemetry) — report delta
- [ ] V2: converged build diversity comparison (B10.2 vs B10.1) — report delta
- [ ] Append cost + V1/V2 findings to `b10-gauntlet-analysis.md §14`
- [ ] Append decisions-log entry (calibration + V2 framing + semantic break point)
- [ ] All tests pass
- [ ] **Confirm with knight-rider before cutting milestone tag** (ADR-003 protocol)
- [ ] Tag: `v1.3-b10-4-swarm-calibration` on `main` — only after knight-rider confirmation
- [ ] Push to `origin/main`
- [ ] Update `simulation/AGENT_STATE.md`
- [ ] Append completion record to this dispatch

---

## Out of scope (explicit non-goals)

- B10 V2 (sequential rooms with HP carryover) — deferred, roadmap item
- Recompose gauntlet redesign — already shipped in B10.2
- Changing trash/elite/mini-boss/boss eff_attr values — swarm only
- Full encounter viz — separate drax work, deferred until B10.4 ships
- Gear in simulation — post-MVP

---

## Engineering disciplines

- **#1 Math-before-code:** C1/C2 DPS math documented before eff_attr change
- **#2 Smoke before full regen:** smoke first, full regen only if smoke is healthy
- **#12 Semantic-shifting:** eff_attr change is a semantic shift in swarm encounter meaning — document the break point explicitly in decisions-log

---

## References

- B10.2 completion record: `agentic_orchestration/dispatches/2026-05-14-gamora-b10-2-pack-proxy.md` — empirical DPS finding (§ completion notes)
- `design/b10-gauntlet-analysis.md` — §11/12/13 have B10.2 math and findings; append B10.4 as §14
- `design/decisions/decisions-log.md` — B10.2 closure entry is the prior reference
- B10.1 cost baseline: 29–34 min full regen, 2–3 min smoke
- Gate 1: jack-ryan, 2026-05-14

---

## Completion record

**Completed (partial):** 2026-05-15 — scope executed; tag BLOCKED pending knight-rider resolution of blocking finding
**Engineer:** gamora

### Scope status

- [x] C1/C2: math note `simulation/math/b10-4-swarm-eff-attr-calibration.md` — eff_attr=7 chosen, DPS math, constraint analysis
- [x] C3: telemetry schema unaffected — DPS runtime-computed, not persisted. No MIGRATION.md.
- [x] Code: `combatant.py` TIER_EFFECTIVE_ATTRIBUTE["swarm"] = 7 (from 0)
- [x] Smoke: 1m44s (target ≤3 min) ✓ — no crashes, pack proxy with eff_attr=7 executing correctly
- [x] Full regen: seed 1005, **1136.3s = 18.9 min** (target 29–34 min, actually FASTER) ✓ cost-wise
- [x] V1 (kills per minute): flagged to knight-rider — aggregate +75% (structural pack-fight artifact; non-pack KPM -25%) 
- [x] V2 (build diversity): stable (80% distinct role-sets, within B10.1 range 73–82%) ✓
- [x] b10-gauntlet-analysis.md §14: cost + V1/V2 + BLOCKING convergence finding documented
- [x] decisions-log.md: B10.4 calibration entry + KPM metric interpretation entry
- [x] Tests: 1291 passed, 0 failures ✓
- [ ] **TAG BLOCKED** — see blocking finding below
- [ ] Push to origin/main — BLOCKED
- [x] AGENT_STATE.md updated

### Math results (C1/C2)

- **Chosen eff_attr: 7** (3.5% DPS increase)
- Projected swarm DPS: 298 → ~308 (B10.2 baseline × 1.035)
- Swarm/trash analytical ratio: 1.035/1.200 = 0.863 (above the 0.40 design-intent bound — not fixable via eff_attr alone; documented as known gap)
- **Timeout threshold:** NOT moveable via eff_attr — pack HP is the binding constraint. "Timeout at modifier=0.1" requires pack HP change (out of scope B10.4). Documented in math note.
- **Semantic break point (Discipline #12):** commit `18e45ef` — all swarm DPS observations pre/post are not directly comparable (3.5% calibration delta)

### Cost findings

- Smoke: 1m44s ✓ (target ≤3 min)
- Full regen: 18.9 min ✓ (target 29–34 min; FASTER than expected because pack fights are very short)
- Delta from B10.1: ~10–15 min FASTER. Pack proxy fights take 0.1–4s (AOE one-shots pack) vs trash fights ~11–15s.

### BLOCKING FINDING: Pack-proxy convergence floor (→ knight-rider required)

**Full regen FAILED validation: 8/10 classes did not converge.**

Root cause (B10.2 structural issue, not B10.4): pack fights have ~100% win rate for almost all classes at any moderate modifier. The gauntlet is 6/12 pack + 6/12 non-pack. For overall WR to reach 50% with pack_WR = 100%, non-pack_WR must = 0% — mathematically impossible in practice.

Actual observed win rates at final modifier ~0.05:
- Pack WR: 99.2–100% (all 10 classes)
- Non-pack WR: 7.5–43% (varies by archetype)
- Overall WR: 55–71% → all above target (40–60%)

Only physical_warrior and experimental classes converged (their lower AOE effectiveness reduces pack WR to ~93–97%, and very low non-pack WR ~7–13% pulls overall down to ~50%).

**This is not caused by eff_attr=7.** It was present in B10.2 (smoke mode masked it: seed-43 smoke also showed hybrid_mage at 70.3% vs 50% target). Full regen at scale reveals the structural issue.

**Knight-rider decision required:**
1. **Option 1 — Adjusted target**: change convergence target from 50% overall → ~75% overall (accounts for pack fight win-rate floor, achieves 50% non-pack WR)
2. **Option 2 — Converge on non-pack WR only**: exclude pack fights from binary search; use non-pack win rate as the convergence signal

Gamora recommendation: Option 2. Pack fights signal AOE advantage differential (by design), not difficulty tier — they shouldn't drive modifier convergence.

**V1 KPM flag (per dispatch mandate):**
Aggregate KPM increased 75% (1.6→2.8). Exceeds 15% threshold → flagged. Root cause same as above (pack fights inflate aggregate KPM). Non-pack KPM decreased 25% (1.6→1.2). Recommendation: accept KPM flag as structural artifact; use non-pack KPM as the comparable metric going forward.

### Commits

- `18e45ef` — B10.4 calibration + math note + gauntlet §14 + decisions-log
- `6653666` — commit hash fix in decisions-log
- `d6002bf` — AGENT_STATE update
- [pending] — gauntlet §14.6 blocking finding + this completion record
