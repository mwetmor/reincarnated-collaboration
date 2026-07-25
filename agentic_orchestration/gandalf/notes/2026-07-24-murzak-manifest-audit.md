# Murzak manifest audit — the column we closed is the only one that answers the question we now have

**Date:** 2026-07-24 · **Author:** gandalf (`ARCHITECT`) · **Method:** GitHub manifest read, no install, no run
**Trigger:** Matt's reframe — *"which tool/process combination is best at building NEW scenes, expanding scenes, or building out other new concepts like new VFX or HUD/UX/UI… Based on that, we owe Murzak some more testing too."*
**Companion:** `2026-07-24-mcp-authoring-surface-audit.md` (the incumbent-vs-Pro audit this one amends)
**Cost:** minutes. **What it corrects:** a capability gap I called structural, and a closure decision we made on the merits.

---

## 0. Headline

`IvanMurzak/Godot-MCP` — 187★, C#, Apache-2.0, core pushed **2026-07-21**, extension family pushed
**2026-07-20** — ships **39 built-in tools across 11 families**, a **GridMap extension**, a **CSG
extension**, a **GPUParticles extension**, and a **template for authoring our own tools**.

Every capability I named as missing in the prior audit is present, reachable, or authorable by us.

## 1. The core surface — 11 families, 39 tools

| Family | Tools | Why it matters here |
|---|---|---|
| **node** | `node-find` · `node-create` · `node-modify` · `node-set-parent` · `node-duplicate` · `node-delete` | Full CRUD. The incumbent has none of create/delete/duplicate |
| **scene** | `scene-open` · `scene-save` · `scene-create` · `scene-list-opened` · `scene-get-data` | Scene authoring from nothing |
| **resource** | `resource-find` · `resource-get-data` · `resource-modify` · `resource-create` · `resource-move` · `resource-delete` | Keeps `.import` sidecars consistent — the thing that bit us |
| **filesystem** | `filesystem-list` · `filesystem-reimport` | **`reimport`** — neither other server has it |
| **script** | `script-read` · `script-create` · `script-update` · `script-delete` · `script-attach-to-node` · `script-validate` | **See §3 — this is the one that breaks the framing** |
| **screenshot** | `screenshot-viewport` · `screenshot-camera` · `screenshot-isolated` | `-camera` is the A1-legal one; `-isolated` is the model viewer D3 retired |
| **editor** | application get/set-state · selection get/set | Drives run-and-play lifecycle |
| **console** | `console-get-logs` · `console-clear-logs` | Editor log collector |
| **reflection** | `reflection-method-find` · `reflection-method-call` | **Any C# method, any loaded assembly, public or private, static or instance** |
| **runtime-errors** | get / clear | Errors from the **running game** — GDScript backtraces, shader errors, unobserved `Task` exceptions |
| **ping** | `ping` | Readiness probe |

## 2. The extension family — ten packages, pushed 2026-07-20

`Godot-AI-GridMap` · `Godot-AI-CSG` · `Godot-AI-Particles` · `Godot-AI-Animation` ·
`Godot-AI-Terrain3D` · `Godot-AI-Tilemap` · `Godot-AI-Navigation` · `Godot-AI-PhantomCamera` ·
`Godot-AI-Beehave` · `Godot-AI-Dialogic`

Three of them land directly on task-classes Matt just named:

- **`Godot-AI-GridMap`** — `gridmap-create` · `gridmap-set-mesh-library` · `gridmap-set-cell` ·
  `gridmap-clear-cell` · `gridmap-clear` · `gridmap-get`. **I called GridMap a structural gap.** It
  is Godot's native 3D modular primitive — the exact abstraction a Synty modular dungeon kit maps
  onto — and my table read `✗ / ✗` across both audited servers. Murzak ships it. One `set-cell` call
  per tile against a `MeshLibrary` is a fundamentally cheaper wire shape than one `add_scene_instance`
  per instance, which changes the latency arithmetic that I treated as settled.
- **`Godot-AI-CSG`** — box/sphere/cylinder/combiner + Union/Intersection/Subtraction. **Blockout
  geometry authored from nothing, with no asset pack at all.** That is T3 NEW SCENE in its purest
  form and nothing else in the field can do it.
- **`Godot-AI-Particles`** — `particles-create` · `particles-configure` · `particles-set-emitting` ·
  `particles-get` for `GpuParticles2D`/`3D`. Squarely the T4-VFX axis.

## 3. The finding that breaks the framing

The `script` family does **CRUD on `.gd` and `.cs`, plus `script-attach-to-node`, plus
`script-validate`.**

M3 — our winning method — is *a headless GDScript builder*. **Murzak can author M3.** It can write
the builder, validate it, attach it, and drive the editor to run it.

So "MCP vs headless script" is not a rivalry in Murzak's case. The ruled doctrine in
`pipeline-game.md` — *"MCP authors recipes / headless scripts run production"* — is not a compromise
between two camps here; it is **a single tool doing both halves.** The program must stop scoring
Murzak as a rival to M3 and start scoring it as *a possible author of M3*.

