# Finding — 2026-05-25 — Cycle 11 Wave 3b — drax M3 + M6 T4 display

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-AMENDMENTS (two INFO items; no WARN; no BLOCK)
**Target:** `drax/v0.1-cycle-11-m3-m6-t4-display-wave-3b-2026-05-25` @ commit `b948d3d`
**Developer:** drax
**Principles applied:** 1 (math-before-code), 2 (smoke-gate), 3 (cross-seam round-trip), 4 (decisions-log), 5 (severity), 6 (round-trip discipline)

---

## Verdict

**PASS-WITH-AMENDMENTS.** Two INFO items recorded; no findings block Cycle 11 final tag cut. Drax may note and track; no rework required before tag.

---

## Principle-by-principle review

### Principle 1 — Math-before-code

No new math in this deliverable. Drax is consumer-side display; all math (η-scoring, strategy selection, BC-axis prediction) resides in rocket §8. The dispatch explicitly confirmed: "No new math — consumer side." Criterion met.

### Principle 2 — Smoke-gate before commit

Smoke evidence is present and sufficient:

- `npm run build`: 773 modules, 0 TypeScript errors — PASS
- Cycle-11+ path (class_0001 sample fixture): RESOURCE_CONVERSION alteration renders M3 panel + M6 toggle + spirit-guide narration — PASS
- Null-case path: all 11 real seasons (no `t4_alteration_output`) — both panels hidden, no broken UI — PASS
- M6 toggle: collapsed by default; expands to show current strategy (violet "selected" badge) + 4 static alternative rows + footer note — PASS

Discipline #11 (empirical inspection over assumption): drax ran actual null-case verification against 11 real seasons, not assumed behavior. This is the correct level of evidence for a null-safe claim.

### Principle 3 — Cross-seam round-trip

Round-trip not applicable — confirmed by dispatch and by drax's own completion record. Drax is the consumer side of star-lord Wave 1 round-trip (already PASSED 79/79). No schema change initiated by drax. Criterion met.

### Principle 4 — Decisions-log single source of truth

All decisions drax made (M3 position below tree; narration woven into M3; M6 toggle pattern; M6 current-only with v1.1 placeholder; `thematic_rationale` primary / §9 template fallback) are within drax's dispatch-granted design-judgment discretion. None conflict with locked decisions-log entries. The Tier 2 framing (intent metadata, defer wire-up to Cycle 12 Layer 6) is correctly carried forward from Matt's P2c ratification. Criterion met.

### Principle 5 — Severity classification

Applied per findings below.

### Principle 6 — Cross-seam round-trip discipline

No cross-seam contract change from drax. The completion record includes the required "Round-trip: not applicable" justification per Principle 6(ii). Criterion met.

---

## What I found

### Finding F1 — INFO — Commit title omits M6 scope

**Severity:** INFO

The commit message at `b948d3d` reads:

> `feat(drax-loadout): Cycle 11 Wave 3b M3 — T4 alteration panel + spirit-guide narration (MIGRATION.md v1.3)`

The commit actually contains five file changes: `T4AlterationPanel.tsx`, `T4ComparisonPanel.tsx` (M6), `SkillTree.tsx` (M3+M6 wiring), `src/data/types.ts` (T4AlterationOutput interface), and `data/sample-season/classes/class_0001.json` (smoke fixture). M6 (`T4ComparisonPanel.tsx`) is fully present and functional; the title just doesn't name it.

**Rationale:** Discipline #10 (attribution clarity — change one thing, measure one thing) applies here in its documentation-corollary sense: the commit message is the attribution record for what changed. A message that omits M6 creates a future archaeology gap if someone bisects this range. This does not affect the tag or Cycle 11 close; it is recorded for hygiene.

**Cite:** Discipline #10; Discipline #11 (empirical inspection — jack-ryan verified directly via `git show b948d3d --name-only`)

**Action:**
- [ ] drax: no immediate action required. At next convenient commit in this seam, ensure multi-component commits enumerate components in the title or body. No rework on `b948d3d` needed.

---

### Finding F2 — INFO — Smoke fixture TODO is acceptable deferred work

**Severity:** INFO

The sample-season `class_0001.json` was patched with a synthetic `RESOURCE_CONVERSION` alteration (including `thematic_rationale`) to enable smoke verification. The patch is tagged `TODO(drax)` in the dispatch completion record: "remove sample-season `t4_alteration_output` fixture from `class_0001.json` when rocket §8 regen ships."

