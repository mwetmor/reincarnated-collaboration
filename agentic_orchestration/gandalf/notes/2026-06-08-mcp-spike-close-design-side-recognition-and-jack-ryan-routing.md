# MCP Bridge Spike Close — Gandalf Design-Side Recognition + Jack-Ryan Routing

**STATUS:** CURRENT (load-bearing routing note; gandalf design-side validation of PC-seam spike close)
**Date:** 2026-06-08
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-08 directive "fire 1 and 2" (read spike artifacts + route Sam proposals to jack-ryan)
**Companion artifacts:**
- `agentic_orchestration/david-h/notes/2026-06-08-ue-mcp-bridge-spike-db-lyon-primary/spike-findings.md` (David-H GREEN verdict)
- `agentic_orchestration/qa/findings/2026-06-08-david-h-ue-mcp-bridge-spike-db-lyon-primary-gate-2.md` (Sam Gate-2 PASS-with-WARN)
- `agentic_orchestration/sam/notes/2026-06-08-proposal-mac-jack-ryan-db-lyon-decisions-log.md` (Sam consultation note — Sam's two Mac-jack-ryan-routed proposals)
- `agentic_orchestration/legolas/research/2026-06-08-three-way-mcp-comparison/synthesis.md` (evidence basis)
- `agentic_orchestration/dispatches/2026-06-08-david-h-ue-mcp-bridge-spike-AMENDMENT-db-lyon-primary.md` (amended commission)

---

## 0. TL;DR

The UE MCP Bridge Spike (db-lyon primary) closed GREEN with Sam Gate-2 PASS-with-WARN. Gandalf-side design validation:

- **db-lyon adoption is architecturally sound** as primary MCP bridge for WS1–WS5 + vertical-slice spike. Cosmograph DataTable ingestion path is empirically operational. License posture clean during dev + bounded migration cost if commercial path closes.
- **Sam Proposal 1 (decisions-log entry for db-lyon adoption):** ENDORSED. Rises to architectural commitment per ADR-002; warrants jack-ryan canonical-write to decisions-log.
- **Sam Proposal 2 Candidate A (mutation-depth testing discipline):** ENDORSED with substrate-led discipline framing. Cross-seam applicable.
- **Sam Proposal 2 Candidate B (third-party version pinning at adoption):** ENDORSED at narrower scope. Cross-seam applicable to Mac seam tooling adoption (catalogue + simulation seams use pip-based tooling).
- **Three gandalf-side downstream amendments** named in § 5: Earth-Avatar vertical-slice spike commission (Sam WARN-002 Blueprint-mutation pre-fire gate), ground-state oracle § 1 (db-lyon adoption entry), future WS1/WS2/WS3 commission preambles (tooling-layer specification + WS2 windowed-mode gate).

---

## 1. Spike close — design-side recognition

The substrate-led discipline rescope on 2026-06-08 ("ecosystem-discovery first, needs-mapping second") that surfaced db-lyon as a candidate the prior needs-driven commission missed → spike empirically validated db-lyon at the load-bearing capability layer in a single session.

**The full chain:**

| # | Artifact | Authority | Outcome |
|---|---|---|---|
| 1 | Legolas workstream-spanning ecosystem inventory | commit `9579181` | 17 implementations surveyed; db-lyon surfaced |
| 2 | Legolas three-way deep comparison | commit `554da75` | db-lyon characterized at parity depth with NAJEMWEHBE + StraySpark |
| 3 | Gandalf design-side ratification of db-lyon-primary posture | this session dialogue | Matt directive ratified the posture explicitly |
| 4 | David-H spike commission AMENDMENT | commit `95d7ad8` | Spike scope flipped from build-from-scratch to db-lyon adoption |
| 5 | Mantis Phase 1 install + Phase 2 validation | commits `3b106a2` + `85be42c` | 26/26 tool tests PASS; DataTable CRUD 7/7; Sequencer 5/5; Niagara 4/5 (1 YELLOW on `add_emitter_to_system` headless crash) |
| 6 | David-H Phase 3 spike-findings + session-boundary-memo | commit `aaaeb85` | GREEN (Path A) verdict |
| 7 | Sam Phase 4 Gate-2 + decisions-log proposal | commit `3eaf178` | PASS-with-WARN ratifying GREEN; 2 WARN items; 2 proposals to Mac-jack-ryan |

**Total cost:** $0 LLM (legolas Mode A research is web-fetch only); spike execution time ~4-8 hr wall-clock per amendment budget.

**Operational state at close:** db-lyon installed in `C:\dev\reincarnated-unreal\Reincarnated\` PC UE 5.7 project; bridge WebSocket binds `ws://127.0.0.1:9877`; bridge starts via `PostEngineInit` at ~3 s to Editor-ready; UE project transitioned from Blueprint-only to C++ project via minimal scaffolds (`Source/Reincarnated.Target.cs` + `ReincarnatedEditor.Target.cs` + `Source/Reincarnated/Reincarnated.{h,cpp,Build.cs}`).

---

## 2. db-lyon adoption — design-side architectural validation

### 2.1 The decision is sound at gandalf design-side scope

The MCP bridge is foundational tooling for the Earth-Avatar Creation Moment architecture (canonical commitment 2026-06-07 — Matt + son design dialogue ratified). The architecture depends on the cosmograph JSON ingestion path being operational on the UE side. db-lyon's `fill_datatable_from_json` action is the literal primitive that ingests engine-pregenerated kit corpus JSON into UE DataTables. The spike empirically validated this primitive PASSes.

WS3 (materialization cinematic) similarly depends on Sequencer authoring at programmatic depth — the kit-to-spirit-form materialization cinematic per Earth-Avatar canonical § 2.4 cannot be authored without Sequencer track + section + keyframe programmatic control. db-lyon's 7 Sequencer actions all PASS empirically.

WS2 (Niagara VFX) is conditionally unblocked. The empirical YELLOW on `add_emitter_to_system` in headless mode is non-fatal. WS2 commission gates on the windowed-mode pre-check (~30 min mantis sub-session). Even if windowed-mode also crashes, db-lyon's 28 Niagara sub-actions remain dramatically better than NAJEMWEHBE's 3 — Path A still preferred.

### 2.2 License posture is clean during dev + bounded migration if commercial path closes

BUSL-1.1 base evaluation grant covers all spike work + vertical-slice spike + WS1–WS5 port workstreams (pre-launch internal development = non-production use). Commercial deployment at game ship is the trigger for paid-license requirement. Three mitigation paths:

- **Pricing inquiry to `licensing@ue-mcp.com`** at productionization decision (Matt-routed; not blocking)
- **2030-06-06 Change Date** auto-converts v1.0.79 to Apache 2.0 (4-year safety net for post-2030 ship scenarios)
- **NAJEMWEHBE migration path** at MEDIUM cost per legolas comparison § 6 (named Path B; not invoked)

### 2.3 Substrate-led discipline payoff worth naming explicitly

The prior 2026-06-07 commission was needs-driven — surveyed UE-MCP prior art through the narrow lens of one scene. db-lyon was missed. The 2026-06-08 rescope to ecosystem-discovery-first per Matt directive ("find everything available... then we can review the data wholistically") surfaced db-lyon. The spike validated it. Net: the rescope intervention saved a from-scratch MCP server build effort (estimated weeks) AND surfaced a tooling layer with capability depth the prior scope would never have discovered.

This is Pattern 6 + Discipline #41 (pre-authored taxonomy interrogation) operating at the research-scoping layer — substrate votes; don't pre-impose what we need. The pattern composes with the discipline architecture across all future tooling-research commissions.

---

## 3. Sam Proposal 1 — decisions-log entry for db-lyon adoption

### Gandalf endorsement: STRONG ENDORSE

Sam's proposal warrants jack-ryan canonical-write to decisions-log. Reasoning:

1. **Architectural commitment per ADR-002 tiered approval.** db-lyon adoption shapes WS1–WS5 commission authoring + vertical-slice spike execution pattern + productionization scope estimate. Not routine implementation; not a discipline candidate — a load-bearing architectural commitment with cross-seam reach.

2. **Cross-seam reach is real.** Gandalf authors WS1/WS2/WS3 commissions that specify db-lyon as the tooling layer. Star-lord may need to coordinate at the export-to-PC boundary (engine JSON packet → UE DataTable ingestion path crosses Mac/PC). Drax /forge web cosmograph and PC cosmograph share underlying JSON contract.

3. **Sam's proposed entry text is well-formed.** Specifies decision + reasoning + alternatives + status + related. Status "ACTIVE — WS1/WS3 authorized; WS2 gated on windowed-mode Niagara verification" is correct nuance.

4. **The cross-cutting annotation Sam recommends is correct.** Mac-side WS2 commission must gate on PC-side windowed-mode Gate (WARN-001 resolution). This is a cross-host coordination constraint that the decisions-log should record so future commission authoring (which fires from Mac per gandalf seam) honors the gate.

**Recommended jack-ryan disposition:** canonical-write to `~/Games/reincarnated-engine/design/decisions/decisions-log.md` substantially as Sam proposed, with the cross-cutting annotation about WS2 windowed-mode gate.

---

## 4. Sam Proposal 2 — engineering-discipline ratification candidates

### Candidate A — Mutation-depth testing discipline at tooling adoption spikes

Sam's framing: "When a spike adopts a third-party tooling layer as the primary execution surface for downstream workstreams, each workstream-mapped tool category must be exercised at mutation depth (create / update / delete operations; not only list / inspect operations) before the corresponding workstream commission is authorized."

### Gandalf endorsement: STRONG ENDORSE with substrate-led discipline framing

This is a real recurring pattern. Read-depth-only testing produces false-positive GREEN verdicts when the actual workstream needs CRUD capability at the same depth. The db-lyon spike caught this empirically — Blueprint category was read-only-exercised; Sam's WARN-002 names the gap; vertical-slice spike commission needs amendment to include Blueprint mutation pre-fire test.

Cross-seam applicability is real:
- **Engine-side tooling adoption** (rare but possible — e.g., catalogue-side pip-based tools, simulation-side numerical libraries): same pattern applies
- **Player-facing tooling adoption** (drax /forge consuming engine JSON packet at runtime): less about CRUD-vs-read but the principle holds (exercise the actual write/serialize path, not only read/deserialize)

Composes cleanly with Discipline #25 (semantic-layer rep-audit) — both are "test at the depth the actual use case will fire" disciplines.

**Recommended jack-ryan disposition:** ratify as Discipline #46 (or next available number) at `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`. Cross-seam scope.

### Candidate B — Third-party dependency version pinning at adoption

Sam's framing: "When a third-party dependency (npm, pip, or equivalent) is adopted as a load-bearing tool layer (as opposed to a dev-time convenience), the version must be pinned at adoption time with an explicit pin-or-defer decision recorded in the spike install record. `npx ue-mcp` without a pinned version silently upgrades on cold-cache environments."

### Gandalf endorsement: ENDORSE at narrower scope; cross-seam applicable

The discipline is sound but applies at narrower scope than Candidate A. Specifically:

- **Applies when:** load-bearing tool layer (not dev-time convenience). Examples: db-lyon (PC seam load-bearing); legolas web-fetch (light layer, dev-time); rocket numerical libraries that participate in P2/P3 math hotspots (load-bearing).
- **Does NOT apply when:** dev-time convenience tooling, easily replaceable libraries, established stable releases with semver guarantees we can rely on.

The pin-or-defer-with-explicit-decision framing is the load-bearing element. "We chose not to pin because X" is sufficient compliance; the discipline is about making the decision explicit, not mandating pinning.

Cross-seam applicability:
- **PC seam:** npm-based db-lyon (this case); future PC tooling adoptions
- **Mac engine seams:** pip-based numerical libraries at P2/P3/P5 math hotspots (substantial — Discipline #18 methodology consultation already governs methodology choice; this candidate would govern version-pinning of the chosen methodology's library)
- **Player-facing seams:** npm-based libraries at /forge cosmograph + loadout app (drax already does package-lock.json so largely covered by ecosystem convention; explicit decision recording would add discipline rigor)

**Recommended jack-ryan disposition:** ratify as Discipline #47 (or next available number) at narrower scope than Candidate A. Frame as "third-party version-pinning OR explicit-defer decision recorded at adoption time for load-bearing tooling layers."

---

## 5. Gandalf-side downstream actions

Three load-bearing amendments fire from gandalf seam consequent to spike close:

### 5.1 Earth-Avatar vertical-slice spike commission amendment

Original commission at `agentic_orchestration/dispatches/2026-06-07-david-h-earth-avatar-creation-moment-vertical-slice-spike.md` was authored before the MCP bridge spike outcome. Needs amendment to include:

- **Sam WARN-002 Blueprint-mutation pre-fire gate:** vertical-slice spike must exercise Blueprint mutation (create node + connect pin + compile) BEFORE committing to MCP-driven scene authoring. ~30 min mantis sub-session at spike start.
- **db-lyon tooling layer specification:** explicit pointer to db-lyon as the MCP bridge to use; install reference to db-lyon-install-record.md
- **Productionization signals from spike findings § 4:** `save_asset` after `create_datatable` pattern; parameter-naming camelCase-native convention; bridge auto-launch consideration (deferred but noted)

Amendment authoring is gandalf-seam. Fires when Matt directs vertical-slice spike re-engagement, or proactively if Matt wants the amendment ready for next David-H session.

### 5.2 Ground-state oracle § 1 entry for db-lyon adoption

After jack-ryan canonical-writes the decisions-log entry, ground-state oracle § 1 ("What is CURRENT TRUTH") should add a row referencing the decisions-log entry. The entry is load-bearing for WS1–WS5 commission authoring + vertical-slice spike + future PC team agent sessions reading first-reads.

Authoring is gandalf-seam per oracle ownership. Fires after jack-ryan's decisions-log canonical-write lands.

### 5.3 Future WS1 / WS2 / WS3 commission preambles

When gandalf authors WS1 (data layer port) / WS2 (rendering layer) / WS3 (materialization cinematic) commissions, each must specify:

- **db-lyon as primary tooling layer** (named explicitly; not assumed)
- **WS2 commission especially:** pre-fire gate on windowed-mode Niagara `add_emitter_to_system` verification per spike WARN-001
- **License posture:** non-production use covered by BUSL-1.1 base grant during port; productionization licensing inquiry separately routed
- **Productionization signals from spike findings § 4** as background knowledge for commission scope

Authoring is gandalf-seam. Fires per workstream sequencing — WS1 + WS3 unblocked at tooling layer now; WS2 conditionally unblocked pending windowed-mode verification.

---

## 6. Routing summary for jack-ryan

**Reads queued for jack-ryan at next Mac session start:**

| # | Artifact | Action |
|---|---|---|
| 1 | `agentic_orchestration/sam/notes/2026-06-08-proposal-mac-jack-ryan-db-lyon-decisions-log.md` | Read; consider Sam's proposed decisions-log entry; evaluate two discipline candidates |
| 2 | `agentic_orchestration/david-h/notes/2026-06-08-ue-mcp-bridge-spike-db-lyon-primary/spike-findings.md` | Read for full spike context backing Sam's proposal |
| 3 | `agentic_orchestration/qa/findings/2026-06-08-david-h-ue-mcp-bridge-spike-db-lyon-primary-gate-2.md` | Read Sam Gate-2 finding directly |
| 4 | This file | Read gandalf design-side endorsement + amendment recommendations |

**Recommended jack-ryan dispositions:**

| Sam item | Gandalf recommendation |
|---|---|
| Proposal 1 — decisions-log entry for db-lyon adoption | **CANONICAL-WRITE** to decisions-log substantially as Sam proposed; include cross-cutting WS2 windowed-mode gate annotation |
| Proposal 2 Candidate A — mutation-depth testing discipline | **RATIFY** as Discipline #46 (or next available number); cross-seam scope |
| Proposal 2 Candidate B — third-party version pinning at adoption | **RATIFY** as Discipline #47 (or next available number); narrower scope per § 4 Candidate B framing |

**Composition note:** jack-ryan canonical-write to decisions-log unblocks gandalf-side ground-state oracle § 1 update (per § 5.2 above). Workflow order: jack-ryan canonical-writes → gandalf consumes → ground-state updates → future PC team session reads inherit the canonical commitment.

---

## 7. Sign-off

**Authored:** gandalf 2026-06-08 per Matt directive "fire 1 and 2" (read spike artifacts + route Sam proposals to jack-ryan).

**Authority:** gandalf cross-cutting recognition-and-routing authority for design-side validation of cross-seam architectural commitments + critique-pair partner relay to jack-ryan via file-based message bus per `canonical/story/2026-06-07-federated-pc-team-architecture-commit.md` § 4.

**Routing:** jack-ryan reads this file at next Mac session start (per first-reads protocol). Gandalf-side downstream amendments (§ 5) fire per Matt sequencing direction or proactively per workstream sequencing.

**Empirical-evidence triggers:**
- jack-ryan decisions-log canonical-write → ground-state oracle § 1 update fires
- Matt fires vertical-slice spike → vertical-slice spike commission amendment fires (§ 5.1)
- Matt directs WS1 / WS3 commission authoring → commission preamble fires per § 5.3
- Mantis windowed-mode Niagara verification PASS → WS2 commission unblocked → commission preamble fires per § 5.3

**Composition with prior canonical commitments:** all preserved (Earth-Avatar Creation Moment Architecture 2026-06-07 + federated PC team architecture 2026-06-07 + cosmograph-pivot 2026-06-05 + atomic-substrate-registry 2026-06-06 + hypothesis-flow 2026-06-06 CANONICAL).

**End of routing note.**
