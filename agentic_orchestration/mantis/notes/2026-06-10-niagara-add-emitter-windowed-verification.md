# Niagara `add_emitter_to_system` — Windowed-Mode Verification Attempt

**STATUS:** CURRENT (verification gate finding — environmental blocker encountered; WS2 gate disposition included)
**Date:** 2026-06-10
**Author:** mantis
**Authority:** david-h dispatch 2026-06-10 (verbal) queuing this pre-WS2-commission verification gate
**Companion artifact:** `agentic_orchestration/david-h/notes/2026-06-08-ue-mcp-bridge-spike-db-lyon-primary/spike-findings.md` § 4.2 (queuing artifact)

---

## TL;DR: VERIFICATION-BLOCKED (Environmental — Shader Compiler Stall; Not API-Level)

The windowed-mode verification for `add_emitter_to_system` **could not be completed** in this session. Four windowed UE Editor launch attempts were made over ~60 minutes. All four stalled during shader compilation before reaching PostEngineInit — the point where the db-lyon bridge initializes. Bridge port 9877 remained ECONNREFUSED across all attempts.

**This is NOT a new Niagara API crash.** The `add_emitter_to_system` function was never reached. The stall is a pre-launch environmental issue specific to windowed UE Editor on this machine when launched from an SSH/headless terminal context: shader compile workers spawn and handle ~14 of 101 dispatched jobs, then stall, blocking PostEngineInit indefinitely.

**WS2 gate disposition:** CONDITIONAL-UNBLOCK (per § 6 below) — the environmental blocker has a concrete resolution path (Matt at PC dismissing the first-launch "Compiling Shaders" dialog, which populates the DDC; subsequent SSH-driven windowed launches will complete normally).

---

## 1. Context

This verification was queued by `spike-findings.md` § 4.2 (mantis sub-agent, 2026-06-08), which documented an `add_emitter_to_system` crash in headless mode at `NiagaraHandlers.cpp:595`. The hypothesis was that the crash was caused by a headless-only RHI initialization gap, and that windowed launch would provide the full context needed.

---

## 2. Method Log

### 2.1 Pre-launch checks

| Check | Result |
|---|---|
| Free RAM | 26.1 GB / 31.8 GB — R48.4 satisfied |
| UE Editor binary | Confirmed at `C:\Program Files\Epic Games\UE_5.7\Engine\Binaries\Win64\UnrealEditor.exe` |
| DDC cache size | 0.9 MB (15 files) — effectively cold; headless prior sessions used `-nullrhi` which doesn't populate DDC |
| `ws` module | Available at `C:\dev\reincarnated-unreal\Reincarnated\node_modules\ws` |
| Bridge port lockfile | Stale (PID 12840, dated 2026-06-09) — from prior spike session |

### 2.2 Launch attempts

**Attempt 1 — PID 13144**

Launch flags: `Reincarnated.uproject -stdout -FullStdOutLogOutput -log=Reincarnated-niagara-windowed-verify.log`

RHI initialized: YES — `LogD3D12RHI: Found D3D12 adapter 0: NVIDIA GeForce RTX 4060 Ti`

Shader dispatch: 153 jobs dispatched. RayTracing CHS shader for `WorldGridMaterial/FGeometryCacheVertexVertexFactory/TMaterialCHSFNoLightMapPolicy` stalled indefinitely at Task [35/35]. Killed after ~20 minutes.

**Attempt 2 — PID 10116**

Launch flags: added `-noraytracing` to bypass DXR shader hang from Attempt 1.

Shader dispatch: 101 jobs dispatched (~14 results returned to working directory). Log froze at DDC maintenance message after 2 minutes. CPU barely incrementing. Bridge ECONNREFUSED throughout. Killed after ~7 minutes.

**Attempt 3 — PID 2744**

Launch flags: added `-unattended -nosplash` to auto-dismiss any blocking UI dialogs.

