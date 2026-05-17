# Audio Strategy — Phase 0

**Status:** **Canonical — Matt-delegated 2026-05-16; gandalf-decided 2026-05-16.** Authored 2026-05-16 by gandalf to close the audio scope gap surfaced as Pattern P6.b (audio entirely unscoped) in `canonical/story/p6-forward-audit-2026-05-16.md`. Matt's delegation: *"Your call on audio. I havent thought about it. Music can be pushed back as far as possible as I have been solving for that by inserting seasonal flavor text into free AI music generators. I have no idea how to scope sound effects."*

**Companion docs:**
- `canonical/story/p6-forward-audit-2026-05-16.md` — sub-pattern P6.b that triggered this doc
- `canonical/story/drift-audit.md` Pattern P6 — the underlying drift framing
- `canonical/story/form-bias-cadence-strategy.md` — substrate-realignment scope this doc explicitly does NOT extend into audio

---

## Headline

**Demo VS2a / VS2b / VS2c ship silent.** Audio is Phase-1+ scope. Two sub-decisions resolve cleanly:

- **Music: deferred indefinitely.** Matt's personal AI-music-generator workflow with seasonal flavor text injection IS the Phase-0 music strategy. Project corpus does not commission music work.
- **SFX: deferred to Phase 1+ at production scope.** Minimal-cost vendor-companion availability audit added to in-flight Step B Tier-1 crawl. Audit data sits ready; SFX commission promoted to near-term only if playtest signal demands.

---

## Music — Matt's workflow as Phase-0 strategy

**The workflow (as Matt described 2026-05-16):**

1. Season generation produces cosmology + per-season thematic flavor text via LLM (current pipeline)
2. Matt feeds seasonal flavor text into free AI music generators (Suno / Udio / equivalent class of tools)
3. Generated music carries per-season thematic register at near-zero cost per season
4. Music is produced personally by Matt; not in any seam's scope; not in any commission

**Why this works for Phase 0:**

- Per-season thematic variety is achievable at zero project-corpus cost — the same LLM step that drives season cosmology drives music generation through copy-paste
- Music is not currently a player-evaluation axis (family playtests can run with browser background music or silent)
- AI music generators are improving rapidly; what Matt produces today via free tools may be production-acceptable by Phase 1
- Personal-workflow scope means no team coordination cost, no vendor sourcing, no integration pipeline

**Why this defers cleanly:**

