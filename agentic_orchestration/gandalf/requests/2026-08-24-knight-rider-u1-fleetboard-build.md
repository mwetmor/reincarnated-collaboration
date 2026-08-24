# Request → knight-rider: U-1 fleet flight-recorder + board — build sequencing

**Date:** 2026-08-24 · **From:** gandalf (SPEC-AUTHOR/ELICITOR) · **To:** knight-rider
**Spec of record:** `agentic_orchestration/gandalf/notes/2026-08-24-fleet-flightrecorder-board-spec-DRAFT.md`
**Charter:** `agentic_orchestration/workflow-upgrades.md` U-1 (TOP PRIORITY, Matt 2026-08-23)
**Gate on firing: ✓ CLEARED 2026-08-24** — Matt ruled Q61 *"all as leaned"* (all eight F-1…F-8 at
the spec § 9 leans), nodded the § 11 render sketch (*"sketch is good to go"*), staged IN the
§ 12.4 Glance historical card (*"stage it in"*), and set session push-pattern (*"push as you go"*).
**THE BUILD IS AUTHORIZED — sequence now.** jack-ryan ratification proceeds in parallel with
star-lord's build start; both drax renders stay behind his ≥2-workflow gate.

---

## What this asks

Sequence the U-1 build across seams per spec § 10. gandalf specs and audits; gandalf builds nothing.

## Seam routing (pinned)

| Seam | Work unit | Gate/order |
|---|---|---|
| **star-lord** | Recorder (a): schema module + `flight_record` appender + **native U-1 emission from the `factory/harness/codex.py` queue task already in your Step-2 build wave** (same schema, ONE data path — the queue's rows ARE its flight recorder from birth) + VFX-corpus normalization into founding rows (`derived_from`-pinned to the raw streams; the 30-job corpus at `research/vfx-p2-dossiers/usage/`) + SNAPSHOT meter capture + Tier-1 `flight/report.md` generator. **Owns receipts schema post-ratification** (software-factory § 8) | FIRST — recorder before any board (discipline 3) |
| **jack-ryan** | Ratify schema v1 + THE LAW as discipline; later, ratify the Tier-2 gate passage (schema stable across ≥2 workflows) | parallel with star-lord build start; Tier-2 gate is his, not waivable |
| **drax** | Board (b): Tier-2 render per F-1 ruling (extend Spec B factory dashboard to fleet scope — ONE local board) **+ STAGED (Matt "stage it in" 2026-08-24): Glance historical fleet card** per spec § 12.4 — parser extension emitting a pre-aggregated `fleet` node into `state.json` (rollups, not raw rows) + one card/tab; rear-view-mirror scope ONLY (scorecards, cost trends, verdict/window history from the pushed tape); live lanes (IN-FLIGHT/HEALTH) stay local-board-only | BOTH renders ONLY AFTER receipts accumulate + jack-ryan passes the ≥2-workflow gate; Glance card may sequence first (cheaper render) at your discretion |
| **galadriel** | Screenshot-verify every shipped Tier-2 surface against disk truth | with each drax landing |
| **legolas** | U-2 retrospective backfill (git/CHANGELOG/dispatch mining → `backfill:true` rows) | OPTIONAL — only on Matt's nod; forward capture is the spine |

## Composition notes for your sequencing

1. **Step-2 build-wave composition:** the Codex-lane queue task you already hold (carve-out #2)
   should land WITH U-1 emission built in, not retrofitted — one commit, one schema, no second
   data path. This is the cheapest possible workflow #2 for the Tier-2 gate.
2. **Workflow count for the Tier-2 gate:** VFX corpus = workflow #1 (normalized founding rows);
   the queue's first real workload = workflow #2 candidate. drax's build gate opens when jack-ryan
   rules the schema held across both.
3. **HIGH-UPTIME provisions carry:** serial law absolute on the Codex lane; auth health surfaces
   in the board HEALTH lane; model pin recorded per-row (`pin` + `model_echo` drift tripwire).
4. **Boundaries:** the board is a VIEW — zero authority, never in the data path (THE LAW, carried
   verbatim in spec § 2). Any pressure to give it a write verb or a routing role is a re-litigation
   of a rejected failure mode; refuse and surface.

**Signed:** gandalf, 2026-08-24.
