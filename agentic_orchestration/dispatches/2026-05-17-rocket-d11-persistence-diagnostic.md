# 2026-05-17 — rocket — D11 persistence-routing diagnostic (verify tax actually wrote to per-class JSONs)

**Authority:** Matt L3 2026-05-17 late evening — gandalf D11 post-mortem (background agent) flagged potential persistence routing bug: per-class JSON shows `damage_multiplier = 1.000` despite manifest claiming `post_process_d11: True`. The 6% v1.13 convergence may be partially conflated with a persistence bug, not a magnitude failure. Matt selected hybrid path γ: diagnose persistence first, then decide whether to fire Option B (α=0.08 + ceiling=10), Option C-prime (ceiling-primary with α≤0.05), or D11.2 redesign.
**Type:** Pattern A — ~30 min targeted file inspection + diagnostic report; no code changes; no salvage re-run unless bug confirmed and fix is trivial.
**Predecessor:** rocket v1.13 D11 implementation + v1.13.1 monster geometry backfill (both shipped).

---

## Why this matters

Gandalf post-mortem inspected `reincarnated-engine/output/standard-demo-regen-2026-05-17/season_002012/classes/class_0012.json` (his original Class C empirical anchor) and reported:
- Manifest claims `post_process_d11: True` + `schema_version: v1.8`
- Per-class JSON has **NO** `d11_post_process` field
- All skills still show `damage_multiplier = 1.000` (UN-taxed)

Your v1.13 math note § 3.2 specified **Site A application** (tax applied at kit-finalization, BEFORE balance loop, written to exported damage_multiplier values on skills). The empirical evidence above contradicts that claim.

Two possible explanations:
1. **PERSISTENCE BUG**: tax was computed correctly in-memory + balance-loop saw it + manifest marked post_process_d11=True, but the per-class JSON writer NEVER persisted the modified damage_multiplier to disk. The 6% convergence is then real — but caused by INVISIBLE tax (manifest-only), not by α=0.07 being too small.
2. **DRAX CONSUMER ROUTING**: tax was persisted to a DIFFERENT field or location than the per-class damage_multiplier (e.g., balance_metadata.element_coverage_tax_multiplier as a multiplier consumed at runtime, NOT a baked-in damage_multiplier value). The 6% convergence is then real but the math-note framing was misleading about where the tax lives in the data structure.

Either way: this is a **critical diagnostic**. Wrong-interpretation here means we tune the wrong lever in D11.1.

---

## Required reading

