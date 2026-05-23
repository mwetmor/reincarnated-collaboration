# reincarnated-canonical-doc-format — Cross-cutting Reference Skill

> **STATUS:** CURRENT (load-bearing as of 2026-05-23) — Stream 3 cross-cutting reference skill per `canonical/02-roadmap.md` § 2.2
>
> **Skill packaging:** Markdown source for the eventual installable skill `reincarnated-canonical-doc-format` (per doc 38 § 4 step 2 + Skill Creator pass).

**Authored:** 2026-05-23
**Author:** gandalf (cross-cutting Stream 3 authoring; primary canonical-doc author)
**Authoritative source:** `canonical/00-ground-state.md` (ground-state oracle defines CURRENT / HISTORICAL / DEAD partitioning)
**Pattern:** universal reference wrapper; load when authoring or amending canonical/ + canonical/story/ docs
**Companion skills:** `reincarnated-engineering-disciplines`; `reincarnated-decision-log-format`; `reincarnated-critique-pair-gate-protocol`

---

## 0. What this skill IS and IS NOT

**IS:** the universal format-spec for canonical docs at `canonical/` (numbered keystone docs) and `canonical/story/` (story + lore + design artifacts). Names: header structure, STATUS protocol, cross-reference rules, oracle-registration requirement, ownership lineage. Loaded by any agent authoring or amending canonical artifacts (primarily gandalf; occasionally jack-ryan, knight-rider, gamora when the artifact crosses their seams).

