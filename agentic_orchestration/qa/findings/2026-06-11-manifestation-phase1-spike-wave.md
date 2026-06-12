# Finding — 2026-06-11 — Manifestation Moment Phase-1 spike wave (S6 + S5 + S1 + S6 import leg)

**Reviewer:** sam (PC-seam)
**Severity:** PASS-with-INFO (overall) — see per-dimension severities below
**Target:** commits `d5819c2` (S6) + `fb01e72` (S5+S1) + `b63a80c` (S6 import leg) + `ca7706d` (radagast verdict)
**Developer:** mantis (UE seam) — design-fit verdict by radagast (composed, not re-litigated)
**Scope:** PC-seam, with ONE cross-cutting flag (UE version-control decision → decisions-log proposal to Mac-jack-ryan)
**Principles applied:** 1 (math/justification-before-claim, applied as claim-substantiation), 2 (smoke-gate), 4 (decisions-log as truth), 5 (severity)
**Composes with:** radagast Pattern A-deep design-fit verdict `agentic_orchestration/radagast/notes/2026-06-11-phase1-spike-wave-design-fit-verdict.md` (design-fit track — no conflict surfaced; FBX + git findings flagged in both registers from different angles per his § 7 "To Sam")

---

## What I found

The wave is process-clean and discipline-honest across all eight review dimensions. Three spikes delivered against commissioned specs (consult § 5 rows S6/S5/S1 + framing-brief § 2/§ 5 guards); all findings notes separate proved-headless from windowed-gated cleanly and report ZERO render evidence where none exists rather than fabricating it (the load-bearing honesty test — passed). Discipline #40 scaffold registers are complete and auditable in all three notes; no value is faked-as-substrate. D7 holds by construction (image→Meshy provenance, no Crusader anywhere, no raw-LLM player-facing surface). The FBX-not-GLB substitution was flagged explicitly by mantis as a scope-faithful adaptation (bridge is UFbxFactory-only; FBX is the Crusader-proven path; same rigged asset), not a silent deviation. Spend (44 Meshy credits / ~$2.20) is within the consult's predicted envelope for authorized spike work. Commit hygiene is correct (prefixes, co-author tags, no premature push, AGENT_STATE updated). The one substantive process exposure is structural, not a fault of this wave: the `reincarnated-unreal` UE project is NOT git-tracked, so the now-substantial authored UE state (`SK_EarthAvatar`, `LV_ManifestationKnoll`, `NS_CelestialSphere`, lighting rigs, materials, 44-credits of Meshy raw assets) is disk-only with no history/remote/rollback. That is a real and growing durability gap warranting a decisions-log entry — flagged here, routed to Mac-jack-ryan as a proposal, decision-authority Matt.

---

## Per-dimension findings

### D1 — Spec-vs-delivery per spike + claimed-vs-verified hygiene — **INFO (PASS)**
- **S6:** specced as "the ONLY unproven avatar leg" (consult § 5). Delivered image-gen→image-to-3D→rig end-to-end + import leg. Exceeds spec (R1 retired). Rig proved by **parsing the glTF chunk** (24 joints, Hips root — Principle 1 substantiation, not assertion); import verified by bridge introspection (boneCount/material/textures/scale all checked, `isDefaultFallback:false` confirmed for the material — i.e. mantis explicitly verified it was NOT a fallback stand-in). Honest.
- **S5:** specced (consult § 3.4) as the hybrid rig. All four pillars landed (moonlight key + skylight + diegetic glow + manual exposure lock). Claimed status "PASS (authoring-complete; render-evidence WINDOWED-GATED)" is accurate — the note does NOT claim render validation it cannot have.
- **S1:** the partial-pass, and partial in exactly the honest way. **S1 § 2 states ZERO render evidence and TWO real gates (Gate A array-binding BP/windowed; Gate B render DXGI-gated).** Verified: the note does not overstate. The "sky reads as sky WITH DEPTH" falsifiable read (§ 2 Gate B) is correctly classed as render-session-only — not claimed.
- **No overstatement found anywhere in the three notes.** S1's honest ZERO-render-evidence posture is matched by S5 (no figure-readability claim) and S6 (only what bridge introspection + glTF parse actually returned). Principle 2 (smoke-gate) is honored in spirit: the wave gates its own unverifiable claims behind the DXGI finding rather than asserting through them.

