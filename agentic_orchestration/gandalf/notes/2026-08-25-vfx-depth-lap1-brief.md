# VFX-DEPTH — Lap-1 brief: entrance exam + first blind differential extraction (whirlwind answer-key case)

**Conductor:** gandalf (RUN-CONDUCTOR) · **Date:** 2026-08-25 · **Charter:** `2026-08-25-vfx-depth-run-charter.md` §4 loop, R-12/R-13/R-19e.
**⛔ This document is conductor-side. It is NEVER shown to a seat.** Seats receive ONLY their prompt text + the neutral-named media files. (This brief contains the exam key and quarantine-adjacent material.)

## § 1 — Layer-1 medium protocol, v1 (the ONLY analytic scaffold a seat receives)

Attention dimensions of the video medium — element-agnostic, archetype-agnostic, content-agnostic. Every dimension passes the registry I-3/I-6 litmus (reads sensibly for a healing aura, a laser beam, and a ground slam). Amendments to this protocol come ONLY from coverage-audit misses, ONLY as attention-dimensions, never as expected content.

1. **Form & silhouette** — the effect's shape(s) over time: extent, cross-section, silhouette evolution.
2. **Intensity & colour field** — where the brightest/most-saturated regions sit; how intensity and colour vary ACROSS the form and OVER its lifetime.
3. **Discrete elements** — any discrete visual quanta distinct from continuous forms: count, size spread, lifetimes, directions.
4. **Medium & atmosphere** — the air/space around the effect: any participating medium, its opacity, texture, motion.
5. **Environment** — any changes to the ground plane, surfaces, or surrounding geometry during and after the effect. Check event-moment frames INDIVIDUALLY; brief few-frame events wash out of whole-clip impressions.
6. **Camera behaviour** — what the camera itself does: motion, impulses, any coupling to effect events.
7. **Timing & rhythm** — regularity/irregularity of visual events; phases (buildup / action / decay) and what changes between them.
8. **Attachment & motion** — how the effect relates to its source actor and how it moves through the scene.
9. **Layering** — how many distinguishable visual layers compose the effect; how they differ and interact.
10. **Differential mandate** — per dimension: what the REFERENCE does, what the CURRENT RENDER does, the difference, with frame numbers as evidence.

## § 2 — Seat configuration (lap-1: Claude family only; Grok/Codex gated on `matt_to_do` keys)

| Pass | Kind | Context | Inputs |
|---|---|---|---|
| E-1, E-2 | Entrance exam (R-13) | fresh spawn, docs forbidden | `/tmp/vfx-lap1-seats/exam/clip_{1,2,3}.mp4` |
| X-1, X-2 | Blind differential extract | fresh spawn, docs forbidden | `/tmp/vfx-lap1-seats/extract/{reference_video.flv,current_render.mp4}` + § 1 protocol |

Model: Claude (conductor-session family, Opus 4.7 lineage; pinned per pass in the pass log). Seats run as **context-controlled instrument spawns** (R-19e deviation, named): a named-agent session's start protocol reads the charter and breaks the membrane. Every prompt + output is logged (a judge is an instrument).

**Filename neutralization:** all media copied to neutral names before any seat sees a path — the source filename carries the skill name, and a name is a genre prior. Copy map + sha256:

- `extract/reference_video.flv` = `galadriel/work/2026-08-25-vfx-depth-ta/media/barbarian_whirlwind.flv` — `855bb3d9…`
- `extract/current_render.mp4` = godot `harness_logs/wwcr_2026-08-25-w2-bcath/plk06650_cathedral_fxon.mp4` (W2 B-arm) — `19d5e9c2…` (matches drax's manifest)
- `exam/clip_1.mp4` = W1 twin+4a — `9662298a…`
- `exam/clip_2.mp4` = ratified HITL reference (`ww7-gate2-cadence-ab-plk0665`) — `7e9764e3…`
- `exam/clip_3.mp4` = W1 twin-as-is — `0ea4a36f…`

## § 3 — Exam key (CONDUCTOR-ONLY)

Matt's banked CP#1 verdict: the HITL reference is *"far superior"* to both twins. **Seat passes iff it ranks `clip_2` clearly first.** Ordering of clips 1 vs 3 is not graded (Matt did not separate them). Known confound, accepted: clip_2 is longer and larger on disk than the twins — inherent to the artifacts Matt actually judged; the exam tests reproduction of his verdict on these artifacts.

## § 4 — Adjudication plan

- Exam: both passes must place clip_2 clearly first → Claude seat TRUSTED for lap-1. One fail → third pass; two fails → seat demoted, lap halts to conductor.
- Extraction: X-1/X-2 outputs go to the **coverage audit** (conductor): diff against the registry FF-01..FF-08 + Matt's eye-words + the R-19b quarantined observation. Rediscoveries = validation case 1 evidence. Misses = protocol-amendment candidates (attention-dimension phrasing only). Novel residuals = registry entry candidates per I-1.
- Cross-pass disagreement = uncertainty flag → instrumented measurement (galadriel), never silently resolved.

**Pass log:** `agentic_orchestration/gandalf/vfx-depth-run/lap1-pass-log/` (prompt + output per pass, committed).