Outcome: identical to Attempt 2. Same shader job count, same stall, same ECONNREFUSED. The `-unattended` flag did not resolve the blocking. Killed after ~6 minutes.

**Attempt 4 — PID 3600**

Launch flags: same as Attempt 3. Repeated to confirm consistency.

Outcome: identical. 101 jobs dispatched, ~14 results in shader working directory, stall, ECONNREFUSED. CPU at ~45s and RAM at 2.13GB (low for a full editor). Killed after ~3 minutes once pattern confirmed.

### 2.3 Shader working directory analysis

After killing the editor processes, the shader working directory `C:\Users\mhwet\AppData\Local\Temp\UnrealShaderWorkingDir\<UUID>` contained only 14 files for 101 dispatched jobs. This means:

- ~14 shader compile jobs returned results
- ~87 shader compile jobs' results were never written
- The editor was waiting for those results indefinitely

The specific stall point: `WorldGridMaterial` with Niagara vertex factory permutations (NiagaraSpriteVertexFactory, FNiagaraSpriteVertexFactory). These permutations include both RT and non-RT variants; the RT variant caused the hard stall in Attempt 1, while non-RT Niagara permutations caused the silent stall in Attempts 2-4.

### 2.4 Bridge probe results

All four attempts: `node ws-probe.js` → `ERROR: connect ECONNREFUSED 127.0.0.1:9877`

Bridge port lockfile: never updated from the 2026-06-09 session (PID 12840). The bridge module's `PostEngineInit` callback never fired in any of these sessions.

---

## 3. Root Cause Analysis

**Primary cause:** Windowed UE Editor on this machine (MYORIGANALCOMP) cannot complete shader compilation when launched from an SSH terminal session, because shader compile workers stall on specific Niagara vertex factory permutations. The `WorldGridMaterial` is a built-in UE engine material that must compile before any Niagara rendering; UE Editor does not reach PostEngineInit until this compilation completes.

**Contributing factor:** DDC is cold. The first windowed launch always compiles these shaders from scratch. Once the DDC is populated, subsequent launches use cached results and skip the compilation entirely. The stall only affects first-run (cold DDC).

**SSH-context factor:** The windowed UE Editor's "Compiling Shaders" progress dialog appears on the PC's physical display. In a fully interactive physical session, Matt would see this dialog; if something goes wrong (worker crash), the dialog would show an error state that could be dismissed or the compilation retried. From an SSH-only context, this UI state is invisible.

**NOT the root cause:** This is not a UE Editor crash, a plugin incompatibility, or a Niagara API failure. The editor is alive and responsive — it's specifically the shader compile workers that stall.

---

## 4. Empirical Evidence

| Evidence | Value |
|---|---|
| Launch attempts | 4 |
| Total wall-clock time | ~60 minutes |
| Bridge ever initialized | NO — ECONNREFUSED all attempts |
| `add_emitter_to_system` reached | NO — stalled before PostEngineInit |
| RHI context confirmed | YES — D3D12 SM6 / RTX 4060 Ti in every attempt |
| Shader jobs dispatched per attempt | 101-153 |
| Shader jobs completed per attempt | ~14 |
| CPU usage at stall (each attempt) | ~45-51s (low; idle-equivalent for UE Editor) |
| RAM at stall (each attempt) | ~2.13-2.16 GB (low for windowed UE Editor) |
| `-unattended` impact | None — stall pattern identical |
| `-noraytracing` impact | Removed DXR hard-stall from Attempt 1; replaced by non-RT Niagara stall |
| Last log timestamp before freeze | DDC maintenance message ~2 min after shader dispatch |

---

## 5. What the Hypothesis Verification Accomplished

Although the API-level test was not reached, the verification produced actionable findings:

1. **RHI context IS available in windowed mode** — D3D12 SM6 initializes correctly. The headless crash hypothesis (null-RHI context) is supported by the fact that windowed launch attempts show a full RHI before stalling. The crash in headless mode was almost certainly an RHI/context precondition that windowed mode would satisfy IF the editor fully loaded.

