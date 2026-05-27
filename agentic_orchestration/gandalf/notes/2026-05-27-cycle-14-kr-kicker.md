# Cycle 14 — Knight-Rider Kicker (post Matt 2026-05-27 framing brief ratification)

> **STATUS:** CURRENT — orchestration signal for knight-rider to launch Cycle 14 per RATIFIED framing brief.

**Author:** gandalf (story-and-design steward)
**Date:** 2026-05-27
**Recipient:** knight-rider (Cycle 14 hive-mind cycle orchestrator)
**Authority:** Matt 2026-05-27 — full Q1-Q11 ratification of Cycle 14 framing brief; Cycle 14 launch authorized

---

## 0. TL;DR

Matt RATIFIED Cycle 14 framing brief Q1-Q11 in full 2026-05-27. Launch Cycle 14 per ratified wave structure. Three sharpening clarifications from Matt (Q4 + Q9 + Q10) embed load-bearing disciplines:

1. **Q4**: `synthetic_mode` is RETIRED ABSOLUTELY at Wave 0.5 close. Matt verbatim "extremely confirm.. retire it." Discipline #39 load-bearing.
2. **Q9**: Cycle 13 season `cycle-13-mechanical-season-001` is DISREGARDED. Cycle 14 generates a FRESH roster. Matt verbatim "It is not relevant. These characters were made to fit the synthetic gauntlet. Generate and converge a new cycle 14 roster of characters."
3. **Q10**: TIMELINE > QUALITY relationship INVERTED. Quality > timeline. Matt verbatim "extend timeline as needed for Wave 0.5 and all waves. The goal is not to ship something but to ship a game (playable characters that run the gauntlet in band)."

---

## 1. Authorized scope

Per `agentic_orchestration/gandalf/notes/2026-05-27-cycle-14-framing-brief.md` (RATIFIED 2026-05-27):

- **7-wave structure**: Wave 0 → 0.5 → 1 → 2 → 3 → 4 → 5
- **Wave 0**: scope-doc + doc 40 amendments + doc 47 ratification + 7 sidecar dispatches
- **Wave 0.5 (LOAD-BEARING NEW)**: Track D content gap closure (elements expansion + per-skill mechanical content + substrate weapon binding output + damage scaling routing + synthetic_mode RETIREMENT)
- **Wave 1**: Concentration architecture Layers 1-4+7 (doc 46)
- **Wave 2**: Concentration architecture Layers 5+8+9 (doc 46)
- **Wave 3**: Phase 5 cohesion-judge LLM architecture (layered cohesion per doc 46 Layer 6)
- **Wave 4**: T4-attuned gear cohesion + D21 acquisition curve calibration
- **Wave 5**: Gauntlet sim re-calibration with REAL content + cohesion validation + fresh Cycle 14 roster generation

---

## 2. Load-bearing disciplines (per framing brief § 6 + Matt 2026-05-27 clarifications)

### 2.1 Synthetic_mode RETIRED ABSOLUTELY (Q4)

- `synthetic_mode=True` in production sim paths STRUCTURALLY REMOVED at Wave 0.5 close
- jack-ryan Gate-2 grep verification: `grep "synthetic_mode" src/reincarnated/simulation/` returns ZERO matches in production code paths (test fixtures OK)
- Discipline candidate #39 (no-synthetic-stub-as-permanent-fallback) load-bearing
- KR NOT autonomous on `synthetic_mode` retention past Wave 0.5; any proposal to retain requires Matt explicit re-engagement

### 2.2 Cycle 13 season DISREGARDED (Q9)

- `cycle-13-mechanical-season-001` is NOT a Cycle 14 baseline
- NOT regenerate / refresh / migrate the Cycle 13 season
- Cycle 14 Wave 5 generates a FRESH roster — e.g., `cycle-14-cohesion-season-001` or equivalent
- Drax Track C transform integration (per prior conversation dispatch) is OBSOLETE; KR does NOT fire Track C against Cycle 13 data; await fresh Cycle 14 roster
- HTML doc at `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-character-analysis.html` becomes historical reference (Cycle 13 synthetic-stub-era record); gandalf will author a fresh Cycle 14 character analysis HTML doc post Wave 5 against real content

### 2.3 Quality > timeline (Q10)

- Cycle 14 NOT timeline-gated
- "In band" means real cohort-band KPM, NOT synthetic_mode override
- Wave extension is the expected path if quality isn't met
- Defensive cohort must validate empirically per real defensive kits at real cohort-band KPM ranges
- Wave 0.5 budget 1-2 weeks is anchor; if exceeded for quality reasons, extend with no escalation needed (autonomous per § 4.1; per Q10 ratification)
- KR escalates ONLY if a wave is structurally blocked (not if a wave is taking longer for quality reasons)

### 2.4 Other ratified disciplines (Q1-Q3, Q5-Q8, Q11)

