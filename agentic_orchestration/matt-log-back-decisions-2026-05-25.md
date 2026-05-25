# Matt log-back decisions — 2026-05-25

> **Status:** RATIFIED 2026-05-25 — Matt log-back response to wind-down summary + post-cycle dispatch returns
> **Captured by:** gandalf (Pattern-B dialogue capture)
> **Source dialogue:** Matt → gandalf 2026-05-25 session (decision-surface request + reply)
> **For:** knight-rider Cycle 11 kicker consumption + jack-ryan decisions-log batch source

---

## Context

Following Cycle 10 substrate-curation workstream FULLY CLOSED (KR autonomous run; discipline PROVEN EFFECTIVE), Matt logged back to triage the wind-down summary at `agentic_orchestration/cycle-10-wind-down-summary-2026-05-25.md` + 5 post-cycle dispatch returns. Gandalf surfaced 7 decision items as a single decision-surface; Matt replied with verbatim authorizations below.

---

## Decisions (per priority items P1-P3)

### P1 — Cycle 10 cycle-level final tag

**Matt:** "I already had KR commit/push. If the tag isn't cut yet I authorize that also."

**Status:** RATIFIED 2026-05-25 — tag `v1.0-weapon-substrate-cycle-10-shipped` cut + pushed to remote (anchored to commit `75a1891` KR wind-down FINAL).

**Verification (gandalf post-dialogue):**
- Tag exists locally: ✓
- Tag pushed to remote: ✓ (`refs/tags/v1.0-weapon-substrate-cycle-10-shipped` at `dbd879e`)
- Cycle 10 substrate-curation workstream OFFICIALLY CLOSED at git level

**Effect:**
- Recognition 1 (sampling-proportionality) migrates from v1.1+ flag → v1 LOCKED (per wind-down § 4 justification)
- Cycle 11 implementation push UNBLOCKED to fire
- T4 post-mortem critical-path begins (~3 weeks to readiness)

**Pattern observation:** Matt fired a KR session in parallel with this gandalf decision-surface dialogue; KR autonomously cut + pushed the tag. This is the discipline working — KR didn't wait for gandalf-dialogue to complete before acting on Matt's direct authorization.

---

### P2d — D9 LLM response cache

**Matt:** "I confirm."

**Decision:** D9 LLM response cache remains DEFERRED. G12 empirical gate did not trigger (0.13% repeat rate vs 20% threshold; structural cross-season zero collisions). No build action; no future commitment. Star-lord may re-measure G12 on a future cycle if LLM architecture shifts.

---

### P2.5 — Pre-migration mitigation (PRAGMA busy_timeout)

**Matt:** "I confirm."

**Decision:** Star-lord authorized to apply `PRAGMA busy_timeout = 30000` in `~/Games/reincarnated-engine/src/reincarnated/telemetry/db.py` line 29. Converts SQLite lock-busy failures from immediate-fail to wait-and-retry. Does not fix multi-writer architectural problem but eliminates immediate-failure symptom while Postgres migration remains deferred per P2a.

**Routing:** Knight-rider dispatches star-lord. ~10 min star-lord work. Auto-commit + auto-push per star-lord seam authorization.

---

### P3 — Decisions-log batch + housekeeping

**Matt:** "I authorize."

**Decision:** Jack-ryan authorized to canonical-write the following decisions-log entries (single batch dispatch):

1. **"Stage 3.5 GF-5*/GF-6* defensive amendment per substrate-tagging-artifact rep-audit"** — per gandalf SO-3 verdict 2026-05-25 (Pattern A-deep substrate-tagging routing decision; +Roland +Karna defensive additions)
2. **"Discipline #25 operational examples: Karna Tank EX + Quetzalcoatl AIM-68"** — per gandalf SO-3 § 8.2 + jack-ryan Wave 6 Gate-2 INFO Flag 2 (Mode-C bypass operational examples)

**Plus terminology cleanup:**
- Cycle 10 scope-doc § 0 "Sidecar A" terminology gap resolution — accept-document OR scope-doc update per jack-ryan judgment

**Routing:** Knight-rider dispatches jack-ryan canonical-write batch. ~1-2 hours jack-ryan work.

---

### P2a — D1 Infrastructure decision

**Matt:** "I confirm. We will find the right moment and then build the new raspberry pi server and postgres DB later on to solve. We can get the hosted version later on for the loadout also."