- No engine work is required (music doesn't touch the engine)
- No demo work is required (browser autoplay-allowed audio is a 10-line drax change if/when needed)
- No catalogue work is required (Matt's music is generated; not sourced from VFX vendors)
- No decisions-log entry is required (workflow-as-strategy is documented here; nothing else to lock)

**When this assumption needs revisiting:**

- If music quality becomes a pitch-positioning factor (external-facing showcase moment) — Matt may want production-track music
- If music integration becomes a player-feel-evaluation factor (playtest signal includes "music helps / hurts the showcase") — promote to scoped work
- If the AI-music-generator landscape regresses (free tools degrade or commercial-license terms change) — re-assess strategy

**Phase-1 revisit trigger:** *whenever Phase 1 starts.* No specific gate before that.

---

## SFX — Phase-1 deferral with in-flight audit

### Current decision

**SFX is Phase-1+ scope at production framing.** Demo VS2a / VS2b / VS2c ship silent. No SFX commissioning, no SFX integration, no SFX vendor purchasing during Phase 0.

### The exception — Step B Tier-1 audit amendment

A near-zero-cost addition to the in-flight Step B Tier-1 dispatch:

**Amendment recommendation:** add `audio_companion_availability` field to per-pack JSONL row. For each VFX pack, record whether the vendor ships companion SFX (yes / no / partial / unknown); if yes, brief notes on format (WAV / OGG / MP3), license terms (if separate from VFX license), and rough quality assessment.

**Why this matters:** several Tier-1 vendors are known to ship companion SFX (CodeManu's kinetic packs often include impact SFX; Pimen's status-effect packs occasionally include cast SFX). If meaningful companion SFX coverage exists across the catalogue, the eventual SFX commission has a starting point — packs we're already buying for VFX may carry usable SFX at no marginal cost.

**Cost:** ~5-10% added Legolas effort per vendor; piggybacks on Step B Tier-1 + Pimen re-crawl already in flight; if Legolas can record the data per-pack at crawl time, it costs significantly less than a future audio-specific re-crawl pass.

**Filing:** the amendment is recommended to knight-rider for inclusion alongside the C.1-C.3 amendments from the gate-3 review + the geometry-signatures amendment from the B11 investigation. Treat as C.5 (or wherever it slots in the dispatch's numbering).

### Phase-1 revisit triggers

Promote SFX to near-term commission scope if any of:

1. **Playtest signal flips the decision.** If feedback names "feels floaty / weightless / missing impact / undersells the abilities" as a recurring concern across multiple playtest cycles, that's usually SFX-absence read as game-feel-absence. Audit data is ready; commission spec can be authored against it.
2. **External-facing showcase moment surfaces.** If demo enters pitch / publisher / community-facing context, silent combat undercuts the work. SFX becomes pre-pitch-required.
3. **Phase 1 starts.** Default trigger; revisit regardless of other signals.

### What we are NOT doing

- Not commissioning a Legolas SFX-specific vendor sweep (would duplicate Step B work)
- Not commissioning an Elrond SFX-categorization rubric (no data to categorize yet)
- Not authoring SFX-register / SFX-substrate / SFX-cipher equivalents to the VFX work (premature)
- Not adding SFX integration scope to drax (drax bandwidth is already binding constraint per roadmap risk-1)
- Not coupling SFX decisions to VFX cipher-width sub-locks (orthogonal axes)
- Not making Matt-level decisions about SFX register (pixel-art chip-sound? orchestral hit? synth impact?) — defer to when commission authors

---

## Why this resolves Pattern P6 sub-pattern P6.b

P6.b named that audio was entirely unscoped in any current canonical doc. The drift this surfaced was implicit-assumption — *"audio happens later"* without naming **when later starts** or **what later looks like.**

This doc resolves P6.b by:

1. **Naming the deferral explicitly.** Audio is Phase-1+ scope. Not implicit; documented.
2. **Naming the Phase-0 strategy for the music dimension.** Matt's workflow IS the strategy; no project-corpus action.
3. **Naming the Phase-1 trigger.** Playtest signal / external-facing moment / Phase 1 start.
4. **Adding a near-zero-cost audit so Phase 1 has data ready.** Step B Tier-1 amendment captures vendor companion SFX availability for free.
5. **Naming what's NOT in scope** to prevent further implicit-assumption drift.

If audio surfaces as a near-term concern despite this deferral, the audit data + this doc's framing provide the scaffold for fast commission authoring.

---

## Cross-references

- `canonical/story/p6-forward-audit-2026-05-16.md` § Sub-pattern P6.b — the drift this doc closes
- `canonical/story/drift-audit.md` — Pattern P6 framing
- `agentic_orchestration/dispatches/2026-05-16-legolas-step-b-tier1-2dvfx-crawl.md` — dispatch receiving the audio-companion amendment recommendation
- `agentic_orchestration/gandalf/requests/2026-05-16-geometry-vfx-coverage-investigation-b11-gating.md` — sibling investigation; same Step B amendment authoring window

---

## Maintenance protocol

When Step B Tier-1 crawl returns:

1. Check audio companion availability across vendors; if meaningful coverage exists, surface to Matt as Phase-1 readiness data
2. If coverage is sparse (no vendor ships companion SFX usefully), flag this so a Phase-1 SFX commission knows to budget for separate sourcing

When any of the Phase-1 revisit triggers fire:

1. Re-read this doc + the audit data
2. Author SFX strategy commission scoped against the trigger that fired
3. Update this doc's status from "Phase 0 — deferred" to "Phase 1 — active scoping"

When future P6 forward-audit re-runs occur:

1. Confirm this doc still names the audio strategy correctly
2. If the strategy has drifted or a new audio sub-dimension surfaces (e.g., spirit-guide voice synthesis as distinct from SFX/music), surface as a new audit finding

— gandalf, 2026-05-16 (Day 4)