This is acceptable at v1. The dispatch explicitly authorized this pattern. The fixture does not affect production behavior (real seasons have `t4_alteration_output: null`). It is the correct instrument for smoke-validating the display path before rocket §8 regens produce live data.

**Rationale:** Discipline #11 (empirical inspection): fixture is required because no live season carries `t4_alteration_output` yet. Without it, smoke-testing the populated path is impossible. The alternative (wait for rocket §8) would have blocked Wave 3b unnecessarily.

**Cite:** Discipline #11; Dispatch open-question resolution (smoke fixture TODO accepted as INFO-level deferred per dispatch §"Cross-cutting")

**Action:**
- [ ] drax: remove `t4_alteration_output` fixture from `class_0001.json` when rocket §8 regen ships and a real season is available as test fixture. Already tracked in loadout AGENT_STATE.md.

---

## Tier 2 framing compliance (PRIMARY scrutiny target)

This is the central Gate-2 check for this deliverable. Verdict: **COMPLIANT**.

### M3 T4AlterationPanel

- **"Build Identity" badge:** present in header strip. Tooltip reads: "Tier 2 framing: intent metadata — not yet wired to combat arithmetic (Cycle 12 Layer 6)." This is precise. It does not promise combat effect; it positions the alteration as design-side identity.
- **Strategy descriptions:** reviewed all 5 static entries. Language analysis:
  - RESOURCE_CONVERSION: "altering how your skills draw from your body and spirit rather than from a standard mana pool. The cost of power becomes something more personal." — Tier 2 compliant. No "deal more damage" claim. "Something more personal" is flavor, not mechanical promise.
  - TRADE_OFF: "gaining exceptional strength in one dimension by accepting a corresponding weakness in another. Power through sacrifice." — Compliant. Trade-off framing is correctly bidirectional; no net-gain overclaim.
  - ELEMENT_CONVERSION: "converting all damage output to a single element — overriding the kit's natural elemental spread for focused resonance. Every strike speaks the same language." — Compliant. Does not claim the conversion produces more damage. "Focused resonance" is aesthetic.
  - DEFENSIVE_CONVERSION: "reframes your survival layer — converting standard armor or regeneration into an alternate defensive geometry. How you endure changes how you fight." — Compliant. "Reframes" and "changes how" language. No "increases your defense by X" claim.
  - GEOMETRY_COLLAPSE: "collapses spatial diversity into concentrated geometry — trading attack-pattern variety for unified, amplified impact within a single pattern." — This entry uses "amplified impact." That phrase walks the line. In context — "within a single pattern" qualifies it as spatial narrowing, not damage amplification — it reads as trade-off language, not overclaim. Acceptable at INFO level only.

- **η-score display:** shown as `η {etaScore.toFixed(2)}` with tooltip "η-score: alteration candidacy score from Algorithm §8". This is correctly positioned as a score (selection signal), not a combat modifier. Compliant.

- **Parameter display:** strategy-specific params (cost_resource, target_element, etc.) rendered as factual key-value pairs. No combat-arithmetic claims attached. Compliant.

- **BC axes display:** shown as chips with tooltip "BC axis predicted to shift when alteration is active." The word "predicted" is load-bearing here — it correctly honors Tier 2 framing. Not "BC axes that WILL shift." Compliant.

- **Spirit-guide narration fallback template:** The fallback text reads: "Summoner, you may have noticed — your spirit has unlocked something truly unique and meaningful. This {strategyLabel} defines how your entire kit operates at its peak. If you would like a walkthrough, I can explain how to help them make the most out of it." — This tracks §9.2 template precisely. "Defines how your entire kit operates" could be read as a strong mechanical claim, but in context (§9 intent: the spirit guide is an in-fiction explainer, not a tooltip) it functions correctly as narrative introduction. Per §9 design authority, this framing is intentional. Compliant.

### M6 T4ComparisonPanel

