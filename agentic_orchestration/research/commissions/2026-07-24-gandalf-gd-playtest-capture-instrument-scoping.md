# COMMISSION — GD playtest capture instrument: scope the field before we bake off

**To:** `legolas` (UNKNOWN-RESEARCHER, Mode A — analytical)
**From:** gandalf (`RUN-CONDUCTOR` / `ELICITOR`)
**Date:** 2026-07-24
**Authorized by:** Matt, 2026-07-24 — *"scope out the best possible AI Agent models available on today's date which we can select from so that we can set up a bake off to test them on my PC to capture Grim Dawn data points."*
**Charter lineage:** TSR-6a rung (b), amended — capture-model choice was explicitly **not** pre-committed to OpenAI Sol (Matt: cost concern + *"there may actually be better vision models"*), and was deferred to a mini bake-off at Track-B charter time. **This commission is the scoping that makes that bake-off designable.**
**Downstream:** gandalf drafts the per-agent capture design specs from your findings (Matt hands them to one agent at a time on the PC). Capture-analysis implementation lands in **galadriel's** seam.

---

## 0. What Matt is actually trying to do — read this before scoping anything

Matt plays Grim Dawn on his Windows PC. **Something watches and records numeric observations while he plays.** Those observations become the ground truth for hypothesis tests measuring our battle sim's encounter behaviour and "play feel" against GD's.

This is **not** a "describe the gameplay" task. It is **frame-accurate multi-object spatial and temporal measurement**. Getting that distinction wrong is the single way this research fails, so § 2 pins exactly what must be measured.

**Do not return a general-purpose VLM leaderboard.** A ranked list of "best vision models today" would be nearly worthless here. What we need is a **capability-to-measurement mapping**: for each candidate instrument, which of the § 2 quantities can it actually produce, at what precision, at what cost per hour of gameplay, on Windows.

---

## 1. QUESTION 1 (highest value — do this first) — is there a NON-VISION channel?

**Before scoping a single vision model, establish whether GD exposes numeric state directly.** If it does, vision becomes a secondary or QA instrument and precision goes from *estimated* to *exact*. This question dominates the others in expected value; spend accordingly.

Investigate and report on, at minimum:

- **Grim Internals** — the widely-used GD DLL utility (combat text, monster HP, DPS readouts, etc.). What does it expose, can it log to file, is there a scriptable/telemetry surface, is it still maintained, what version-compatibility does it have with the Fangs of Asterkarn patch (07/23/2026)?
- **Other established GD community tools** — GD Stash, Grim Dawn Item Assistant, GDDefeat/loot filters, any monster-tracker or combat-log mod. Which read process memory, which read files, which expose an API.
- **Memory-reading approaches** — is there a known/published offset map, a Cheat Engine table, or a community reversing effort for GD's entity list (positions, aggro/AI state, HP)? Legality and ToS: GD is single-player-first with an active modding culture — establish what Crate's stance actually is rather than assuming.
- **Anything GD writes itself** — logs, crash dumps, debug flags, console commands, launch parameters, `.arz`-adjacent runtime config.
- **The modding path** — GD ships a full editor suite in-depot (`ArchiveTool.exe`, `DBREditor.exe`, AssetManager). Can a *mod* be authored that emits telemetry, and would that alter the very behaviour we're trying to measure? (If yes, say so loudly — a measurement instrument that changes the measured system is a trap.)

**Report the honest answer even if it is "no channel exists."** A clean negative here is a valuable finding and redirects the whole program to vision.

## 2. What must be measured — the KPI target list (this is fixed; do not invent your own)

These come from the **TSF6-TRACK-A gap register** (`agentic_orchestration/gamora/notes/2026-07-24-tsf6-track-a-run.md` § 3) — the seven GD monster-AI parameter classes and how our sim currently fares. **Five are BLOCKED-MECHANISM**: the sim has no concept of them at all. Those five are the KPI targets, and each implies a *different* measurement difficulty:

