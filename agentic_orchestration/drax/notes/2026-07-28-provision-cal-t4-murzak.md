# PROVISION-CAL — cell PC-T4 (Tier 4: Murzak family + Pro probe)

**Run:** PROVISION-CAL · **Conductor:** gandalf (`RUN-CONDUCTOR`) · **Executor:** drax (presentation seam)
**Charter:** `agentic_orchestration/gandalf/notes/2026-07-28-provision-cal-run-charter.md` — §3 Tier 4, §4 laws, §6 R-PC-6, §8 M-T4 amendments 1–4
**Inputs:** provisioning menu §3.1/§3.2/§3.3 (`legolas/notes/2026-07-26-plugin-provisioning-menu.md`); version re-read (`legolas/notes/2026-07-28-provision-cal-w1b-murzak-version-reread.md`)
**Boundary law:** LOADS? / REACHES?, never BETTER.
**Date:** 2026-07-28 · **Status:** COMPLETE — all seven steps executed. Exit summary at the end.

> **LAB PROJECT (M-T4 #4 — clean, outside `reincarnated-godot`):**
> **`/Users/admin/Games/mcp-lab/pct4/`** — created empty 2026-07-28 22:04.
> Godot project root: `/Users/admin/Games/mcp-lab/pct4/project/`
> Nothing was copied in from `reincarnated-godot`. Left intact as evidence.

---

## STEP 1 — Environment prep ✓

### 1.1 · The four local-only env vars, named from current source

Set in `/Users/admin/Games/mcp-lab/pct4/env.sh`. Names taken from legolas PC-W1-B §1.2, which read
them from `GodotMcpConfig.cs` lines 52–76 **at v0.20.1** (not from the L3 runbook):

```bash
export GODOT_MCP_CONNECTION_MODE=Custom
export GODOT_MCP_AUTH_OPTION=None
export GODOT_MCP_HOST=http://localhost:27435
export GODOT_MCP_LOG_LEVEL=Debug
```

All four survive the 0.19.1 → 0.20.1 bump with identical names and identical semantics (null diff
across the whole connection/identity/auth layer). The compiled-in default remains
`GodotMcpConnectionMode.Cloud` with `DefaultCloudBaseUrl = "https://ai-game.dev"` — **these four vars
are the only thing holding self-hosting.**

### 1.2 · `DOTNET_CLI_HOME` redirect (R-PC-6 T7 rider) — set BEFORE any restore, and it held

`export DOTNET_CLI_HOME="$PCT4/dotnet-home"` (plus the base lab's `DOTNET_ROOT` / `NUGET_PACKAGES`
redirects, sourced from `/Users/admin/Games/mcp-lab/env.sh`).

Measured, before and after the restore+build:

| Probe | Before | After |
|---|---|---|
| `find ~/.dotnet \| wc -l` | 5667 | **5667** |
| `find ~/.dotnet -newermt "2026-07-28 22:00" \| wc -l` | 0 | **0** |
| `find ~/.nuget -newermt "2026-07-28 22:00" \| wc -l` | 0 | **0** |
| `$PCT4/dotnet-home/.dotnet/sdk-advertising/` | absent | **present** (`.workloadAdvertisingUpdates8.0.400`, `8.0.423.toolpath.sentinel`, …) |

**The L3 §7 escape is closed.** The workload-advertising metadata that leaked to `$HOME` last lap
landed inside the lab this lap. Zero filesystem entries under `~/.dotnet` or `~/.nuget` carry a
mtime from this cell.

### 1.3 · Install targets, exactly as pinned (M-T4 #1 + #3)

| Component | Pin | Provenance |
|---|---|---|
| core addon `godot_mcp` | **v0.20.1** | `godot-mcp-addon-0.20.1.zip`, 898 589 B, GH release `v0.20.1`; unpacked `plugin.cfg` reads `version="0.20.1"` |
| server | **9.2.4** | `gamedev-mcp-server-osx-arm64.zip`, 41 864 909 B; **SHA-256 verified against the release `SHA256SUMS`** → `1556c479cc3c841fcf352522b515eb57ccfa97c7ed8a2a3f55d22449213da3ce` (match) |
| `com.IvanMurzak.ReflectorNet` | **5.4.0** | consumer csproj pin (M-T4 #3) |
| `com.IvanMurzak.McpPlugin` | **7.5.2** | consumer csproj pin (M-T4 #3) |
| Godot | `4.6.3.stable.mono.official.7d41c59c4` | lab `godot-net` |
| .NET SDK | `8.0.423` | lab-local `DOTNET_ROOT` |

### 1.4 · `dotnet build` — SUCCEEDED on the bumped pins

```
Restored /Users/admin/Games/mcp-lab/pct4/project/pct4_lab.csproj (in 1.04 sec).
pct4_lab -> .../.godot/mono/temp/bin/Debug/pct4_lab.dll
Build succeeded.  3 Warning(s)  0 Error(s)   Time Elapsed 00:00:03.29
```

The 3 warnings are all `CS0618` deprecations inside the vendor addon
(`EditorPlugin.AddControlToDock` / `RemoveControlFromDocks` → `AddDock`/`RemoveDock` at Godot 4.6) —
**vendor-side, not ours, and not errors.** Recorded, not smoothed.

**M-T4 #3 verified by construction:** the build was run against 5.4.0/7.5.2. It was not attempted on
the stale 5.3.2/7.3.0 pins, so this cell does not independently confirm the "won't compile" claim —
it confirms the prescribed pins are sufficient.

---

## STEP 2 — PACKET-QUIET ASSERT ✓ **PASS**

### 2.1 · Scope, restated before the measurement (R-PC-6 + PC-W1-B §1.6)

The assert is **"nothing leaves the host."** It is **not** "the identity fields are never serialized."
Legolas's source read established that `GodotProjectIdentity.BuildInstanceMetadata` runs
unconditionally at `Start()` regardless of mode; mode controls only the URL the metadata is appended
to. This cell measured exactly that distinction and it is the correct one — see §2.4.

### 2.2 · Instrument, and its validation BEFORE any NO was recordable (L-N)

`tcpdump` is unavailable to this seam: `/dev/bpf0` is `crw------- root:wheel` and
`tcpdump -i en1 -c 1 -w /dev/null` returns *"You don't have permission to capture on that device
((cannot open BPF device) /dev/bpf0: Permission denied)"*. **No root was taken.** The instrument is
therefore socket-table based:

**`/Users/admin/Games/mcp-lab/pct4/bin/netwatch.py`** — polls `lsof -nP -i -a -p <pids>` at 5 Hz,
**re-expanding the PID set to all live descendants on every poll**, and records every distinct
`(cmd, pid, proto, local, remote, state)` tuple with first-seen / last-seen / hit count. Each remote
endpoint is classified LOOPBACK (`127.*`, `::1`, `*`, unbound) or EXTERNAL. Verdict is
`EGRESS-DETECTED` if any EXTERNAL tuple was ever observed, `PACKET-QUIET` otherwise.

**Positive control (L-N — clear the instrument before recording a NO).** Same instrument, same
invocation, watching a shell that curled `https://example.com` eight times:

```
{"polls": 34, "distinct_sockets": 4, "external_socket_count": 4, "verdict": "EGRESS-DETECTED"}
EXTERNAL: curl 64287 TCP [2600:1700:...]:49282 -> [2606:4700:10::6814:179a]:443 (ESTABLISHED)
EXTERNAL: curl 64307 TCP [2600:1700:...]:49284 -> [2606:4700:10::6814:179a]:443 (SYN_SENT)
EXTERNAL: curl 64318 TCP [2600:1700:...]:49285 -> [2606:4700:10::6814:179a]:443 (ESTABLISHED)
EXTERNAL: curl 64348 TCP [2600:1700:...]:49288 -> [2606:4700:10::6814:179a]:443 (ESTABLISHED)
```

Two properties this control proves, both load-bearing: (a) the instrument sees egress from
**descendant** processes it was not directly given; (b) it catches a **`SYN_SENT`** — an outbound
*connection attempt* that never completed. The charter's scope word is "outbound-connection-attempts",
and the instrument is demonstrated to catch attempts, not merely established sessions.
Evidence: `/Users/admin/Games/mcp-lab/pct4/evidence/CONTROL_netwatch_positive.json`.

**Honest limit, stated rather than smoothed:** at 5 Hz this instrument could in principle miss a
connection whose entire lifetime (DNS + connect + teardown) fell between two polls. It is mitigated
but not eliminated by (i) the control's SYN_SENT capture, (ii) 390 polls over 90 s, and (iii) the
L3-measured behaviour that a Cloud-mode failure **retries indefinitely** rather than giving up — a
leak of this class is persistent, not a blip. A root-capable `tcpdump`/`pktap` run would close the
residue; it was not available and was not forced.

### 2.3 · The measurement

Server 9.2.4 started first (`MCP_PLUGIN_PORT=27435`; its own log: *"Start listening on port: 27435
**(bind: loopback)**"*, *"MCP auth mode: none (transport: streamableHttp, bind: loopback)"*). Editor
launched headless with the four env vars set, watch started in the same command line.

```
{"polls": 390, "distinct_sockets": 9, "external_socket_count": 0, "verdict": "PACKET-QUIET"}
```

Every socket the Murzak stack opened in 90 s, verbatim:

| first→last (s) | hits | process | socket |
|---|---|---|---|
| 0.017 → 90.017 | 390 | `gamedev-m` 64449 | `127.0.0.1:27435 (LISTEN)` |
| 0.017 → 90.017 | 390 | `gamedev-m` 64449 | `[::1]:27435 (LISTEN)` |
| 2.026 → 90.017 | 381 | `Godot` 64477 | `127.0.0.1:6006 (LISTEN)` |
| 2.253 → 90.017 | 380 | `Godot` 64477 | `127.0.0.1:49293 (LISTEN)` |
| 3.848 → 90.017 | 373 | `Godot` 64477 | `127.0.0.1:6005 (LISTEN)` |
| 4.529 → 79.503 | 325 | `Godot` 64477 | `[::1]:49295 -> [::1]:27435 (ESTABLISHED)` |
| 4.750 → 79.503 | 324 | `gamedev-m` 64449 | `[::1]:27435 -> [::1]:49295 (ESTABLISHED)` |
| 4.750 → 90.017 | 369 | `gamedev-m` 64449 | `[::1]:27435 -> [::1]:49296 (ESTABLISHED)` |
| 4.750 → 90.017 | 369 | `Godot` 64477 | `[::1]:49296 -> [::1]:27435 (ESTABLISHED)` |

**Nine sockets. Zero external. Every remote endpoint is `::1`.** The two `6005`/`6006` listeners are
Godot's own debugger/LSP ports, bound to `127.0.0.1`.

Raw: `/Users/admin/Games/mcp-lab/pct4/evidence/PACKETQUIET_boot1.json`

### 2.4 · Corroboration from the addon's own `Debug`-level log

`/Users/admin/Games/mcp-lab/pct4/logs/editor-boot1.log`:

```
[Godot-MCP] plugin loaded
[Godot-MCP] local server default port -> ProjectIdentity-derived host http://localhost:23212.
[Godot-MCP] project identity: pin=bc73558b derivedPort=23212 (portOverridden=False); enrolled serverTarget=<none>.
[Godot-MCP] connecting (mode=Custom, host=http://localhost:27435) ...
[McpPlugin] HubConnection: Starting transport. Transfer mode: Text. Url:
  'ws://localhost:27435/hub/mcp-server?instance_id=cd30207e-…&engine=godot&project_name=pct4_lab
   &project_path_hash=bc73558b32cc…&project_path_hash_legacy=bc73558b32cc…
   &machine_name=Matthews-Mac-mini&id=TDA_7MuHrOERVl36cSim_w'
[Godot-MCP] connected.
```

- **Every `ws(s)://` literal in the whole boot log** (`grep -oE 'wss?://…' | sort | uniq -c`):
  **one** — `ws://localhost:27435/hub/mcp-server`. No `wss://`, no remote host, anywhere.
- **`ai-game.dev` occurrences in the editor log: 0.** (The single grep hit in `server.log` is a false
  positive — my pattern's `.` matched the hyphen in the install path `.ai-game-dev/server/osx-arm64`.
  Recorded because a silent false positive is how a bad NO gets filed.)
- **The identity fields DID go on the wire — to loopback**, exactly as PC-W1-B §1.6 predicted:
  `machine_name=Matthews-Mac-mini`, `project_name`, `project_path_hash`, `instance_id`. The scoping
  ruling is what makes this a PASS instead of a FAIL, and it is the correct scoping: the metadata is
  built unconditionally, and Custom mode sent it to `localhost`.

**★ One fact correction to PC-W1-B §1.6, on this cell's own evidence.** Legolas read
`GodotProjectIdentity.cs:100–123` as *"the released pin sends only `project_path_hash`"* and called
the legacy twin transition insurance. **At v0.20.1 on the wire, `project_path_hash_legacy` IS sent**
(here identical in value to `project_path_hash`). It changes nothing about the ruling — both go to
loopback — but the source read was one field short of the observed handshake. **Six identity fields
observed, not five** (`instance_id`, `engine`, `project_name`, `project_path_hash`,
`project_path_hash_legacy`, `machine_name`).

### 2.5 · Verdict

> ## **PACKET-QUIET — PASS.** Zero outbound connection attempts left the host across a 90-second
> instrumented boot of core addon v0.20.1 + server 9.2.4 under the four R-PC-6 env vars.
> The Murzak chain is **NOT** blocked. Steps 3–7 proceed under this gate.

*(Had this failed, the standing instruction was: stop the chain, verdict the family
`BLOCKED(telemetry-not-silenced)`, reopen the fork to Matt. It did not fail.)*

---

## STEP 3 — Core load + `tools/list` NAME SET ✓

### 3.1 · The addon-load line, asserted (§6 check 1)

**`[Godot-MCP] plugin loaded`** — present, **verbatim in the charter's original form** at v0.20.1.
No rename occurred across the version bump; the check-1 assertion string is still literal.
Followed 4.5 s later by `[Godot-MCP] connected.` Headless, zero tool loss (as L3 §4.2 measured).

### 3.2 · `tools/list` — the NAME SET (M-T4 #2; the count is recorded only to demonstrate the trap)

`serverInfo: {"name":"gamedev-mcp-server","version":"9.2.4.0"}`, protocol `2025-06-18`.

**39 names** — and **39 is exactly what L3 measured at 0.19.1, while the SET has changed.** A count
assert would have passed vacuously. Full set:

```
console-clear-logs            node-modify                   scene-create
console-get-logs              node-reorder  ← NEW at 0.20.x scene-get-data
editor-application-get-state  node-set-parent               scene-list-opened
editor-application-set-state  reflection-method-call        scene-open
editor-selection-get          reflection-method-find        scene-save
editor-selection-set          resource-create               screenshot-camera
filesystem-list               resource-delete               screenshot-isolated
filesystem-reimport           resource-find                 screenshot-viewport
node-create                   resource-get-data             script-attach-to-node
node-delete                   resource-modify               script-create
node-duplicate                resource-move                 script-delete
node-find                     runtime-errors-clear          script-read
                              runtime-errors-get            script-update
                                                            script-validate
```

Machine-readable: `/Users/admin/Games/mcp-lab/pct4/evidence/CORE_tools_NAMESET.txt`,
`/Users/admin/Games/mcp-lab/pct4/evidence/CORE_tools_list_v0.20.1.json`.

### 3.3 · The three hidden System tools, identified independently (not assumed)

The addon wrote 42 `SKILL.md` directories at boot. Set-differenced against `tools/list`:

```
in .claude/skills but NOT in tools/list  ->  ['godot-skill-create', 'godot-skill-generate', 'ping']
in tools/list but NOT in .claude/skills  ->  []
```

**Exactly the three `McpToolType.System` tools legolas named, identified from the wire + the
filesystem rather than taken on the source read's word.** The real surface at v0.20.1 is
**42 tools, 39 advertised.**

### 3.4 · The `ping` endpoint regression, reproduced (M-T4 #3 — NOT our failure)

```
POST /api/tools/ping         -> 404  {"error":"Tool with Name 'ping' not found."}
POST /api/system-tools/ping  -> 200  {"status":"success","structured":{"result":"pct4"}}
```

Shipped upstream regression, reproduced exactly as documented. **Any of our runbooks or scripts
still POSTing `/api/tools/ping` will 404 against 0.20.x** — including
`~/Games/mcp-lab/bin/editor_up.sh`, whose readiness poll goes through the MCP `tools/call` path
rather than the REST route and is therefore unaffected, but the L3 §8 procedure text should be read
with this in mind.

---

## STEP 4 — All ten `Godot-AI-*` extensions ✓ **LOADS-CLEAN, all ten**

### 4.1 · Pin re-verified before install (L-C)

All ten NuGet ids re-queried against the search index 2026-07-28: **every one still `0.1.0`.** The
menu's pin holds; nothing moved under us this time.

Installed by declaring ten `<PackageReference>` entries in the consumer csproj (source-only NuGet —
the `.cs` are injected as `<Compile>` items by each package's auto-imported `build/*.props` and
compile inside `pct4_lab.dll`).

### 4.2 · Rebuild

```
Restored pct4_lab.csproj (in 2.01 sec).
pct4_lab -> .../.godot/mono/temp/bin/Debug/pct4_lab.dll
Build succeeded.  3 Warning(s)  0 Error(s)   Time Elapsed 00:00:03.60
```

**Zero new warnings.** The 3 are the same vendor `CS0618`s from step 1. Ten packages, one rebuild,
no conflict, no additional dependency resolution.

### 4.3 · ★ THE 4.6 COMPAT RISK DOES NOT FIRE

The menu's headline extension risk was that **no `Godot-AI-*` CI leg tests past 4.5.1** while our
stack is 4.6.3. **Measured: all ten compile and all ten register their tools on
`4.6.3.stable.mono.official.7d41c59c4`.** The risk was real and named; it did not materialise.
Recorded as a measurement, not as reassurance.

### 4.4 · Second packet-quiet assert, post-extension

```
{"polls": 184, "distinct_sockets": 9, "external_socket_count": 0, "verdict": "PACKET-QUIET"}
```

Identical 9-socket loopback shape. **Installing ten extensions added no egress** — which is what
the menu's source audit predicted (zero `http(s)://` / `HttpClient` / `WebSocket` in any `src/`) and
is now measured rather than reasoned. Evidence: `evidence/PACKETQUIET_boot2_tenext.json`.

### 4.5 · ★★ CHECK 2 SETTLED ON THE WIRE — **63, not 58**

`tools/list` went **39 → 102**. **Delta = exactly 63. Zero core tools removed.**

> **The lab's `extension_catalog_summary.txt` (63) was right; the READMEs (58) were wrong.**
> Settled where the charter said it should be — on the wire, not on paper (L-B).

Live name set by family, with the README's claimed count for comparison:

| Family | README | **LIVE** | Δ | Live tool names |
|---|---|---|---|---|
| `animation-` | 7 | **7** | — | `-add-track` `-create` `-defaults` `-get` `-insert-key` `-library-add` `-player-create` |
| `beehave-` | 5 | **6** | **+1** | `-add-composite` `-add-decorator` **←new** `-add-leaf` `-defaults` `-get` `-tree-create` |
| `csg-` | 6 | **7** | **+1** | `-box-create` `-combiner-create` `-cylinder-create` `-defaults` **←new** `-get` `-set-operation` `-sphere-create` |
| `dialogic-` | 5 | **5** | — | `-character-create` `-defaults` `-get` `-timeline-add-text` `-timeline-create` |
| `gridmap-` | 7 | **7** | — | `-clear` `-clear-cell` `-create` `-defaults` `-get` `-set-cell` `-set-mesh-library` |
| `navigation-` | 6 | **7** | **+1** | `-agent-configure` `-agent-create` `-defaults` **←new** `-get` `-link-create` `-region-create` `-region-set-mesh` |
| `particles-` | 5 | **5** | — | `-configure` `-create` `-defaults` `-get` `-set-emitting` |
| `phantomcamera-` | 7 | **7** | — | `-create` `-defaults` `-get` `-host-create` `-set-follow` `-set-look-at` `-set-priority` |
| `terrain3d-` | 4 | **6** | **+2** | `-create` `-defaults` `-get` `-set-data-directory` `-set-material` `-set-region-size` |
| `tilemap-` | 6 | **6** | — | `-clear` `-create` `-erase-cell` `-get-used-cells` `-set-cell` `-set-tileset` |
| **TOTAL** | **58** | **63** | **+5** | |

**The +5 is fully accounted for:** Beehave +1, CSG +1, Navigation +1, Terrain3D +2. Four families
also carry **name drift** the READMEs got wrong (`beehave-create-tree` → `beehave-tree-create`;
`dialogic-add-event` → `dialogic-timeline-add-text`; `dialogic-get-timeline` → `dialogic-get`;
Terrain3D's `-set-height` and `-get-info` **do not exist**, replaced by `-get`,
`-set-data-directory`, `-set-material`, `-set-region-size`). **A plan written from the READMEs would
have called three tools that are not there.**

**Whole-surface total at v0.20.1 + all ten:** 102 advertised + 3 System = **105 tools.**
Machine-readable: `evidence/TENEXT_tools_NAMESET.txt`, `evidence/TENEXT_tools_list.json`.

**L7 relevance, restated not re-litigated:** the menu §3.2 finding stands unchanged — `particles-`
is 5 tools whose entire parameter surface is `dimension name parentPath amount lifetime oneShot
explosiveness randomness speedScale preprocess localCoords`. **None of the 63 reaches
`ParticleProcessMaterial`.** That is what makes step 5 the deciding call.

---

## STEP 5 — ★★★ THE DECIDING CALL (check 3) ✓ **YES — REACHES**

### 5.1 · The schema moved; the charter's shape is now the `jsonPatch` argument

At v0.20.1 `node-modify` no longer takes a flat property object. Its two surfaces are
`pathPatches` (list of `{path, value:SerializedMember}`) and **`jsonPatch`** — an RFC 7396 JSON
Merge Patch **string**. The charter's shape goes in verbatim as that string. Recorded because a plan
written to L3's schema will fail against 0.20.x.

### 5.2 · The chain, all on the wire

| # | Call | Result |
|---|---|---|
| 1 | `resource-create {"resourcePath":"res://pp_pct4.tres","typeClassName":"ParticleProcessMaterial"}` | `uid://dr0s3io70otj8` created |
| 2 | `scene-create {"resourcePath":"res://pct4_check3.tscn","rootTypeClassName":"Node3D","rootName":"Root"}` | root instanceId `1631483661773` |
| 3 | **`particles-create`** (the extension) `{"dimension":"3D","name":"PCT4Particles","amount":64,"lifetime":1.5}` | `TypeName: "GPUParticles3D"` |
| 4 | `node-find {"nodeRef":{"instanceId":0,"path":"Root/PCT4Particles"}}` | instanceId `1639754829289`, type `GPUParticles3D` |
| 5 | **THE CALL** — `node-modify {"nodeRef":{"instanceId":1639754829289},"jsonPatch":"{\"ProcessMaterial\":{\"instanceId\":0,\"resourcePath\":\"res://pp_pct4.tres\"}}"}` | see below |
| 6 | `scene-save {}` | `isError:false` |

**The wire's own answer to call 5** (read via `result[].Type`, not `isError` — L3 §4.5 discipline):

```json
[{"Depth":2,"Message":"Resolved Resource resourcePath='res://pp_pct4.tres' to a live 'Material'.","Type":"Success"},
 {"Depth":1,"Message":"Object 'null' modified with type 'Godot.Material'.","Type":"Success"}]
```

80.5 ms. *(The `"Object 'null'"` phrasing is a cosmetic defect in the reflection layer's logging —
it is not an indication of failure, as the disk read proves. Named so nobody misreads it later.)*

### 5.3 · **INDEPENDENT DISK READ — the instrument that decides**

`cat /Users/admin/Games/mcp-lab/pct4/project/pct4_check3.tscn`, verbatim, no tool in the loop:

```
[gd_scene format=3 uid="uid://cn3ink30vise"]

[ext_resource type="Material" uid="uid://dr0s3io70otj8" path="res://pp_pct4.tres" id="1_3naxe"]

[node name="Root" type="Node3D" unique_id=1500185249]

[node name="PCT4Particles" type="GPUParticles3D" parent="." unique_id=1429434368]
amount = 64
lifetime = 1.5
process_material = ExtResource("1_3naxe")
```

> ## **CHECK 3 = YES.** `node-modify` with the ResourceRef shape **reaches
> `GPUParticles3D.process_material` and the assignment persists to disk.** The silent-success class
> that bit L3 did not recur on this call. **W-MUR has an L7 cell worth running.**

Minor recorded fact: the `ext_resource` header widens the type to `type="Material"` rather than
`ParticleProcessMaterial` (matching the wire's *"resolved … to a live 'Material'"*). Godot accepts
and re-loads it; noted, not treated as a defect.

Raw: `evidence/CHECK3_node-modify_raw.json`.

### 5.4 · ★ RIDER (in scope, because the answer above is worthless without it): can the wire
### AUTHOR the material it just attached?

Attaching an empty `ParticleProcessMaterial` reaches nothing visually. So one extra probe:
`resource-modify` on `res://pp_pct4.tres`.

**It reaches.** A `pathPatches` call and a `jsonPatch` call, each single-property on a fresh
resource, both wrote to disk and both emitted `Depth 0 · "Resource '…' modified and saved."`
A seven-property `jsonPatch` landed `emission_shape=1`, `emission_sphere_radius=0.38`,
`spread=20.0`, `gravity=Vector3(0, 0.5, 0)`, `scale_min=1.7`, `scale_max=3.5`,
`color=Color(1, 0.55, 0.15, 1)` — **these are exactly the L7-V hand-authored parameter class.**
**The `ParticleProcessMaterial` surface is reachable from the wire via `resource-modify`, not via
the `particles-` extension.** The menu §3.2 consequence is confirmed AND the fallback it named is
confirmed to work.

**★ And one hazard found while confirming it — a surviving partial-write class, named precisely:**

`resource-modify` is **all-or-nothing on disk, and its in-memory mutation is not rolled back.**
One-variable proof on a virgin resource, `jsonPatch = {"Spread":33.0,"Damping":1.0}` (my `Damping`
scalar is wrong — Godot 4.6 exposes it as a `Vector2`; **my input error, not the tool's**):

```
Success | Set value  was: value='45'  new: value='33'.
Success | Value '33' modified to 33.0
Error   | Value '(0, 0)' modification failed: The JSON value could not be converted to Godot.Vector2
Warning | No modifications were made; the resource was not re-saved.
```
disk after: `[resource]` — **empty. `spread` was NOT written.**

Three things to carry forward:
1. **It is NOT silent** — PR #321's guard is working: an `Error` entry and an explicit `Warning`
   naming the non-save. **L-N is satisfied by the instrument itself.**
2. **The `Warning` text is factually wrong.** *"No modifications were made"* contradicts the two
   `Success` lines above it. A modification **was** made — in memory.
3. **★ The real hazard:** because the in-memory mutation survives, **a later, unrelated successful
   `resource-modify` flushes the values you were told were not saved.** I hit this live: the
   seven-property patch reported no save, then a subsequent one-property `pathPatches` call wrote
   **all eight properties** to disk. Any plan that batches property patches must treat a
   `Warning: … not re-saved` as *dirty state pending*, not as *nothing happened*.

Raw: `evidence/CHECK3_rider_partial_patch.json`.

---

## STEP 6 — `.claude/skills` write-set fingerprint (check 8) ✓

| Stage | Files | Skill dirs | Manifest md5 | Evidence |
|---|---|---|---|---|
| **before core install** | **0 — the tree does not exist** | 0 | — | project authored by hand contained only `project.godot`, `pct4_lab.csproj`, `addons/godot_mcp/**`, `.ai-game-dev/**`. `stat` shows `.claude` and `.claude/skills` **both created `Jul 28 22:08:47`** — the timestamp of the first editor boot, by `MaybeAutoGenerateSkills`, unasked. |
| **after core (v0.20.1)** | **42** | 42 | `b798950d801c5a0341d30eb6318b6c30` | boot log: *"auto-generate skills: ensured up-to-date skills in …/project/.claude/skills"* |
| **after all ten** | **105** | 105 | `220425fba6e8a8602a1a1ce06ef6d820` | `evidence/SKILLS_after_ten.txt` |

**Write-set growth: 0 → 42 → 105 (+42, then +63). 708 KB.**

- **Granularity is per-tool, one `SKILL.md` per directory, confirmed at both sizes** (105 files /
  105 `SKILL.md` / 105 dirs). Legolas's prediction of 39 → 42 was right on the count and right on
  the mechanism; the **unread `McpPlugin` 7.3.0 → 7.5.2 generator did not change granularity or
  filename scheme.** That gap is now closed by measurement.
- The write-set tracks the **full** tool surface including the three hidden System tools — which is
  how §3.3 identified them.
- **22 skill families written**, including all ten extension families
  (`animation beehave csg dialogic gridmap navigation particles phantomcamera terrain3d tilemap`)
  alongside the twelve core ones.
- **T6 stands and is larger than filed:** the addon writes 105 files into a `.claude/` directory of
  a project that never asked for it, at boot, on by default (`GenerateSkillFiles = true`). **In
  `reincarnated-godot` this would collide with our own `.claude/` tree.** Recorded as a fact of the
  instrument; disposition is the conductor's.

---

## STEP 7 — Pro probe (check 4) ✓ — **RENDERS CAPTURED; JUDGEMENT IS MATT'S**

> **This step is a Matt-eye checkpoint (charter §7). I do not verdict the images.** What follows is
> the call transcript, the structural facts, and the capture paths. Nothing below is an aesthetic claim.

### 7.1 · Same lab project — and the swap that made it possible

**godot-mcp-pro 1.15.1 occupies the SAME addon directory as Murzak: `res://addons/godot_mcp/`,
hardcoded in 68 places across its GDScript.** They cannot coexist. So, in the same project:

1. Murzak addon → `/Users/admin/Games/mcp-lab/pct4/parked/murzak_godot_mcp` (moved **outside** the
   project so `Godot.NET.Sdk`'s `**/*.cs` glob would not still compile it), csproj preserved verbatim
   at `parked/pct4_lab.csproj.murzak`.
2. Pro addon copied in from `/Users/admin/Games/vendor/godot-mcp-pro/addons/godot_mcp` (`plugin.cfg`
   `version="1.15.1"`; server `package.json` `"version": "1.15.1"` — **both halves agree**).
3. csproj reduced to a bare `Godot.NET.Sdk` shell; `dotnet build` → **0 Warning(s) 0 Error(s)**.
4. **Restored afterward.** The lab now stands in its Murzak configuration (rebuilt, 0 errors) with
   the Pro addon parked at `parked/pro_godot_mcp`. Both are on disk; neither was deleted.

Editor boot log: `[MCP] Godot MCP Pro v1.15.1 started (ports 6505-6514)` · `[MCP] Registered 174
commands`. `tools/list` over stdio: **175** (the addon registers 174 command handlers; the server
advertises 175 tools). **The manifest, the `plugin.cfg` description and the wire all agree at 175** —
matching L3's measurement and the menu §3.3 note. Evidence: `evidence/PRO_tools_list.json`.

Pro's addon is the WebSocket **client** (dials `127.0.0.1:6505..6514` on a 3 s retry); handshake
landed in 1.0 s / 2 probes on the first plan and 2.1 s / 3 probes on the second.

### 7.2 · Call transcript — 11 calls, 11 OK, 0 failed

| Plan | seq | tool | args | ms | ok |
|---|---|---|---|---|---|
| 1 | 1 | `open_scene` | `{"path":"res://pct4_pro.tscn"}` | 98.4 | ✓ |
| 1 | 2 | `get_scene_tree` | `{}` | 97.4 | ✓ |
| 1 | 3 | **`apply_particle_preset`** | `{"node_path":"FX","preset":"fire"}` | **126.6** | ✓ |
| 1 | 4 | `get_particle_info` | `{"node_path":"FX"}` | 471.7 | ✓ |
| 1 | 5 | `save_scene` | `{"path":"res://pct4_pro_fire.tscn"}` | 34.4 | ✓ |
| 2 | 1–3 | `open_scene` → **`apply_particle_preset` smoke** → `save_scene` | — | 75–126 | ✓ |
| 2 | 4–6 | `open_scene` → **`apply_particle_preset` sparks** → `save_scene` | — | 75–126 | ✓ |

Wire ledger: plan 1 — 5 calls, **5 ok / 0 failed**, median 98.4 ms; plan 2 — 6 calls, **6 ok / 0
failed**, median 106.5 ms. Raw: `wire/pro_presets.jsonl`, `wire/pro_presets2.jsonl`.

Target scene authored by hand on disk (`res://pct4_pro.tscn`): `Node3D "Root"` → `GPUParticles3D "FX"`,
nothing else, so the preset is the only variable.

### 7.3 · What the presets wrote — verified by independent disk read of each saved `.tscn`

**`fire`** — `amount=24 lifetime=1.2`; `ParticleProcessMaterial` with `direction=(0,1,0) spread=15
initial_velocity 1.5–3.0 gravity=(0,0,0) scale 0.8–1.5` **+ a 4-stop `Gradient` → `GradientTexture1D`
→ `color_ramp`**.
**`smoke`** — `amount=16 lifetime=3.0`; `spread=25 initial_velocity 0.5–1.2 damping 1.0–2.0 scale
1.5–3.0` + 3-stop grey ramp fading to alpha 0.
**`sparks`** — `amount=48 lifetime=0.4 one_shot=true explosiveness=0.95 emitting=false`; `spread=180
initial_velocity 8–16 gravity=(0,9.8,0) damping 1.0–3.0 scale 0.1–0.3` + 3-stop white→amber→red ramp.

**REACHES — measured, not documented.** `apply_particle_preset` builds and assigns a whole
`ParticleProcessMaterial` *plus* a `Gradient`/`GradientTexture1D` colour ramp in **one call**. That is
the parameter class the menu §3.2 said Murzak's `particles-` extension cannot touch, and the menu's
"documented, not measured" caveat on Pro is now discharged in Pro's favour.

### 7.4 · ★ A structural fact both instruments share, found while rendering — **NEITHER WIRE SETS A DRAW PASS**

`grep -rn "draw_pass" ~/Games/vendor/godot-mcp-pro/addons/` → **zero hits.** Murzak's
`particles-create` likewise never sets one (menu §3.2's parameter list has no mesh/draw-pass entry,
and step 5's `.tscn` confirms it). **A `GPUParticles3D` with `draw_pass_1 == null` draws nothing.**

Measured, not argued — three renders of the three presets **exactly as Pro emitted them**:

```
8acc07e307569eeddd564fc91767006e  7300  pro_fire_asemitted.png
8acc07e307569eeddd564fc91767006e  7300  pro_smoke_asemitted.png
8acc07e307569eeddd564fc91767006e  7300  pro_sparks_asemitted.png
```

**All three byte-identical — to each other and to an empty stage.** Every rig log line reads
`draw_pass_1=null`.

So each preset was rendered **twice**, and the two modes are labelled in the filename so nothing is
conflated:

- **`_asemitted`** — the scene exactly as Pro wrote it. Nothing added. *This is what the tool produces.*
- **`_rigquad`** — identical scene, except **my rig** assigns `draw_pass_1` a neutral 0.5 m `QuadMesh`
  with an unshaded, vertex-colour, particle-billboard `StandardMaterial3D`. **The rig supplies this,
  not Pro.** *This is what the preset's authored parameters look like once something is drawn.*

### 7.5 · Render conditions (fixed, not chosen per-image)

Fixed ARPG camera **R-6 — dist 34, fov 24, yaw 47, pitch −50, aim_h 1.0**; ground plane per R-10;
1280×720, Metal, windowed (headless `SubViewport` capture returns null on 4.6.3/M2); 150 settle
frames; glow ON at threshold 1.25 (L7-V: glow innocent), **SDFGI OFF** (L7-V: SDFGI is the
accumulator). Rig: `/Users/admin/Games/mcp-lab/pct4/project/pct4_shoot.gd` + `.tscn`.

**One rig correction made and disclosed:** the `sparks` preset ships `one_shot=true emitting=false
lifetime=0.4`. At 150 settle frames (~2.5 s) the burst is long expired — the first `sparks_rigquad`
came back byte-identical to the empty stage. The rig now **re-fires one-shot emitters 9 frames before
capture** so the frame records the preset rather than an expired emitter. Continuous emitters are
untouched. *Pressing play is not authoring; it is disclosed anyway.*

### 7.6 · ★ CAPTURE PATHS — the Matt-eye checkpoint

All under **`/Users/admin/Games/mcp-lab/pct4/renders/`**:

| File | md5 | bytes |
|---|---|---|
| `pro_fire_asemitted.png` | `8acc07e3…` | 7300 |
| **`pro_fire_rigquad.png`** | `d5080413…` | 7743 |
| `pro_smoke_asemitted.png` | `8acc07e3…` | 7300 |
| **`pro_smoke_rigquad.png`** | `207ed56a…` | 7547 |
| `pro_sparks_asemitted.png` | `8acc07e3…` | 7300 |
| **`pro_sparks_rigquad.png`** | `913aeff1…` | 7829 |

The three `_rigquad` frames are pairwise distinct; the three `_asemitted` frames are pairwise
identical. **I confirmed the capture path is valid (a frame with content, correct dimensions, correct
camera) and I am not offering an opinion on the images. They are Matt's to look at.**

---

## EXIT SUMMARY

| Step | Verdict |
|---|---|
| 1 · Environment prep | ✓ four env vars from current source; `DOTNET_CLI_HOME` redirect **held** (0 new entries in `~/.dotnet` / `~/.nuget`); build clean on 5.4.0 / 7.5.2 |
| 2 · **PACKET-QUIET ASSERT** | ✓ **PASS — zero external sockets, 390 polls / 90 s.** Instrument validated against a positive control first (L-N). **The Murzak chain is NOT blocked.** |
| 3 · Core load | ✓ `[Godot-MCP] plugin loaded` verbatim; `tools/list` = **39 names** (set changed, count did not — M-T4 #2 vindicated); 3 System tools identified independently; `/api/tools/ping` → `/api/system-tools/ping` regression reproduced |
| 4 · All ten extensions | ✓ **10/10 LOADS-CLEAN on Godot 4.6.3** — the named "no 4.6 CI leg" risk did not fire. **Check 2 settled: 63, not 58.** 39 → 102 advertised (105 total). Four families carry README name drift. Second packet-quiet assert passed. |
| 5 · **THE DECIDING CALL** | ✓ **CHECK 3 = YES.** `process_material = ExtResource("1_3naxe")` on disk. **W-MUR has an L7 cell worth running.** Rider: `resource-modify` reaches the `ParticleProcessMaterial` surface too; one partial-write hazard named. |
| 6 · Skills fingerprint | ✓ **0 → 42 → 105** files, per-tool granularity, 708 KB, unasked, on by default |
| 7 · Pro probe | ✓ 11/11 calls OK; `apply_particle_preset` writes a full `ParticleProcessMaterial` + colour ramp in one call; **6 PNGs captured at R-6.** Judgement withheld — Matt's. |

### Findings for the conductor (logged, not acted on)

1. **★ `project_path_hash_legacy` IS on the wire at v0.20.1** — PC-W1-B §1.6 read the source as
   sending only `project_path_hash`. Six identity fields observed, not five. Ruling unaffected (all
   loopback); the source read was one field short of the handshake.
2. **★ Check 2's 58 was the READMEs' error, and it is worse than a miscount.** Three tools named in
   the READMEs **do not exist** (`terrain3d-set-height`, `terrain3d-get-info`, `beehave-create-tree`),
   and two more are renamed. A plan authored from documentation would have called them.
3. **★ `resource-modify` is all-or-nothing on disk but NOT on the in-memory object.** One bad key in a
   multi-property patch forfeits the save of every good key — announced by an explicit `Warning`
   (so: legible, not silent) whose text *"No modifications were made"* is factually false, and the
   dirty in-memory state is later flushed by an unrelated successful call. **Treat
   `not re-saved` as *dirty state pending*.** Observed live.
4. **★ NEITHER wire sets `draw_pass_1`.** Murzak's `particles-create` and Pro's `create_particles` /
   `apply_particle_preset` all leave it null, and a null draw pass renders nothing. **Any L7 cell on
   either wire must source the draw-pass mesh + material from outside the wire.** This is a
   symmetric ceiling — it does not separate the contestants, and it should be in the L7 brief so
   neither arm loses a round to it.
5. **T6 is larger than filed:** 105 `SKILL.md` files written unasked into `<project>/.claude/skills`
   at boot. In `reincarnated-godot` that collides with our own `.claude/` tree.
6. **The core addon's `plugin.cfg` description still reads *"cloud-connected to ai-game.dev"*** at
   v0.20.1 — cosmetic, but it is what a reader of the installed addon sees.

### Residue / lab state

- Lab left **intact and coherent** at `/Users/admin/Games/mcp-lab/pct4/` (171 MB), restored to its
  Murzak configuration and rebuilt clean. Pro addon parked at `parked/pro_godot_mcp`; Murzak csproj
  copy at `parked/pct4_lab.csproj.murzak`.
- **All processes reaped** — `pgrep -fl 'Godot|gamedev-mcp-server'` → empty.
- **Zero writes to `reincarnated-godot`.** Zero writes to `~/.dotnet` or `~/.nuget`.
- Godot `4.6.3.stable.mono.official.7d41c59c4` · .NET SDK `8.0.423` · addon `v0.20.1` ·
  server `9.2.4` · extensions `0.1.0` ×10 · Pro `1.15.1`.

**Signed:** drax, 2026-07-28. Cell PC-T4. Written incrementally; every verdict carries the
measurement that earned it.

---
---

# MOTION — cell PC-T4-MOTION (rider on step 7)

**Run:** PROVISION-CAL · **Conductor:** gandalf (`RUN-CONDUCTOR`) · **Executor:** drax
**Trigger:** Matt reviewed the step-7 static Pro renders and ruled the checkpoint format
insufficient — *"I need to see it in motion. A static VFX is just a picture."* Correct per rubric
law: check 4's question is judgeable-EFFECT-or-stub, and **effect is temporal.** A single frame
cannot answer it.
**Date:** 2026-07-28 · **Status:** COMPLETE — 3 clips captured.

> **JUDGEMENT WITHHELD, same as step 7.** Below is the capture method, the conditions, the
> verification that the clips are valid recordings, and the paths. **Nothing below is an aesthetic
> claim.** Matt's eye is the instrument.

---

## M.1 · Where this ran, and why it is a SEPARATE project inside the same lab

`reincarnated-godot` has cell **PC-LIGHT in flight in another session** and was declared untouchable
for this cell. **Zero reads and zero writes were made to it.** (The one live `Godot` process on the
host during this cell — `/Applications/Godot.app … tmp/pclight/light_rig.tscn` — is that session's
and was deliberately left running. My binary is the lab's own
`mcp-lab/godot-net/Godot_mono.app`, a different build entirely, so the two runs cannot collide.)

Everything happened under `/Users/admin/Games/mcp-lab/pct4/`. New capture project:

**`/Users/admin/Games/mcp-lab/pct4/motion/`** — minimal, no addons, no autoloads, no C#.

It is separate from `pct4/project/` for a concrete reason, not tidiness: **step 7.1 restored the lab
to its Murzak configuration, but `pct4/project/project.godot` still declares three Pro GDScript
autoloads** (`MCPScreenshot`, `MCPInputService`, `MCPGameInspector` → `res://addons/godot_mcp/mcp_*_service.gd`).
Those files moved to `parked/pro_godot_mcp` with the rest of Pro. Booting that project now throws on
autoload resolution before a rig could run. Rather than mutate the parent project (and destroy the
"lab left intact as evidence" property), the capture project stands alongside it.

**The three preset scenes were copied, not re-authored — md5-verified identical to the ones Pro's
`apply_particle_preset` wrote in step 7:**

| scene | md5 (`project/` original == `motion/` copy) |
|---|---|
| `pct4_pro_fire.tscn` | `66a7d63612c845456012529cb979c973` |
| `pct4_pro_smoke.tscn` | `c018885b6cec50f45a5681eef208034c` |
| `pct4_pro_sparks.tscn` | `bb3dfd489da53bd7b50550ac5456aa68` |

All three are fully self-contained (`sub_resource` only, zero `ext_resource`), so the copy carries no
dependency on the addon that authored them.

---

## M.2 · CAPTURE METHOD — Godot **Movie Maker mode**, named and justified

**Method: Godot 4.6's built-in Movie Maker writer (`--write-movie`), MJPEG-AVI at quality 1.0,
transcoded to H.264 MP4 with ffmpeg 8.1.2.** Not a screen recording, not a frame-grab loop.

Exact invocation, one per preset:

```bash
source /Users/admin/Games/mcp-lab/env.sh
"$GODOT_NET" --rendering-driver metal --resolution 1280x720 \
  --path /Users/admin/Games/mcp-lab/pct4/motion \
  --write-movie /Users/admin/Games/mcp-lab/pct4/renders/raw/pro_<preset>_rigquad.avi \
  --fixed-fps 60 \
  -- res://pct4_pro_<preset>.tscn

ffmpeg -i raw/pro_<preset>_rigquad.avi \
  -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -r 60 \
  -movflags +faststart pro_<preset>_rigquad.mp4
```

**Why Movie Maker and not a frame-dump loop.** Movie Maker forces a **fixed delta of 1/fps**
regardless of how long each frame takes to render and encode. A hand-rolled "grab the viewport every
frame" loop advances on wall-clock delta, so a slow GPU-readback frame makes the particles jump — the
clip would then be a record of *my capture cost*, not of the effect. Encoding cost here was
4.6 ms/frame; under wall-clock that would have been visible motion corruption. Fixed delta makes the
clip **temporally faithful**, which is the entire point of the rider.

Godot's own report per run confirms the mode engaged, e.g. fire:

```
Movie Maker mode enabled, recording movie in 1280×720 @ 60 FPS...
301 frames at 60 FPS (movie length: 00:00:05:01), recorded in 00:00:03 (166% of real-time speed).
Encoding time: 1.44 seconds (average: 4.78 ms/frame)
```

Rig: `/Users/admin/Games/mcp-lab/pct4/motion/pct4_motion.gd` + `.tscn`.
Project settings: `editor/movie_writer/fps=60`, `mjpeg_quality=1.0`, `disable_vsync=true`.

### Conditions — IDENTICAL to the step-7 stills, deliberately

Same stage, same fixed ARPG camera, so the clips are comparable to the PNGs frame-for-frame:
**R-6 — dist 34, fov 24, yaw 47, pitch −50, aim_h 1.0**; ground plane per R-10; 1280×720; Metal,
Forward+, windowed; glow ON at threshold 1.25; **SDFGI OFF**. Same rig quad on `draw_pass_1`
(0.5 m `QuadMesh`, unshaded, vertex-colour, particle-billboard) — **the rig supplies this, neither
wire does** (PC-T4 finding 4). Every clip log line still reads `draw_pass_1=null` on load.

**The camera is the judge; the judge was not moved.**

### fps and durations

| clip | fps | frames | duration | source AVI |
|---|---|---|---|---|
| fire | 60 | 301 | **5.017 s** | 5 860 658 B |
| smoke | 60 | 361 | **6.017 s** | 6 747 058 B |
| sparks | 60 | 271 | **4.517 s** | 5 472 176 B |

---

## M.3 · The emission TIMELINE — a rig action, disclosed

The brief asked for the **full lifecycle: spawn → motion → decay.** A continuous emitter left running
for the whole clip only ever shows spawn → steady state; it never decays. So emission is driven on a
clock. **No preset PARAMETER was touched.** This is the same class of action step 7.5 already
disclosed (re-firing the one-shot `sparks` emitter for the still) — pressing play, now on a schedule:

| preset | as shipped | timeline applied |
|---|---|---|
| **fire** | continuous, `amount=24 lifetime=1.2` | emit from t=0; **emission stopped at t=3.60 s**; clip runs to 5.02 s so the population dies out on camera (last particle ≈ 4.8 s) |
| **smoke** | continuous, `amount=16 lifetime=3.0` | emit from t=0; **emission stopped at t=3.00 s**; clip runs to 6.02 s (last particle ≈ 6.0 s) |
| **sparks** | `one_shot=true emitting=false lifetime=0.4 explosiveness=0.95` | **5 bursts re-fired at t = 0.40 / 1.20 / 2.00 / 2.80 / 3.60 s**; clip runs to 4.52 s, so the 5th burst fully decays on camera (≈ 4.0 s) with a 0.5 s empty tail |

A single `sparks` burst is 0.4 s long. One burst inside a 4.5 s clip would be 91 % empty stage, so the
burst is repeated — **each burst is the preset's own complete lifecycle**; the clip simply contains
five of them.

---

## M.4 · ★ CAPTURE ANOMALIES — two found, both mine, both fixed

**1 · Float-accumulation drift in the burst schedule (fixed, re-captured).**
First `sparks` pass accumulated the schedule in float seconds (`_next_burst += 0.8`). Burst 2 fired at
**t = 1.21667 instead of 1.200 — one frame late.** Cause: `0.4 + 0.8 == 1.2000000000000002` in IEEE
double, which is greater than frame 72's exact `t == 1.2`, so the `>=` test missed by 1 ulp and
fired on frame 73. Fixed by resolving each burst to an exact **integer frame index**
(`round((start + i*period) * fps)`), which cannot drift. Re-captured; the log now reads
`0.400 / 1.200 / 2.000 / 2.800 / 3.600` exactly. **The shipped `pro_sparks_rigquad.mp4` is the
corrected capture.**

**2 · Clip ended mid-burst (fixed, re-captured).** The uncapped schedule fired a 6th burst at
**t = 4.400 s with only 0.1 s of clip remaining** — the clip cut off a burst in flight, so the
"decay" third of spawn→motion→decay was missing from the ending. Fixed with an explicit
`burst_n` cap chosen so the last burst has room to decay to empty inside the clip.

**3 · Godot teardown noise (cosmetic, not fixed, not ours).** Every run exits with
`ERROR: 1 shaders of type ParticlesShaderRD were never freed` +
`ERROR: 1 RID allocations of type '…Shader' were leaked at exit`. This is Godot 4.6.3's own
particles-shader teardown on `get_tree().quit()`, after the movie file is already closed and
finalised. It does not touch the output. Recorded rather than smoothed.

---

## M.5 · Verification that the clips are VALID RECORDINGS (not a verdict on the effects)

**Instrument: per-frame mean luminance (`ffmpeg signalstats YAVG`) across every frame of each clip.**
An empty stage renders a constant YAVG; a clip with content varies. Measured:

| clip | frames | YAVG min | YAVG max | range | distinct values | peak frame | **last frame** |
|---|---|---|---|---|---|---|---|
| fire | 301 | 79.1357 | 79.6782 | 0.5425 | 269 | 83 (t=1.38 s) | **79.1357** |
| smoke | 361 | 79.1357 | 79.2797 | 0.1440 | 222 | 147 (t=2.45 s) | **79.1357** |
| sparks | 271 | 79.1357 | 81.8268 | 2.6911 | 121 | 227 (t=3.78 s) | **79.1357** |

Two things this settles:
- **`79.1357` is the empty-stage constant** — it is the min of all three clips, and it is the value of
  `sparks` frame 0 (before the first burst). All three clips **return to it exactly on their last
  frame**, which is the decay tail landing where it should. The timeline in M.3 did what it claimed.
- **All three vary, and vary differently from each other.** Unlike the step-7 `_asemitted` stills
  (byte-identical to each other and to an empty stage), these are three distinct recordings.

**On-screen occupancy at each clip's peak frame**, measured against the empty-stage reference
(per-pixel RGB difference > 8):

| clip | pixels differing | % of 1280×720 frame | bounding box |
|---|---|---|---|
| fire | 6 415 | 0.696 % | 100 × 120 px |
| smoke | 1 542 | **0.167 %** | 48 × 42 px |
| sparks | 19 528 | 2.119 % | 277 × 262 px |

**Stated as a capture condition, not as a judgement:** at the fixed R-6 camera these effects subtend a
small fraction of the frame, and `smoke` is the smallest by an order of magnitude relative to
`sparks`. This is consistent with the step-7 stills (`pro_smoke_rigquad.png` was 7 547 B against an
empty stage's 7 300 B). **It is a property of the preset at this camera, not a defect in the capture**
— the recording is confirmed valid by the frame-to-frame variance above. If Matt wants the effects
larger in frame, that is a camera change and it is his call, not mine; R-6 was held because it is the
camera the stills were judged at.

**I confirmed the capture path is valid (correct codec, correct dimensions, correct frame count,
correct camera, real frame-to-frame variance, clean decay to baseline). I am not offering an opinion
on the effects. They are Matt's to watch.**

---

## M.6 · ★ CLIP PATHS — the Matt-eye checkpoint

All under **`/Users/admin/Games/mcp-lab/pct4/renders/`** — H.264 / MP4, 1280×720, 60 fps,
`+faststart` (they will stream/scrub without a full download):

| File | duration | bytes | md5 |
|---|---|---|---|
| **`pro_fire_rigquad.mp4`** | 5.017 s | 178 279 | `0f303d1fbe56065e589793fa9a0c2e9b` |
| **`pro_smoke_rigquad.mp4`** | 6.017 s | 42 593 | `02d28f21ffa5ae9016df01a38064dfbe` |
| **`pro_sparks_rigquad.mp4`** | 4.517 s | 219 151 | `545dbcfe63bfb14a5812887c1f28929d` |

Supporting artifacts, kept:
- `renders/raw/pro_{fire,smoke,sparks}_rigquad.avi` — the Movie Maker originals (MJPEG q1.0), 18 MB
  total. The MP4s are derived from these; kept so the transcode can be redone without re-rendering.
- `renders/motion_peakframes/` — the peak frame of each clip extracted as PNG, plus
  `EMPTY_STAGE_ref_sparks_f000.png`, the empty-stage reference the occupancy table was measured
  against.

**`_rigquad` only.** There is no `_asemitted` motion clip and there should not be: step 7.4 measured
that an as-emitted preset has `draw_pass_1 == null` and therefore **draws nothing**. A 5-second clip
of it would be 300 identical frames of empty stage. The still already carries that finding.

---

## MOTION EXIT SUMMARY

| Item | Result |
|---|---|
| Clips | ✓ **3 MP4s**, 1280×720 / 60 fps / H.264, 4.5–6.0 s each, at the same fixed R-6 camera as the stills |
| Method | ✓ **Godot 4.6.3 Movie Maker mode** (`--write-movie`, fixed delta 1/60) → ffmpeg H.264 CRF 16. Fixed delta chosen so the clip records the effect, not the capture cost |
| Lifecycle | ✓ spawn → motion → decay in all three; verified by every clip returning to the exact empty-stage YAVG constant (`79.1357`) on its last frame |
| Anomalies | ✓ 2 found and fixed (1-frame float drift in burst schedule; clip ending mid-burst) — both re-captured. 1 cosmetic Godot teardown shader-leak error, not ours, does not touch output |
| `reincarnated-godot` | ✓ **untouched — zero reads, zero writes.** PC-LIGHT's live Godot process was left running |
| Lab state | ✓ `pct4/project/` **byte-unchanged**; all new work isolated in `pct4/motion/` + `pct4/renders/`. All my processes reaped |
| Judgement | **withheld — Matt's** |

**Signed:** drax, 2026-07-28. Cell PC-T4-MOTION.
