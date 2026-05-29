# Discipline #48 RAM-Awareness Retirement — Recommendation to jack-ryan

> **STATUS:** CURRENT (gandalf retirement recommendation as of 2026-05-29 evening) — Matt 2026-05-29 evening direction: "Let's retire the RAM awareness." gandalf-authored retirement scope + reasoning; jack-ryan canonical-write target for `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` discipline-architecture amendment.

**Date:** 2026-05-29 evening
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-29 evening verbatim: "Let's retire the RAM awareness"
**Companion docs:**
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 48 — host-RAM-aware operational concurrency (R48.1-R48.5; jack-ryan canonical-write target)
- `agentic_orchestration/gandalf/notes/2026-05-28-mac-mini-freeze-diagnosis.md` — Discipline #48 founding incident artifact
- `agentic_orchestration/gandalf/notes/2026-05-29-cascade-resumption-3-class-eradication-authorization.md` — Amendment 2 R48.4 relaxation + Amendment 3 (this batch) full retirement

---

## 0. TL;DR

**Retire Discipline #48 host-RAM-aware operational concurrency** per Matt 2026-05-29 evening directive. Empirical re-validation: months of parallel sub-agent fan-out without freeze recurrence; the 2026-05-28 Mac mini freeze attribution to sub-agent fan-out was likely confounded with Matt's parallel installer workload at the same time.

**Specific R-prescription disposition:**

| R-prescription | Retain? | Rationale |
|---|---|---|
| R48.1 — no recursive `grep` against directory tree without `find -size +100M` pre-flight | **RETIRE under #48 + reclassify** | Empirically still load-bearing for oversized-file safety, BUT this is about grep-against-binary-content (operational safety), NOT RAM-awareness per se. Reclassify under Discipline #11 empirical inspection OR new Discipline #49 "Operational safety on grep/find against unknown content size" |
| R48.2 — no `grep` against single file > 200 MB without head/streaming/--max-count | **RETIRE under #48 + reclassify** | Same — oversized-file safety; reclassify with R48.1 |
| R48.3 — no `find -exec` against directory trees containing GB-scale binary content | **RETIRE under #48 + reclassify** | Same — oversized-file safety; reclassify with R48.1 + R48.2 |
| **R48.4 — single-seam sub-agent at a time; no parallel fan-out** | **RETIRE entirely** | Empirically refuted: months of parallel sub-agent fan-out without incident; 2026-05-28 freeze likely confounded with parallel installer workload |
| **R48.5 — pre-flight `vm_stat` confirm > 1 GB free if any operation expected to allocate > 500 MB** | **RETIRE entirely** | Same empirical refutation; macOS inactive-page reclamation handles RAM pressure naturally |

**Net architectural change:** Discipline #48 (as named: "host-RAM-aware operational concurrency") is retired entirely. R48.1/R48.2/R48.3 (oversized-file safety) reclassified under a different rubric per jack-ryan canonical-write.

---

## 1. Empirical re-validation of the 2026-05-28 freeze attribution

**Founding incident (per `2026-05-28-mac-mini-freeze-diagnosis.md`):** Mac mini freeze observed 2026-05-28 during multi-sub-agent dispatch period. At the time, attribution was to parallel sub-agent fan-out exhausting host RAM on 8 GB constrained system.

**Empirical re-validation (Matt 2026-05-29 evening claim):**
- Months of parallel sub-agent fan-out preceding the 2026-05-28 freeze without incident
- Matt confirmed parallel UE installer workload running concurrent with the sub-agent fan-out at the freeze moment
- UE installer (FC02 FileConstructionFail at 75% twice on this host) is empirically known to be RAM-intensive
- No subsequent freeze incidents under parallel sub-agent fan-out

**Honest assessment:** the 2026-05-28 incident's attribution to sub-agent fan-out was a confluence error. The freeze was likely Matt's parallel installer (UE installer being RAM-intensive + crashing twice at 75%) rather than the sub-agent fan-out. The sub-agent fan-out at ~600 MB RSS per agent × 2-3 concurrent = ~1.2-1.8 GB, well within macOS's inactive-page reclamation buffer on an 8 GB host.