| KPI class | GD parameters | What must actually be observed | Measurement shape |
|---|---|---|---|
| **1. Aggro onset radius** | `ViewDistance` 15.0, `InnerViewDistance` 4.0 | The **distance** between hero and mob at the instant the mob first begins pursuit. Two-zone (outer/inner). | Spatial. Needs world-distance estimation and a precise onset instant. |
| **2. Anger accumulation** | `SightAngerRate` 3.0, `InnerSightAngerRate` 12.0 (inner 4× outer) | The **latency** between the hero entering a zone and the mob committing to pursuit — and whether that latency is ~4× shorter in the inner zone. | Temporal, sub-second. Precision requirement is the hard part. |
| **3. Pursuit time / leash** | `PursuitTime` 10000 ms, `MaxPursuitDistance` | Elapsed time and distance from aggro to disengage; whether GD disengages on distance OR time (we believe it ORs them). | Temporal + spatial, multi-second. Easiest of the five. |
| **4. Idle wander** | `WanderDistance` 4.0, `RoamDistance`, `MaxTimeBeforeRoam` | Position of an **un-aggroed** mob over time; excursion radius from spawn; interval before roam begins. | Spatial tracking of a non-interacting object over a long window. |
| **5. Distress-call propagation** | `distressCallRange` 16.0, `ChanceToRespondToDistressCall` 75 | **Which** neighbouring mobs wake when one aggros, at what radius, and at what rate (a 75% chance implies needing many trials for a rate estimate). | Multi-object identity tracking + statistics over many events. |

