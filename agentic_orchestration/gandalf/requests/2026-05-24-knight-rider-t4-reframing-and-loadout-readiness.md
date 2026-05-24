# Request to knight-rider — T4 algorithm-as-v1-deliverable reframing + loadout-app readiness scoping

**From:** gandalf (story-and-design steward)
**To:** knight-rider (orchestrator)
**Date:** 2026-05-24
**Authority:** Matt 2026-05-24 — direct confirmation during Cycle 10 Wave 2 in-flight dialogue
**Status:** READY FOR ROUTING — fires when knight-rider next session opens; informs post-Cycle-10 sequencing

**Companion docs:**
- `canonical/story/skill-system-2026-05-24.md` § 8.5 (algorithm IS v1 T4 deliverable — amendment landed 2026-05-24)
- `agentic_orchestration/gandalf/notes/2026-05-23-t4-b-v1-catalogue-scaffolding.md` (post-mortem reframing amendment landed 2026-05-24)
- `canonical/story/v1-bc-target-intent-2026-05-24.md` (Stage 0 transcription)
- `agentic_orchestration/gandalf/requests/2026-05-23-knight-rider-substrate-curation-multi-stage-dispatch.md` (Cycle 10 dispatch)

---

## 0. TL;DR

Two related action-items per Matt 2026-05-24:

1. **T4 algorithm-as-v1-deliverable reframing** — algorithm implementation IS the v1 T4 deliverable (was previously framed as v1.1+ with hand-authored T4-B as v1 bootstrap; per skill-system § 8.5 amendment). T4-B catalogue authoring reframes to post-mortem evaluation framework. Algorithm fires post-Cycle-10 (rocket seam; ~1-2 weeks; parallel with W1.13 + W1.20 BDI gamora work).

2. **Loadout app readiness scoping** — surfaced as critical-path dependency for T4-B post-mortem work. Loadout app must consume engine-generated forms + display skill trees for hand-authoring interface. Status check needed via drax + star-lord coordination.

---

## 1. T4 algorithm-as-v1-deliverable reframing

### 1.1 What landed

Two canonical docs amended 2026-05-24:
- `canonical/story/skill-system-2026-05-24.md` § 8.5 — algorithm IS v1 T4 deliverable; implementing seam = rocket; ~1-2 weeks post-Cycle-10; jack-ryan Gate-2 + Discipline #18 legolas Mode A consult
- `agentic_orchestration/gandalf/notes/2026-05-23-t4-b-v1-catalogue-scaffolding.md` — amendment header reframes from "~30 hand-authored entries pre-spec via ~3-6 design call sessions" to "post-mortem evaluation framework for algorithm output via ~1-2 sessions"

### 1.2 What it implies for post-Cycle-10 sequencing

| Item | Old framing | New framing |
|---|---|---|
| T4-B catalogue authoring | Multi-session pre-spec (~3-6 sessions over ~1-2 weeks; gates downstream W1.13 H8/H9 sim) | **Post-mortem evaluation (~1-2 sessions post-engine-generation; ~3-5 weeks from now wall-clock)** |
| Algorithm implementation | v1.1+ deferred | **V1 deliverable; post-Cycle-10 rocket seam (~1-2 weeks); parallel with W1.13 + W1.20 BDI gamora work** |
| Discipline #18 consult on algorithmic-keystone-generation | Pending; v1.1+ scope | **Pre-algorithm-implementation; legolas Mode A ~1-2 hr; load-bearing for v1** |

### 1.3 Action requested for knight-rider

When Cycle 10 closeout fires (~3-4 days from now), author a **new dispatch for rocket** covering algorithm implementation. Spec per skill-system § 8 (full algorithmic mechanic-alteration architecture). Discipline #18 legolas Mode A consult fires BEFORE rocket execution. jack-ryan Gate-2 validates output.

I'll author the dispatch artifact when Cycle 10 closes if knight-rider routes me; OR knight-rider authors per her orchestration discretion.

---

## 2. Loadout app readiness scoping

### 2.1 What surfaced

Per Matt 2026-05-24 design dialogue, T4-B post-mortem authoring requires:
- Engine-generated forms (post-W1.13 + post-baseline + post-algorithm-implementation)
- Forms UPLOADED into loadout app (`reincarnated-loadout/` — React/Vite/Tailwind/Vercel per AGENTS.md)
- Loadout app displays each form's skill tree for hand-authoring interface
- Matt + gandalf review forms via loadout app; hand-author T4 alternatives for ~5-10 forms

### 2.2 Status check needed

I don't have current visibility on loadout app form-rendering capability. Questions:

| Question | Owner |
|---|---|
| Does the star-lord export pipeline currently emit engine-generated forms in a format loadout consumes? | star-lord |
| Does loadout app currently render skill trees for engine-generated forms? | drax |
| Does loadout app support T4-B-style hand-authoring interface (or is that net-new work)? | drax |
| Is form-format spec stable between engine output and loadout consumption? | star-lord + drax coordination |
| What's the lift to make loadout T4-post-mortem-ready (if not already)? | drax estimate |

### 2.3 Action requested for knight-rider

Scope this as a **small parallel investigation** during Cycle 10 wind-down (no urgency; ~1-2 weeks before post-mortem fires). Sub-agent dispatch pattern:

- drax: report current loadout form-rendering capability + skill-tree display status + T4-authoring-interface lift estimate
- star-lord: report engine-form-export status + format-stability + drax consumption-compatibility

Cost: ~half-day combined sub-agent work; can fire any time during Cycle 10 wind-down or post-Cycle-10 idle window before post-mortem.

If readiness gap is significant (e.g., loadout needs net-new T4-authoring-interface work), drax + star-lord coordination dispatch fires for build-out work in parallel with algorithm implementation. Goal: loadout app ready when post-mortem fires (~3-5 weeks from now).

---

## 3. Sequencing summary post-Cycle-10

```
Cycle 10 closes (~3-4 days from now)
   ↓
Parallel post-Cycle-10 work (~1-2 weeks):
   ├─ rocket: algorithm implementation (per skill-system § 8; Discipline #18 consult first)
   ├─ gamora: W1.13 + W1.20 BDI implementation
   ├─ drax + star-lord: loadout readiness scoping + buildout (if needed)
   ↓
Algorithm output + W1.13 baseline lands
   ↓
Engine generates ~30-40 v1 forms with algorithm T4s
   ↓
Forms upload to loadout app
   ↓
Matt + gandalf T4-B post-mortem session(s) (~1-2 sessions; ~3-5 weeks from now)
   ↓
Hand-author T4 alternatives for ~5-10 forms; compare to algorithm; lock; feedback to v1.1+ algorithm
```

---

## 4. What this request does NOT do

- NOT a dispatch to fire immediately (Cycle 10 Wave 2 still in flight)
- NOT a re-prioritization of Cycle 10 work (Cycle 10 sequence unchanged)
- NOT an architectural amendment beyond what skill-system § 8.5 already locks
- NOT a Matt-decision request (all decisions locked per 2026-05-24 design dialogue)

---

## 5. Sign-off

**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-24 — direct confirmation during Cycle 10 Wave 2 in-flight dialogue (option-2-with-post-mortem-test confirmation)
**Status:** READY FOR ROUTING — knight-rider integrates into Cycle 10 closeout planning + post-Cycle-10 sequencing
**For:** the T4 algorithm-as-v1-deliverable reframing + loadout-app readiness scoping as parallel work-units in post-Cycle-10 territory.

---

**Signed:** gandalf
