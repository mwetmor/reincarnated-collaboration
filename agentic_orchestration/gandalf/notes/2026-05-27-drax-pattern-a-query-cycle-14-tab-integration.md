# Drax Pattern-A Query — Cycle 14 Tab Integration Verification

> **STATUS:** CURRENT — Pattern-A query for KR to route to drax (loadout app seam owner). Verifies current drax tab state vs Cycle 14 Wave 5 production requirements + doc 49 Loadout/Sample distinction.

**Author:** gandalf (story-and-design steward)
**Date:** 2026-05-27 evening
**Recipient (via KR routing):** drax (Reincarnated loadout app seam)
**Authority:** Matt 2026-05-27 verbatim "Will there be any decisions resulting from the added pieces here?" + "I would like to replace the prior Canary season's data in the Summary tab with this first New Engine season data" + Loadout/Sample distinction clarification
**Source docs:**
- `canonical/49-loadout-sample-player-surface-design-2026-05-27.md` (just authored; load-bearing for this query)
- `agentic_orchestration/gandalf/notes/2026-05-27-path-iii-faction-assembly-extension.md` (Path III + drax surfacing requirements)
- `agentic_orchestration/gandalf/notes/2026-05-27-no-classes-architectural-recommitment.md` (vocabulary lock at player-surface)
- Star-lord Seam 3 commits (`bf7f659` ExportFactionCluster + `94f8c88` PM1-wiring)

---

## 0. TL;DR

Drax Pattern-A query — verify current loadout app tab integration state across 6 tabs (Summary / Loadout / Sample / Analytics / Encounters / Court) against Cycle 14 Wave 5 production data emission + doc 49 Loadout/Sample distinction. Identify integration gaps requiring follow-on dispatches.

---

## 1. Pattern-A query for KR to route to drax

**Pasteable to KR:**

---

**Drax Pattern-A query — Cycle 14 tab integration verification**

**Subject:** Verify current loadout app tab integration state against Cycle 14 Wave 5 production data emission + doc 49 Loadout/Sample distinction.

**Required reading before responding:**
- `canonical/49-loadout-sample-player-surface-design-2026-05-27.md` (NEW; load-bearing for this query; locks Loadout vs Sample distinction; specifies engine emission requirements per tab)
- `agentic_orchestration/gandalf/notes/2026-05-27-no-classes-architectural-recommitment.md` (vocabulary lock at player-surface labels — NO "class" vocabulary in tab labels)
- `agentic_orchestration/gandalf/notes/2026-05-27-path-iii-faction-assembly-extension.md` (G-B primary_faction_pair + F-C inter-faction relationships at Summary tab)
- Star-lord Seam 3 commits: `bf7f659` (ExportFactionCluster 21 fields) + `94f8c88` (PM1-wiring G-B fields added)

**Verification questions (per-tab):**

### 1.1 Summary tab

Q-Summary-1: Is Summary tab currently grouping characters by **Season** or by **Faction**? Matt 2026-05-27 requests Faction grouping for Cycle 14 (only one new-engine season; faction grouping more useful than season).

Q-Summary-2: Does Summary tab consume ExportFactionCluster schema (Star-lord `bf7f659`)? Specifically:
- `faction_label_canonical` (LLM-generated name per PM-2 D-Hybrid)
- `cluster_compactness` + `cosine_similarity_max` + `diversity_flag` (per Phase 7 spec § 2.3)
- `primary_pair_flag` (per G-B selection; Star-lord `94f8c88`)
- `gb_selection_rationale` + `pairwise_distance_distribution` (per G-B telemetry)

Q-Summary-3: Will Summary tab consume ExportFactionRelationship (Path III F-C; Wave 3 dispatch authoring imminent) for inter-faction narrative surfacing? If yes, what's the expected drax wiring effort?

Q-Summary-4: **Seasonal hero selection mechanism** — currently no engine emission selects "seasonal hero." gandalf-recommend H-5 hybrid (substrate-led top-3 + gandalf curation) per Path III recognition record. Is there a current seasonal-hero mechanism in drax, or NEW work required?

