# 00 — Ground State (Router)

> **STATUS:** ROUTER (thin). On 2026-06-30 (canonical reorg, Tranche 2) this doc's heavy per-doc CURRENT/HISTORICAL/DEAD **registry was dissolved** — canon now lives in **three folders** (below). The old "ground-state oracle" content is in **git history** (`git show <pre-reorg>:canonical/00-ground-state.md`), recoverable, not pre-load material.
> **Status:** LIVING. Still the **first read for every agent on every invocation.** The path is unchanged, so every "read `00-ground-state.md` first" instruction stays valid — you now get a *router*, not a registry.
> **Game:** **Reap. Die. Rise.** — ARPG / roguelite-descent, **death-faith** frame (retitled from "Reincarnated" 2026-06-29; the isekai positioning is RETIRED).
> **Maintained by:** gandalf.

---

## Where canon lives — three homes

| You want… | Go to |
|---|---|
| **The STORY spec** — death-faith frame, demigod-jailer / death-god patron / hub-ensemble cast, projection / Hall of Heroes / cosmograph / molting, the manufactured-rebellion keystone, villain-protagonist arc | `canonical/reap-die-rise-story/` |
| **The ENGINE spec** — generation, simulation, balance, gear / stat / T4 architecture, progression, content-emission, the build / networking / perf / render stack | `canonical/reap-die-rise-engine/` |
| **Where the build is vs. the spec** — the deltas, what's still owed | `canonical/current-to-end-state/` → `…-engine.md` (build gaps) + `…-story.md` (open story decisions) |
| **Anything older** — epoch history, wave-close records, superseded designs, curation logs, the old oracle | **git** — recoverable, searchable, not pre-load |

**Two questions, two homes:** `reap-die-rise-{story,engine}` = the **END STATE** (what we're building). `current-to-end-state/{story,engine}` = the **DELTA** (how far the build is from it).

> **⚠ REORG IN PROGRESS (born 2026-06-30).** The folders + physical relocations are done; the content **fold** is mid-flight. Until it completes:
> - the **engine spec** seed has landed in `reap-die-rise-engine/` (build/networking/perf/godot/vfx/design-decisions); the numbered docs `canonical/37–51` still fold in;
> - the **story spec** seed has landed in `reap-die-rise-story/` (`story-keystone`, `story-expansion`, `gameplay-loop-design`, + `spec-index` — the v2 lexicon/supersession index); the surviving `canonical/story/` experiential-structure docs still fold in (a design session resolves them).
>
> Each spec folder's **`00-index.md` carries the live fold-worklist and forwards you to the authoritative current location.** Read the index first when in doubt. Tracking ledger: `agentic_orchestration/gandalf/notes/2026-06-30-canonical-reorg-fold-map.md`.

---

## First reads by role (after this doc)

The reorg collapses the old bespoke per-agent reading lists. The universal shape is three items:

1. **Your side's spec folder** — story work → `reap-die-rise-story/`; engine work → `reap-die-rise-engine/` (during the fold, plus the numbered docs its index forwards you to).
2. **Your side's delta tracker** — `canonical/current-to-end-state/current-to-end-state-{story|engine}.md`.
3. **Your own latest 2–3 notes** — `agentic_orchestration/<agent>/notes/`.

Plus role-specific:

| Role | Also reads |
|---|---|
| **gandalf** | BOTH trackers + both spec folders (story-and-design steward spans both); `style-register`; legacy-categorical-cleanup-audit |
| **knight-rider** | BOTH trackers (orchestrator — sequences engine build + the story-decision queue); latest `agentic_orchestration/skill_handoff_*`; current hive-mind state file; engineering-disciplines |
| **jack-ryan** | engineering-disciplines; decisions-log; latest critique-pair / Gate dispatch |
| **rocket / gamora / star-lord** | `reap-die-rise-engine/` (your sections); engine tracker; engineering-disciplines |
| **drax** | `reap-die-rise-story/` presentation sections; loadout / demo / godot repo READMEs |
| **galadriel** | `style-register`; visual-benchmark; geometry-vfx-coverage |
| **elrond** | substrate / catalogue / lineage layer (elrond-owned, outside these three folders) |
| **legolas** | latest gandalf request; relevant hive-mind protocol section |

**Do NOT re-walk the historical archive on every invocation.** It is searchable when needed; it is not pre-load material.

---

## When docs disagree

1. **The spec folders govern.** `reap-die-rise-{story,engine}/` (and the numbered `37–51` engine docs still folding in) override any older framing. Anything they superseded is git-lineage, not truth.
2. **The latter is canonical.** When two live docs disagree, the more recent wins.
3. **`decisions-log.md` is temporal ground truth** for decisions; if it disagrees with a spec/story doc, decisions-log wins.
4. **`engineering-disciplines.md`** overrides any older discipline lists.
5. **Cross-cutting canon** (these folders, decisions-log, disciplines, this router, AGENTS.md): the latest canonical-write wins. *(The Mac/PC two-host authority split retired 2026-06-30 with the PC team — single-host now.)*

---

## Drift-guards (locked vocabulary + dead branches)

*Migrating into the spec folders during the fold; held here through the transition.*

- **Locked term — `flavor element`:** thematic flavor variant of a primary `canonical_element` (pure naming/visual layer; does NOT change damage_scaling_type, affinity, or resistance). Retired: `sub-element`, `element canonical-pair flavor`.
- **DEAD — do not build on these:** isekai framing · the warm future-self **spirit guide** as an entity (RETIRED 2026-06-30; splits 3 ways — demigod-jailer / death-god patron / hub ensemble) · **seasonal-RELEASE** cadence (retired 2026-06-02; we ship runs/descents, not seasons) · pure-auto-combat (rejected; variable-execution-by-build is the lock) · mobile-first (PC/console-first) · non-humanoid playable forms · pre-imposed aesthetic/axis taxonomy (substrate votes). If you're building on any of these, stop — you're in a dead branch.

---

**Author:** gandalf, 2026-06-30 (canonical reorg, Tranche 2). The oracle remembered every doc; the router only needs to remember the three doors. Git keeps the rest.