1. **Your v1.13 math note** — `reincarnated-engine/output/standard-demo-regen-2026-05-17/D11-hybrid-mage-tuning-math-note-2026-05-17.md` (§ 3.2 application Site A; § 6.3 salvage strategy; what was SUPPOSED to be written)
2. **Your v1.13 implementation** — `scripts/d11_post_process_salvage.py` (locate the actual write path; identify which fields get written and where)
3. **Empirical inspection target** — `reincarnated-engine/output/standard-demo-regen-2026-05-17/season_002012/classes/class_0012.json` (gandalf's anchor)
4. **Manifest** — `reincarnated-engine/output/standard-demo-regen-2026-05-17/season_002012/manifest.json` (post_process_d11=True; schema_version=v1.8)
5. **Salvage summary** — `reincarnated-engine/output/standard-demo-regen-2026-05-17/d11_salvage_summary.json` (per-instance pre/post WR; expected reflection of actual tax applied)
6. **Monolithic classes.json** — `reincarnated-engine/output/standard-demo-regen-2026-05-17/season_002012/classes.json` (demo consumes this; check whether tax shows here)
7. **Demo public/seasons** — `reincarnated-demo/public/seasons/season_002012/classes.json` (what drax-demo actually consumes; should mirror engine output)

---

## Scope — six diagnostic checks

### Check 1 — Per-class JSON inspection (gandalf's anchor)

Read `season_002012/classes/class_0012.json`:
- Does the class have `archetype_tag: hybrid_mage`?
- Does the file have a `d11_post_process` field at class level? Or `element_coverage_tax_*` fields?
- For each skill in `class_0012.skills[]`: report `damage_multiplier` value
- Compute expected post-tax value: if class has n_elements=3, expected damage_multiplier on damage-bearing skills = baseline × (1 - 0.07 × max(0, 3-2)²) = baseline × 0.93. If baseline was 1.000, expected = 0.930.

Report: actual vs expected; gap = persistence bug evidence

### Check 2 — Monolithic classes.json inspection

Read `season_002012/classes.json` (monolithic; demo consumes this):
- Find the same hybrid_mage class entry
- Same damage_multiplier comparison
- Determine whether per-class file and monolithic file have consistent values (could be different routing)

### Check 3 — Salvage summary cross-reference

Read `d11_salvage_summary.json`:
- Does it show pre-D11 WR vs post-D11 WR for class_0012?
- Was the WR delta computed in-memory only, or by re-running balance loop on persisted tax values?
- If WR shifted (e.g., pre=0.85 → post=0.79 = -7% damage reduction effect), tax was applied SOMEWHERE in the pipeline; question is whether at runtime (in-memory) or persisted to disk

### Check 4 — Trace the write path

Read `scripts/d11_post_process_salvage.py`:
- Identify where the function writes per-class JSON files
- Identify where the function writes monolithic classes.json
- Identify where the function applies tax to damage_multiplier
- Determine: does the apply-tax mutation propagate to BOTH per-class AND monolithic file writes? Or only one? Or only in-memory?

### Check 5 — Balance loop consumption path

Quick check: does `balance_loop.py` (gamora's seam) consume tax via:
- (a) Reading `damage_multiplier` directly from kit (in which case persistence to per-class JSON matters)
- (b) Reading `balance_metadata.element_coverage_tax_multiplier` and applying at runtime (in which case persistence layout differs from math-note § 3.2 claim)
- (c) Both / hybrid

This determines whether the "Site A" claim in the math note is technically correct (even if the per-class JSON values look untaxed, the runtime application would still produce post-tax WR — and the 6% convergence is real).

### Check 6 — Demo public/seasons sync

Read `reincarnated-demo/public/seasons/season_002012/classes.json`:
- Does it have post-D11 damage_multiplier values?
- Was it overwritten by rocket v1.13.1 monster backfill? Check git log or file mtime
- Is what drax-demo actually serves matching what the engine claims to have produced?

---

## Diagnostic verdict format

Output one of:
- **PERSISTENCE BUG CONFIRMED** — per-class and/or monolithic JSON have damage_multiplier=1.000 (UN-taxed) on damage-bearing skills of hybrid_mage classes. Tax was computed in-memory + WR effect visible in salvage_summary BUT never written to disk. Fix path: amend `d11_post_process_salvage.py` to persist tax mutation to per-class + monolithic; re-run salvage on 5 seasons; sync to demo.
- **PERSISTENCE OK; TAX LIVES IN BALANCE_METADATA** — Tax is persisted to a field other than `damage_multiplier` (e.g., `balance_metadata.element_coverage_tax_multiplier` runtime multiplier). Math note § 3.2 framing was technically incorrect (said Site A; actually Site B at runtime). The 6% convergence is real but caused by tax MAGNITUDE not persistence routing. Recommendation: clarify math note framing; original convergence miss interpretation stands.
- **PERSISTENCE OK; TAX BAKED INTO damage_multiplier** — Per-class JSON SHOULD show 0.93 multipliers; gandalf's inspection of class_0012 may have been on a wrong class (non-hybrid_mage; n=2 elements; un-taxed by design). Report which class he likely inspected vs what he should have inspected. The 6% convergence is real.
- **MIXED / UNEXPECTED FINDING** — describe what was found

For each verdict, document:
- What was inspected
- What was found
- Evidence (file paths + specific field values)
- Fix path (if bug) OR clarification path (if math-note framing was misleading)
- Estimated effort to remediate

### Deliverable: diagnostic report

Author `reincarnated-engine/output/standard-demo-regen-2026-05-17/D11-persistence-diagnostic-2026-05-17.md`:

1. § 0 TL;DR verdict (one of the four above)
2. § 1 Per-class JSON inspection (Check 1)
3. § 2 Monolithic classes.json inspection (Check 2)
4. § 3 Salvage summary cross-reference (Check 3)
5. § 4 Write-path trace (Check 4)
6. § 5 Balance loop consumption (Check 5)
7. § 6 Demo public/seasons sync (Check 6)
8. § 7 Fix path (if bug) — concrete code-level recommendation
9. § 8 Implication for D11.1 (does Option B / Option C-prime / D11.2 framing change?)
10. § 9 HANDOFF → knight-rider (determines whether to halt D11.1 queue OR resume) + → matt (decision after diagnostic)

---

## Out of scope (DO NOT)

- ❌ DO NOT fix the bug yet — diagnostic + report only; Matt approves fix path
- ❌ DO NOT re-run salvage (diagnostic only; no full re-process)
- ❌ DO NOT modify any code beyond minimal print/inspect helpers if needed
- ❌ DO NOT touch v1.13 outputs (preserve state for further inspection)
- ❌ DO NOT pre-empt D11.1 framing change — your diagnostic INFORMS the next sprint dispatch; doesn't author it

---

## Acceptance criteria

- [ ] Diagnostic report authored at `reincarnated-engine/output/standard-demo-regen-2026-05-17/D11-persistence-diagnostic-2026-05-17.md`
- [ ] All 6 checks completed (per-class JSON, monolithic, salvage summary, write path trace, balance loop consumption, demo sync)
- [ ] One of four verdicts assigned with evidence
- [ ] Fix path documented (if bug) OR clarification documented (if framing-only)
- [ ] § 8 implication for D11.1 explicit (do we proceed with Option B as authored? Switch to C-prime? Different path?)
- [ ] PRE-SIGNAL § 14.1.1 before hive-log
- [ ] Hive-log STATE
- [ ] No tag (diagnostic; not code change)
- [ ] HANDOFF → knight-rider with auto-fire control instruction (resume D11.1 queue / halt + redirect / etc.)
- [ ] Append diagnostic-completion record to this dispatch

---

## Coordination

- **HALTS:** jack-ryan D11.1 Gate-1 + rocket D11.1 auto-fire queue PENDING your verdict
- **Parallel-safe with**: gamora D11.1 math note (in flight; will complete with current ENDORSE framing regardless; if your diagnostic changes the picture, gamora's output may need amendment)
- **Parallel-safe with**: legolas-4 audio crawl (in flight); D11.1 sprint chain (gated on diagnostic)
- **PRE-SIGNAL § 14.1.1** before hive-log

---

*Dispatched 2026-05-17 by knight-rider per Matt L3 hybrid-path γ + gandalf STOP verdict + persistence-bug hypothesis. ~30 min. Append diagnostic report when done. D11.1 queue gated on your verdict.*

---

## Completion record

**Completed:** 2026-05-17
**Agent:** rocket
**Duration:** ~30 min (all 6 checks; read-only; no code changes; no salvage re-run)

**Verdict: MIXED / UNEXPECTED FINDING**

Two distinct persistence failures; no fundamental pipeline corruption.

**Finding 1 — Per-class files stale (low severity):**
`season_002012/classes/class_0012.json` shows `damage_multiplier = 1.000` on all skills. This is a D10-era snapshot. The D11 salvage script (`d11_post_process_salvage.py`) writes ONLY the monolithic `classes.json` and never updates the per-class `classes/<id>/class_XXXX.json` files. Gandalf inspected the wrong file. The per-class files are not consumed by any production pipeline (balance loop, demo).

**Finding 2 — Demo sync is pre-D11 (medium severity):**
`reincarnated-demo/public/seasons/season_002012/classes.json` (mtime 18:10) was written BEFORE the D11 salvage completed (engine monolithic written at 18:41). Demo serves un-taxed kits with `damage_multiplier = 1.000`.

**Finding 3 — Monolithic pipeline is correct:**
Engine `season_002012/classes.json` shows `damage_multiplier = 0.93` on all 5 damage-bearing skills of class_0012. `element_coverage_tax` provenance is present and correct. Balance loop consumed the taxed kit (Site A confirmed — tax baked into Skill.damage_multiplier, not applied at runtime).

**Finding 4 — 6% convergence is real magnitude failure:**
Tax alpha=0.07 is genuinely insufficient. 1/17 hybrid_mage converged (season_002011 class_0001 with n_elements=2 and tax_multiplier=1.0 — effectively untaxed). All 16 floor-pinned instances had n_elements=3 and tax_multiplier=0.93; none converged.

**Deliverable:** `reincarnated-engine/output/standard-demo-regen-2026-05-17/D11-persistence-diagnostic-2026-05-17.md`

**HANDOFF → knight-rider:** RESUME D11.1 queue. D11.1 Option B (alpha=0.08 + ceiling=10) is correct path. Fixes A (per-class file update) and B (demo sync) are post-D11.1 cleanup items requiring Matt approval.

**No tag** (diagnostic only; no code change).