Q-Summary-5: **Character image rendering** — Matt 2026-05-27 requests legolas-generated character images + galadriel AI-tell inspection (<5 fingers; same outfit). Phase 6 visual coalescence is DEFERRED Cycle 15+ per Path (1). Possible lighter Cycle 14 sidecar (G-2 parallel sidecar gandalf-recommend). Is current Summary tab rendering any character images? What's the implementation gap for the lighter Cycle 14 sidecar?

Q-Summary-6: Replace prior **Canary season's data** with Cycle 14 first-New-Engine-season data — what's the current Canary-season-display state? Is replacement a config swap OR substantive integration work?

### 1.2 Loadout tab

Q-Loadout-1: Is the Loadout tab currently implemented per doc 49 § 1.1 spec? Specifically:
- (a) Empty skill tree (all nodes uninvested) at startup
- (b) Per-node investment slots respecting prerequisites + chain depth + branching gates (D69)
- (c) ONE T4 capstone toggleable
- (d) Gear catalog filtered by kit fit (primary_stat + weapon_type_family)
- (e) Live stat calculator (per doc 47 § 4 damage formulas + doc 41 progression scaling)
- (f) User per-kit-per-build theorycraft persistence

Q-Loadout-2: If Loadout tab is NOT fully implemented, identify the implementation gap per (a)-(f) above. Which dimensions are LANDED vs MISSING?

Q-Loadout-3: Drax-side stat calculator — is there a current implementation? Does it reference doc 47 § 4 formulas accurately? Or does drax compute stats differently? **Single source of truth: doc 47 § 4 IS the authoritative damage scaling.**

Q-Loadout-4: User persistence layer for theorycraft state — is drax-side database in place for saving builds per user per kit? OR is this NEW work?

Q-Loadout-5: Gear catalog source — drax consumes which gear pool? Currently per-season gear pool exists from Cycle 13 work; Wave 4 produces full Cycle 14 gear pool (sets + legendary + T4-attuned annotations). Wave 4 dependency surfaced.

Q-Loadout-6: Reset capability — can player reset investment + clear gear selections? Sandbox semantics per doc 49 § 1.1.

### 1.3 Sample tab

Q-Sample-1: Is the Sample tab currently implemented per doc 49 § 1.2 spec? Specifically:
- (a) Immutable read-only display of kit AS gauntlet-passed
- (b) Skill investment LOCKED at gauntlet-passed state
- (c) Active T4 LOCKED per `active_t4_chain` field
- (d) Gear loadout LOCKED per gear_representative + Wave 4 specific gear instances
- (e) Statistics IMMUTABLE per gauntlet-time computation

Q-Sample-2: Per doc 49 § 2.3 hybrid derivation — does drax derive Sample tab from engine kit_committed_state directly? Or compute differently? **Single source of truth: engine kit_committed_state IS the canonical Sample data.**

Q-Sample-3: Sample tab DOES NOT permit editing — confirm read-only enforcement is operational. Any state mutation attempt should be inert.

Q-Sample-4: Composition with Path III primary_faction_pair + inter-faction relationships — does Sample tab surface kit's faction membership + primary-pair status + inter-faction tension narratives? OR is this Summary-tab-only?

### 1.4 Analytics tab

Q-Analytics-1: Does Analytics tab consume star-lord telemetry (Q-E-3 telemetry per Phase 4 Gamora Dispatch 3A `749d5aa`)? Specifically:
- Cohort KPM band distribution
- Phase 7 verdict tracking (`phase7_gate_status` per ExportFactionCluster)
- G-B pairwise distance distribution (per Star-lord `94f8c88` `gb_selection_rationale` + `pairwise_distance_distribution`)
- Substrate-anchor distribution (D-Sharpened metadata)
- LLM call volume + cost tracking (SC-3 + Path III F-C)