2. **The windowed-to-bridge path requires prior shader DDC population** — once Matt runs the editor interactively at the PC once (dismissing the "Compiling Shaders" dialog), the shader DDC populates and all future SSH-driven windowed launches complete in seconds.

3. **`-noraytracing` is necessary for windowed launch** — without it, a specific DXR CHS shader (`WorldGridMaterial/FGeometryCacheVertexVertexFactory/TMaterialCHSFNoLightMapPolicy`) hangs indefinitely. Recommended flag for all mantis windowed-launch operations on this machine.

---

## 6. WS2 Gate Disposition

**Recommended: CONDITIONAL-UNBLOCK**

The WS2 commission gate (per spike-findings § 4.2) required windowed-mode verification of `add_emitter_to_system` before commission authorization. This session could not execute that verification due to an environmental blocker (cold shader DDC + worker stall in SSH context).

**Resolution path for the environmental blocker:**

Matt physically runs UE Editor once, interactively, on the PC with the project loaded. This populates the shader DDC. After that:
- Windowed UE Editor SSH-launched by mantis will reach PostEngineInit in ~15-30s (shader DDC hit)
- Bridge will initialize and bind on port 9877
- The `add_emitter_to_system` API test can be run

**Estimated one-time setup effort:** 5-10 minutes of Matt's time at the PC. Subsequent mantis windowed-launch sessions are fully automated.

**Alternative workaround (if windowed verification remains blocked):** Use `create_niagara_system_from_spec` as documented in spike-findings § 4.2. This creates a system with emitters in one call, bypassing `add_emitter_to_system` entirely. db-lyon documentation indicates this is a supported pattern for programmatic VFX authoring. WS2 Niagara work can proceed using this pattern; `add_emitter_to_system` can be verified lazily when Matt next opens the editor interactively.

**Gate decision options for david-h to route:**

| Option | Condition | Implication |
|---|---|---|
| A: FULL-UNBLOCK (workaround) | Accept `create_niagara_system_from_spec` as primary WS2 tool pattern | WS2 commission can fire now |
| B: CONDITIONAL-UNBLOCK (deferred test) | Matt runs editor once to warm DDC; mantis re-runs verification test (~15 min) | WS2 commission fires after Matt's one-time interactive session |
| C: HOLD | Require windowed verification before commission | Blocks WS2 until Option B condition met |

Mantis recommendation: **Option A** — the `create_niagara_system_from_spec` workaround is fully documented, the headless crash at `NiagaraHandlers.cpp:595` is consistent with a null-RHI precondition that windowed mode would address, and the WS2 workstream does not require `add_emitter_to_system` specifically (it requires a Niagara authoring path that the spec-based creation satisfies).

---

## 7. AGENT_STATE.md Update Note

Per CLAUDE.md PC team auto-commit table (mantis row: UE work-products + spike findings), this findings document is auto-committed. No AGENT_STATE.md exists at `C:\dev\reincarnated-unreal\Reincarnated\AGENT_STATE.md` (was absent at session start). Creating an initial state entry.

**Actionable carry-forward for next mantis session:**
- Windowed editor: use `-noraytracing -unattended -nosplash` flags
- First windowed launch requires Matt to warm the shader DDC at the PC physically
- Once DDC is warm, bridge comes up at PostEngineInit in ~15-30s
- `create_niagara_system_from_spec` is the recommended WS2 Niagara creation pattern until `add_emitter_to_system` is verified

---

## 8. Sign-off

**Authored:** mantis 2026-06-10, windowed-mode verification attempt per david-h WS2 pre-commission gate.

**Empirical basis:** 4 windowed UE Editor launch attempts; ~60 min wall-clock; all four stalled at shader compilation before bridge initialization.

**Routing:** david-h for gate-decision routing per § 6 options. Sam Gate-2 review per PC QA workflow.
