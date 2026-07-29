# PROVISION-CAL W1-B — Murzak version-bump re-read (L-C lap)

**Run:** PROVISION-CAL, Wave-1 cell PC-W1-B (relaunch after stream-timeout loss of attempt #1)
**Conductor:** gandalf (RUN-CONDUCTOR) · **Charter:** `agentic_orchestration/gandalf/notes/2026-07-28-provision-cal-run-charter.md` §3 Tier 4 + §6 R-PC-6
**Executes:** §6 check 10 of `agentic_orchestration/legolas/notes/2026-07-26-plugin-provisioning-menu.md`
**Mode:** A (analytical), READ-ONLY. No installs, no builds, no execution.
**Date:** 2026-07-28
**Status:** COMPLETE — all four questions settled. Verdict in §7.

---

## §0 — Baseline being re-read against (the lab's L3 read)

| Component | Lab version (L3, 2026-07-24) | Current (per menu §6 check 10) |
|---|---|---|
| nuget `com.IvanMurzak.GameDev.MCP.Server` | **9.2.0** | **9.2.2** |
| core addon `godot_mcp` | **0.19.1** | **v0.20.0** (published 2026-07-26) |

**Baseline env-var mitigation** (drax L3 report §4.1, `agentic_orchestration/drax/notes/2026-07-24-tcp-l3-murzak-standup-run-report.md` lines 236–240), enforced in `editor_up.sh`:

```bash
export GODOT_MCP_CONNECTION_MODE=Custom
export GODOT_MCP_AUTH_OPTION=None
export GODOT_MCP_HOST=http://localhost:27435
export GODOT_MCP_LOG_LEVEL=Debug
```

**Baseline mechanism** (drax L3 §4.1, citing addon source `Runtime/Connection/GodotMcpEnvFile.cs:145–185` @ 0.19.1): mode precedence is **env var > `.env` file > loopback-host inference > config default**, and *the config default is Cloud*. Baseline outbound at boot, before any tool call:

```
wss://ai-game.dev/mcp/hub/mcp-server?instance_id=…&engine=godot&project_name=tcp_l3_lab
  &project_path_hash=eb8c59d8…&machine_name=Matthews-Mac-mini
```

Identity fields transmitted at baseline: `instance_id`, `engine`, `project_name`, `project_path_hash`, `machine_name`.

---

## §0.1 — FIRST FINDING: the charter's targets are already stale (the lap moved under us)

The menu's check 10 named **9.2.2** and **v0.20.0**. Re-read today, both are behind head-of-line:

| Component | L3 lab | Menu check-10 target | **Actual current (2026-07-28)** |
|---|---|---|---|
| `com.IvanMurzak.GameDev.MCP.Server` (nuget / GH release) | 9.2.0 | 9.2.2 | **9.2.4** (`v9.2.4`, 2026-07-28T04:07:14Z) |
| core addon `godot_mcp` | 0.19.1 | v0.20.0 | **v0.20.1** (2026-07-28T18:40:03Z) |

Sources: `gh api repos/IvanMurzak/GameDev-MCP-Server/releases`; `gh api repos/IvanMurzak/Godot-MCP/releases`;
NuGet search index `azuresearch-usnc.nuget.org/query?q=packageid:com.IvanMurzak.GameDev.MCP.Server` → `"version": "9.2.4"`.

Release cadence measured over the window: **13 server releases** since 2026-06-11 and **v0.11.1 → v0.20.1 in ~5 weeks**.
This is a fast-moving upstream; any Tier-4 verdict should record the **exact tag installed**, not "current".

**Tag SHAs** (`gh api repos/IvanMurzak/Godot-MCP/tags`):
- `v0.19.1` = `34374fe8f6bb2bd1c46ba48d6004990d71718e4c` (the lab's version)
- `v0.20.0` = `8a9f3e4b11e640baea3eb6cd342bcc4c967b5b1c`
- `v0.20.1` = `6bd23f6a832ac5e75798d4b68e42155c6e3a187a`
- repo `main` HEAD at read time = `eba58e0c6a305f34c53ddf855307935358dee325` (2026-07-28 16:12 −0700, `ci(release): gate the Discord announcement on the HTTP response (#333)`) — **past v0.20.1**, CI-only.

Method: repo cloned read-only to `agentic_orchestration/legolas/scratch/2026-07-28-pcw1b/godot-mcp`. **Never built, never executed.**

---

## §1 — Q1 (RULING-CRITICAL): env vars, endpoints, identity, connect-on-load

### 1.1 · Verdict: **UNCHANGED — the entire connection/identity/auth layer is byte-identical v0.19.1 → v0.20.1**

The strongest possible form of this answer is a null diff, and that is what the source gives. `git diff v0.19.1 v0.20.1 -- <file>` returns **zero lines** for every file that governs Q46:

| File | Diff lines 0.19.1 → 0.20.1 |
|---|---|
| `addons/godot_mcp/Runtime/Connection/GodotMcpEnvFile.cs` | **0** |
| `addons/godot_mcp/Runtime/Connection/GodotMcpConfig.cs` | **0** |
| `addons/godot_mcp/Runtime/Connection/GodotProjectIdentity.cs` | **0** |
| `addons/godot_mcp/Editor/Connection/GodotAccountAuth.cs` | **0** |
| `addons/godot_mcp/Editor/Connection/GodotDeviceAuthService.cs` | **0** |
| `addons/godot_mcp/Editor/Connection/DevControl/DevControlServer.cs` | **0** |

The only change anywhere in `Runtime/Connection/` across the two bumps:

- `GodotMcpConnection.cs` — **two hunks**: `FallbackPluginVersion` string `"0.19.1"` → `"0.20.1"`, and a
  `Tools.Tool_Node.InstallReflectionResolver();` call added under `#if TOOLS` (issue #292 — instance-method
  reflection by `{"instanceId": N}`). Neither touches transport, host, mode, auth or identity.
- `GodotMcpServerView.cs` — the `ServerVersion` pin constant only (see §1.5).

**drax's L3 mechanism read (`GodotMcpEnvFile.cs`) therefore still holds verbatim at v0.20.1.** No re-derivation
needed; the file has not been edited.

### 1.2 · The env vars, named exactly as the CURRENT source defines them

Declared as constants in `GodotMcpConfig.cs` (lines 52–76), aliasing `GodotMcpEnv.*`. Full set present in the
v0.20.1 tree (`grep -o "GODOT_MCP_[A-Z_]*"`, occurrence counts):

| Env var | Occurrences | Role |
|---|---|---|
| **`GODOT_MCP_CONNECTION_MODE`** | 14 | `GodotMcpConfig.EnvConnectionMode`. Highest-precedence mode selector. **Present, same name, same semantics.** |
| **`GODOT_MCP_HOST`** | 22 | `GodotMcpConfig.EnvHost`. Custom-mode server host. **Present, unchanged.** |
| **`GODOT_MCP_AUTH_OPTION`** | 7 | `GodotMcpConfig.EnvAuthOption`. Custom-mode auth; env wins live via `ActiveAuthOption`. **Present, unchanged.** |
| **`GODOT_MCP_LOG_LEVEL`** | 9 | `GodotMcpConfig.EnvLogLevel`. Cross-cutting; env wins live via `ActiveLogLevel`. **Present, unchanged.** |
| `GODOT_MCP_TOKEN` | 28 | `EnvToken`. Routes to the active mode's token field. Not in our four. |
| `GODOT_MCP_CLOUD_URL` | 9 | `EnvCloudUrl`. Cloud base override; **env-only contract — no serialized backing field**. |
| `GODOT_MCP_DEV_CONTROL` / `_PORT` | 23 / 5 | Opt-in local dev-control HTTP listener (§1.6). Off unless set. |
| `GODOT_MCP_HARNESS*` (4 vars) | 5 | Test-harness only. |

**All four of R-PC-6's launch env vars survive with identical names and identical semantics.** The `editor_up.sh`
block from drax L3 §4.1 is valid against v0.20.1 as written.

### 1.3 · Precedence — unchanged

`GodotMcpEnvFile.cs:137–156` (doc comment on `Apply`) states the ladder still in force:

> Mode selection (highest wins): an explicit `GODOT_MCP_CONNECTION_MODE` from the env layer already wins via
> `GodotMcpConfig.ActiveMode` (it is not set here — env is live). Otherwise an explicit mode in the `.env` file
> wins; otherwise, if the effective host (env host > file host > configured host) is a loopback address,
> auto-select `GodotMcpConnectionMode.Custom` (parity with Unity-MCP's loopback inference).

Same four rungs drax recorded: **env var > `.env` file > loopback-host inference > config default.**

### 1.4 · Does the compiled-in default remain Cloud? **YES.**

`addons/godot_mcp/Runtime/Connection/GodotMcpConfig.cs:118`:

```csharp
public GodotMcpConnectionMode ConnectionMode { get; set; } = GodotMcpConnectionMode.Cloud;
```

and line 81:

```csharp
public const string DefaultCloudBaseUrl = "https://ai-game.dev";
```

Corroborated outside the source by the repo's own GitHub description, unchanged today: *"AI tools for the Godot
Editor in C#, **with cloud connection to ai-game.dev**."* and by `CLAUDE.md`: *"connects to an MCP server (cloud
`ai-game.dev` by default, or a custom local server)"*. **T1 stands exactly as filed. A bare launch still leaks.**

### 1.5 · New outbound endpoints? **NONE introduced by this bump.**

Exhaustive grep of `https?://` literals across all addon `.cs` at v0.20.1, after removing licence/schema/doc URLs:

- `https://ai-game.dev` — `GodotMcpConfig.cs:81`, the cloud default (pre-existing, = T1).
- `https://discord.gg/cfbdMZX99G` — `SupportFooterLinks.cs:30`, a static UI hyperlink label. Not fetched.
- `https://github.com/{repo}` — `ExtensionsPanelText.cs:85`, string-formatting for an extension's display link.
- `http://{BindHost}:{_port}/` — `DevControlServer.cs:58`, the **opt-in local** dev-control listener.

**Zero new remote hosts.** The OAuth/device-authorization surface (`GodotAccountAuth`, `GodotDeviceAuthService`,
`GodotTokenRefresher`, `MachineCredentialStore`) is present but **pre-dates the lab's read** — all three files show a
null diff, so whatever drax observed at 0.19.1 already contained them. Their activation is gated:

- `GodotMcpConnection.cs:350–359` — the credential provider consults the account store **only** `if (_config.ActiveMode == GodotMcpConnectionMode.Cloud && _account.IsSignedIn)`; the source comment states *"every Custom-mode connection behaves exactly as before."*
- `GodotDeviceAuthFlow` (the thing that actually calls the device endpoints) is constructed from the **UI sign-in path** in `ConnectionPanel.cs`, not from boot.

So under `GODOT_MCP_CONNECTION_MODE=Custom` + `GODOT_MCP_AUTH_OPTION=None` on a machine with no stored credential,
the account layer is inert. **This is a reasoning-from-source conclusion, not a measurement** — the packet-quiet
assert in R-PC-6 remains the thing that decides it.

### 1.6 · New identity fields transmitted? **NO — same five, and they follow the host.**

`GodotMcpConnection.cs:361–375` (unchanged in content across the bump — only the file's other hunk moved lines):

```csharp
// the client appends {instance_id, engine, project_name, project_path_hash, machine_name} to the hub URL
var instanceMetadata = GodotProjectIdentity.BuildInstanceMetadata(
    projectRootPath, ResolveProjectName(), GodotProjectIdentity.SessionInstanceId,
    System.Environment.MachineName);
```

The same **five** fields drax captured at 0.19.1 — `instance_id`, `engine`, `project_name`, `project_path_hash`,
`machine_name`. No sixth field. (`GodotProjectIdentity.cs:100–123` documents an optional
`project_path_hash_legacy` **dual-hash**, but explicitly notes *"the released pin sends only `project_path_hash`"* —
the legacy twin is transition insurance carried by the LIB, not an added transmission at our pin.)

**Load-bearing nuance for the packet-quiet assert:** the metadata is built **unconditionally at `Start()`,
regardless of mode**. It is not a Cloud-only construction. What mode controls is the **hub URL it is appended to** —
in Custom mode that URL is `http://localhost:27435/hub/mcp-server`, so the identity fields go to the *loopback*
server. The assert should therefore expect to see `machine_name` in the local traffic and must be scoped to
"nothing leaves the host", not "machine name is never serialized".

### 1.7 · Changed connect-on-load behaviour? **NO.**

`GodotMcpConnection.Start()` (line 330) is unchanged in shape: idempotent, *"the connect itself is fire-and-forget
from the editor's perspective — the McpPlugin client manages (re)connection in the background."* The `[Tool]`
`EditorPlugin` still boots on editor load and still connects. drax's L3 §4.1 observation — that a Cloud-mode failure
**retries the cloud indefinitely and never falls back to loopback** — has no contradicting change in the diff.

### 1.8 · Q1 bottom line

**SAFE-TO-PROCEED-AS-CHARTERED on Q1.** R-PC-6's four env vars are correct, correctly named, and mechanically
identical at v0.20.1. The Cloud default persists (so the mitigation remains mandatory, exactly as R-PC-6 says).
No new endpoint, no new identity field, no changed connect-on-load. The one carried caveat is §1.6's scoping note
for the assert.


---

## §2 — Q2: what else changed (behaviour, not just fixes)

### 2.1 · Server 9.2.0 → 9.2.4 — **no authored behaviour change at all**

All four release bodies (`gh api repos/IvanMurzak/GameDev-MCP-Server/releases`) contain nothing but
dependency bumps, a CI action upgrade, and the release commit:

| Release | Content |
|---|---|
| v9.2.1 (07-21) | CI Node20→Node24 actions (#28); McpPlugin → 7.4.0 (#29) |
| v9.2.2 (07-25) | McpPlugin → 7.5.0 (#31); *"restore McpPlugin lockstep with McpPlugin.Server at 7.5.0"* (#32) |
| v9.2.3 (07-27) | ReflectorNet → 5.3.3 (#34); McpPlugin → 7.5.1 (#35) |
| v9.2.4 (07-28) | ReflectorNet → 5.4.0 (#37); McpPlugin → 7.5.2 (#38) |

**Finding:** the server's behaviour delta is entirely *inherited* from `com.IvanMurzak.McpPlugin`
7.3.0 → 7.5.2 and `com.IvanMurzak.ReflectorNet` 5.3.2 → 5.4.0. Those two libraries are **closed to this
read** — they are consumed as NuGet binaries, and their repos were not audited on this lap. **Named as a
gap, not as an accusation** (§5).

### 2.2 · Addon 0.19.1 → 0.20.1 — four real behaviour changes

**(a) THE ONE THAT MATTERS TO THIS RUN — PR #321 closes the silent-success class.**
*"fix(tools): stop reporting success for no-op reimports and Variant/Node reflection calls"* — the PR body
calls it *"the 'reports success while doing nothing' class."* Root cause traced through ReflectorNet 5.3.2:
`Godot.Variant`'s only two properties are get-only, no converter was registered, selection fell through to
`GenericReflectionConverter<object>`, `SerializedMemberConverter.Read` threw on the unknown key, and
`ExtensionsJsonElement.cs` swallowed it with **a bare `catch {}`**, returning `default(Variant)` == `Nil`.
`MethodWrapper.VerifyParameters` waved the boxed default through. Result: `System.Void` success, no effect,
nothing in the `Logs` sink.

Measured pre-fix behaviour, verbatim from the PR:

```
OBJ-SHAPE  {"VariantType":"String","Obj":"res://CharacterCreator.tscn"}  -> Godot.Variant, VariantType=Nil
RAW-STRING "res://CharacterCreator.tscn"                                 -> Godot.Variant, VariantType=Nil
NODE-REF   {"instanceId":123}                                            -> null
```

Four new files close it: `GodotVariantPayload.cs` (the pure parser), `Godot_Variant_ReflectionConverter.cs`,
`Godot_Node_ReflectionConverter.cs`, `ReflectionArgumentGuard.cs`, plus `Tool_Node.ReflectionResolver.cs`.
The guard is the general fix: `Tool_Reflection.MethodCall` now passes a `Logs` sink **per argument** and
**refuses to invoke** when it records `Error`/`Critical`. The PR states: *"There is no path left that yields a
silent `Nil`."*

> **Consequence for charter §3 Tier-4 check 3 (the pivotal `node-modify` ProcessMaterial call).** drax's L3
> §"MCP-level `isError: false`. Transport `ok`. **Nothing written.**" is the exact defect this PR closes.
> **The check-3 probe should be run against v0.20.1, not 0.19.1** — its failure mode changes from
> *silent no-op* to *either it works or it raises an `ArgumentException` carrying the wire-format help*.
> `{"instanceId": N}` now resolves to a live node via `Godot_Node_ReflectionConverter`. This does **not**
> promise the ProcessMaterial call succeeds — it promises the answer will be legible. **That is a strictly
> better instrument for the single call that decides whether W-MUR has an L7 cell (L-N: clear instrument
> before recording NO).** Re-running check 3 on the old pin would measure a fixed bug.

Also changed in the same PR: `Godot_Resource_ReflectionConverter.ToResourceRef` now marshals its native
reads onto the editor main thread (`MainThread.Instance.Run`) because `reflection-method-call` serializes
results off-thread — a latent crash/garbage path on the Resource side, which is *our* side of check 3.

**(b) `filesystem-reimport` no longer lies about native files.** `EditorFileSystem.ReimportFiles` silently
ignores `.tscn`/`.tres`/`.gd`/`.cs`/`.gdshader` (no `ResourceFormatImporter`), yet the tool answered
*"Reimported 4 file(s); filesystem settled."* Now partitioned on the `<file>.import` sidecar: importable →
`ReimportFiles`, native → `EditorFileSystem.UpdateFile`, and the status string names both groups.
*(Relevant to any Synty `.import`-patch workflow that used this tool to settle.)*

**(c) Tool surface grew 39 → 42 and 11 → 12 families.** Measured directly: `[AiTool` attribute count in
`addons/` is **39 at `v0.19.1`, 42 at `v0.20.1`**. The 12 families are `Tool_Console`, `Tool_Editor`,
`Tool_FileSystem`, `Tool_Node`, `Tool_Ping`, `Tool_Reflection`, `Tool_Resource`, `Tool_RuntimeErrors`,
`Tool_Scene`, `Tool_Screenshot`, `Tool_Script`, **`Tool_Skills`** (new). New/changed tools:
- `node-reorder` (new) — moves a node among its siblings; the "rearrange an existing scene" gap.
- `node-create` gains a trailing optional `index`; `NodeData` now reports `index` so both are self-verifying.
- `godot-skill-create`, `godot-skill-generate` (new, both System).

> **⚠ COUNT TRAP for the Tier-4 assert (charter §3, §6 check 1 + check 2).** `ping` was **moved from
> Standard to System** (`McpToolType.System`, `Tool_Ping.cs:49`). Per README: System tools are
> *"reachable over the server's `/api/system-tools/` HTTP surface, **not advertised to AI agents in
> `tools/list`**."* Three of the 42 are System (`ping`, `godot-skill-create`, `godot-skill-generate`).
> **So `tools/list` returns 39 at v0.20.1 — the same number drax measured at 0.19.1 — while the SET has
> changed** (`ping` left, `node-reorder` joined). A `count == 39` assert passes vacuously.
> **Assert the NAME SET, never the count.** This also moves the baseline under §6 check 2's 58-vs-63
> reconciliation: both of those figures were computed against a 39-tool core.

**(d) The `ping` REST route MOVED — a shipped regression window.** `/api/tools/ping` →
**`/api/system-tools/ping`**. PR #316's refine pass records that three hardcoded callers were missed, all
five `runtime-harness` legs went red, and `cli/src/utils/probe.ts` (`PING_ENDPOINT`) backs `godot-cli
status` and `wait-for-ready` — *"a **shipped** regression, not only a CI one."*
**Any script or runbook step of ours that POSTs `/api/tools/ping` will fail against v0.20.x.**

### 2.3 · Install-procedure change: the consumer `.csproj` pins moved

`Godot-MCP.csproj` diff v0.19.1 → v0.20.1:

```xml
- <PackageReference Include="com.IvanMurzak.ReflectorNet" Version="5.3.2" />
- <PackageReference Include="com.IvanMurzak.McpPlugin"   Version="7.3.0" />
+ <PackageReference Include="com.IvanMurzak.ReflectorNet" Version="5.4.0" />
+ <PackageReference Include="com.IvanMurzak.McpPlugin"   Version="7.5.2" />
```

Because Godot compiles every `.cs` in the project into one assembly, **the consumer project must declare the
same pins** (`CLAUDE.md`: *"keep all three in lockstep; never bump here"*), plus the
`extensions.catalog.json` `<EmbeddedResource>` (unchanged this lap). **Tier 4 must bump the lab project's
pins to 5.4.0 / 7.5.2 or the addon will not compile.** The ten `Godot-AI-*` extensions declare
`com.IvanMurzak.McpPlugin >= 6.10.0`, which 7.5.2 satisfies.

`plugin.cfg` `version="0.19.1"` → `"0.20.1"`; `godot-cli` npm tracks in lockstep (`dist-tags.latest = 0.20.1`).

---

## §3 — Q3: extension auto-discovery + `.claude/skills` self-write (telemetry finding T6)

### 3.1 · Extension auto-discovery — **UNCHANGED**

`git diff --name-only v0.19.1 v0.20.1 -- addons/godot_mcp/Runtime/Extensions/ addons/godot_mcp/Editor/Extensions/`
returns **empty**. The mechanism is as filed: `GodotExtensionRegistry` → `GodotExtensionCatalog.LoadEmbedded()`
→ `GetManifestResourceStream("Godot-MCP.extensions.catalog.json")`, with **no `res://` / disk / cloud
fallback** — an absent embedded resource yields an EMPTY extension list (so a missed `<EmbeddedResource>` in
the consumer csproj presents as "no extensions", not as an error). T2's "extensions are transport-agnostic"
basis for R-PC-6 is untouched.

### 3.2 · `.claude/skills` self-write — **mechanism unchanged, but the surface GREW**

**Unchanged:** boot-time auto-generation still fires and is still **ON by default**.
`GodotMcpConfig.cs:259` → `GenerateSkillFiles = true`; `GodotMcpConnection.cs:511` → `MaybeAutoGenerateSkills(_plugin)`
→ line 897 `plugin.GenerateSkillFilesIfNeeded(skillsDir)`, destination `<project>/.claude/skills`
(`GodotMcpConnection.cs:450`). PR #316 states explicitly: *"**Intentionally untouched:**
`MaybeAutoGenerateSkills` (boot-time auto-generate) still uses `GenerateSkillFilesIfNeeded` — different
semantics (only writes when stale), left as-is."* **T6 stands.**

**CHANGED — three ways the write surface is larger than when T6 was filed:**

1. **A second, agent-callable write path.** `godot-skill-generate` (System tool) regenerates every `SKILL.md`
   on demand, into a caller-supplied project-relative `path` argument (guarded by
   `SkillsToolPaths.RequireSafeRelativeSkillsFolder` — no `res://`, no `..` traversal, must stay inside the
   project). Previously the only writer was boot-time auto-generate. **An agent can now trigger the
   `.claude/skills` write mid-session, at a folder it chooses.**
2. **A source-writing tool.** `godot-skill-create` writes a **new C# file under `res://`** (rejects `.gd`),
   routed through `Tool_Script.WriteScript` — same write + reimport + bounded-settle path as `script-create`.
3. **The write SET must grow**, because the registry it is generated from grew 39 → 42 tools / 11 → 12
   families. T6's measured baseline was **39 `SKILL.md` files**, which equals the 0.19.1 *tool* count —
   consistent with per-tool granularity. **Prediction: 39 → 42.** If granularity is per-family instead, 11 → 12.

**HONEST GAP (do not skip check 8):** the generator itself is `IMcpPlugin.GenerateSkillFilesIfNeeded`, which
lives in `com.IvanMurzak.McpPlugin` — bumped **7.3.0 → 7.5.2** in this window and **not readable from this
repo**. Granularity, filename scheme and content could have changed inside the LIB without appearing in any
addon diff. **The before/after fingerprint of §6 check 8 is therefore MORE necessary this lap, not less.**
Also fingerprint `res://` for the `godot-skill-create` surface, and note that both new tools carry
`Enabled = false`, which per PR #316 *"only affects listing metadata; `McpSystemToolManager.RunSystemTool`
dispatches regardless"* — **they are callable even though they read as disabled.**

---

## §4 — Q4: does 0.20.x change the Godot support matrix? (we pin 4.6.3.stable.official.7d41c59c4)

**NO — and 4.6.3 is an explicit, named CI leg, at both versions.**

`.github/workflows/test_pull_request.yml` at **both** `v0.19.1` and `v0.20.1` runs four Godot suites across
five versions each (20 legs):

```
godotVersion: "4.3.0"  "4.4.0"  "4.5.1"  "4.6.3"  "4.7.0"
```

`grep -c '4.6.3'` = **4 at v0.19.1** and 4 at v0.20.1 (one per suite); same for `4.7.0`. The identical matrix
is mirrored in `release.yml`. Diff of `.github/workflows/` across the bump touches only `release.yml`
(Discord announcement) and `test_godot_runtime_harness.yml` (the `/api/system-tools/ping` route fix, §2.2d) —
**no version was added, removed or changed.**

**Our pin `4.6.3.stable.official.7d41c59c4` is directly covered by the vendor's own CI at v0.20.1.**

**The caveat that does NOT change:** menu §6 check 1's real risk was never the *core addon* — it was the ten
`Godot-AI-*` **extensions**, whose CI matrix stops at **4.5.1**. Nothing in this lap moved that. The
extensions were not re-read here (out of this cell's scope); check 1 stands as written.

Secondary matrix facts, unchanged: the SDK floor is `Godot.NET.Sdk/4.3.0`; the `runtime-errors` capture path
is documented Godot 4.5+ (`Logger._LogMessage`); PR #321 §#293 records that a running game's stdout is
**not reachable** from the editor at any version — `EditorInterface` exposes no PID/handle/pipe.

---

## §5 — Gaps this read did NOT close

- **`com.IvanMurzak.McpPlugin` 7.3.0 → 7.5.2 and `com.IvanMurzak.ReflectorNet` 5.3.2 → 5.4.0 were not
  audited.** They are consumed as NuGet binaries. They carry the entire behaviour delta of server 9.2.0→9.2.4
  (§2.1) **and** the `SKILL.md` generator (§3.2). This is the single largest unread surface of the lap.
- **Nothing here is a measurement of running software.** Every statement is source/release-metadata. The
  packet-quiet assert of R-PC-6 remains mandatory and is not pre-empted by §1.
- **The ten `Godot-AI-*` extensions were not re-read** — this cell's scope was the core addon + server.
  Their `>= 6.10.0` McpPlugin floor is satisfied by 7.5.2, but their own versions may also have moved.
- **`~/Games/mcp-lab/` remains unread** (forbidden ground, carried from the menu).

---

## §6 — Source list (all accessed 2026-07-28)

**Read locally**
- `agentic_orchestration/gandalf/notes/2026-07-28-provision-cal-run-charter.md` (§3, §5, §6 R-PC-6)
- `agentic_orchestration/legolas/notes/2026-07-26-plugin-provisioning-menu.md` (§4 T1/T2/T6/T7, §6 checks 1/2/3/8/10)
- `agentic_orchestration/drax/notes/2026-07-24-tcp-l3-murzak-standup-run-report.md` (§4.1 lines 199–244; the 39-tool and silent-no-op observations)

**GitHub API (`gh`)**
- `repos/IvanMurzak/Godot-MCP/releases`, `/tags`, `/pulls/{316,318,321}`
- `repos/IvanMurzak/GameDev-MCP-Server/releases`
- `search/repositories?q=user:IvanMurzak+MCP` (repo descriptions, incl. the unchanged *"with cloud connection to ai-game.dev"*)

**Registries**
- NuGet search index — `azuresearch-usnc.nuget.org/query?q=packageid:com.IvanMurzak.GameDev.MCP.Server` → `9.2.4`
- npm registry — `registry.npmjs.org/godot-cli` → `dist-tags.latest = 0.20.1`

**Source read directly (cloned read-only to `agentic_orchestration/legolas/scratch/2026-07-28-pcw1b/godot-mcp`; NEVER built, NEVER executed)**
- `addons/godot_mcp/Runtime/Connection/` — `GodotMcpEnvFile.cs`, `GodotMcpConfig.cs`, `GodotMcpConnection.cs`, `GodotMcpServerView.cs`, `GodotProjectIdentity.cs`
- `addons/godot_mcp/Editor/Connection/` — `GodotAccountAuth.cs`, `GodotDeviceAuthService.cs`, `GodotDeviceAuthFlow.cs`, `DevControl/DevControlServer.cs`
- `addons/godot_mcp/Editor/GodotMcpPlugin.cs`, `Runtime/Tools/SkillsToolPaths.cs`, `Runtime/Tools/Tool_Ping.cs`, `Runtime/Reflection/Godot_Resource_ReflectionConverter.cs`
- `.github/workflows/test_pull_request.yml`, `release.yml`, `test_godot_runtime_harness.yml`
- `Godot-MCP.csproj`, `addons/godot_mcp/plugin.cfg`, `README.md`, `CLAUDE.md`, `cli/package.json`
- Diffs: `git diff v0.19.1 v0.20.0`, `v0.20.0 v0.20.1`, `v0.19.1 v0.20.1` (per-file, as cited inline)

---

## §7 — Verdict

**SAFE-TO-PROCEED-AS-CHARTERED on the Q46 ruling** (§1), **with three carried changes** the Tier-4 cell must
absorb: the pin targets moved to **v0.20.1 / 9.2.4** (§0.1), the `tools/list` count is a **vacuous assert**
(§2.2c), and the **consumer csproj pins must be bumped to 5.4.0 / 7.5.2** or the addon will not compile
(§2.3). Plus one improvement in our favour: **check 3 should be run on v0.20.1**, where the silent-success
path it was designed to catch has been closed (§2.2a).

**Signed:** legolas, 2026-07-28. Cell PC-W1-B, relaunch. Read-only throughout.