- **"Intent Metadata" header label:** present in panel header. Exact string: "Intent Metadata". Dispatch required this. Present.
- **"Cycle 12 Layer 6 wire-up" footer citation:** panel footer reads: "v1.1 will surface actual candidate scores + per-candidate thematic rationale when rocket §8 multi-candidate output ships." This correctly defers live scoring to a future version. The header separately cites "Algorithm §8 — Candidate Strategy Comparison" + "Intent Metadata" tooltip: "Tier 2 framing: intent metadata — post-mortem evaluation of alteration selection." Together these honor the Tier 2 framing correctly.
- **Alternative strategy descriptions in M6:** brief descriptions ("Skills draw from HP or a non-standard pool. Higher risk, higher reward." etc.) are intentionally sparse. No η-scores for alternatives — shown as `v1.1` placeholder. This is correct per dispatch open-question resolution (current-only with v1.1 placeholder). Compliant.
- **Q2 TOGGLE:** toggle button with ▶ chevron, `closed by default` via `useState(false)`. `aria-expanded={open}` present. Mobile-friendly text tap target. Q2 RATIFIED requirement met.
- **Q3 main-weapon-only:** no off-hand surface in M6. Verified by code inspection. Q3 RATIFIED requirement met.
- **"GEOMETRY_COLLAPSE amplified" language in M6:** M6 uses a shorter brief: "Spatial diversity collapses to concentrated geometry. One pattern, amplified." Same "amplified" word. Same INFO-level note as M3 above — acceptable in trade-off framing context.

---

## Schema round-trip verification (Principle 3 / Discipline #8)

### Python AlterationOutput vs TypeScript T4AlterationOutput

Python dataclass (`mechanic_alteration.py` lines 75-101):
```
strategy_type: str
strategy_params: dict
applied_axis_targets: list
eta_score: float
thematic_rationale: str
```

TypeScript interface (`src/data/types.ts`):
```typescript
interface T4AlterationOutput {
  strategy_type: T4StrategyType;           // maps str → union type
  strategy_params: Record<string, string | number | boolean | null>;  // maps dict
  applied_axis_targets?: string[];          // maps list (optional-guarded)
  eta_score?: number;                       // maps float (optional-guarded)
  thematic_rationale?: string | null;       // maps str (optional-guarded)
}
```

**Field-name alignment:** exact match on all 5 fields. `strategy_type`, `strategy_params`, `applied_axis_targets`, `eta_score`, `thematic_rationale`. No rename drift.

**Type alignment:** all types map correctly (str → string, dict → Record, list → string[], float → number).

**Optionality direction:** TypeScript marks `applied_axis_targets`, `eta_score`, and `thematic_rationale` as optional. Python's dataclass declares them as required (no `Optional` type). This optionality asymmetry is intentional and correct — the JSON transport layer may have pre-§8 classes where these fields are absent. The TypeScript optional-guard is a defensive consumer pattern matching the MIGRATION.md v1.3 null-safe consumption guidance. Not a schema drift.

**6th strategy gap:** Python defines 6 strategy constants: RESOURCE_CONVERSION, TRADE_OFF, ELEMENT_CONVERSION, DEFENSIVE_CONVERSION, GEOMETRY_COLLAPSE, DEFENSIVE_TRADEOFF. The drax T4StrategyType union includes 5 named literals + `string` forward-compat. DEFENSIVE_TRADEOFF is NOT in the named union. This is handled by the forward-compat `| string` arm — the panel's `STRATEGY_LABELS` and `STRATEGY_DESCRIPTIONS` lookups will fall through to their `?? strategyType.replace(/_/g, ' ')` and generic fallback strings for DEFENSIVE_TRADEOFF. The display degrades gracefully (raw-enum-reformatted label; generic description). This is the correct behavior for a forward-compat arm. Recording at INFO — drax should add DEFENSIVE_TRADEOFF to STRATEGY_LABELS + STRATEGY_DESCRIPTIONS + T4ComparisonPanel's ALL_STRATEGIES when rocket §8 regen confirms this strategy ships in live data.

**Discipline #8 compliance:** TypeScript `T4AlterationOutput` interface, `ClassData.t4_alteration_output?: T4AlterationOutput | null` field, and the SkillTree.tsx `const t4Alteration = classData.t4_alteration_output ?? null` null-guard together implement schema validation at the consumer boundary. No runtime access to subfields without the top-level null check. Compliant.

---

## Finding F3 — INFO — DEFENSIVE_TRADEOFF strategy not in named label/description tables

**Severity:** INFO

Python's `mechanic_alteration.py` defines 6 strategies: the 5 in drax's `STRATEGY_LABELS` + `DEFENSIVE_TRADEOFF` (6th strategy per legolas methodology §3.4, confirmed at `STRATEGY_DEFENSIVE_TRADEOFF = "DEFENSIVE_TRADEOFF"`, class `DefensiveTradeoffStrategy`). Drax's `T4StrategyType` union and `ALL_STRATEGIES` array in T4ComparisonPanel omit DEFENSIVE_TRADEOFF. The forward-compat `| string` arm in T4StrategyType and the `?? strategyType.replace(/_/g, ' ')` fallbacks handle it gracefully — a class with DEFENSIVE_TRADEOFF will display "Defensive Tradeoff" label and the generic description. This is non-breaking but will produce a less polished display than the 5 explicitly-named strategies.