**Discipline #42a framing-audit Instance 7 case-type (new):** "founding-incident-confounding-attribution" — when a discipline is authored from a single founding incident, the attribution may be confounded with concurrent confounding factors. Discipline authoring should empirically isolate variables OR explicitly flag attribution as provisional.

**Composes with Instance 6 (component-existence-context) pattern:** both are "claim propagated across canonical artifacts without empirical refutation cycle." Instance 7 specific to founding-incident attribution claims.

---

## 2. What this changes operationally

### 2.1 cascade-resumption-3 (immediate)

Already addressed in cascade-resumption-3 authorization Amendment 3 (this batch): R48.4 + R48.5 fully retired; parallel sub-agent fan-out at KR coordination discretion per dependency graph. Pre-flight vm_stat checks REMOVED from required-action sequence.

### 2.2 Future workstreams (post-Cycle-14)

| Workstream | Before retirement | After retirement |
|---|---|---|
| Hive-mind cycle Wave coordination | R48.4 single-seam constraint forced strict sequential dispatch | Parallel dispatch where dependency graph permits; KR coordinates fan-out |
| Substrate crawl / catalog work | R48.4 sweep-resident-on-host clause forced serialization | Sweep-resident workstreams self-throttle internally; KR can fire parallel non-sweep dispatches alongside |
| Math hotspot work (P2/P3/P5) | R48.4 effectively serialized math hotspots with other work | Math hotspots can fire parallel with non-conflicting work |
| Engine refactor + simulation | R48.4 + R48.5 pre-flight added ~5-15min per dispatch handoff | Pre-flight removed; faster dispatch handoffs |

**Trajectory implication:** Cycle 14 + Cycle 15 work programs estimated under sequential R48.4 constraint may be ~30-50% faster wall-clock under parallel-enabled architecture.

### 2.3 What still holds (R48.1/R48.2/R48.3 reclassification candidates)

These three prescriptions are NOT about RAM-awareness; they're about oversized-file operational safety:

- **R48.1 (recursive grep against dir tree without size pre-flight)** — protects against OOM on multi-GB binary content (Unreal asset directories, cache files, etc.)
- **R48.2 (grep against single file > 200 MB without streaming)** — protects against OOM on large JSON/SQL dumps
- **R48.3 (find -exec against GB-scale binary content trees)** — protects against process explosion + OOM

**jack-ryan canonical-write candidate location:**
- **Option A — reclassify under Discipline #11 (empirical inspection over assumption):** R48.1/R48.2/R48.3 become sub-prescriptions of Disc #11 because they're about empirically pre-flighting file sizes before running ops. Cleanest if the rubric fits.
- **Option B — new Discipline #49 "Operational safety on grep/find/exec against unknown content size":** standalone discipline if the rubric doesn't fit Disc #11 cleanly.
- **Option C — fold into Disc #5 (right tool for the validation question):** R48.1/R48.2/R48.3 are about using the right tool (streaming/--max-count/size-pre-flight) for grep/find ops. Marginal fit.