Q-Analytics-2: F-C inter-faction relationship analytics — when Wave 3 lands, will Analytics surface relationship_type distribution + tension_narrative diversity (TF-IDF cosine distance per Star-lord Seam 3) + ai_tell_compliance_score tracking?

Q-Analytics-3: Discipline #43 design-quality audit at wave-close — does Analytics tab surface gandalf audit verdicts (PASS / PASS-with-design-concerns / DRIFT-DETECTED) per wave? Composes with Phase 7 IMPL verdict emission.

### 1.5 Encounters tab

Q-Encounters-1: Encounter set — currently displays Cycle 13's ~18 reference encounters? OR new Cycle 14 encounter set? D-6 from gandalf-recommend: reuse Cycle 13 18 encounters; new encounter set only if substantial change required.

Q-Encounters-2: Per-encounter difficulty + cohort fit display — does Encounters tab surface Phase 7 verdict per (kit × encounter) tuple per gamora Phase 7 IMPL hand-back? Gates on Phase 7 IMPL close.

Q-Encounters-3: Spatial-gauntlet vs scalar-gauntlet — per gamora Pattern-A response, `spatial_gauntlet/` is R2 research; `gauntlet_sim.py` is 1D scalar production sim. Encounters tab consumes scalar gauntlet output only? OR has hooks for future spatial integration?

### 1.6 Court tab

Q-Court-1: Court tab current population — currently empty? Or populated with prior-season Spirits? Per Cycle 14 v1 spec: minimal single-season first-emergence view OK (per canonical_archetype_register first-emergence registration per Math Note 5 E2 at Wave 5 commit).

Q-Court-2: Full Court mechanics (cross-season Spirit accumulation; ascension records; archetype-shape lineage tracking) is DEFERRED Cycle 15+ per `project_earth_meta_layer` memory. Confirm Cycle 14 v1 Court tab scope is minimal-single-season view, NOT full mechanics?

Q-Court-3: canonical_archetype_register schema — per Math Note 5 E2 + Path III recognition. Does drax consume this? OR is it engine-internal only at Cycle 14 v1?

### 1.7 Cross-tab + No-classes vocabulary compliance

