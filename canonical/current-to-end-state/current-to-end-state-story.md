# Current State → End State: STORY (LIVING)

**STATUS:** LIVING CANONICAL — the story-side delta tracker. Sibling to `current-to-end-state-engine.md` (which tracks the battle-sim + emission + v2-fit engine gaps). This doc tracks **what the story spec has LOCKED vs. what a story session still owes** under the v2 *Reap. Die. Rise.* frame.
**Born:** 2026-06-30 (canonical reorg, Tranche 2) — split out of the single consolidated tracker so story-side open decisions stop hiding inside an engine-gap doc.
**Author:** gandalf (story-and-design steward).

> **Engine sibling:** `current-to-end-state-engine.md` — currently still at `canonical/story/current-to-end-state.md`; it relocates into this folder (renamed `…-engine.md`) in the reorg's final verified rewire pass (alongside retiring `canonical/reap-die-rise/`). Until then, read it at the old path.
> **End-state story SPEC** (what we're building toward): `canonical/reap-die-rise/` → `story-keystone.md`, `story-expansion.md`, `gameplay-loop-design.md` (these migrate to `canonical/reap-die-rise-story/` in the final pass). This tracker is the DELTA, not the spec.

---

## HOW THIS DOC WORKS (living-doc protocol)

- **SESSION-DELTA LOG** at top: latest entry governs. Prepend a dated block when a story decision lands, an open question resolves, or a new one surfaces.
- **PART A** = the LOCKED frame (what a story session may NOT silently reopen — Matt-ruled). **PART B** = the OPEN queue (what a story session still owes). **PART C** = the frame-reconciliation worklist (the (b)-consolidation of surviving experiential-structure docs into the v2 story spec).
- Mark resolved items ✓ with date + ruling; never silently delete — strike and date.

---

## SESSION-DELTA LOG (latest governs all below)

### 2026-06-30 — Doc born (reorg Tranche 2)

Split from `current-to-end-state.md`. Seeds PART A from the 2026-06-30 frame-refinement + Flag #6 ruling; PART B from the frame-reconciliation memo's open flags (#2, #4) + the newly-opened S2-companion investigation + undecided keystone beats; PART C from the surviving experiential-structure docs that must fold into the v2 story spec. No story decision changed in the birth — capture only.

---

## PART A — The LOCKED story frame (Matt-ruled; do not silently reopen)

| # | Locked | Source |
|---|---|---|
| A1 | Game = **Reap. Die. Rise.** | Matt 2026-06-29 retitle |
| A2 | isekai → **death-faith**; the player is a soul bound to a death-cult, not a transported hero | `reap-die-rise/` frame |
| A3 | Earth Self → **home-realm self** (time-agnostic; the persistent identity in the link) | projection doc |
| A4 | per-season cadence → roguelite **run / descent** (seasonal-RELEASE model retired 2026-06-02) | season-archive pivot |
| A5 | **Spirit guide RETIRED** (removed, not relabeled). Function splits **3 ways**: **(A)** demigod-jailer = tutorial + punctuated Mercer-mentor key beats; **(B)** death-god / patron Daikoku-Mahakala = rare unreadable Rorschach guidance (§19.3); **(C)** hub NPC ensemble (Rita + cult faces) = daily relationship + banter | Matt 2026-06-30 |
| A6 | **patron deity = a GOD** (not a demigod); the **demigod is the jailer** (built the cage, barred from the god, selects/steers — NOT the player's future self) | Matt 2026-06-30 |
| A7 | **banter / retort axis = the HUB NPC ENSEMBLE** (the Hades model). defiance↔devotion expressed via **actions** (hand-in vs. hoard), judged by hub NPCs — this IS the cult-standing economy given a voice (Flag #6 RULED) | Matt 2026-06-30 |
| A8 | Experiential STRUCTURE survives the frame change: **projection / Hall of Heroes / cosmograph sky / molting / temporal dyad** (past-companion ↔ present-self; the future corner collapsed when the spirit guide retired) | projection + companion-as-Hall docs (Flag #3 resolved) |
| A9 | Companion = a **Hall-sourced past self**, singular/reverent (D2-merc class), **Path Pure** (run 1 you fight alone) — *the WHEN of the companion is reopened, see B3* | companion-as-Hall (Path Pure RULED 2026-06-16) |
| A10 | Villain-protagonist stance **[RATIFIED-OPEN]** — ratified as a direction; execution/extent still a story-session call | loop-doc §2c |

PART A is the floor. A story session works *above* it.

---

## PART B — OPEN story decisions (the queue a story session owes)

| # | Open question | Gates | State |
|---|---|---|---|
| **B1** | **Flag #2 — run-persistence contract.** What survives a run vs. resets? (Hall accumulation, home-realm progress, cult standing.) The death-faith "you die and rise" loop needs its persistence rules. | the engine per-kit / progression model (cross-ref engine tracker PART III.2) | **OPEN — awaiting Matt** |
| **B2** | **Flag #4 — molt → run-trigger equivalent.** Path Pure says "first molt returns as your first companion," built on the retired per-season cadence. What's the run-model trigger that unlocks the past-self companion? | companion unlock timing; rocket companion-gen source param | **OPEN — awaiting Matt** |
| **B3** | **Season-two-companion investigation.** Under the v2 frame, does a companion belong in "season two" / a later chapter **at all**? Maybe it has a place, maybe not. *If yes*, re-derive the difficulty-inversion concern (D2-merc "mandatory crutch"; scale the threat, not just HP) — reasoning in git (`2026-06-18-companion-difficulty-inversion…`, deleted in reorg). | whether the companion layer ships; gauntlet companion cohort | **OPEN — story session decides (Matt 2026-06-30)** |
| **B4** | **Demigod warm-then-recede tragedy-phase.** Optional: the demigod-jailer starts as a warm Mercer-style mentor whose helpfulness later reads as manipulation (the betrayer detonates). Deliberate arc or keep him punctuated-neutral? | tutorial + key-beat tone; the §435 LLM-vs-templated decision (now scoped to hub banter, not demigod) | **OPEN — undecided (gandalf note in keystone §19.1)** |
| **B5** | **Keystone [OPEN] beats.** The story-keystone (`reap-die-rise/story-keystone.md`) carries Matt's own [OPEN] framing questions (§19.1 et al.) — the manufactured-rebellion reveal sequence, what the demigod *wants*, how the player learns the cage is manufactured. | the narrative spine of a run | **OPEN — Matt's keystone tags** |

---

## PART C — Frame-reconciliation worklist (the story-side (b)-consolidation)

The surviving experiential-structure docs predate the v2 death-faith/demigod/hub frame and carry the old "spirit guide / season / isekai" labels in their bodies (banners flag them; bodies not yet rewritten). The (b) consolidation **folds their load-bearing structure into the v2 story spec** (`reap-die-rise-story/`), reconciled, then deletes the sources.

| Source doc (in `story/`) | What survives (folds into `reap-die-rise-story`) | Reconcile away |
|---|---|---|
| `2026-06-11-avatar-projection-and-hall-of-heroes-framing` | projection model; Hall (possession) vs. cosmograph (possibility); molting = harvest-not-erasure | "spirit guide advises you" (retired); Operator-as-future-self framing |
| `2026-06-07-earth-avatar-cosmograph-creation-moment-architecture` | the creation-moment scene; cosmograph sky as in-fiction night sky | season-release cadence refs |
| `2026-06-05-cosmograph-pivot` | cosmograph-as-possibility-space recognition | — |
| `2026-06-13-companion-as-hall-of-heroes-ally-commitment` | companion = past-self; scarcity discipline; lookup-not-generation; temporal **dyad** | temporal *triad* (future corner gone); per-season bootstrap (→ B2/B3) |
| `2026-06-22-seasonal-descent-architecture-recognition` + `…-faction-descent-and-reward-loop-recognition` + `…-content-audit` | descent structure; faction-walled-from-combat discipline | "seasonal" naming → run/descent |

**Discipline:** reconcile, do not amputate (`reap-die-rise/00-index.md` §4). The structure is load-bearing; only the retired *labels* die. Open reconciliation items live in PART B; the memo `agentic_orchestration/gandalf/notes/2026-06-29-path-a-frame-reconciliation-flags.md` is the lineage.

---

**Signed:** gandalf, 2026-06-30. The engine tracker asks "how far is the build from the spec." This one asks "how settled is the story." Two different debts, two different ledgers.