**gandalf recommendation:** Option B (new Discipline #49). The prescriptions are specific to oversized-file ops; deserve their own rubric. Disc #11 is about empirical inspection broadly; mixing oversized-file ops with general empirical inspection muddies the discipline.

---

## 3. jack-ryan canonical-write target

**Engineering-disciplines.md amendment scope:**

1. **§ 48 host-RAM-aware operational concurrency** — REPLACE current content with retirement entry:
   - Status: RETIRED 2026-05-29 per Matt directive + gandalf retirement recommendation
   - Founding incident attribution re-validated: confounded with parallel installer workload; not sub-agent fan-out
   - R48.4 + R48.5 retired entirely
   - R48.1/R48.2/R48.3 reclassified under § 49 (new) per gandalf Option B
   - Cross-reference to retirement note: `agentic_orchestration/gandalf/notes/2026-05-29-discipline-48-ram-awareness-retirement.md`

2. **§ 49 Operational safety on grep/find/exec against unknown content size** — NEW (replacing R48.1/R48.2/R48.3 content):
   - R49.1 — no recursive `grep` against directory tree without `find <dir> -size +100M` pre-flight
   - R49.2 — no `grep` against single file > 200 MB without head/streaming/--max-count
   - R49.3 — no `find -exec` against directory trees containing GB-scale binary content
   - Cross-reference to retirement note (lineage from § 48)

3. **Discipline-list amendment** (if engineering-disciplines.md has a top-level list):
   - § 48 marker: RETIRED
   - § 49 marker: NEW (oversized-file operational safety)

4. **Decisions-log entry** (jack-ryan canonical-write):
   - 2026-05-29: Discipline #48 host-RAM-aware operational concurrency RETIRED + § 49 NEW
   - Reasoning: empirical re-validation refutes founding-incident attribution; months of parallel sub-agent fan-out without incident; oversized-file safety prescriptions (R48.1/R48.2/R48.3) reclassified under § 49
   - Status: LOCKED per Matt 2026-05-29 evening directive

---

## 4. Composition with cascade-resumption-3 Amendment 3

Cascade-resumption-3 authorization Amendment 3 (same commit batch):
- R48.4 + R48.5 references in authorization text struck through OR marked RETIRED
- Pre-flight vm_stat actions removed from required-action sequences
- Parallel sub-agent fan-out enabled unconditionally per dependency graph (Amendment 2 was conditional on R48.5 pre-flight; Amendment 3 makes unconditional)
- Trajectory estimate updated to remove pre-flight handoff overhead

Cascade-resumption-3 continues with Amendment 3 architecture; current KR session reads the amendment + proceeds without halt+restart.

---

## 5. Discipline #42a Instance 7 sub-case capture (new)

**Instance 7 case-type — founding-incident-confounding-attribution:**

When a discipline is authored from a single founding incident, attribution may be confounded with concurrent confounding factors. Discipline authoring should empirically isolate variables (e.g., observe incident under fan-out alone vs fan-out + installer; with-vs-without conditions) before locking attribution.

**Instance 7 founding case:** Discipline #48 RAM-awareness — founding incident attributed to sub-agent fan-out; empirically refuted via months of parallel fan-out without incident; likely confounded with parallel UE installer workload.

**Discipline #42a Q-extension:** "isolate confounding variables at discipline-founding-incident" — Q7 (NEW) at framing-audit checklist for discipline-authoring time.

**gandalf will add Instance 7 to pushback memo amendment in next batch** (separable from this retirement note; non-blocking).

---

## 6. Sign-off

**Authored:** gandalf (story-and-design steward) per Matt 2026-05-29 evening directive

**For:** the durable retirement recommendation + jack-ryan canonical-write target specification + Instance 7 case-type capture + composition with cascade-resumption-3 Amendment 3

**Next steps:**
1. Cascade-resumption-3 Amendment 3 commits in this batch (formalizes R48.4 + R48.5 retirement in authorization scope)
2. jack-ryan consumes this retirement recommendation at next canonical-write window (post-cascade-close OR earlier if Matt elects)
3. Engineering-disciplines.md § 48 RETIRED + § 49 NEW lands at next jack-ryan canonical-write commit
4. Decisions-log entry per § 3 of this note
5. Pushback memo Instance 7 amendment by gandalf at next batch (non-blocking)

**Discipline-architecture observation:** this retirement is the second discipline-amendment in 24 hours (first: Amendment 2 R48.4 relaxation per parallel fan-out evidence; second: full retirement per Matt directive). Pattern: empirical re-validation of disciplines under operational use surfaces founding-incident-confounding-attribution failures. Worth jack-ryan + gandalf design-quality reflection at Cycle 14 wave-close on the discipline-architecture maturation pattern.