**Rationale:** Discipline #8 (schema validation at consumer boundary) — the schema is correct; the display tables are incomplete for the 6-strategy v1 set. Discipline #13a (implementation-vs-intent drift) — dispatch states 6 v1 strategies; drax implements labels/descriptions for 5.

**Cite:** Discipline #8; Discipline #13a; MIGRATION.md §v1.3 (strategy enum listed with 5 examples; 6th not called out in MIGRATION.md — this is also a MIGRATION.md gap, but MIGRATION.md is star-lord's seam, not a drax blocker)

**Action:**
- [ ] drax: when rocket §8 regen produces live DEFENSIVE_TRADEOFF classes, add DEFENSIVE_TRADEOFF to `STRATEGY_LABELS`, `STRATEGY_DESCRIPTIONS`, and `ALL_STRATEGIES` in both panels. Track in loadout AGENT_STATE.md under "outstanding TODOs." No rework needed before Cycle 11 final tag cut — forward-compat arm handles it gracefully.

---

## Null-safe handling verification

- `T4AlterationPanel` returns `null` immediately when `!alteration` — correct.
- `T4ComparisonPanel` returns `null` immediately when `!alteration` — correct.
- `SkillTree.tsx` gates both panels behind `{t4Alteration && ...}` — redundant double-guard but harmless.
- `alteration.strategy_params ?? {}` — null-coalesce on params dict before `.entries()` — correct.
- `alteration.applied_axis_targets ?? []` — null-coalesce on optional array — correct.
- `alteration.eta_score ?? null` — null-coalesce on optional float — correct.
- `alteration.thematic_rationale ?? null` — null-coalesce on optional string — correct.
- TypeScript interface marks all three optional fields (`applied_axis_targets`, `eta_score`, `thematic_rationale`) as `?` — type system enforces null-handling at compile time.
- The drax completion record claim "all 11 real seasons unaffected" is consistent with the null-case smoke result and the type-level enforcement. Accepted.

**Discipline #8 verdict:** PASS. Consumer boundary is correctly hardened.

---

## Engineering discipline compliance summary

| Discipline | Check | Result |
|---|---|---|
| #1 Math-before-code | No new math; consumer display only | PASS (N/A) |
| #8 Schema validation at consumer boundary | Null-guards present at all access points; TypeScript type-system enforcement | PASS |
| #10 Attribution clarity | Commit message omits M6 in title | INFO (F1) |
| #11 Empirical inspection over assumption | Smoke against 11 real seasons + sample fixture; null-case verified empirically | PASS |
| #13a Implementation-vs-intent drift | 5/6 strategies in label tables; DEFENSIVE_TRADEOFF handled by forward-compat arm only | INFO (F3) |
| #25 Semantic-layer rep-audit | Spirit-guide narration correctly positioned as semantic-layer explainer, not mechanical-layer combat claim; §9 template honors in-fiction register | PASS |

---

## References

- `agentic_orchestration/dispatches/2026-05-25-jack-ryan-cycle-11-gate-2-drax-wave-3b.md` (this dispatch)
- `agentic_orchestration/dispatches/2026-05-25-drax-cycle-11-m3-m6-t4-display-wave-3b.md` (drax dispatch + completion record)
- `agentic_orchestration/matt-log-back-decisions-2026-05-25.md` §P2c (Matt authorization + Q1-Q5 RATIFIED)
- `agentic_orchestration/cycle-11-v1-implementation-push-state.md` §Wave 3b (Tier 2 framing source)
- `/Users/admin/Games/reincarnated-loadout/src/components/SkillTree/T4AlterationPanel.tsx` (M3 source)
- `/Users/admin/Games/reincarnated-loadout/src/components/SkillTree/T4ComparisonPanel.tsx` (M6 source)
- `/Users/admin/Games/reincarnated-loadout/src/components/SkillTree/SkillTree.tsx` (M3+M6 wiring)
- `/Users/admin/Games/reincarnated-loadout/src/data/types.ts` (T4AlterationOutput interface)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/mechanic_alteration.py` (Python AlterationOutput dataclass; 6 strategy constants)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` §v1.3 Cycle 11 schema extensions
- `canonical/story/skill-system-2026-05-24.md` §9 (spirit-guide explainer pattern)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` #8, #10, #11, #13a, #25
