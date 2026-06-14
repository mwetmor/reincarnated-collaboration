# NEXT-SESSION START — david-h (PC)

**STATUS:** SESSION-START PRIMER. First read for the next david-h PC session (after `00-ground-state.md` + the federated-PC-team commit doc per OP § 1). Supersedes `2026-06-13-next-steps-memo-post-p0-1.md` (that plan is fully executed).
**Date filed:** 2026-06-13
**Author:** david-h (PC-side orchestrator, mhwet/WSL SSH session)
**Context:** P0.1 celestial-sphere/figure-lighting dispatch is RATIFIED + ACTIVE; Wave 1 (mantis Tier-A headless) is CLOSED + pushed; Wave 2 (Tier-B console) is staged for Matt.

---

## 0. First actions next session (in order)

1. **Session-start protocol** per OP § 1: read `canonical/00-ground-state.md`, the federated-PC-team commit doc, latest CHANGELOG entry, in-flight dispatches addressed to PC team, and own latest notes.
2. **`git pull origin main`** at session-start (PC-side pull discipline; captures any Mac-side commits since this session — including any Mac-KR / Mac-gandalf response to the cross-host note filed this session).
3. **Check whether Matt has run Wave 2** (the console Tier-B pass). Two branches below.

## 1. Where things stand (one paragraph)

P0.1 produced findings, not captures. One defect (the 1,005,000-particle origin cloud — a duplicate point-cloud Niagara system never bound to the star JSON, on CPU sim) blocked both S1 (sky) and S5 (figure-lighting). David-H authored a mantis dispatch, PC-trio ratified it (Pattern E: sam Gate-1 PASS-WITH-WARN, radagast design-fit PASS-WITH-WARN, all folded), flipped it ACTIVE. Matt split the wave: **Wave 1** = mantis Tier-A headless (math/transform note + 1,005,000 root-cause + ordered M1–M7 manual-BP-step list for the console) — CLOSED, sam Gate-2 PASS-WITH-WARN, commit `1828499` / tag `mantis/v1.0-celestial-sphere-rework-tierA-1`, pushed. **Wave 2** = Matt executes M1–M7 at the PC console (DXGI-gated render work) and banks S1 + S5 — pending Matt's time.

## 2. The two branches for next session

### Branch A — Matt HAS run Wave 2 (console captures exist)
- Get the S1 + S5 captures + `stat gpu` numbers from Matt.
- **Close Tier-B (B1–B5):** confirm against the dispatch acceptance. If render-evidence is good, the manifestation Phase-1 spike S1+S5 are finally banked.
- Fold render-evidence into a Tier-B close memo; route any final-key-light-VALUES design read to radagast if the mythic-weight (#5) judgment needs a design eye.
- File a Mac-KR update: P0.1 captures banked; manifestation Phase-1 spike forward register advanced.
- If any console step surfaced a NEW defect, that's a fresh finding → route (mantis repair if UE-side; engine consult only if it traces to the JSON/schema — Wave-1 already verified the export is clean, so default assumption is UE-side).

### Branch B — Matt has NOT run Wave 2 yet
- Tier-B stays staged. Do NOT re-fire mantis on Tier-A (it's banked).
- Other PC-seam work can proceed independently; Wave 2 is Matt-gated on console availability, not blocked on any agent.
- Leave the manual-step list untouched; it's complete per sam Gate-2.

## 3. Standing constraints (carry every session)

- **DXGI gate:** NEVER open a windowed editor over SSH — crashes at viewport creation (no GPU-attached desktop). Headless `-nullrhi` authoring only. Render-evidence + the #5 mythic-weight judgment require Matt at the PC console / RDP.
- **Push context:** this mhwet/WSL session has the mhwet-scoped GitHub SSH key. The `TheSa` console profile does NOT — commits made there stage but don't reach origin until pushed from mhwet/WSL. Do NOT mutate `TheSa` `core.sshCommand` (WSL depends on it).
- **Wave-close push** is a standing PC-seam pattern (no per-push re-ask) after Gate-2 PASS + session-boundary memo.
- **Commit prefix:** `david-h: ...`.

## 4. Open forward items

1. **Wave 2 (Matt console):** M1–M7 → S1 + S5 captures. The whole point of the spike.
2. **Q5 ambiguous-spirit visual:** still `FigureStandIn` placeholder. Cross-cutting creation-moment refinement → radagast↔Mac-gandalf consult, triggered by WS2 art-direction iteration. Gates the *aesthetic* B4 contrast read only (A5/B4 close the LIGHTING-RIG question). NOT urgent.
3. **Mantis M4 micro-fix (non-blocking):** sam Gate-2 WARN — fold a concrete M4 figure-light starting rotation (from the camera vector) on a future mantis pass. Cosmetic; values are console-tuned anyway.

## 5. Key artifacts (paths)

- Dispatch (ACTIVE): `agentic_orchestration/dispatches/2026-06-13-mantis-celestial-sphere-rework-and-figure-lighting-rig-repair.md`
- Manual-BP-steps for Matt (Wave 2): `agentic_orchestration/mantis/notes/2026-06-13-celestial-sphere-MANUAL-BP-STEPS-for-matt-console.md`
- Wave-1 close: `agentic_orchestration/david-h/notes/2026-06-13-wave1-close-mantis-tierA-banked.md`
- Mac-KR cross-host note: `agentic_orchestration/david-h/notes/2026-06-13-consultation-mac-kr-p0-1-findings-not-captures.md`
- sam Gate-1 / Gate-2 findings: `agentic_orchestration/qa/findings/2026-06-13-mantis-celestial-sphere-rework-gate-1.md` + `...-tierA-gate-2.md`
- radagast design-fit: `agentic_orchestration/radagast/notes/2026-06-13-celestial-sphere-rework-design-fit.md`

**End primer.**
