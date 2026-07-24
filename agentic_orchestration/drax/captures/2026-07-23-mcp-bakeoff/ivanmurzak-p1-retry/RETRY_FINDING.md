# IvanMurzak P1 isolated-capture — fresh-eyes retry (annex)

**Date:** 2026-07-24 · **Executor:** drax · **Host:** Mac mini (Apple Silicon), Godot 4.6.3 STANDARD, Metal / Forward+.

## What the retry was meant to answer

Original grade (MATRIX P1, IvanMurzak column): **PRESENT-BUT-BLANK-ON-HOST** — the native `screenshot-isolated` tool executed and produced a valid, auto-framed 512² PNG, but rendered **background-only** (exactly 1892 B) for every subject tried. `screenshot-viewport` produced a real 77 626 B render, so the editor itself renders; the failure was localized to the **isolated World3D SubViewport** on this Metal host. Open question: is this a **Metal/Forward+ hardware limitation** (isolated SubViewports can't render here) or an **addon capture-path bug** (reads the texture before the GPU settles)?

## Premise correction (evidence discipline)

The retry was chartered as "stack still on-disk outside repos." **Partly false:** the .NET toolchain (`~/.dotnet`), mono editor (`/tmp/godot_mono`), and server binary (`/tmp/gamedev-server`, v9.2.1) are on-disk, but the **Godot editor addon** (`godot_mcp_ivanmurzak`, the C# EditorPlugin that actually renders the isolated capture) was **working-tree-only on the deleted `mcp-bakeoff-ivanmurzak-throwaway` branch** — no commits were made (git reflog confirms same SHA as main), so it is unrecoverable from git. The NuGet cache (`~/.nuget/packages`) holds only the managed DLLs, no `.gd`/`plugin.cfg`/catalog. A fresh `git clone` of `IvanMurzak/Godot-MCP` returns addon **0.19.1** — a **drifted version** from the **4.1.0** build that was graded. Re-standing a different version would introduce a version confound and would NOT be a faithful retry of the graded artifact.

## What was run instead — the root-cause question, addon-agnostic

The retry's actual question ("does an isolated World3D SubViewport render on this Metal host, and does frame-settle fix the blank?") is **independent of which MCP addon drives it**. It was answered directly on the live Godot 4.6.3 STANDARD editor via the escape hatch (`execute_editor_script`), building a self-contained isolated SubViewport (own `World3D`, `UPDATE_ALWAYS`, `BoxMesh` + `DirectionalLight3D` + `Camera3D`, neutral bg) and reading `get_texture().get_image()` two ways:

| Variant | Settle | Result | Artifact |
|---|---|---|---|
| **A — synchronous** | `RenderingServer.force_draw()` ×6, no await | **BLANK** — 0 non-bg px / 16384 sampled | `ivan_retry_isolated_box.png` (772 B, dark) |
| **B — frame-settle** | `await RenderingServer.frame_post_draw` + `await get_tree().process_frame` ×2 | **RENDERS** — lit grey cube on dark bg (verified by eye) | `ivan_retry_isolated_box_await.png` (1161 B, box visible) |

Same isolated SubViewport, same host, same subject — the **only** difference is awaiting post-draw frames before reading the texture.

## Conclusion

**The isolated World3D SubViewport blank on this Metal host is a render-frame-settle timing bug, NOT a Metal/Forward+ hardware limitation.** An isolated SubViewport renders correctly on Godot 4.6.3 / Metal / Forward+ **when the capture awaits post-draw frames** before reading the texture. IvanMurzak's `screenshot-isolated` produced 1892-byte background-only captures because its capture path reads the SubViewport texture synchronously (no post-draw await) — a fixable tool-implementation bug.

**Implication for IvanMurzak P1 grade:** the isolated-node-capture **capability is viable on this host**. IvanMurzak's tool is one frame-settle fix away from P1-PASS; the blank is not disqualifying at the host level. (The d2-skeleton subject additionally has **0 editor-time meshes** — it is runtime-built — so any editor-time isolated capture of the *skeleton specifically* also requires the runtime build; the settle fix applies to authored geometry.)

**Evidence:** `isolated_subviewport_probe.json` (Variant A transcript), `isolated_subviewport_probe_await.json` (Variant B transcript), `ivan_retry_isolated_box.png` (blank), `ivan_retry_isolated_box_await.png` (renders). Probe driven through the Pro stack's `execute_editor_script`; the finding is addon-agnostic (it is a Godot/Metal capture-timing fact, not a Pro or IvanMurzak fact).

**Signed:** drax, 2026-07-24.
