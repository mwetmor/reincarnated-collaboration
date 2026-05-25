# knight-rider — Cycle 11 kicker (v1 implementation push)

> **Authored:** 2026-05-25 (same-session as Cycle 10 close + Matt log-back decisions)
> **Author:** gandalf (story-and-design steward)
> **Authority:** Matt 2026-05-25 — 7-decision log-back ratification captured at `agentic_orchestration/matt-log-back-decisions-2026-05-25.md`
> **For:** knight-rider next session (Cycle 11 entry)
> **Length:** minimal — scope-doc + decisions-capture do the heavy lifting

---

## The kicker — paste into KR session-open

**Open Cycle 11 — v1 implementation push.** This is the post-Cycle-10 work cycle. Cycle 10 substrate-curation is FULLY CLOSED (tag `v1.0-weapon-substrate-cycle-10-shipped` cut + pushed). v1_scope = 2,293 LOCKED as v1 substrate.

**Before firing anything, read the new authority-of-record:**

1. Your OP step 5a (MANDATORY): `agentic_orchestration/cycles/cycle-11-hive-mind-scope.md` (RATIFIED 2026-05-25)
2. Matt's 7-decision capture: `agentic_orchestration/matt-log-back-decisions-2026-05-25.md` (RATIFIED; all 7 items)
3. Push posture for Cycle 11: **push-per-wave LIVE** (inherited from Cycle 10 pattern; Matt confirmed preference)

---

## Session-open entry-protocol actions (per hive-mind-protocol.md § 2.2)

Cycle 11 enters hive-mind state on this session-open. Per entry protocol:

**Step 4 — Create live state file** (REQUIRED at session-open before firing first Wave):
- Path: `agentic_orchestration/cycle-11-v1-implementation-push-state.md` (or KR's naming judgment using the Cycle-10 precedent pattern `<cycle>-<subject>-state.md`)
- Initial content: cycle metadata header (cycle # / subject / owner / authority / authoring agent / routing source / scope-doc path / entry path) per Cycle 10 state file precedent at `agentic_orchestration/weapon-substrate-curation-cycle-10-state.md` § 0
- Plus: Wave 0 placeholder + Day-1 parallel-fire intent + post-fire PID tracking template
- Auto-commit + push per scope-doc § 4 push-per-wave authorization

**Step 4.5 — Load hive-mind-protocol skill** alongside your OP per § 0 layering pattern (`agentic_orchestration/operating-procedures/hive-mind-protocol.md`).

**Step 5 — Fire Day-1 parallel dispatches per § "Cycle 11 work to fire" below.**

Distributed-protocol pattern note: Cycle 11 does NOT have a single monolithic `canonical/story/hive-mind-protocol-cycle-11.md` doc (the way Cycle 8 substrate-acquisition + QD-engine-rebuild had). Instead, the operational content is distributed across: this kicker (operational index) + scope-doc (autonomous-scope authority) + matt-log-back-decisions-2026-05-25.md (decision capture) + canonical reference docs (legolas methodology recommendation + drax scoping memo + skill-system § 8 + composition policy v1). Per hive-mind-protocol.md § 2.1 requirement (1), this distributed-protocol pattern satisfies the "canonical protocol doc" requirement in substance; future cycles may benefit from a thin "protocol stub" amendment to canonicalize the pattern.

---

## Cycle 11 work to fire

Per scope-doc § 1 + § 8 sequencing recommendation, fire the following in parallel where dependencies allow:

### Day 1 (immediate fires — zero or near-zero dependencies)

1. **Pre-migration mitigation dispatch → star-lord**
   - Apply `PRAGMA busy_timeout = 30000` in `~/Games/reincarnated-engine/src/reincarnated/telemetry/db.py` line 29
   - ~10 min star-lord work
   - Per Matt P2.5 authorization

2. **Decisions-log canonical-write batch → jack-ryan**
   - 2 enumerated entries per Matt P3 authorization:
     - "Stage 3.5 GF-5*/GF-6* defensive amendment per substrate-tagging-artifact rep-audit" (per gandalf SO-3 verdict 2026-05-25)
     - "Discipline #25 operational examples: Karna Tank EX + Quetzalcoatl AIM-68" (per gandalf SO-3 § 8.2)
   - Plus terminology cleanup: Cycle 10 scope-doc § 0 "Sidecar A" terminology gap (jack-ryan judgment on accept-document vs scope-doc update)
   - ~1-2 hours jack-ryan work

3. **Drax M4 dispatch → drax**
   - Attribute coupling labels in stats display (no dependencies; cosmetic; data already present)
   - ~0.25 day drax work

4. **Star-lord schema extensions dispatch → star-lord**
   - 4 fields added to class JSON export:
     - `t4_alteration_output` (gates Drax M3 / M6)
     - `main_weapon` (gates Drax M1)
     - `secondary_item` (gates Drax M2; itself gated on Sidecar B completion which IS already done as of Cycle 10 close)
     - `source_library` (gates Drax M5; small field pass-through)
   - ~1.75-3.25 days star-lord work
   - Per drax loadout scoping memo § 4.3

5. **Rocket Algorithm § 8 implementation dispatch → rocket**
   - Implement scored-candidate strategy registry per legolas methodology recommendation § 3
   - **v1 scope: 6 sim-extension-free strategies** (Natural Subset per Matt P2b "Confirm minima"):
     1. Resource-conversion (Blood Magic class)
     2. Trade-off (Resolute Technique class)
     3. Element-conversion (Avatar of Fire class)
     4. Defensive-conversion (Iron Reflexes class)
     5. Geometry-collapse / Concentrated Effect (range-for-amplitude trade)
     6. (verify exact 6th item from legolas methodology recommendation § 3.4 — likely resource-conversion variant OR conditional-modifier-light)
   - 4 deferred to v1.1: resource-buffer / mechanic-replacement / zone-control / conditional-modifier-full
   - proxy-spawn remains v1.1+ deferred
   - **MANDATORY prerequisite per Discipline #18 + #19.1:** BC-shift validation sweep BEFORE broader rocket commitment fires
     - ~200-300 min compute on 10-15 kits per legolas § 5
     - Cheapest-refuting-test: if validation surfaces "poor differentiation," escalate to Matt before continuing
   - Rocket effort: ~1-2 weeks
   - Spirit-guide explainer pattern (skill-system § 9) template authoring is parallel gandalf work (post-Cycle-11 canonical authoring queue; not blocking rocket § 8)

### Day 4-7 (after star-lord schema lands)

6. **Drax M1 / M2 / M5 dispatch → drax**
   - M1 — Main weapon field + WeaponSlot display component (~1 day)
   - M2 — Off-hand item field + OffHandSlot display component (~1 day)
   - M5 — Provenance flag display badge (~0.25 day)
   - Gated on star-lord schema extension

### Day 10-21 (after rocket § 8 + star-lord schema land)

7. **Drax M3 / M6 dispatch → drax**
   - M3 — T4 alteration output + SkillTree rendering (~1.5 days)
   - M6 — T4 comparison panel for post-mortem authoring (~1.5 days; toggle display per Matt Q2)
   - Gated on rocket § 8 implementation + star-lord schema

8. **T4 post-mortem readiness milestone** — KR drafts wind-down summary at known path; surfaces for Matt log-back per discipline pattern

---

## Drax memo Q1-Q5 RATIFIED (per Matt P2c "Approved")

When firing drax M1-M6 dispatches, reference these locked decisions:

- **Q1** — v1_scope flag kept internal; provenance badge visible (not raw boolean)
- **Q2** — T4 comparison panel uses **toggle** display (mobile-friendly)
- **Q3** — T4 post-mortem proceeds with **main weapon only**; off-hand display for v1.0 production launch
- **Q4** — `/the-work` analytics suite remains in scope for post-T4-post-mortem implementation wave
- **Q5** — Vercel deploy: **preview-only** for T4 post-mortem (production deploy ADR-006 trigger deferred until post-mortem closes)

---

## What Cycle 11 does NOT include (DO NOT autonomously fire)

Per scope-doc § 5:
- **Pi infrastructure execution** (Matt "right moment" deferral; NOT in Cycle 11)
- **Hosted-Postgres setup for loadout DB** (deferred per Matt P2a; NOT in Cycle 11)
- **Tailscale install G11** (Matt 15-min window; independent of Cycle 11; can fire any time)
- **D9 LLM cache build** (G12 NOT TRIGGERED; D9 DEFERRED per Matt P2d)
- **Algorithm § 8 v1.1 strategies** (4 sim-extension-required + proxy-spawn; gated on sim seam refactor)
- **Loadout v1.1+ items D1-D13** (per drax memo § 4.2)
- **W1.13 hypothesis testing re-fire** (chain blocked; gamora awaits prereq resolution; do NOT autonomously re-fire — that's a fresh Matt-authorization)
- **Architectural amendments** to canonical docs (gandalf authors; Matt ratifies)
- **Scope amendments to Cycle 11** (e.g., expanding Algorithm § 8 to v1.1 strategies; changing M1-M6 list; firing infrastructure work early)
- **Final Cycle 11 tag** (Matt ratifies before tag cut — UNLESS skip-confirmation directive re-authorized at wind-down)

---

## Narrow escape hatches — DO ask Matt BEFORE firing IF:

Per scope-doc § 5 + § 6:
- Algorithm § 8 BC-shift validation sweep returns "poor differentiation" (architecture doesn't differentiate keystones meaningfully)
- Rocket § 8 implementation surfaces that one of the 6 "sim-extension-free" strategies actually requires sim hooks (genuine boundary issue)
- P2b "Confirm minima" ambiguity surfaces — if downstream work suggests Matt may have meant MINIMAL cherry-pick (3-4 strategies) instead of Natural Subset (6), route back BEFORE rocket § 8 implementation dispatch fires
- Mac mini kernel panic recurs during sustained Cycle 11 workload; PRAGMA busy_timeout mitigation insufficient → may trigger "right moment" infrastructure escalation
- Star-lord schema extension surfaces backwards-compat breaking change
- Catastrophic specialist failure that cross-seam collaboration can't resolve

---

## Discipline-test framing (Cycle 11)

This is the **second test** of the hive-mind-scope-discipline pattern. Cycle 10 PROVEN EFFECTIVE (zero ask-safety pauses; zero Matt mid-cycle escalations). Cycle 11 is the first PROSPECTIVE test (Cycle 10 was founding retroactive instance).

**Anti-pattern to actively avoid:** treating the scope-doc as exhaustive whitelist. Items NOT enumerated default to **in-scope per scope-discipline § 5.3** — fire forward via hive-mind decision-routing § 4 (seam-owner-first sub-agent invocation); flag the gap for next-cycle scope-doc refinement. Ambiguity does NOT default to ask.

**Skip-confirmation fire-forward pattern:** Cycle 10 demonstrated this works for cycle wind-down. For Cycle 11, KR can use the same pattern at wind-down IF Matt re-authorizes at that time (NOT automatic; the skip-confirmation authorization was Cycle-10-specific per the original directive). Default: KR drafts wind-down summary + proposes final-tag; Matt ratifies on log-back (~15 min target unless skip-confirmation re-authorized).

---

## When to ask Matt (this cycle)

- Architectural amendments to canonical docs
- Scope amendments to Cycle 11 (adding new workstreams; expanding § 8 to v1.1; changing M1-M6)
- Cross-cycle commits (W1.13 re-fire; Pi infrastructure; hosted-Postgres setup; Cycle 12 prep)
- ADR-002 tier-2/3 decisions
- Final Cycle 11 tag (unless skip-confirmation re-authorized at wind-down)
- The narrow escape-hatches enumerated above

## When NOT to ask Matt (this cycle)

- Anything in scope-doc § 1-3 (dispatch authoring, sub-agent sequencing, Wave-handling, intermediate tags, state-file updates, Gate-1 coordination, routine commits, per-wave pushes)
- Pre-resolved known-unknowns per scope-doc § 6
- Drax memo Q1-Q5 questions (RATIFIED per Matt P2c "Approved")
- Sequencing decisions for parallel sub-agent work (KR discretion)
- Unenumerated decisions where seam-routing applies — fire forward

---

## Cycle 11 wall-clock estimate

~3 weeks to T4-post-mortem readiness (per drax memo § 4.3 + legolas § 6).

| Workstream | Duration |
|---|---|
| Pre-migration mitigation (star-lord) | ~10 min |
| Decisions-log batch (jack-ryan) | ~1-2 hrs |
| Drax M4 | ~0.25 day |
| Star-lord schema extensions | ~1.75-3.25 days |
| Rocket § 8 implementation (6 strategies + BC-shift validation) | ~1-2 weeks |
| Drax M1/M2/M5 (after schema) | ~2.25 days |
| Drax M3/M6 (after rocket § 8) | ~3 days |
| **Total wall-clock to T4 readiness** | **~3 weeks** |

---

## Companion docs

### Authority-of-record (MANDATORY reads)
- **`agentic_orchestration/cycles/cycle-11-hive-mind-scope.md`** — Cycle 11 autonomous scope (per OP § 1 step 5a)
- **`agentic_orchestration/matt-log-back-decisions-2026-05-25.md`** — Matt's 7 decisions captured
- **`agentic_orchestration/operating-procedures/hive-mind-scope-discipline.md`** — the discipline

### Reference for Cycle 11 dispatches
- `agentic_orchestration/legolas/research/algorithm-section-8-methodology-consult-2026-05-25/methodology-recommendation.md` — rocket § 8 implementation brief
- `agentic_orchestration/drax/notes/2026-05-25-loadout-app-readiness-scoping.md` — drax M1-M6 implementation brief + Q1-Q5 ratified
- `agentic_orchestration/dispatches/2026-05-25-star-lord-g1-infrastructure-measurement.md` — G1 findings (informs pre-migration mitigation context)
- `canonical/story/skill-system-2026-05-24.md` § 8 — Algorithm § 8 architecture (rocket implementation reference)
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` — v1 substrate scope (Cycle 10 output now LOCKED)
- `canonical/story/infrastructure-raspberry-pi-postgres-and-closed-loop-pipeline-2026-05-25.md` — Pi recognition record (P2a deferred-execution context)

### Operational
- `agentic_orchestration/operating-procedures/knight-rider.md` (your OP; session-start protocol § 1 includes step 5a mandatory scope-doc read)
- `agentic_orchestration/operating-procedures/hive-mind-protocol.md` § 2.2 + § 4 (entry protocol + decision routing)
- `CLAUDE.md` § "Team commit + push discipline" — team-level commit/push addendum
- `agentic_orchestration/cycle-10-wind-down-summary-2026-05-25.md` — prior cycle close context

---

## Closing

Cycle 10 PROVEN EFFECTIVE; Cycle 11 inherits the discipline. Scope-doc ratified. Push-per-wave authorized. 8 dispatches enumerated for parallel firing per § 8 sequencing.

Fire forward. Drive to T4-post-mortem readiness milestone (~3 weeks wall-clock).

**Confirm understanding** (brief acknowledgment that scope-doc + decisions-capture + § 8 sequencing recommendation is read), **then operate.**

---

**Drafted by:** gandalf 2026-05-25 (same-session as Cycle 10 close + Matt log-back decisions)
**For Matt to relay** to knight-rider next session-open. Knight-rider's response shape: read scope-doc + decisions-capture + kicker → confirm understanding → fire Day-1 parallel dispatches → drive forward through Cycle 11 toward T4 readiness.
