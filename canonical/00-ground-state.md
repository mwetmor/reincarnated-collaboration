# 00 — Ground State (Router)

> **STATUS:** ROUTER (thin). On 2026-06-30 (canonical reorg, Tranche 2) this doc's heavy per-doc CURRENT/HISTORICAL/DEAD **registry was dissolved** — canon now lives in **three folders** (below). The old "ground-state oracle" content is in **git history** (`git show <pre-reorg>:canonical/00-ground-state.md`), recoverable, not pre-load material.
> **Status:** LIVING. Still the **first read for every agent on every invocation.** The path is unchanged, so every "read `00-ground-state.md` first" instruction stays valid — you now get a *router*, not a registry.
> **Game:** **Reap. Die. Rise.** — ARPG / roguelite-descent, **Glitch Archive** frame (Matt ruling 2026-07-28: the death-faith frame is DISSOLVED — no longer story canon). The premise: a teenage kid finds an old ARPG floppy disk, 3D-prints an adapter for his VR console, and gets stuck inside the glitching game — saving the ARPG kits (and himself) from deletion by defeating them one by one, adding them to the adapter, and *becoming* them. Frame authority: `reap-die-rise-story/archive-frame.md` (RULED 2026-07-21) + founding capture `agentic_orchestration/gandalf/notes/2026-07-25-glitch-archive-story-concept-capture.md`. (Retitled from "Reincarnated" 2026-06-29; the isekai positioning is RETIRED.)
> **Maintained by:** gandalf.

---

## Where canon lives — three homes

| You want… | Go to |
|---|---|
| **The STORY spec** — **Glitch Archive** frame (kid / floppy disk / VR adapter / rescue-kits-from-deletion / become-them; `archive-frame.md` is the frame authority) — the death-faith-era docs (demigod-jailer / death-god patron / manufactured-rebellion keystone / villain-protagonist arc) are SUPERSEDED pending re-reconciliation fold | `canonical/reap-die-rise-story/` |
| **The ENGINE spec** — generation, simulation, balance, gear / stat / T4 architecture, progression, content-emission, the build / networking / perf / render stack | `canonical/reap-die-rise-engine/` |
| **The GAME spec** — the playable product: the One Realm MVP demo scope (THE DENOMINATOR for demo-critical vs launch-scope), roster accounting, wishlist machinery | `canonical/reap-die-rise-game/` (born 2026-07-02) |
| **Where the build is vs. the spec** — the deltas, what's still owed | `canonical/current-to-end-state/` → `…-engine.md` (build gaps) + `…-story.md` (open story decisions) + `…-game.md` (playable-presentation-build / Godot gaps — born 2026-06-30) + `…-serial-content-emission.md` (the content-factory product: emission current→end, run registry, demo bundle — born 2026-07-02) |
| **What's waiting on MATT** — the human-in-the-loop queues; check at session start/end | `canonical/matt_decision_needed/` (decisions — born 2026-06-30) + `canonical/matt_to_do/` (actions only Matt can perform — born 2026-07-02) |
| **Anything older** — epoch history, wave-close records, superseded designs, curation logs, the old oracle | **git** — recoverable, searchable, not pre-load |