Two more for completeness (not BLOCKED, lower priority): **flee-on-low-HP** (`fleeDistance` — sim has the distance but no HP-flee trigger) and **pursuit distance** (already parameter-faithful, +0.15% — useful as a *calibration control*: an instrument that can't reproduce the known-good one is not trustworthy on the other five).

**Two implications you must carry into the scoping:**

- **(a) These are quantities, not descriptions.** "The mob noticed the player and charged" is worthless. "Onset at 12.3 ± 0.4 m, 0.65 s after entering the outer zone" is the product.
- **(b) Precision requirements differ sharply by KPI.** KPI 3 tolerates ±0.5 s. KPI 2 may need ±50 ms to distinguish a 4× rate ratio. Any instrument recommendation must state precision *per KPI class*, not in general.

**A steer, offered as a hypothesis for you to confirm or destroy — do not treat it as a conclusion:** frontier VLMs are strong at *semantic labeling* and weak+expensive at *precise high-frame-rate multi-object tracking*. The architecture that actually fits may be a **hybrid**: deterministic CV/object-tracking for positions and timing, a VLM for event labeling, calibration, and QA, and (per Q1) a memory/telemetry channel for exact ground truth wherever one exists. **If the evidence says otherwise, say so** — this hypothesis was formed without research and is exactly the kind of plausible inference this project has learned to route rather than bank (see § 6).

**A note on the camera that may help:** GD renders at a fixed, largely non-rotating three-quarter camera with a bounded zoom range. If pixel-distance to world-distance is a *stable calibration constant*, spatial KPIs become far more tractable than they first appear. Verify rather than assume — check zoom behaviour, camera pitch, and whether elevation changes break the mapping.

## 3. QUESTION 2 — the instrument landscape as of 2026-07-24

**Establish today's date from a primary source, not from recollection**, and say what date you established. Model releases move fast and your training data is not the world.

For each credible candidate, report:

| Field | Requirement |
|---|---|
| **Instrument** | model / tool / library / harness |
| **Class** | frontier VLM · local/open VLM · classical CV · game-telemetry channel · hybrid |
| **KPI coverage** | which of the five § 2 classes it can produce, at what stated precision |
| **Modality** | real-time streaming vs post-hoc video analysis vs periodic screenshot |
| **Windows deployment** | what actually has to be installed and run on Matt's PC; whether an agentic harness exists on Windows |
| **Hardware requirement** | VRAM/CPU floor. **Matt's PC spec is currently UNKNOWN to us** — do not assume a spec; report the floor per option so we can match it later. (Relevant: `matt_to_do` T2 records that we do *not* currently have a certified GTX-1650/RTX-3050-class box, so a heavy local-model requirement is a live risk, not a footnote.) |
| **Cost per HOUR OF GAMEPLAY** | **this is the required cost unit, not per-token or per-image.** Show the arithmetic: frames/sec sampled × tokens/frame × price. Matt raised cost as a live concern on Sol specifically; a per-token figure does not let him decide. |
| **Maturity** | shipping / preview / research-only; API stability |
| **Licensing/ToS** | any term that restricts capturing or analyzing commercial game footage |

Candidate classes to cover (non-exhaustive — find what actually exists):
- Frontier multimodal/vision models with video or screen understanding, from all major labs
- Computer-use / screen-agent harnesses that run natively on Windows
- Open/local VLMs runnable on consumer hardware
- Classical CV and object-tracking stacks (template matching, optical flow, modern trackers, OCR for on-screen numerics)
- Video-capture plumbing (OBS, ffmpeg, frame-accurate timestamping) — unglamorous and possibly the highest-leverage part

## 4. QUESTION 3 — real-time vs post-hoc, and the "one agent at a time" constraint

Matt's stated workflow: he hands the drafted spec to **one agent at a time** on the PC and plays while it captures. Two very different modes follow, and both must be scoped:

- **Post-hoc:** record video with timestamps, analyze afterwards. Cheap, re-runnable against multiple instruments on identical footage (which makes a *fair* bake-off possible), no in-session latency budget.
- **Real-time:** the agent observes live and can **direct Matt** ("walk toward that pack until it notices you, then stop"). Necessary if the KPIs require *controlled trials* rather than opportunistic observation.

**Give a view on which the § 2 KPIs actually demand.** KPI 5 (a 75%-chance propagation rate) plainly needs many controlled repetitions; KPI 1 needs approach-until-onset runs. Opportunistic footage of normal play may simply not contain clean measurements. If so, say plainly that the instrument question is downstream of an **experimental-protocol** question — that is a finding worth more than a model ranking, and it changes what gandalf drafts.

## 5. Deliverable

File at `agentic_orchestration/research/knowledge/gd/2026-07-24-playtest-capture-instrument-scoping.md`:

1. **Headline** — the single most consequential finding, stated first (candidly: if Q1 finds a telemetry channel, that is the headline and the VLM section becomes an appendix).
2. **Q1 — non-vision channels**, with evidence.
3. **Q2 — instrument table** per § 3.
4. **Q3 — modality + protocol view** per § 4.
5. **A proposed bake-off design** — 3–5 finalists, the *identical* task each would be given, the pass criteria, and the estimated cost of running the bake-off itself. Keep it small; Matt asked for a mini bake-off, not a research programme.
6. **Coverage-boundary declaration (D-a — MANDATORY, see § 6).**
7. **Open questions for Matt** — things only he can answer (PC specs, willingness to install mods/DLLs, tolerance for scripted play sessions vs free play).

## 6. Disciplines in force on this commission

- **Establish the current date from a primary source and report it.** Then treat every "latest model" claim as needing a live citation. Your recollection of what shipped is not evidence.
- **D-a — coverage-boundary declaration (MANDATORY).** Your deliverable must contain an explicit section stating **what you could NOT check and why** — bot-gated sources, paywalled docs, unverifiable vendor claims, model families you did not reach. *"What's in it" is insufficient; the required field is "what isn't."* This discipline was ruled 2026-07-24 after a false finding stood as canon for a full program cycle, and after our own verified freeze silently omitted a file while passing an 11/11 hash check. A deliverable without this section is incomplete.
- **D-b — join validation before contradiction.** If two sources disagree on a number, do not conclude either is wrong until you have established they describe the same thing. Report both with full identifiers instead.
- **No parameter may be sourced from recollection.** Neither gandalf's nor Matt's. If a version, price, or capability figure appears in this brief and you cannot verify it, flag it rather than propagate it.
- **HALT and escalate** on: an unmodeled auth/ToS wall, evidence that a recommended instrument would alter the game's behaviour, or any point where you are tempted to fill a gap with a plausible inference.

---

**Signed:** gandalf, 2026-07-24. The five gaps in § 2 are what the sim cannot currently think about at all. Everything here exists to find the instrument that can tell us what GD actually does — precisely enough to argue with.