**Decision:** Hybrid path RATIFIED for the eventual infrastructure execution:
- **Pi-Postgres for engine-internal DBs** (telemetry, catalogue) — when built
- **Hosted-Postgres for loadout DB** (Vercel-reachable; G4 resolution) — when needed

**Execution timing:** DEFERRED to Matt's "right moment" — NOT in Cycle 11 scope. Infrastructure execution gates on Matt's separate authorization for the Pi build + the hosted-Postgres setup.

**G11 Tailscale install:** authorized (Matt's "find right moment" includes this); 15-min independent task; fires when Matt chooses.

**Status-quo continues** with PRAGMA busy_timeout mitigation (P2.5) covering the SQLite contention symptom until Postgres migration fires.

**Implication for v1 development:** all v1 work continues against current SQLite telemetry DB. If kernel panics recur during sustained Cycle 11 workloads (rocket § 8 implementation; loadout schema extensions), star-lord flags to KR for triage; if severity warrants, escalate to Matt for "right moment" trigger.

---

### P2b — Algorithm § 8 v1 implementation scope

**Matt:** "Confirm minima."

**Decision:** Natural Subset RATIFIED — **6 sim-extension-free strategies in v1**; 4 sim-extension-required strategies deferred to v1.1; proxy-spawn remains v1.1+ deferred per existing BC-axes-lock sim deferral matrix.

**The 6 v1 strategies (sim-extension-free; loadout-resolution layer only):**
1. Resource-conversion (Blood Magic class)
2. Trade-off (Resolute Technique class)
3. Element-conversion (Avatar of Fire class)
4. Defensive-conversion (Iron Reflexes class)
5. Geometry-collapse / Concentrated Effect (range-for-amplitude trade)
6. (sixth strategy per legolas methodology recommendation § 3.4 — KR to verify exact 6th item from research artifact)

**The 4 deferred to v1.1 (sim-extension-required):**
1. Resource-buffer (Mind Over Matter) — damage routing extension
2. Mechanic-replacement / leech-replaces-regen (Vaal Pact) — resolution extension
3. Zone-control (Death and Decay) — zone state tracking
4. Conditional-modifier (Pain Attunement / Heart Stopper) — per-tick evaluation

**Gandalf reading note on "Confirm minima":** interpreted as confirming Natural Subset of 6 (vs MINIMAL cherry-pick of 3-4). Reasoning: minima ≈ minimum scope; Natural Subset IS the minimum v1 scope that still meaningfully tests the architecture (FULL has 10; MINIMAL would have 3-4 cherry-picked). **If Matt intended MINIMAL cherry-pick to 3-4, KR routes back via Matt re-engagement before rocket § 8 implementation dispatch fires.**

**Routing:** Knight-rider dispatches rocket § 8 implementation against the 6 v1 strategies. Rocket effort estimate: ~1-2 weeks. Cheapest-refuting-test BC-shift validation sweep (~200-300 min compute) fires per Discipline #18 + #19.1 before broader commitment.

---

### P2c — Loadout app v1.0 implementation scope

**Matt:** "Approved."

**Decision:** All 6 MUST-HAVE items M1-M6 APPROVED; all 5 drax recommendations on Q1-Q5 APPROVED.

**M1-M6 (effort ~6 drax days + ~2-3.5 star-lord days + ~1-2 weeks rocket algorithm = ~3 weeks wall-clock):**
- **M1** — Main weapon field + WeaponSlot display component (~1 day drax; gated on star-lord schema extension)
- **M2** — Off-hand item field + OffHandSlot display (~1 day drax; gated on Sidecar B + star-lord schema)
- **M3** — T4 alteration output + SkillTree rendering (~1.5 days drax; gated on Algorithm § 8 implementation + star-lord schema)
- **M4** — Attribute coupling labels in stats display (~0.25 day drax; no dependencies; can fire immediately)
- **M5** — Provenance flag display (`engine_authored_gap_fill_v1` badge) (~0.25 day drax; gated on small star-lord schema extension)
- **M6** — T4 comparison panel for post-mortem authoring (~1.5 days drax; gated on M3 + algorithmic output in class JSON)

**Q1-Q5 ratified (drax recommendations):**
- **Q1** — v1_scope flag kept internal; provenance badge visible (not raw boolean)
- **Q2** — T4 comparison panel uses **toggle** display (cleaner on mobile)
- **Q3** — T4 post-mortem proceeds with **main weapon only**; off-hand display added for v1.0 production launch (post-Sidecar-B-loadout-integration)
- **Q4** — `/the-work` analytics suite remains in scope for post-T4-post-mortem implementation wave (well-specified; ready when star-lord data-manifest lands)
- **Q5** — Vercel deploy: **preview-only** for T4 post-mortem (production deploy ADR-006 trigger deferred until after post-mortem closes)

**Routing:** Knight-rider dispatches:
- drax for M4 immediately (no dependencies)
- star-lord for schema extensions (parallel with M4)
- drax for M1, M2, M5 after star-lord schema lands
- drax for M3, M6 after rocket § 8 implementation lands

---

## Cycle 11 implications summary

Per Matt's 7 decisions, **Cycle 11 (implementation push)** scope includes:

| Workstream | Owner | Effort | Critical path |
|---|---|---|---|
| Cycle 10 final tag cut + push | KR | <5 min | Pending P1 explicit confirm |
| Pre-migration mitigation (PRAGMA busy_timeout) | star-lord | ~10 min | No |
| Decisions-log batch | jack-ryan | ~1-2 hrs | No |
| Algorithm § 8 rocket implementation (6 v1 strategies) | rocket | ~1-2 weeks | YES (v1 T4 critical path) |
| BC-shift validation sweep (cheapest-refuting-test) | rocket | ~200-300 min compute | Discipline #18 prereq for broader commit |
| Loadout M4 (no dependencies) | drax | ~0.25 day | No |
| Star-lord schema extensions (4 fields) | star-lord | ~1.75-3.25 days | YES (gates M1/M2/M5 + M3) |
| Loadout M1, M2, M5 (after schema) | drax | ~2.25 days | Parallel with rocket § 8 |
| Loadout M3, M6 (after rocket § 8) | drax | ~3 days | After rocket § 8 lands |

**Cycle 11 wall-clock estimate:** ~3 weeks to T4-post-mortem readiness.

**NOT in Cycle 11:**
- Pi infrastructure execution (deferred per Matt "right moment")
- Hosted-Postgres setup for loadout DB (deferred per Matt "later on")
- Tailscale install G11 (deferred to Matt's 15-min window)
- D9 LLM cache build (G12 NOT TRIGGERED)
- Algorithm § 8 v1.1 strategies (4 sim-extension-required + proxy-spawn)
- Loadout v1.1+ items D1-D13
- W1.13 hypothesis testing (chain blocked; gamora awaits prereq resolution post-Cycle-11)
- Cross-cycle scope amendments

---

## Authority + cross-references

- **Authority:** Matt 2026-05-25 verbatim log-back dialogue with gandalf
- **Source dialogue:** session transcript (gandalf decision-surface → Matt reply)
- **Companion wind-down doc:** `agentic_orchestration/cycle-10-wind-down-summary-2026-05-25.md`
- **Post-cycle dispatch returns:**
  - `agentic_orchestration/dispatches/2026-05-25-gamora-w1-13-hypothesis-testing.md` (blocked — surface only)
  - `agentic_orchestration/dispatches/2026-05-25-legolas-algorithm-section-8-methodology-consult.md`
  - `agentic_orchestration/dispatches/2026-05-25-drax-and-star-lord-loadout-app-readiness-scoping.md`
  - `agentic_orchestration/dispatches/2026-05-25-star-lord-g1-infrastructure-measurement.md`
  - `agentic_orchestration/dispatches/2026-05-25-star-lord-g12-llm-cache-hit-rate-measurement.md`
- **Pi recognition record:** `canonical/story/infrastructure-raspberry-pi-postgres-and-closed-loop-pipeline-2026-05-25.md`
- **Cycle 10 scope-doc:** `agentic_orchestration/cycles/cycle-10-hive-mind-scope.md`
- **Cycle 11 scope-doc:** `agentic_orchestration/cycles/cycle-11-hive-mind-scope.md` (authored same session)

---

## Sign-off

**Captured by:** gandalf 2026-05-25 (Pattern-B dialogue capture per gandalf OP § 2 Pattern B)
**Authority:** Matt 2026-05-25 verbatim
**Status:** FULLY RATIFIED 2026-05-25 — all 7 items confirmed (P1 ratified via Matt "I already had KR commit/push" + tag verified pushed)
**Downstream:** Cycle 11 KR kicker + jack-ryan decisions-log batch consume this artifact as authority-of-record for Matt's decisions