### D2 — Discipline #40 scaffold-flag compliance — **INFO (PASS)**
- All three notes carry complete scaffold registers (S6 § 5 / 7 rows; S5 § 3 / 8 rows; S1 § 3 / 8 rows). Star positions (S1 #1), sphere radius R=8000 (S1 #2), exposure values 0.03/−2.0 (S5 #4), spirit-glow 2200 (S5 #3), cluster count 6 (S1 #3) — **all flagged as deliberate placeholders, each with a "locked by" gate**, none faked-as-substrate.
- S1 #1 explicitly states "FLAGGED PLACEHOLDER, never faked-as-substrate" against contract 6.7 (which does not yet exist). Correct #40 + #41 discipline — the substrate-truthful posture mantis took on cluster-count (6, the data that exists, not 7, the scaffold) is the harder-but-correct call. No #40 fault.

### D3 — D7 compliance (substrate-grounded pipeline; no raw-LLM player-facing; Crusader constraint) — **INFO (PASS)**
- Avatar is image-gen→Meshy image-to-3D→rig, substrate-grounded; image-pass-through-to-Meshy provenance preserved via `input_task_id` chaining (S6 § 1.1). No raw-LLM player-facing surface.
- **Crusader constraint honored — verified in outputs:** the Crusader appears NOWHERE as a player-facing asset. The internal test biped is `SKM_Quinn_Simple` (S5 § 1, NiagaraExamples Gallery, internal-test-only) — not the Crusader. S6 § 3.5 explicitly confirms "no Crusader in any player-facing capacity." Clean.
- Note for the record (not a finding): S6 § 1.1 documents that the ONLY image-gen key on host is `MESHY_API_KEY`, so Meshy text-to-image is both the available AND the substrate-grounded path — the dispatch allowed this substitution, and it does not weaken D7 (the image is still passed through Meshy in-pipeline).

### D4 — FBX-not-GLB substitution (process view) — **INFO (PASS — scope-faithful adaptation, NOT silent deviation)**
- Dispatch named "GLB via Interchange"; mantis imported `earth_avatar_rigged.fbx` because the UE_MCP_Bridge import handlers are all `UFbxFactory`-based with no glTF/Interchange factory exposed (S6 § 8.2).
- **Process ruling: ACCEPTABLE.** The deviation was (a) **flagged explicitly** in the findings note, the commit body, AND AGENT_STATE — not silent; (b) the FBX twin is the **same Meshy-rigged asset** (identical 24-joint Hips-rooted skeleton; § 1.3 parsed the GLB, § 8.3 verified the FBX import gives the same boneCount/root); (c) FBX is the **already-proven** Crusader import path. This is the correct disposition of a spec-aspiration that the deterministic tooling could not honor literally — take the proven route, flag the aspiration, do not force an unvalidated headless Interchange path. Radagast accepted this on the design side (his § 4); I concur on the process side. The "GLB via Interchange" literal import is a backlog forward-item (new bridge handler), correctly classed as NOT-an-MVP-blocker.
- **Why this is INFO not WARN:** a silent spec deviation would be WARN-or-worse (Principle 4 — outputs must match documented intent). This deviation is the *opposite* of silent — it is one of the most thoroughly-documented adaptations in the wave. The transparency is the disposition.

### D5 — Spend authorization fit — **INFO (PASS)**
- 44 Meshy credits (~$2.20), balance 666→622, ledgered in `s6_state.json` (S6 § 0). The consult (§ 5 row S6) predicted "a few Meshy credits"; the framing brief authorized the image-gen→Meshy pipeline as the S6 spike's core work.
- Spend is within the authorized spike workstream — no scope-amendment, no cross-cycle drift. On-spec. (For the record: model choice `gpt-image-2` at 9cr was the prompt-adherence call for the load-bearing "empty hands / no fantasy" negatives; cheaper `nano-banana` alternatives are registered for corpus-scale — good forward cost-discipline, S6 § 5 #1.)

### D6 — `reincarnated-unreal` NOT git-tracked (durability gap) — **WARN (PC-seam, with cross-cutting decisions-log proposal)**
- **Description (what exists):** the UE project has no `.git` anywhere under the tree (mantis-verified, S6 § 4). As of this wave the on-disk-only authored UE state is now non-trivial: `SK_EarthAvatar` (24.4 MB skeletal mesh + skeleton + physics asset + material + 2× 7.5 MB textures), `LV_ManifestationKnoll` (18-actor reusable hub level), `NS_CelestialSphere` Niagara system, two lighting rigs, materials, and 44-credits of Meshy raw assets in `RawAssets/EarthAvatar_S6/`. No history, no remote, no rollback.
- **Why WARN not INFO:** the gap is now load-bearing. This wave converted the UE project from "bridge-plumbing + a sequencer stub" into the substrate that holds the entire Phase-1 player-facing manifestation scene. A disk event now costs "re-run several spikes," and the 44-credit Meshy spend has no backup. Every other seam in this ecosystem is version-controlled; the UE seam — which now holds the most player-facing-load-bearing assets on the PC — is not. That asymmetry is invisible until a disk event makes it catastrophic.
- **Why NOT BLOCK:** (a) this is not a fault of *this wave's outputs* — mantis flagged it correctly (S6 § 4, § 8.6, AGENT_STATE) and routed it as out-of-spike-scope, which is the right disposition; blocking the wave for it would be misattributing an infrastructure gap to clean spike work. (b) Partial mitigation exists and is genuinely good discipline: the driver scripts (`s6_pipeline.py`, `gen-sphere-stars.js`, `s5-night-lighting.js`, `s1-celestial-sphere.js`, `s6-import-earth-avatar.js`) are all re-runnable, so most authored state is code-reproducible — though re-runnable scripts are NOT a substitute for version control of the binary `.uasset` outputs + imported textures + the Meshy raw assets (the 44 credits live only in `RawAssets/`).
- **Disposition:** WARN — fix advisable, not blocking THIS wave's push; the decision belongs to Matt. Routed as a decisions-log entry PROPOSAL to Mac-jack-ryan (§ "Decisions-log proposal" below). Recommendation carried (not decided): git + Git LFS for the binary blobs — the industry-standard UE-on-git path; Perforce is heavier than this solo-dev-scale project needs. I align with radagast's design-stewardship recommendation (his § 5); my process view adds the severity classification (WARN) and the decisions-log routing.

### D7 — DXGI gate finding recorded for future-session discoverability — **INFO (PASS)**
- The wave proved the documented cold-DDC windowed-blocker framing WRONG and replaced it with a sharper finding: `DXGI_ERROR_NOT_CURRENTLY_AVAILABLE` at viewport creation — the SSH/WSL session has no GPU-attached interactive desktop, so this is a STANDING constraint on the SSH-invocation model, not a one-time DDC warm.
- **Discoverability verified:** the superseding finding is recorded in AGENT_STATE.md (the file future sessions read first) under an explicit "ENVIRONMENT LEARNING — windowed launch from SSH/WSL crashes on DXGI (supersedes cold-DDC framing for windowed work)" header AND in the S5/S1 findings notes. **It is NOT buried only in a findings note** — it is in the live state file with a "supersedes" flag pointing at the prior framing. This is exactly the right place. The prior cold-DDC framing lower in AGENT_STATE (§ "Windowed UE Editor — environmental constraint") is now stale — see action item below (INFO, not a fault: the supersession is clearly stated at the top; the stale lower section is a tidy-up, not a discoverability failure).

### D8 — Commit hygiene — **INFO (PASS, with one note)**
- Prefixes correct (`mantis:` ×3, `radagast:` ×1). Co-author tags present and correct on all four. No premature push (all four unpushed vs `origin/main`; david-h pushes at wave-close per standing PC-seam pattern). AGENT_STATE.md updated to reflect S6 import + S5/S1 + DXGI learning. Findings notes scoped to the collab repo only — no UE binary leaked into git (consistent with the not-git-tracked reality).
- **Note (not a fault):** commit `ca7706d` carries the `radagast:` subject-prefix but the git author identity is `mantis` (PC sessions share the host `mantis` git user). The subject-prefix correctly attributes the authoring agent; the git-author field is a host-config artifact, not a hygiene fault. Flagging for the record only — the convention (prefix = agent attribution) is honored.

---

## Rationale

- **Principle 1 (substantiation-before-claim):** S6 proved the rig by parsing the glTF chunk and verified the import by bridge introspection — claims are substantiated by artifact inspection, not asserted. This is the discipline working.
- **Principle 2 (smoke-gate):** the wave gates its own unverifiable claims (render reads, TSR, figure-readability) behind the DXGI finding rather than asserting through them — the smoke-gate-equivalent for a render-gated wave.
- **Principle 4 (decisions-log as truth):** the FBX-vs-GLB adaptation is transparent (not a silent departure from documented intent); the version-control gap has no governing decisions-log entry, which is the gap the proposal closes.
- **Discipline #40 / #41:** scaffold registers complete; substrate-truthful cluster-count (6) chosen over scaffold-number (7) with a flag — the harder-but-correct call.
- **D7 (AI-tell line):** clean by construction across the wave.

---

## Cross-cutting flag

**UE-seam version-control is an architectural/durability decision with no governing decisions-log entry.** The decision-authority is Matt (per radagast's routing and per ADR-002 — this exceeds PC-seam tiered-approval scope; it is infrastructure, not docs/test/patch/within-PC-refactor). Per Sam drift-discipline § 6.6, decisions-log entry PROPOSALS route to Mac-jack-ryan for canonical-write. I file the proposal below; Mac-jack-ryan reviews + canonical-writes if ratified; Matt holds the actual go/no-go on git+LFS adoption.

---

## Decisions-log entry PROPOSAL (routed to Mac-jack-ryan)

> Proposed for Mac-jack-ryan canonical-write per Sam drift-discipline § 6.6 + Principle 4. Decision-authority: Matt. Sam classifies the underlying gap as WARN (D6).

**Title:** 2026-06-11 — `reincarnated-unreal` UE project version-control decision (git + Git LFS recommended)

**Decision (PROPOSED — pending Matt):** Bring the `reincarnated-unreal` UE project under version control via git + Git LFS (LFS for binary `.uasset`/`.umap`/texture blobs + Meshy raw-asset staging). Alternative (Perforce) rejected as heavier than solo-dev scale needs.

**Reasoning:** As of the 2026-06-11 Manifestation Phase-1 spike wave, the UE project holds the entire Phase-1 player-facing manifestation scene (reusable hub level, imported `SK_EarthAvatar`, Niagara sky system, lighting rigs, materials) plus 44 Meshy-credits of raw assets — all disk-only, no history/remote/rollback. Every other seam in the ecosystem is version-controlled; the UE seam, now the most player-facing-load-bearing PC surface, is not. Re-runnable driver scripts partially mitigate (most authored state is code-reproducible) but are not a substitute for VC of binary outputs + raw assets. Durability cost has crossed from "annoying" to "re-run several spikes + re-spend credits."

**Alternatives considered:** (1) Status quo (disk-only + re-runnable scripts) — rejected: scripts don't cover binary `.uasset` blobs or the Meshy raw-asset credits-spend. (2) Perforce — rejected: heavier than solo-dev scale needs; git+LFS is the industry-standard UE-on-git path. (3) Mirror raw assets into the collab repo only — partial; doesn't version the `.uasset` authored state.

**Status:** PROPOSED (Sam → Mac-jack-ryan; awaiting Matt go/no-go on adoption).

**Related:** radagast verdict § 5 + § 7 (design-stewardship recommendation); this finding D6; mantis S6 § 4 / § 8.6 (gap surfaced).

---

## Action

- [ ] **Mantis (tidy-up, non-blocking, next PC session):** prune or mark-stale the now-superseded "Windowed UE Editor — environmental constraint (WS2 gate)" cold-DDC section lower in AGENT_STATE.md, so only the DXGI framing remains authoritative. The top-of-file supersession flag already prevents misreading; this is housekeeping.
- [ ] **David-H (wave-close):** this Gate-2 verdict is PASS-with-INFO + one WARN (D6, non-blocking-to-push). Proceed with wave-close push of the accumulated commits per standing PC-seam pattern. Carry the decisions-log proposal + UE-VC routing into the wave-close memo so it reaches Mac-jack-ryan (origin push) for next Mac session.
- [ ] **Mac-jack-ryan (consultation, next Mac session):** review the decisions-log entry proposal above; canonical-write to decisions-log if ratified.
- [ ] **Matt (decision — not a BLOCK gate on this wave):** go/no-go on git + Git LFS adoption for `reincarnated-unreal`. Radagast's recommendation: do not let the gap grow another wave undecided.

---

## References

- `agentic_orchestration/mantis/notes/2026-06-11-s6-meshy-image-to-3d-avatar-spike.md` (incl. § 8 import leg)
- `agentic_orchestration/mantis/notes/2026-06-11-s5-night-lighting-register-spike.md`
- `agentic_orchestration/mantis/notes/2026-06-11-s1-sky-from-ground-celestial-sphere-spike.md`
- `agentic_orchestration/radagast/notes/2026-06-11-phase1-spike-wave-design-fit-verdict.md` (design-fit track this composes with)
- `agentic_orchestration/radagast/notes/2026-06-10-manifestation-moment-ue-feasibility-consult.md` (§ 5 spike specs; § 7 scaffold register; § 5 non-spike risk R1)
- `agentic_orchestration/gandalf/notes/2026-06-10-ue-manifestation-moment-mvp-framing-brief.md` (§ 5 discipline guards; § 2 avatar pipeline)
- `C:\dev\reincarnated-unreal\Reincarnated\AGENT_STATE.md` (DXGI environment-learning record; S6 import state)
- Commits reviewed: `d5819c2`, `fb01e72`, `b63a80c`, `ca7706d`

---

**Overall verdict: PASS-with-INFO** (seven dimensions INFO/PASS; one dimension WARN — D6 UE version-control gap, non-blocking to this wave's push, routed as a decisions-log proposal to Mac-jack-ryan with Matt as decision-authority). No BLOCK. The wave is process-clean, discipline-honest, and scope-faithful. The single WARN is a pre-existing infrastructure gap correctly surfaced by mantis, not a fault of these outputs.

**Authored:** sam (PC-seam Gate-2, DEV-MODE) 2026-06-11. NOT pushed (david-h wave-close push).