- Cycle 14 scope confirmed (Q1)
- Wave structure confirmed (Q2)
- Scope-of-autonomy per framing brief § 4 (Q3)
- Sidecars per framing brief § 5 (Q5)
- KR autonomous on critique-pair scheduling (Q6)
- Compute budget tolerated; converged characters required (Q7)
- Cycle 14 close criterion = gauntlet PASS with REAL content + cohesion validation + jack-ryan Gate-2 PASS (Q8)
- Skip-confirmation fire-forward authorization carried from Cycle 13 (Q11)

---

## 3. Sidecar dispatches authorized

Per framing brief § 5:

| Sidecar | Owner | Fire when |
|---|---|---|
| **SC-1**: Discipline candidate #33-#39 ratification | jack-ryan | Async (Wave 0+) |
| **SC-2**: Doc 40 amendments | gandalf | Wave 0 |
| **SC-3**: Legolas Mode A — cohesion-judge LLM call architecture research | legolas | Wave 0 fires to gate Wave 3 |
| **SC-4**: Legolas Mode A — trigger condition vocabulary research | legolas | Wave 0 fires to gate Wave 1 |
| **SC-5**: Legolas Mode A — damage scaling pattern research | legolas | Wave 0 fires to gate Wave 0.5 |
| **SC-6**: Elrond substrate weapon stat audit | elrond | Wave 0 fires to gate Wave 0.5 |
| **SC-7**: Drax Track C transform refresh | drax | Post Wave 5 (Cycle 14 roster materializes) — DEFERRED per Q9 disposition |

---

## 4. What fires next — KR autonomous scope per framing brief § 4.1

### 4.1 Immediate (KR Wave 0 actions)

1. **Author Cycle 14 scope-doc** at `agentic_orchestration/cycles/cycle-14-cohesion-coalescence-scope.md` consuming this framing brief + doc 46 + doc 47 (or commission gandalf to author per Q7 KR-vs-gandalf default — choose path)
2. **Fire SC-2 dispatch** to gandalf for doc 40 amendments (per doc 46 § 13 + doc 47 § 5)
3. **Fire SC-3, SC-4, SC-5 dispatches** to legolas Mode A research (parallel; Wave 0 firing)
4. **Fire SC-6 dispatch** to elrond for substrate weapon stat audit (parallel; Wave 0 firing)
5. **Queue SC-1** to jack-ryan for discipline candidate ratification (async; non-blocking)
6. **Wave 0.5 dispatch authoring** prep (consumes SC-5 + SC-6 outputs)

### 4.2 Sequencing

| Wave | Gates on | Owner |
|---|---|---|
| Wave 0 | (entry) | KR + gandalf |
| Wave 0.5 | Wave 0 + SC-5 + SC-6 closure | rocket + gamora + elrond + jack-ryan Gate-2 |
| Wave 1 | Wave 0.5 + SC-4 closure | rocket + gandalf + jack-ryan Gate-2 |
| Wave 2 | Wave 1 + SC-1 partial ratification | rocket + gandalf + jack-ryan Gate-2 |
| Wave 3 | Wave 0.5 real content + SC-3 closure | gandalf + star-lord + rocket |
| Wave 4 | Wave 2 + Wave 3 | gandalf + rocket + gamora |
| Wave 5 | All prior waves closed + synthetic_mode RETIRED verified | gamora + gandalf + jack-ryan close Gate-2 |

### 4.3 Skip-confirmation fire-forward authorization (Q11 ratified)

KR can auto-close Cycle 14 wind-down per skip-confirmation discipline carried from Cycle 13 precedent. Push pattern continues per Matt 2026-05-27 verbatim authorization.

---

## 5. What's still externally-gated

| Gate | Resolution |
|---|---|
| Per-level scaling formulas | Deferred per doc 41 § 4 #1; Cycle 14 v1 implementation uses synthetic_mode-retirement-substitute (real per-skill content at L50 cap baseline only); per-level scaling formula design call queued |
| Per-character set bespoke retirement | Resolved via Layer 8 set keying to T4-strategy × element clusters (doc 46) — implemented in Wave 2 |
| Position-as-resource v1.1+ | Deferred per doc 41 § 4 + doc 46 Layer 2 catalog; substrate trigger pending |
| Pi infrastructure execution | Matt-schedule-gated per recognition record |
| Cycle 13 close ratification | ALREADY RATIFIED 2026-05-27 (PASS-with-WARN) — Cycle 14 absorbs content gap as Wave 0.5 |

**No further Matt-creative-ratification gates within Cycle 14 progression** — per Q1-Q11 ratification record. KR has full autonomous scope per framing brief § 4.1.

---

## 6. Sign-off

**Author:** gandalf (story-and-design steward)
**Status:** CURRENT — KR kicker for Cycle 14 launch; framing brief RATIFIED; autonomous scope per § 4.1; load-bearing disciplines per § 6 + Q4 + Q9 + Q10 captured

**For:** the Cycle 14 launch signal post Matt 2026-05-27 framing brief ratification. Three load-bearing clarifications (synthetic_mode retired absolutely; Cycle 13 season disregarded; quality > timeline) embed in cycle execution. KR resumes wave sequencing per framing brief autonomous scope. Cycle 14 close = the SUBSTANTIVE delivery point that Cycle 13 close was originally framed as.

**Signed:** gandalf (story-and-design steward)