**IS NOT:** the substantive content guide (each canonical doc's substance is per-topic; this skill governs FORMAT only). NOT the ground-state oracle itself (that's `canonical/00-ground-state.md`; ALWAYS the source of CURRENT-status truth). NOT the decisions-log format (that's `reincarnated-decision-log-format`; lighter temporal-decision format).

---

## 1. Where canonical docs live

| Path | Contents |
|---|---|
| `canonical/` | Numbered keystone docs (00 ground-state oracle; 02 roadmap; 37 engine-vs-game; 38 delivery strategy) |
| `canonical/story/` | Story + lore + design artifacts (substrate architecture, hive-mind protocols, recognition records, design-spec-as-math, etc.) |
| `canonical/historical/` | HISTORICAL-stamped docs (informative for lineage; NOT current truth) |
| `canonical/dead/` | DEAD-stamped docs (do NOT consult as current truth; preserved for archaeology) |
| `canonical/story/historical/` | Same partitioning for story docs |

**Authoring rule:** new docs land in `canonical/` (keystone) or `canonical/story/` (design/lore). Move to `historical/` or `dead/` only via explicit status demotion + 00-ground-state.md update.

---

## 2. Header structure (every canonical doc)

```markdown
# <Doc Title>

> **STATUS:** <CURRENT | HISTORICAL | DEAD> (load-bearing as of YYYY-MM-DD) — see `canonical/00-ground-state.md`

**Date:** YYYY-MM-DD (authoring session note)
**Author:** <agent name> (role description)
**Status:** v<N> <description of version + lock status>
**Authority:** Matt YYYY-MM-DD — <authorization note>
**Companion docs:**
- <path 1> — <one-line relationship>
- <path 2> — <one-line relationship>
- ...

---

## 0. TL;DR

<3-5 bullets or 1-3 paragraph summary>
<If recognition record: "Recognition Record — architectural commitments deferred per § X" framing required>

---

## 1-N. Substantive sections

<...>

---

## (Final). Cross-references

<canonical, operational, decisions-log, prior-art links>

---

**Signed:** <author> (role description)
**For:** <one-sentence purpose statement>
```

**Header field discipline:**
- **STATUS stamp** — CURRENT only when load-bearing; HISTORICAL when informative-only; DEAD when superseded structurally
- **Date** — initial authoring date; never edit (use amendment notes inline for revisions)
- **Author** — primary author; co-authors named in v<N> amendments
- **Status** — version + lock state (v1, v1.1, v2; "canonical lock" / "draft" / "recognition record")
- **Authority** — who authorized the artifact's existence + when (Matt for major commitments; gandalf for design-side; knight-rider for orchestration-side)
- **Companion docs** — direct dependencies + tight relationships; not exhaustive cross-references

---

## 3. STATUS protocol (CURRENT / HISTORICAL / DEAD)

Per `canonical/00-ground-state.md`:

| Status | Means | Do |
|---|---|---|
| **CURRENT** | Load-bearing top-of-stack | Treat as authoritative for ongoing work |
| **HISTORICAL** | Shaped current canon; not current truth | Consult for lineage only; do not direct |
| **DEAD** | Superseded structurally; do NOT consult | Treat as anti-pattern reference only |

**STATUS lifecycle:**

1. **New doc:** authored as CURRENT (if load-bearing) or as recognition record (commitments deferred)
2. **Demotion to HISTORICAL:** later canonical doc supersedes; this doc moves to `canonical/historical/` AND status edited to HISTORICAL
3. **Demotion to DEAD:** structural retirement (e.g., Pattern 4-5-6 retirements 2026-05-22); doc moves to `canonical/dead/`; status edited to DEAD with retirement note
4. **Re-stamp to CURRENT (rare):** operational re-stamp when doc resurfaces as load-bearing; precedent: visual-benchmark-vs2a, geometry-vfx-coverage-assessment, loadout-analytics-suite info-arch (2026-05-23 re-stamps)

**Ground-state oracle update required:**
- New CURRENT doc → add row to `canonical/00-ground-state.md` § 1
- Status demotion → move row from § 1 to § 2 (HISTORICAL) or § 3 (DEAD)
- Re-stamp to CURRENT → move row back to § 1

---

## 4. Cross-reference protocol

Cross-references in canonical docs:

- **Path-based** — `canonical/story/<doc>.md` or `~/Games/reincarnated-engine/<path>`; NOT URL-style
- **Section-anchored when load-bearing** — `canonical/story/<doc>.md § 6.4` not just the file
- **Bidirectional when substantive** — if doc A cites doc B as Companion, doc B should reference doc A back (especially for recognition records that get superseded)
- **Decisions-log entries by date-title** — `2026-05-12: Recompose-first arithmetic adoption` not by line number
- **Tags by name** — `v1.3-b14-2` not by commit hash
- **Commit hashes only when load-bearing** — `commit f72690f` for specific architectural locks

---

## 5. Recognition record special case

When authoring a recognition record (substantive design recognition + architectural commitments deferred per substrate-led discipline):

- **STATUS:** CURRENT — recognition records ARE load-bearing as recognition; the deferred commitments are not load-bearing
- **TL;DR framing:** explicit "Recognition Record — architectural commitments deferred per § X" line
- **Empirical-evidence criteria named** — what would gate re-engagement (specific substrate threshold, playtest result, methodology output)
- **Predictions registered** — if the recognition were to fire as architectural commitment, what would land
- **Precedent:** `canonical/story/fate-genre-recognition-and-mobile-alignment-trajectory-2026-05-23.md`

---

## 6. Ownership lineage

- **`canonical/00-ground-state.md`** — gandalf authors + maintains (oracle)
- **`canonical/02-roadmap.md`** — gandalf authors + maintains; knight-rider co-maintenance authority
- **`canonical/<NN>-<topic>.md`** — keystone docs; gandalf primary, knight-rider for orchestration-side, jack-ryan for process-side
- **`canonical/story/<topic>-YYYY-MM-DD.md`** — design/lore docs; primarily gandalf; occasionally jack-ryan (process), gamora (simulation-architecture), star-lord (pipeline-architecture)
- **HISTORICAL/DEAD demotions** — gandalf approves; knight-rider executes restructure dispatch

---

## 7. Update protocol for this skill

This skill evolves when:
- A new STATUS state lands (rare — partitioning is stable)
- A new header field becomes load-bearing
- A new recognition-record pattern is established (e.g., new framing requirements)
- A new sub-folder partitioning lands

Authored / maintained by **gandalf** (cross-cutting Stream 3 owner + primary canonical-doc author).

---

**Signed:** gandalf (cross-cutting Stream 3 reference-skill author)
**For:** the universal format-spec for authoring canonical docs at `canonical/` + `canonical/story/`. Header structure + STATUS protocol + cross-reference rules + ground-state oracle registration + recognition-record special case. Authoritative source for CURRENT-status truth remains `canonical/00-ground-state.md`.
