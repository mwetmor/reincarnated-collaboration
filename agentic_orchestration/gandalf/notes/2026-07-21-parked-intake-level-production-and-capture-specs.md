# Parked intake — level-production + capture-harness spec drop (discussed, no conclusion)

> **STATUS:** PARKED INTAKE POINTER · author: gandalf, 2026-07-21 · per Matt same-day: the four docs were **discussed but no conclusion was reached**; park for later. No processing record exists anywhere in `agentic_orchestration/` or `canonical/` (grep-verified 2026-07-21) — this note is the only durable pointer.

## The four docs (all in `claude-mobile-session-docs/`, synced 2026-07-20 19:18–19:19, untracked in git)

| Doc | One-line content | Status |
|---|---|---|
| `level-design-and-extraction-ideas/RDR_Encounter_Geometry_Spec_Authoritative.md` | Multi-source (D2 + Titan Quest + Grim Dawn) encounter-geometry extraction: pluggable adapters → normalized monster/area schema → spatial-behavioral archetypes → **room-size solved in the battle sim** ("solved output, not measured input") | AUTHORITATIVE of the pair |
| `level-design-and-extraction-ideas/RDR_Encounter_Geometry_Extraction_Spec.md` | v1, D2-only version | self-declared SUPERSEDED by the authoritative doc |
| `level-design-and-extraction-ideas/RDR_Level_Production_and_Validation_Reference.md` | Full level-production arc: author (taxonomy + bounded vignette set) → assemble (socket contracts + affordance-tagged scatter + DressingProfile; PoE-tileset precedent) → capture → judge loop | consolidates + supersedes the MCP capture spec |
| `godot-development-ideas/Godot_MCP_Capture_Harness_Spec.md` | In-engine deterministic CaptureRig + engine-level MCP server ranking (replaces manual mp4/PNG QA capture); §6 30-min test overrides the paper ranking | FOLDED into the reference doc per its own header |

## Owed on resume (first touch)

1. **Full read** of the two live docs (authoritative geometry spec + production reference); v1 + MCP spec are lineage/folded.
2. **Role binding** — each doc says "bind Orchestrator / Designer / Judge to the owning named agents" (likely KR / gandalf+drax / galadriel; the capture seam is galadriel's, the Godot seam drax's, room-size-solve rides gamora's sim).
3. **Intake assessment vs existing canon** — where each lands against: KPM/pressure bands (already in hand per the specs), gauntlet beat-families spec, galadriel's capture pipeline, `reap-die-rise-game/` scope, and the Q11 density contingency. What's genuinely new vs already-covered.
4. **Conclusion Matt didn't reach** — the discussion (mobile session, ~2026-07-20) ended without a ruling; surface the actual decision points when resumed rather than assuming adoption.

**Not blocking anything currently in flight.** VDM-2 (F1–F6), Archive-Frame fold (§6 motive fork), and the Q32 roster are independent of this drop.

**Signed:** gandalf, 2026-07-21.