Q-Cross-1: **Vocabulary lock compliance (Discipline #45)** — verify NO "class" vocabulary appears in player-facing tab labels. Acceptable: Spirit / Form / Kit / Archetype / Faction Member. Unacceptable: Class / Class Name / Class Selection. If "class" vocabulary exists, identify locations for redaction.

Q-Cross-2: **Token cost projection** — what's drax-side LLM call volume (if any) for tab rendering? Should be ZERO at drax tier (LLM calls happen at star-lord seam during Phase 5 cohesion-judge). Drax consumes already-LLM-generated text.

Q-Cross-3: **Star-lord Track C transform consumption** — does drax currently consume Track C transform output? Per § 3 of doc 49: Track C should emit `kit_shape` + `kit_committed_state` + `kit_metadata` + `season_metadata`. Confirm or identify gaps.

---

## 2. Expected output structure

Pattern A-light structured critique format per gandalf OP § 2:

```
[CURRENT STATE — per tab]
- Summary tab: <status; integration with Cycle 14 schemas>
- Loadout tab: <status; doc 49 § 1.1 compliance>
- Sample tab: <status; doc 49 § 1.2 compliance>
- Analytics tab: <status; telemetry consumption>
- Encounters tab: <status; encounter set + Phase 7 verdict>
- Court tab: <status; minimal v1 vs Cycle 15+ full>

[IMPLEMENTATION GAPS — per dimension]
- Engine schema consumption gaps
- Doc 49 compliance gaps
- Vocabulary lock (Discipline #45) compliance gaps
- Wave 4 gear pool dependency surfacing

[EFFORT ESTIMATES]
- Per-tab integration effort (low / medium / high)
- Per-schema wiring effort
- Net Cycle 14 timeline impact for full drax integration

[RECOMMENDED ROUTING]
- Follow-on dispatch requirements (if any)
- KR scope adjustments needed (if any)
- Pattern-B engagement with Matt (if any decisions surface)

[OPEN QUESTIONS]
- Any items requiring Matt design call
```

≤200 words inline OR file output at `agentic_orchestration/drax/notes/2026-05-27-cycle-14-tab-integration-pattern-a-response.md` per gandalf OP § 2 Pattern A discriminator. Drax decides per invocation shape.

---

## 3. Composition with current Cycle 14 sequencing

### 3.1 What this Pattern-A query unblocks

Drax response identifies integration gaps. Gaps surface as:
- **Cycle 14 scope additions** (if Wave 5 production season requires drax integration work)
- **Cycle 15+ deferred items** (if integration is Cycle 15+ territory)
- **Matt design calls** (if scope decisions surface)

### 3.2 Composition with Wave 4 + Wave 5 sequencing

| Wave | Drax dependency |
|---|---|
| **Wave 3 (Phase 5 LLM)** | ExportFactionRelationship schema → drax Summary tab inter-faction narrative surfacing |
| **Wave 4 (T4-attuned gear + D21)** | Per-season gear pool + per-kit gear loadout → drax Loadout catalog + Sample display |
| **Phase 7 IMPL (gamora bridge)** | kit_archive ACCEPTED → gauntlet sim verdict → drax Sample tab + Encounters tab |
| **Wave 5 production season** | Full season output → drax Summary + Loadout + Sample + Analytics + Encounters + Court tabs |

Drax integration gaps should land BEFORE Wave 5 production season commits — otherwise Wave 5 output ships to a Cycle-13-era drax UI that can't surface Cycle 14's new schemas.

### 3.3 Cycle 14 timeline impact

| Drax integration scope | Estimated effort |
|---|---|
| Full doc 49 + Cycle 14 schemas integration | ~2-4 weeks drax sub-agent work |
| Minimal integration (Summary + Loadout + Sample core; defer Analytics + Encounters + Court polish) | ~1-2 weeks |
| Verification-only (no new integration; current tabs verified compatible) | ~half-day |

Pattern-A response identifies which scope applies.

---

## 4. Routing instructions for KR

**Sequencing:**

1. KR consumes this Pattern-A query doc + companion `canonical/49-loadout-sample-player-surface-design-2026-05-27.md`
2. KR fires drax sub-agent with this query + required reading list
3. Drax sub-agent responds Pattern A-light (≤200 words inline) OR Pattern A-deep (file output at specified path; if multi-question structure warrants)
4. Response identifies gaps + effort estimates + routing recommendations
5. KR routes follow-on dispatches per drax response (if Cycle 14 scope additions needed)
6. KR surfaces to Matt if scope decisions emerge requiring Pattern B engagement

**Apply Discipline #42 framing-audit at drax sub-agent invocation:** drax verifies the framing of this query before executing; can refuse (Discipline #44) if framing flaws caught.

**Apply Move 1 quality-criterion at dispatch authoring:** if follow-on drax dispatches fire, they include quality-criterion section per KR OP § 3.X.

---

## 5. Sign-off

**Author:** gandalf (story-and-design steward)
**Status:** CURRENT — Pattern-A query authored for KR to route to drax sub-agent verification of Cycle 14 tab integration state
**Authority:** Matt 2026-05-27 evening Loadout/Sample distinction articulation + Summary tab requirements + doc 49 canonical lock

**For:** verification of drax loadout app tab integration state across 6 tabs (Summary / Loadout / Sample / Analytics / Encounters / Court) against Cycle 14 Wave 5 production data emission + canonical doc 49 Loadout/Sample distinction + Path III faction-assembly extension + no-classes vocabulary lock. Identifies integration gaps requiring follow-on Cycle 14 dispatches OR Cycle 15+ deferral. Composes with Wave 3 + Wave 4 + Phase 7 IMPL + Wave 5 sequencing.

**Signed:** gandalf (story-and-design steward)
