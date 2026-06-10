# David-H WS3.1 Routing Memo — Mantis Fire Signal + WS3 WARN Amendments + BLOCK-WS1-A Ratification

**STATUS:** FIRE — WS3.1 routed to mantis; WS3 commission amended in-line per Sam Gate-1 § 6
**Date:** 2026-06-10
**Author:** david-h (PC-side orchestrator)
**Authority:** Matt 2026-06-10 routing ratifications (BLOCK-WS1-A Path A; WS3.1 GO signal)
**Audience:** mantis (executor); sam (Gate-2 downstream); knight-rider (cross-host fetch at next Mac session)
**Companion docs (read in order):**

1. `agentic_orchestration/dispatches/2026-06-10-david-h-ws3-materialization-cinematic-sequencer-commission.md` (gandalf commission; baseline scope)
2. `agentic_orchestration/qa/findings/2026-06-10-gate-1-ws1-ws3-paired-pre-fire.md` (Sam Gate-1 PASS-WITH-AMENDMENTS; 4 WS3 WARN amendments captured § 4 + § 6.2)
3. `canonical/story/2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md` § 2.5 materialization cinematic + § 12.9 spirit guide voice patterns + § 12.13 voice-acting deferral
4. `agentic_orchestration/dispatches/2026-06-08-david-h-ue-mcp-bridge-spike-AMENDMENT-db-lyon-primary.md` (db-lyon Sequencer 7/7 validated tooling baseline)

---

## 0. TL;DR

**Matt routing ratifications (2026-06-10):**