**The shape:** `reap-die-rise-{story,engine,game}` = the **END STATE** (what we're building — narrative / systems / playable product). `current-to-end-state/{story,engine,game,serial-content-emission}` = the **DELTA** (how far the build is from it) — four ledgers: the sim (engine), the narrative (story), the playable build (game), the content factory (serial-content-emission, born 2026-07-02). `matt_decision_needed/` + `matt_to_do/` = the **Matt queues** (decisions awaiting his ruling; actions only he can perform).

> **✓ REORG COMPLETE (2026-07-01).** The fold finished: the numbered engine spine (37–51 survivors) + the engine-mechanics corpus moved into `reap-die-rise-engine/`; `canonical/story/` **dissolved** (style-register trimmed + re-homed to `reap-die-rise-story/`; everything else moved, harvested, or deleted — lineage in git); `canonical/` root holds this router only. Each spec folder's **`00-index.md` carries the move/fold record** and forwards you to authoritative locations. Run ledger: `agentic_orchestration/gandalf/notes/2026-06-30-canonical-reorg-fold-map.md`.

---

## First reads by role (after this doc)

The reorg collapses the old bespoke per-agent reading lists. The universal shape is three items:

1. **Your side's spec folder** — story work → `reap-die-rise-story/`; engine work → `reap-die-rise-engine/`; playable-product / Godot work → `reap-die-rise-game/` (read its `00-index.md` first — it maps the corpus).
2. **Your side's delta tracker** — `canonical/current-to-end-state/current-to-end-state-{story|engine}.md`.
3. **Your own latest 2–3 notes** — `agentic_orchestration/<agent>/notes/`.

Plus role-specific:

| Role | Also reads |
|---|---|
| **gandalf** | ALL THREE trackers (engine + story + game) + all three spec folders (story-and-design steward spans all); both Matt queues; `style-register`; legacy-categorical-cleanup-audit |
| **knight-rider** | ALL THREE trackers (orchestrator — sequences engine build + story-decision queue + game-presentation build); both Matt queues; latest `agentic_orchestration/skill_handoff_*`; current hive-mind state file; engineering-disciplines |
| **jack-ryan** | engineering-disciplines; decisions-log; latest critique-pair / Gate dispatch |
| **rocket / gamora / star-lord** | `reap-die-rise-engine/` (your sections); engine tracker; engineering-disciplines |
| **drax** | `reap-die-rise-game/one-realm-mvp-scope.md` (THE build denominator) + `current-to-end-state-game.md` (the playable-build tracker — your delta); `reap-die-rise-story/` presentation sections; loadout / demo / godot repo READMEs |
| **galadriel** | `style-register`; visual-benchmark; geometry-vfx-coverage |
| **elrond** | substrate / catalogue / lineage layer (elrond-owned, outside these three folders) |
| **legolas** | latest gandalf request; relevant hive-mind protocol section |

**Do NOT re-walk the historical archive on every invocation.** It is searchable when needed; it is not pre-load material.

---

## When docs disagree

1. **The spec folders govern.** `reap-die-rise-{story,engine,game}/` override any older framing. Anything they superseded is git-lineage, not truth.
2. **The latter is canonical.** When two live docs disagree, the more recent wins.
3. **`decisions-log.md` is temporal ground truth** for decisions; if it disagrees with a spec/story doc, decisions-log wins.
4. **`engineering-disciplines.md`** overrides any older discipline lists.
5. **Cross-cutting canon** (these folders, decisions-log, disciplines, this router, AGENTS.md): the latest canonical-write wins. *(The Mac/PC two-host authority split retired 2026-06-30 with the PC team — single-host now.)*

---

## Drift-guards (locked vocabulary + dead branches)

*Held in the router — cheap to keep at the first-read surface.*

- **Locked term — `flavor element`:** thematic flavor variant of a primary `canonical_element` (pure naming/visual layer; does NOT change damage_scaling_type, affinity, or resistance). Retired: `sub-element`, `element canonical-pair flavor`.
- **DEAD — do not build on these:** isekai framing · **the death-faith frame** (DISSOLVED by Matt ruling 2026-07-28 — demigod-jailer / death-god patron / manufactured-rebellion keystone are superseded story canon; the Glitch Archive frame governs, `reap-die-rise-story/archive-frame.md`) · the warm future-self **spirit guide** as an entity (RETIRED 2026-06-30) · **seasonal-RELEASE** cadence (retired 2026-06-02; we ship runs/descents, not seasons) · pure-auto-combat (rejected; variable-execution-by-build is the lock) · mobile-first (PC/console-first) · non-humanoid playable forms · pre-imposed aesthetic/axis taxonomy (substrate votes). If you're building on any of these, stop — you're in a dead branch.

---

**Author:** gandalf, 2026-06-30 (canonical reorg, Tranche 2). The oracle remembered every doc; the router only needs to remember the three doors. Git keeps the rest.