## 4. The ceiling is not the tool surface

`reflection-method-call` finds and calls any C# method in any loaded assembly via ReflectorNet. That
is a strict superset of Pro's `execute_editor_script`. Combined with `[AiToolType]` (§5), **every gap
in my prior capability table — AABB, bounds, GridMap, clock control — is reachable.**

Which means the honest question changed shape. It is no longer *"what can this tool do?"* It is:

1. **Latency** — how many round-trips does the task take, and at what ms/call.
2. **Aim** — can the agent hit the right call without a control to check itself against.
3. **Blast radius** — a reflection call into private methods is an escape hatch with no guardrail.

Those are the three axes the laps should measure. Capability enumeration is finished.

## 5. The surface is extensible **by us**

`Godot-AI-Tools-Template` — *"write C# `[AiToolType]` MCP tools and ship them as a source-only NuGet
package (no bundled Godot, no version lock)."* Auto-discovered after rebuild; no registry edit.
Unity-MCP's description puts it plainly: *"any C# method may be turned into a tool by a single line."*

**The AABB gap is one C# method.** UNKNOWN-1 from the prior audit — *"can Pro measure an
un-instantiated FBX?"* — was framed as a capability ceiling. Against Murzak it is an afternoon's
engineering. The template's own proof is the testbed build: package `.cs` injected as `<Compile>`
items into the consumer, compiling against the consumer's own GodotSharp, CI-tested across a
multi-Godot matrix without a Godot binary.

This reframes the whole program's terminal question from *"which tool wins"* to **"which substrate do
we extend."**

## 6. Standup is no longer heavy — and that was half the closure rationale

The bake-off closed Murzak partly on *"heaviest standup (3-hop, mono, .NET SDK)."* Current path:

```
npm install -g godot-cli
godot-cli install-plugin ./project     # idempotent: addon + NuGet refs + project.godot
godot-cli login                        # OAuth 2.1 device login  ← MATT-ONLY
godot-cli setup-mcp claude-code ./project
godot-cli open ./project ; godot-cli wait-for-ready ./project
```

`~/.dotnet` survives on disk; `/tmp/godot_mono` and `/tmp/gamedev-server` were cleared.

## 7. The governance flag — and it is a real one

Default connection is the **ai-game.dev hosted cloud**, via OAuth 2.1 device login that writes a
**machine-wide credential the editor plugin auto-adopts.** Self-hosting is supported (*"point at your
own server"*, Docker image published).

Two things follow, and neither is mine to rule:

- **Cloud vs self-hosted is a commitment-boundary.** Cloud mode means our scene geometry, script
  contents and screenshots transit a third party. ADR-006 (read-only-by-default on external systems)
  does not cover this shape. → `matt_decision_needed`.
- **`godot-cli login` is a Matt-only action.** Browser OAuth, machine-wide credential. → `matt_to_do`.
  Every Murzak lap is gated behind it.

## 8. The closure rationale, re-read against what we now know

From `2026-07-24-mcp-bakeoff-verdict-rec.md` §3:

> *"No slot: strengths (C# reflection, **editor-time authoring**) map to **no proven need**."*

Both named strengths are, four days later, **exactly the two named unknowns.** Editor-time authoring
is T2/T3; C# reflection is the escape hatch that makes every capability gap closable. The column was
closed for having capabilities we had not yet needed — which is the precise failure mode of a
*proven*-needs rubric, and the **third** instance of that defect in this workstream (bake-off probe
weighting 4:2 observation-over-authoring; this closure; the replica lap chartered to favour the
already-winning method).

This is not hindsight. It is the same rubric error, named at the time, firing a third time.

## 9. The shelf-life finding

Core pushed **2026-07-21**; the entire ten-package extension family pushed **2026-07-20**. Our
bake-off ran **2026-07-23** and its verdict doc was written against a Murzak that had shipped a
GridMap extension three days earlier and a Particles extension we would have called decisive.

**A tool-capability verdict has a shelf life measured in days.** That becomes a standing program law
(L-C): re-read the manifest at every lap, record the version read, never carry a prior verdict
forward as fact.

## 10. Two flags, not chases

- **`IvanMurzak/ai-game-dev-plugin`** (2★, JS) — *Claude Code plugins* for Unreal/Unity/Godot: a
  **non-MCP integration surface** that installs the engine plugin, logs in and opens the editor.
  A fourth method-class we have not modelled. Note; do not chase.
- **`IvanMurzak/Context-Engine`** (3★, C++, pushed 2026-07-25) — *"AI-first, file-authoritative,
  headless-complete game engine."* Uncanny convergence with our own ruled doctrine. **Not a tool —
  an engine.** Flag for awareness. Chasing it would be exactly the scope-drift this program exists to
  discipline.

---

**Signed:** gandalf, 2026-07-24. Second manifest audit in one session; second correction to a claim I
had committed. The discipline is now proven twice and should be canonical: **capability is read from
the manifest, reliability is read from behaviour, and neither is inferred from the other.**