1. **BLOCK-WS1-A → Path A ratified** — multi-repo PC clones (`reincarnated-engine` + `reincarnated-loadout` added to `C:\dev\`) + engine emits substrate-registry + experiential-axes JSON sidecars. Mac-side execution chain follows separately (Matt schedules PC clones; gandalf authors 2 JSON sidecar design-specs; rocket + gamora implement engine emit; engine pushes; PC pulls). **WS1 fires AFTER BLOCK resolution; not now.**

2. **WS3.1 → GO signal** — fire WS3.1 mantis Sequencer asset authoring NOW, in parallel with BLOCK-WS1-A Mac-side resolution. WS3.1 has no WS1 data dependency at the asset-authoring layer (placeholder data acceptable per Sam Gate-1 § 5 INFO-CROSS-A Path 2 interleaved phasing).

**Phase-partition (explicit per WARN-WS3-B):**

| Phase | Gates on | Status |
|---|---|---|
| WS3.1 (Sequencer asset authoring + 5-track structure) | None — placeholder data acceptable | **FIRES NOW** |
| WS3.2 (4-phase spirit form keyframe animation) | WS1 GREEN | DEFERRED |
| WS3.3 (Spirit guide voice integration) | WS1 GREEN (matched-kit ID for voice text) | DEFERRED |
| WS3.4 (Camera composition) | WS1 GREEN | DEFERRED |
| WS3.5 (WS3 close report) | WS3.2-4 GREEN + Sam Gate-2 PASS | DEFERRED |
| Criterion #9 (Composition with WS1 DataTables operational) | WS1 GREEN | DEFERRED |

WS3.1 IS the wave's fire scope. WS3.2-WS3.5 + criterion #9 verification activate post-WS1-GREEN in a downstream wave.

**Estimated wall-clock for WS3.1 isolated:** 3-7 days (Sequencer asset + 5 tracks + persistence + Editor close/reopen verification + Sam Gate-2 + david-h wave-close memo). Sub-scope of the 1-3 week full-WS3 estimate.

---

## 1. WS3.1 mantis scope (consolidated; supersedes WS3 commission § 2 Phase WS3.1 for fire purposes)

Mantis executes the following sub-scope per db-lyon Sequencer 7/7 validated tooling:

### 1.1 Sequencer asset creation

- Create materialization cinematic Sequencer asset via db-lyon `create_sequence` action
- Asset location: project Content directory (mantis chooses UE-idiomatic location per asset organization convention; document choice in close report)
- Asset name: `LS_Materialization_Cinematic` (or mantis-chosen UE-idiomatic name; document choice)
- **Acceptance check:** asset visible in Content Browser; opens in Sequencer editor

### 1.2 5-track structure (per WS3 commission § 1.2 db-lyon action map)

Mantis adds 5 tracks via db-lyon `add_track` action:

| # | Track | Type | Placeholder data | Note |
|---|---|---|---|---|
| 1 | Camera | CineCameraActor track or CameraComponent transform | Default camera at origin; no keyframes | WS3.4 keyframes the composition |
| 2 | Spirit form transform | Actor transform / Skeletal mesh transform | Placeholder actor (cube or default character mesh); identity transform | WS3.2 keyframes the 4-phase transformation |
| 3 | VFX | **Sequencer-native particle-system track OR placeholder track** (see § 2.1 WS3 WARN-A amendment) | Empty section or placeholder Cascade particle reference | Niagara cluster-rune integration DEFERRED to vertical-slice spike (gates on WS2 GREEN per Option B Niagara windowed-mode verification) |
| 4 | Audio | AudioComponent / SoundCue track | Empty section or placeholder silence asset | WS3.3 integrates spirit guide voice (templated TTS placeholder OR silent caption track per § 2.2 WS3 WARN-D amendment) |
| 5 | Spirit guide voice | Sub-track or dedicated audio track per § 12.9 voice patterns | Empty section or placeholder silence asset | WS3.3 integrates templated voice per § 12.9 |

**Acceptance check:** 5 tracks visible in Sequencer editor; each track is correctly typed; mantis documents each track type in close report for downstream WS3.2-WS3.5 + vertical-slice spike consumption.

### 1.3 Asset persistence

- Save Sequencer asset via db-lyon `save_asset` action
- Verify persistence: close UE Editor; reopen; confirm asset + 5 tracks present
- **Acceptance check:** asset persists; 5 tracks intact post-close-reopen

### 1.4 Mantis close report content (mandatory)

Mantis authors close report at `agentic_orchestration/mantis/notes/2026-06-10-ws3-1-sequencer-asset-close.md` (or next-business-day-date file if execution crosses days). Required sections:

1. **Per-acceptance-criterion verdict** (matches numbered acceptance criteria in § 3 below)
2. **Sequencer asset location + name** (Content Browser path; asset name)
3. **5-track structure document** (per-track type + UE class/struct used)
4. **Persistence verification evidence** (close/reopen sequence + verification screenshot or log)
5. **Performance observation at WS3.1 scope** (Editor frame rate during Sequencer playback of empty sequence; for WS3.2-WS3.5 framerate criterion #8 reference per § 2.3 WS3 WARN-C amendment)
6. **D7 AI-tell line preservation note** (no raw LLM dialogue in track authoring; all voice deferred to templated)
7. **Gap notes for downstream WS3.2-WS3.5** (what asset structure assumptions WS3.2-WS3.4 will need to consume; what data WS3.2 needs from WS1 once WS1 GREEN)
8. **db-lyon tooling observations** (any divergence from 7/7 PASS baseline at production WS3.1 scope; any tool-call quirks worth surfacing for future use)

---

## 2. WS3 commission amendments per Sam Gate-1 § 6.2 (apply at mantis consumption layer; commission text not edited in-place)

David-H captures the 4 WS3 WARN amendments inline below; mantis treats this routing memo as the authoritative scope-of-fire for WS3.1. The gandalf commission baseline (`2026-06-10-david-h-ws3-materialization-cinematic-sequencer-commission.md`) remains canonical for WS3 as-a-whole; this memo applies amendments at the fire-scope layer.

### 2.1 WS3 WARN-A — VFX track scope (mantis consumption)

**Amendment text (replaces WS3 commission criterion #2 silent-on-VFX-scope):**

> **VFX track scope at WS3.1:** Sequencer-native particle-system track or placeholder track at WS3.1 baseline. Full Niagara cluster-rune VFX integration is DEFERRED to vertical-slice spike assembly (gates on WS2 GREEN per Option B Niagara windowed-mode verification per Sam Gate-2 2026-06-08 WARN-001).

**Mantis action:** at WS3.1, mantis adds the VFX track as Sequencer-native particle-system track OR placeholder track. **DO NOT** integrate Niagara `add_emitter_to_system` at WS3.1. Document chosen track type in close report § 1.3 above.

### 2.2 WS3 WARN-B — Phase-partition explicit (already captured § 0 above)

Phase-partition surfaced explicitly in this memo § 0 + Sam Gate-1 § 4 WARN-WS3-B. WS3.1 fires NOW; WS3.2-WS3.5 + criterion #9 verification fires post-WS1-GREEN.

### 2.3 WS3 WARN-C — Framerate target sharpened

**Amendment text (replaces WS3 commission criterion #8 qualitative "smooth"):**

> **Criterion #8 (amended):** Performance: cinematic playback holds ≥60 FPS at AAA fidelity per TSR+TAA pipeline (target consistent with vertical-slice spike AMENDMENT criterion #13).

**Mantis action at WS3.1:** at WS3.1 scope, Sequencer asset is empty (no animation content); framerate criterion #8 is verifiable at WS3.2-WS3.5 once keyframes are authored. At WS3.1, mantis records the **Editor playback frame rate of the empty Sequencer asset** in close report § 1.5 above as baseline observation for WS3.2-WS3.5 reference. Criterion #8 itself activates at WS3.2-WS3.5 verification.

### 2.4 WS3 WARN-D — Voice integration scope disambiguated

**Amendment text (replaces WS3 commission criterion #4 ambiguous "voice plays"):**

> **Criterion #4 (amended):** Spirit guide voice integration validated via templated TTS placeholder OR silent caption track per § 12.9 template structure. Canonical human voice-acting recording DEFERRED per § 12.13.

**Mantis action at WS3.1:** at WS3.1 scope, mantis adds the spirit guide voice track structure (track 5 per § 1.2 above) without populating audio content. WS3.3 (deferred to post-WS1-GREEN wave) integrates templated TTS placeholder OR silent caption track content. D7 AI-tell line preserved (no raw LLM dialogue at WS3.1 or WS3.3).

### 2.5 WS3 INFO-A — ADR-006 discipline citation (informational; close report addition)

**Mantis action:** add to close report § 1.6 (D7 line preservation) an additional bullet:

> ADR-006 — read-only-by-default external systems; db-lyon BUSL-1.1 base evaluation grant covers WS3.1 same as prior db-lyon usage in WS1 spike (parallel discipline framing).

---

## 3. WS3.1 acceptance criteria (consolidated; subset of WS3 commission § 3 plus amendments)

| # | Criterion (WS3.1 scope) | Source |
|---|---|---|
| 1 | Materialization cinematic Sequencer asset created + saved via db-lyon `create_sequence` + `save_asset` actions | WS3 commission criterion #1 |
| 2 | 5 tracks present (camera / transform / VFX-placeholder / audio / spirit guide voice) per § 1.2 above structure with placeholder data | WS3 commission criterion #2 amended per WARN-A |
| 3 | Sequencer asset persists post-Editor-close-and-reopen | WS3 commission criterion #7 |
| 4 | Empty Sequencer playback frame rate documented as baseline observation (criterion #8 itself activates at WS3.2-WS3.5) | WS3 commission criterion #8 amended per WARN-C |
| 5 | D7 AI-tell line preserved (no raw LLM dialogue in track authoring) | WS3 commission criterion #12 |
| 6 | Mantis close report authored per § 1.4 above; 8 mandatory sections present | This memo |
| 7 | Sam Gate-2 review PASS or PASS-WITH-WARN | WS3 commission criterion #10 |
| 8 | David-H wave-close memo authored + committed per PC-seam standing pattern; auto-push at wave-close fires this commit + prior Sam Gate-1 commit 975c2e2 forward | WS3 commission criterion #11 + CLAUDE.md PC-seam standing wave-close push pattern |

**Deferred from WS3 commission § 3 criteria (activate at downstream WS3.2-WS3.5 wave post-WS1-GREEN):**

- Criterion #3 (4-phase spirit form transformation through concretization / racial / elemental / weapon) — WS3.2 scope
- Criterion #4 (spirit guide voice integration) — WS3.3 scope per WARN-D amendment
- Criterion #5 (camera composition matches § 2.1 scene description) — WS3.4 scope
- Criterion #6 (cinematic plays end-to-end on `play_sequence` trigger) — WS3.2-WS3.5 scope
- Criterion #8 (≥60 FPS at AAA fidelity per TSR+TAA pipeline) — WS3.2-WS3.5 scope per WARN-C amendment
- Criterion #9 (Composition with WS1 DataTables operational) — gates on WS1 GREEN per phase-partition

---

## 4. Out-of-scope at WS3.1 (explicit; prevents over-scoping)

- ❌ Spirit form 4-phase keyframe animation (WS3.2; deferred to post-WS1-GREEN wave)
- ❌ Spirit guide voice content integration — templated TTS placeholder OR silent caption track (WS3.3; deferred to post-WS1-GREEN wave per WARN-D)
- ❌ Camera composition keyframes matching § 2.1 scene (WS3.4; deferred to post-WS1-GREEN wave)
- ❌ End-to-end `play_sequence` trigger verification (WS3.2-WS3.5; deferred)
- ❌ Niagara `add_emitter_to_system` integration into VFX track (deferred to vertical-slice spike per WARN-A; gates on WS2 GREEN)
- ❌ Composition with WS1 DataTables — gates on WS1 GREEN (criterion #9; deferred)
- ❌ Performance at ≥60 FPS AAA fidelity target — WS3.2-WS3.5 scope (criterion #8 amended per WARN-C; WS3.1 captures baseline empty-playback framerate only)
- ❌ Spirit form 3D model + rigging (Meshy + Control Rig pipeline; per asset-pipeline canonical; deferred)
- ❌ Music + SFX (canonical 38 D7 — human-composed; deferred to audio pipeline)
- ❌ Vertical-slice spike assembly (separate AMENDMENT dispatch)

---

## 5. BLOCK-WS1-A Path A ratification (informational; affects future WS1 fire — NOT WS3.1)

Matt ratified Path A for the source-JSON staging BLOCK at Sam Gate-1 § 2:

**Path A (multi-repo PC clones + engine emits substrate-registry + experiential-axes JSON sidecars):**

- Add `C:\dev\reincarnated-engine\` and `C:\dev\reincarnated-loadout\` to PC sibling clones (Matt schedules)
- Mac-side discipline: engine + loadout push to origin; PC pulls per existing CLAUDE.md PC-side pull discipline at session-start
- New Mac-side artifacts required (NOT mantis scope):
  - Gandalf authors 2 JSON sidecar design-specs (atomic-substrate-registry → JSON sidecar emission; hypothesis-flow § 1.8 experiential axes → JSON sidecar emission)
  - Rocket + Gamora implement engine emit (per gandalf design-specs)
  - Engine push to origin
  - PC pulls at next session-start

**Why this matters for mantis at WS3.1:** **IT DOES NOT.** WS3.1 has no WS1 data dependency. Mantis fires WS3.1 with placeholder data per § 1.2 above. BLOCK-WS1-A resolution is concurrent Mac-side work that unblocks the downstream WS1 wave (not this WS3.1 wave).

**Why this matters for downstream waves:** WS1 will fire after Path A completes Mac-side execution chain. WS3.2-WS3.5 + criterion #9 verification then activates post-WS1-GREEN. This memo documents the ratification so mantis + sam + knight-rider have consistent context across hosts.

**Mantis action at WS3.1:** none for Path A. Proceed with WS3.1 per § 1 above.

---

## 6. Routing instructions

### 6.1 For mantis

1. Open new terminal on PC (or via SSH from Mac per CLAUDE.md SSH invocation pattern)
2. `cd C:\dev\reincarnated-unreal\Reincarnated\`
3. `claude --agent mantis`
4. Session-start protocol per mantis OP (read AGENT_STATE.md, read this routing memo as primary in-flight dispatch)
5. Execute WS3.1 per § 1 above scope
6. Author close report per § 1.4 above at `agentic_orchestration/mantis/notes/2026-06-10-ws3-1-sequencer-asset-close.md` (or next-day if execution crosses days)
7. Auto-commit close report + AGENT_STATE.md update per CLAUDE.md PC team auto-commit table (mantis row)
8. Do NOT push at mantis session close; wave-close push fires once Sam Gate-2 + david-h wave-close memo land

### 6.2 For sam (Gate-2 post-mantis)

1. Triggered when mantis close report lands at `agentic_orchestration/mantis/notes/2026-06-10-ws3-1-sequencer-asset-close.md` (or next-day file)
2. Gate-2 DEV-MODE review per Sam OP + critique-pair-gate-protocol § 4
3. Output: `agentic_orchestration/qa/findings/<date>-ws3-1-mantis-gate-2.md`
4. Gate-2 PASS or PASS-WITH-WARN per acceptance criteria § 3 above
5. Auto-commit Gate-2 finding per CLAUDE.md PC team auto-commit table (sam row)
6. Do NOT push at sam session close; wave-close push fires after david-h wave-close memo lands

### 6.3 For david-h (wave-close)

1. Triggered after Sam Gate-2 PASS lands
2. Author wave-close memo at `agentic_orchestration/david-h/notes/<date>-ws3-1-wave-close.md`
3. Auto-commit wave-close memo per CLAUDE.md PC team auto-commit table (david-h row)
4. AUTO-PUSH per PC-seam standing wave-close push pattern (CLAUDE.md addendum 2026-06-08); the push moves forward:
   - Prior Sam Gate-1 commit 975c2e2 (still local-only)
   - This routing memo commit
   - Mantis WS3.1 output + close report commit
   - Sam Gate-2 finding commit
   - David-H wave-close memo commit

### 6.4 For knight-rider (cross-host fetch at next Mac session)

Mac-KR consumes this routing memo + downstream wave commits at next Mac session. Path A Mac-side execution chain (PC clones + JSON sidecar design-specs + engine emit) is Mac-KR's routing scope to schedule with gandalf + rocket + gamora. This memo surfaces the ratification; Mac-KR routes the work.

---

## 7. Discipline citations (added at this routing memo layer)

- **CLAUDE.md PC-seam standing wave-close push pattern (2026-06-08)** — auto-push at wave-close fires this commit + prior 975c2e2 + downstream wave commits together
- **CLAUDE.md PC team auto-commit table** — mantis + sam + david-h auto-commit work-products from authorized cycle work; no per-commit Matt re-ask
- **Hive-mind decision-routing (Matt 2026-05-23)** — david-h orchestrates in-scope WS3.1 routing without further Matt escalation; Matt is last-resort escalation
- **Sam Gate-1 PASS-WITH-AMENDMENTS (2026-06-10)** — WS3 amendments captured per § 2 above
- **D7 AI-tell line** — preserved at WS3.1 (no raw LLM dialogue in track authoring; templated voice + silent caption track structurally compatible at WS3.3 downstream)
- **Mantis OP single-Editor-instance constraint** — preserved per Sam Gate-1 § 5 INFO-CROSS-A Path 2 interleaved phasing (WS3.1 mantis Editor-time runs while BLOCK-WS1-A Mac-side resolution proceeds concurrently)
- **ADR-006 (read-only-by-default external systems)** — db-lyon BUSL-1.1 base evaluation grant covers WS3.1 same as WS1 + prior spike
- **Recognition-validate-commit** — WS3.1 empirically validates § 2.5 materialization cinematic intent at Sequencer asset-authoring layer; downstream waves validate at keyframe + voice + composition layers

---

## 8. Sign-off

**Authored:** david-h 2026-06-10 per Matt routing ratifications (BLOCK-WS1-A Path A; WS3.1 GO signal).
**Authority:** david-h PC-side orchestrator scope per OP + hive-mind decision-routing.
**Routing:** mantis fires WS3.1; sam Gate-2; david-h wave-close memo + auto-push per PC-seam standing pattern.
**Commit:** auto-commit per CLAUDE.md PC team auto-commit table (david-h row: "PC-seam orchestration dispatches").
**Push:** deferred to wave-close per PC-seam standing pattern; not pushed at routing-memo-authoring time.
**Composition:** all prior canonical commitments preserved.
**End of routing memo.**
