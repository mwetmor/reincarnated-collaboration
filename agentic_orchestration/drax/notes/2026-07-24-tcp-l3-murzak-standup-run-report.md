# TCP-L3 — MURZAK STANDUP (run report)

**Program:** Tool-Capability Program · lap **L3**, class **standup**
**Charter:** `agentic_orchestration/gandalf/notes/2026-07-24-tcp-l3-murzak-standup-charter.md`
**Conductor:** gandalf (`RUN-CONDUCTOR`) · **Executor:** drax (presentation seam)
**Status:** **CLOSED — PASS.** All six exit-predicate items met, plus the three added for L3b.
**Ran as:** L3a (2026-07-25 00:37–00:49, stopped by conductor) + **L3b** (01:00–01:12, this run).
Findings from both laps are folded together below; the lap reads as one lap.

---

## §0 — Verdict, in one paragraph

**W-MUR stands up self-hosted on this machine, and the wire behaves.** 39 tools over 11
families, exactly as the audit predicted — the first documented number in this program to
survive contact with the wire. It **runs fully headless** with no tool loss, which retires
the GUI-window failure class outright. It authored a scene, and it authored a **GDScript
builder that ran headless in 0.30 s and produced correct geometry** — **the W→H path
(TCP-5) is closed, end to end, with a picture.** Against that: the addon's **compiled-in
default connection mode is Cloud**, and launched bare it ships machine name and project
identity to `ai-game.dev` before any tool call — a **silent violation of Matt's Q45
ruling**, and the second one this lap found. Property addressing is C#-reflection-shaped
and **undiscoverable from the wire's own schemas**. And **one of my own banked numbers was
wrong**: the "≈114 ms/call" figure was a contaminated mean; the true steady state is
**8.03 ms**, statistically indistinguishable from Pro.

## §1 — Rubric diff against §0 intent (law L-I — name what falls out, out loud)

The charter says this lap answers **readiness + live surface + one behavioural proof**, and
is *deliberately incapable* of saying whether Murzak is **good** at anything. That holds.
Restating what a PASS here does **not** license:

- It says nothing about **authoring quality**, **design arrival**, or **iteration speed**.
- The frames below are **boxes and pillars**. They prove the wire writes correct geometry.
  They are not evidence that Murzak builds a decent room. That is L4/L5/L7.
- The W→H proof is a **minimal** proof: a builder that makes eight boxes. It establishes
  that the path exists and closes. It does not establish that Murzak can author a
  *production-grade* builder.

One thing I want on the record as **falling out and mattering**: this lap measured the wire
under **headless** conditions. Every latency and reliability number below is a headless
number. L5 (T4-UI) is the one lap that may genuinely need a **windowed** editor, because
`screenshot-viewport` is how a UI lap looks at its own work. **L5 should not inherit this
lap's latency figures.**

## §2 — The defect that stopped L3a, and what replaced it

**What happened.** Three `Godot_mono.app --editor` processes launched 00:40:03, 00:41:27 and
00:47:07, all orphaned to PID 1, two idling at 0.0% CPU. A launch-retry loop with no
reaping. gandalf killed all three and stopped the run. The stop was correct.

**Root cause, now known.** Not flakiness. `godot-cli open` spawns the editor **detached**
and injects three environment variables the addon needs. When the editor appeared not to
come up, relaunching was treated as a diagnostic. It is not one — and the actual failure
was invisible without reading the launch log, which named it on line 14.

**What replaced it.** `~/Games/mcp-lab/bin/editor_up.sh` — a launcher that *structurally*
cannot stack processes:

1. Refuses to launch if the tracked PID in `logs/editor.pid` is alive.
2. Refuses to launch if **any** Godot process is alive, tracked or not (orphan blindness
   was the actual L3a failure — the check has to be `ps`-wide, not pidfile-wide).
3. Captures the PID to a file the instant it launches.
4. Polls the wire's own **`ping`** tool for readiness. Never relaunches as a diagnostic.
5. On timeout, **reaps what it started** and exits non-zero.

Plus `bin/editor_down.sh`, which kills the tracked PID and then asserts `ps` is Godot-free.

**Editor launches this lap: three, never concurrent, each reaped before the next.**

| # | Mode | PID | Outcome |
|---|---|---|---|
| 1 | headless | 26498 | Timed out at 150 s. **Reaped by the launcher.** Diagnostic recovered from log (§4.1). |
| 2 | headless | 26774 | **Ready in 4 s, one ping attempt.** All wire work. Reaped. |
| 3 | headless | 27413 | Ready in 4 s. Settled one open question (§4.10). Reaped. |

Launch #2 was **not a blind retry**. Launch #1's log named its own cause explicitly; the
route changed on that evidence, with the first process already dead. I am flagging the
distinction rather than hiding it, because "diagnosed route correction" is exactly the
excuse a retry loop would make for itself. The check that makes it honest is guard #2: a
second launch was *impossible* while the first lived.

**Also reaped: an inherited orphan.** `gamedev-mcp-server` PID **25887**, alive since 00:43,
parented to PID 1, still LISTENING on 27435 when L3b started. gandalf's cleanup killed the
three editors but not the server — it is a separate detached process and it outlived them.
Adopted as a tracked PID at session start and killed at lap end.

**End state:** `pgrep Godot` → none. `pgrep gamedev-mcp-server` → none. `pgrep dotnet` →
none. Port 27435 → not listening. **Exit-predicate item 7 satisfied.**

## §3 — Pre-registered predictions, each resolved to a recorded fact

### P-A — user-local .NET install without `sudo` — **CONFIRMED**

.NET SDK 8.0.423 installed via `dotnet-install.sh --install-dir ~/Games/mcp-lab/dotnet`.
`Godot_mono.app` side-by-side in `~/Games/mcp-lab/godot-net/`. No `sudo`. No machine-wide
install. `/Applications/Godot.app` never invoked. Gatekeeper never blocked.

**Correction to the charter's premise.** §1.2 states *"no `dotnet` SDK exists on this
machine at all."* **That was already false when the charter was written.** A complete
user-local SDK **8.0.423** sits at `~/.dotnet`, dated **2026-07-23 22:42** — two days
before this lab existed. It is simply not on `PATH` (`which dotnet` → not found), which is
what the recon actually measured. Not mine, not touched, not removed (§7). The charter's
*conclusion* — install user-local in the lab — remains right; only its stated reason was.

### P-B — live manifest disagrees with documentation — **FALSIFIED for Murzak**

**39 tools, 11 families**, `gamedev-mcp-server 9.2.0.0` + addon `0.19.1`, protocol
`2025-06-18`. The audit's prior of *"39 tools / 11 families"* was **exactly right**.

This is the first time in this program a documented number has survived the wire. Pro's
docs said 77; Pro's wire said 175. Murzak's audit said 39; Murzak's wire says 39.

**Re-enumerated in L3b under headless (L-C — verdicts expire, re-read every lap):**
**39 tools, byte-identical name set** to the L3a GUI enumeration. Diff both directions: empty.

```
[console] 2  [editor] 4  [filesystem] 2  [node] 6  [ping] 1  [reflection] 2
[resource] 6  [runtime] 2  [scene] 5  [screenshot] 3  [script] 6
```

Artifacts: `evidence/MUR_LIVE_MANIFEST.json`, `evidence/MUR_LIVE_TOOLNAMES.txt`,
`evidence/MUR_LIVE_MANIFEST_L3b_headless.json`.

**L-B still holds — one level down.** The tool *list* matched. Three tool *schemas* do not
describe what the wire accepts (§4.5, §4.6). The manifest was right about *what exists* and
insufficient about *how to call it*.

### P-C — `Godot-AI-*` extension packages not installed by the core addon — **CONFIRMED**

**10 packages / 63 tools in the catalog. Zero present in the live 39.** Re-verified against
the fresh headless manifest — every family probed returns ABSENT:

```
gridmap ABSENT · csg ABSENT · particle ABSENT · tilemap ABSENT · navigation ABSENT
animation ABSENT · terrain ABSENT · dialogic ABSENT · beehave ABSENT · phantom ABSENT
```

**GridMap, CSG and Particles — the three capabilities that reopened this entire column —
are gated behind per-package installs. L4/L5/L7 must budget for that**, and the GridMap
correctness prediction in the program charter (§L4) cannot be tested until they are.

Artifact: `evidence/extension_catalog_summary.txt`.

### P-D — a sub-agent cannot wire an MCP server into its own running session — **CONFIRMED**

`claude mcp list` from this session lists only the Vercel plugin server. The
`ai-game-developer` entry written to `~/Games/mcp-lab/project/.mcp.json` is invisible here,
for two independent reasons: it is **project-scoped** to the lab project (this session's cwd
is the meta-repo), and MCP servers are resolved at **session start**.

**But the path around it is better than the thing it routes around**, and this is the useful
half of P-D. This entire lap drove the wire through
`~/Games/mcp-lab/bin/mur_mcp_client.mjs` — a ~120-line JSON-RPC client speaking Streamable
HTTP directly. That gives three things a session-wired MCP client would not:

- **A per-call latency ledger** — without which §4.4's correction would not exist.
- **Scriptable plans** (`--plan file.jsonl`) — deterministic, replayable, diffable.
- **No session restart in the loop**, so a route change costs seconds.

**Recommendation for L4: do not session-wire.** Drive Murzak with the client. Session
wiring buys ergonomics and costs measurement.

### P-E — asset route for L4 — **MEASURED**

Pack ruled (in-run, §6 authority): **`polygon-dungeon-realms`** — 100 MB, 2494 files,
1221 FBX. Mid-distribution and directly relevant to an L4 dungeon expansion.

| Measurement | Result |
|---|---|
| Copy into lab (100 MB, 2494 files) | **1 s** |
| **Cold import** (`--headless --import`) | **50 s**, RC=0 |
| Imported artifacts produced | **2530** (63 MB cache) |
| **Warm re-import** (cache present) | **10 s**, **0 errors** |
| Cold-import error lines | 1854 lines / **14 distinct** missing paths |
| Do refs resolve? | **Geometry and PNG textures: yes.** 14 `.psd` refs: no — see below. |
| Is the cache reusable? | **Yes** — warm import is 5× faster and clean. |

**The 14 unresolved refs are benign, and I verified that rather than assuming it.** They are
`.psd` paths baked into Synty's FBX material slots — `_Cameron/Exports/`,
`_Cameron/Textures/`, `_Textures/`. **Zero `.psd` files exist anywhere in the product repo's
Synty tree** (`find … -name '*.psd' | wc -l` → 0), so these are Synty's internal authoring
sources, shipped in no pack, and equally unresolvable in `reincarnated-godot` today. They
are noise, not breakage — but **1854 error lines will drown an L4 import log**, so filter
them rather than triage them.

**Is the cache transplantable between projects?** Yes, **if the `res://` path is mirrored.**
The `.import` sidecars are project-relative and path-bound — e.g.
`source_file="res://Assets/Synty/polygon-dungeon-realms/Textures/Gold_Normal.png"`, with
`dest_files` pointing into that project's `.godot/imported/`. Place a pack at the **same
relative path** and the sidecars stay valid; place it anywhere else and Godot rewrites
them. **That rewrite behaviour is why the charter's prescribed symlink was unsafe (§5.2).**

**Verdict for L4: a sibling .NET project is viable.** One pack costs ~1 minute cold and
~10 s warm. No Matt-gated .NET conversion of `reincarnated-godot` is required.

## §4 — Findings

### 4.1 The addon's default connection mode is **Cloud**, and it dials out before any tool call — Q45 violation, and the worse of the two

Launch #1's log, line 14:

```
[Godot-MCP] connecting (mode=Cloud, host=https://ai-game.dev/mcp) ...
```

Line 29 shows what it sent:

```
wss://ai-game.dev/mcp/hub/mcp-server?instance_id=…&engine=godot&project_name=tcp_l3_lab
  &project_path_hash=eb8c59d8…&machine_name=Matthews-Mac-mini
```

Rejected with `Authorization failed. Token may be missing, invalid, or revoked.` — then it
**retried the cloud indefinitely and never fell back to loopback.** That is why launch #1
timed out: not a headless problem, not a Godot problem. A default.

**Mechanism**, from the addon source (`Runtime/Connection/GodotMcpEnvFile.cs:145–185`):
mode precedence is env var > `.env` file > loopback-host inference > **config default**.
The config default is Cloud. `godot-cli open` injects `GODOT_MCP_CONNECTION_MODE=Custom`;
a direct binary launch does not, and gets the vendor default.

**This is the second Q45 violation this lap found, and they are different in kind.** The
banked one (`evidence/mcp.json.setup-mcp-DEFAULT-CLOUD`) was `setup-mcp` writing a *client*
config pointing at `https://ai-game.dev/mcp/p/eb8c59d8` — bad, but inert until used, and
caught because the default was captured before overriding it. **This one is the editor
plugin itself, at boot, actually transmitting** machine name and project identity to a
third party. Matt ruled self-hosted. The out-of-the-box wiring violates that ruling
**twice, silently, in two different components**.

**Mitigation, now enforced in `editor_up.sh`:**

```bash
export GODOT_MCP_CONNECTION_MODE=Custom
export GODOT_MCP_AUTH_OPTION=None
export GODOT_MCP_HOST=http://localhost:27435
export GODOT_MCP_LOG_LEVEL=Debug
```

With these, launch #2 connected `mode=Custom, host=http://localhost:27435` and was ready in
4 s. **Any L4 launch that does not set these leaks to the cloud.** Do not delegate this to
`godot-cli`; set it explicitly and assert the log line.

Artifact: `evidence/CLOUD_DEFAULT_addon_boot.txt`.

### 4.2 Murzak runs **fully headless** with zero tool loss — this retires the defect class that stopped L3a

`--headless --editor` yields **39/39 tools, identical name set**. Every node, scene, script,
resource and reflection tool works. Only the three `screenshot-*` tools degrade, and they
degrade **honestly** — a structured error, `isError: true`, naming the cause:

> *"Viewport texture read back an empty image — the viewport produced no GPU render (common
> under '--headless', which has no rendering device). Run the capture in a windowed editor
> with a real GPU."*

Their manifest descriptions **document this in advance**, and the wire matched the doc. In a
stack governed by L-K, that deserves saying: **this is the one place all lap where the
documentation, the schema and the behaviour all agreed.**

**Consequence: L4 needs no GUI editor at all.** The failure mode that stopped L3a —
orphaned editor windows on Matt's screen — is not something to be disciplined about. It is
something to **not do**.

### 4.3 The server hosts nothing; it relays. With no editor connected, `tools/list` returns **0**

A free probe before launching anything:

```
count: 0    tools: []          # server up, editor not connected
ping →  isError: true, "Failed to invoke … after 10 retries."   (10.02 s)
```

All 39 tools are proxied from the editor plugin over SignalR. **An MCP client that
initializes before the editor is connected sees an empty tool list** — and MCP clients cache
the tool list at initialize. **Launch order is a hard constraint for L4**, and it is the
concrete reason P-D's session-wiring route is fragile: a session started at the wrong moment
gets a permanently empty toolset.

It also makes `ping` a *valid* readiness probe (it fails loudly in 10 s rather than hanging),
which is what `editor_up.sh` relies on.

### 4.4 **Latency: I need to correct my own banked number.** 114 ms was a contaminated mean; the truth is 8.03 ms

Banked from L3a: *"Latency ≈114 ms/call against Pro's 8.33 ms — a 14× spread between
instruments."* **That claim is wrong and I withdraw it.**

Measured in L3b, headless, clean:

| Call | n | mean | median | max |
|---|---|---|---|---|
| `ping` (no editor work) | 40 | **1.01 ms** | 0.93 ms | 2.00 ms |
| `node-create` (real mutation) | 30 | **8.03 ms** | 7.92 ms | 9.85 ms |

And the decisive evidence — server-side handler times parsed from `server.log` across
**both** laps, 252 calls:

```
n=252   mean=578.92 ms   median=3.67 ms   max=10026.55 ms
```

**The median was ~4 ms even during L3a.** The 114 ms mean was dragged by a handful of
**10-second retry timeouts** — the `"No connected clients. Retrying [n/10]"` events from
§4.3, i.e. calls made while no editor was attached. Those are not latency. They are a
disconnected wire.

**Corrected finding: Murzak (8.03 ms) and Pro (8.33 ms) are in the same latency class.**
The 14× spread does not exist between instruments. There *is* a large spread — between
**connected and disconnected**, and plausibly between headless and GUI — but not between
these two tools.

**This is the same error class as TCP-15, second instance, and this one is mine.** gandalf
generalized one instrument's 114–180 ms into a category constant; I generalized one
contaminated mean into an instrument comparison. **A median would have caught both.**
Consequences run the same direction as TCP-15: the **T4-UI case for the wire gets stronger**,
and L4's three-way should be run on capability, not conceded on speed.

Artifact: `evidence/LATENCY_L3b_headless.txt`.

### 4.5 Property addressing is **C# reflection names**, and getting it wrong returns `isError: false` — L-K

`node-modify` speaks the **C# surface**, not GDScript's. `Position` works; `position` does
not. Vector components are `X`/`Y`/`Z`, not `x`/`y`/`z`. The failure, verbatim:

```json
{"Depth":0,"Message":"Segment 'position' not found on type 'MeshInstance3D'.\nAvailable
 fields: NativePtr\nAvailable properties: Mesh, Skin, …, Position, Rotation, …"}
{"Depth":0,"Message":"No modifications were made.","Type":"Warning"}
```

**MCP-level `isError: false`. Transport `ok`. Nothing written.** An agent that checks the
error flag — which is what an MCP client surfaces by default — sees success and proceeds.
This is **L-K wearing a new coat**, and it is the exact wall L3a hit at 00:49 and did not get
past.

Mitigation for L4: the failure payload **enumerates every valid property name**, so it is
self-correcting *if you read the body*. Treat `result[].Type == "Error"` as the real error
channel; `isError` is not it.

### 4.6 Resource-valued properties are **undiscoverable from the wire's own schemas**

Assigning a mesh took four attempts. Three failed, all with `isError: false`:

| Attempt | Result |
|---|---|
| `jsonPatch {"Mesh":"res://…tres"}` | `Failed to read a ResourceRef … could not be converted` |
| `pathPatches` w/ `typeName: "Godot.BoxMesh"` | same |
| `pathPatches` w/ `typeName: "…Data.ResourceRef"` | `Instance creation failed for type ResourceRef` |
| **`jsonPatch {"Mesh":{"instanceId":0,"resourcePath":"res://…tres"}}`** | **`Resolved Resource … to a live 'Mesh'.`** |

**I found the working shape by reading the addon's C# source**
(`Runtime/Data/ResourceRef.cs`), not the manifest. `node-modify`'s schema types `jsonPatch`
as an opaque `string` and never mentions `ResourceRef` in its `$defs`. **An agent with only
the wire in front of it cannot assign a mesh.**

This is a real **aim** cost and it belongs in L4's budget: the wire's advertised surface is
complete about *what exists* and silent about *how to call it* for any resource-valued
property — meshes, materials, textures, shaders. That is most of dressing.

### 4.7 One unreproducible duplicate execution — reported at exactly the strength the evidence supports

During the first authoring burst, `resource-create` returned
`isError: true, "A resource already exists at 'res://tcp_l3b_box.tres'"` — **for a file that
did not exist before the call and did exist, valid, immediately after it.** Editor-side logs
show **3 executions of `resource-create` for 2 client calls**, identical parameters,
completions at `00:59:29.858` (ok) and `00:59:39.547` (already-exists) — **9.7 s apart.** The
saved scene likewise carries two phantom nodes (`@MeshInstance3D@19110`,
`@MeshInstance3D@19987`) beside the correctly-named ones.

**I could not reproduce it.** A clean single call: 1→1, correct. A controlled probe: 1→1. An
8-call burst: **8 issued, 8 executed, 8 correct nodes on disk.**

**So I am not claiming Murzak double-executes.** What is established: (a) a duplicate
execution demonstrably occurred, (b) an **error return did not mean the write had not
happened**, (c) it is not reproducible under isolated or burst conditions.

Most probable mechanism, stated as hypothesis: the `gamedev-mcp-server` process had been
alive since 00:43 **across an editor restart**, retaining sessions (`TotalSessions: 3`), and
a queued invocation from the dead L3a session replayed on reconnect. The transport has an
explicit 10-retry loop, and 9.7 s fits its timeout.

**Mitigation for L4, cheap and worth taking: restart the server together with the editor.
Never let the relay outlive an editor session.** (It also orphans to PID 1 — see §2.)

**The operative lesson is the lap's own thesis.** L-K says a `ok` return is not evidence a
write happened. This says an **error return is not evidence it did not.** *Neither polarity
of the return code is evidence.* Only an independent read is.

### 4.8 `script-create` genuinely validates, genuinely rejects, and genuinely writes nothing

Fed deliberately malformed GDScript, it returned a **real** failure:

```
isError: true — Tool execution failed for 'Script / Create':
  (GDScript failed to parse (ParseError). Fix the syntax and retry. (Parameter 'content'))
```

and `res://tcp_l3b_bad.gd` **was not created on disk** (verified by shell). The documented
"invalid `.gd` is rejected and nothing is written" claim holds exactly.

`script-validate` returned `ok: true, errorCount: 0, fidelity: "Precise"` for the good
script, and `script-read` round-tripped the content. **This is the most trustworthy family
on the wire** — and it is, not coincidentally, the one the program cares most about.

(One cosmetic defect: `script-create`'s response reports `lineCount: 0` for a 45-line file.)

### 4.9 **W→H is closed (TCP-5)** — the wire authored the builder, the builder ran production

The full loop, each step verified independently of the tool that performed it:

1. **Murzak wrote** `res://tcp_l3b_builder.gd` (1404 bytes) via `script-create` — a
   `SceneTree` script building a floor plus 8 pillars of arithmetically increasing height,
   a light and a camera, packed and saved.
2. `script-validate` → `ok: true`. `script-read` → round-trips.
3. **Independent shell read** of the file off disk: present, correct, 1404 bytes.
4. **Executed headless on the lab's own Godot** (`Godot_mono.app`, *not* the product
   editor, *not* `/Applications/Godot.app`):
   `$GODOT_NET --headless --path project --script res://tcp_l3b_builder.gd` →
   **0.30 s real.**
5. **Independent read of the output** `res://tcp_l3b_built.tscn` (2836 bytes): 8 `BoxMesh`
   sub-resources with sizes `1, 1.35, 1.7, 2.05, 2.4, 2.75, 3.1, 3.45` — **the exact
   arithmetic progression specified** — plus the `PlaneMesh` floor.
6. **Rendered** (§4.11). The pixels agree.

**This reframes L4 exactly as predicted.** Murzak does not have to win on wire throughput,
because it does not have to *use* the wire for assembly. It can write the builder and let
the builder run — the ruled `pipeline-game.md` doctrine ("MCP authors recipes / headless
scripts run production") executing itself inside one tool. **0.30 s for a scene the wire
would have spent ~11 node-creates on.**

### 4.10 A near-miss I want on the record: I nearly filed a false L-K instance

My capture rig reported `aabb=[P:(0,0,0) S:(0,0,0)]` for the node-CRUD scene, and the
`.tscn` on disk carried **no `mesh` property** — despite `node-modify` returning two
`"Type":"Success"` messages including `Resolved Resource … to a live 'Mesh'`. That is
textbook L-K shape, and it was one sentence away from being written up as a sixth instance.

**It was my bug.** I never called `scene-save` after that assignment. One tracked editor
relaunch, the same call followed by `scene-save`, and the disk shows:

```
[ext_resource type="BoxMesh" uid="uid://dg8lfigupe1l3" path="res://tcp_l3b_box.tres" id="1_5kk1r"]
[node name="Alpha" type="MeshInstance3D" parent="." unique_id=1196783076]
mesh = ExtResource("1_5kk1r")
```

**The instrument was correct and I was about to blame it.** Worth stating plainly because
this program's laws bias hard toward distrusting the tool, and that bias has a false-positive
direction. The independent read cleared Murzak the same way it convicts it — which is the
argument for the independent read, not for the suspicion.

### 4.11 Frames (exit item 3) — ours, not the instrument's

Rendered with **`project/tcp_l3b_shoot.gd`, a drax-authored rig**, per **TCP-8**: we score
authoring, not capture rigs. Murzak's own `screenshot-*` were additionally unusable here
because the editor ran headless (§4.2). The rig loads the scene, supplies environment and —
only if the scene lacks them — a light and a framed camera, then saves the viewport.

| Frame | Path | Shows |
|---|---|---|
| **BUILT** | `evidence/frames/BUILT_wire_authored_builder.png` | The **W→H** output: floor + 8 pillars, ascending heights, correct ring. Camera is the one the **Murzak-authored builder** placed. |
| **PROOF** | `evidence/frames/PROOF_wire_node_crud.png` | Pure `node-create`/`node-modify` authoring: the box, framed by the **camera Murzak positioned** via `node-modify`. |
| CLEAN | `evidence/frames/CLEAN_wire_node_crud.png` | The §4.10 near-miss, retained as evidence of the pre-`scene-save` state. |

The BUILT frame is the judgeable one, and it is judgeable: eight pillars stepping upward
around a plane, correctly lit, correctly framed. **It agrees with the `.tscn` text.**

### 4.12 The addon writes into the project without being asked

`[Godot-MCP] auto-generate skills: ensured up-to-date skills in …/project/.claude/skills.`

39 `SKILL.md` files, one per tool, written into the project on plugin load. Harmless in a
lab. **Worth flagging for any future lap that installs this addon into a product repo** —
it is an unrequested write, in the same class as L-J's three known residues.

## §5 — Charter defects found

The charter asked me to assume there were more. There were three.

### 5.1 The blast-radius predicate is **structurally blind** to the asset tree

TCP-18 constraint 4 and charter §4.4 define the verification as *"a clean `git status`
INCLUDING untracked files."* **`/Assets/Synty/` is gitignored** (`reincarnated-godot/.gitignore:13`,
under the Synty license rule — *"must not share the source files of any Assets outside your
team"*). Writes into the asset tree produce **no git signal at all**, tracked or untracked.

The predicate cannot detect the writes the **P-E probe in the same charter** was most likely
to cause. I substituted a fingerprint check — `find … -exec stat -f '%m %z %N' | sort |
shasum -a 256` over all 2494 files — and recorded it before and after (§6).

**Recommendation:** any lap touching assets verifies by **fingerprint**, not by `git status`.
This is L-J's "byte-perfect belief is not byte-perfect verification" with a new instrument:
here the *detector itself* was blind, not merely incomplete.

### 5.2 P-E's prescribed **symlink** would have written into the product repo — which the same charter makes a HALT

Charter §3 P-E: *"Symlink **one** Synty pack from `~/Games/reincarnated-godot/Assets/` into
the lab project."* Charter §6: HALT on *"any need to write into `reincarnated-godot`."*

**These conflict.** Godot writes `.import` sidecars **next to source files** — there are
already **1246** of them inside that pack — and each is bound to a project-relative path:

```
source_file="res://Assets/Synty/polygon-dungeon-realms/Textures/Gold_Normal.png"
dest_files=["res://.godot/imported/Gold_Normal.png-acd5832c….ctex"]
```

Symlinked into a lab project at any different `res://` path, Godot finds `source_file`
mismatched and **rewrites the sidecar — through the symlink, into the product repo,
invisibly to git** (per §5.1). Symlinked at the *same* path, `dest_files` still point at the
other project's `.godot/`, and the sidecars churn.

**Substitution, declared as a substitution (§6 authority): `rsync` copy at the mirrored
relative path** `project/Assets/Synty/polygon-dungeon-realms/`. Cost: **1 second**, 100 MB.
It answers every P-E question the symlink would have, writes nothing into the product repo,
and the mirrored path is what made the cache-transplant finding measurable.

**Not escalated as a HALT** because a strictly safer route existed at negligible cost and
the measurement was unaffected. Flagging it as a charter defect rather than silently
working around it, per §6's substitution rule.

### 5.3 The charter's toolchain premise was already false

Covered in P-A: `~/.dotnet` holds a complete SDK 8.0.423 from 2026-07-23. The charter's
"no `dotnet` SDK exists on this machine at all" described `PATH`, not the machine.
Conclusion unaffected; premise corrected.

## §6 — Blast radius, verified (TCP-18)

| Constraint | Status | Evidence |
|---|---|---|
| 1. Everything in `~/Games/mcp-lab/` | **HELD**, with one named exception | §7 residue |
| 2. `/Applications/Godot.app` untouched | **HELD** | Never invoked; every run used `$GODOT_NET` in the lab |
| 3. `dotnet` user-local, no `sudo` | **HELD** | `dotnet-install.sh --install-dir`; no sudo issued this lap |
| 4. `reincarnated-godot` byte-unmodified | **HELD** | below |
| 5. Uninstall procedure written | **DONE** | `~/Games/mcp-lab/UNINSTALL.md` |

**Product repo, verified four ways** (because §5.1 proved one way is not enough):

- `git status --short --untracked-files=normal` — **identical to the baseline** taken at lap
  start (`evidence/BLAST_BASELINE_reincarnated-godot.txt`).
- `project.godot` sha256 `a76d666a4a3ece81d508d0a0a183d6674bf6d8ad9509cdb55b01233f81ae2680`
  — **unchanged**.
- `Assets/Synty/polygon-dungeon-realms` fingerprint over all 2494 files
  `96284fd0ba1c642ec22362e778209236ff91075518da9adf492b074819c2064e` — **unchanged**,
  before copy, after copy, and after import.
- `find . -newermt '2026-07-25 00:30' -type f` → **0 files.**

**The pre-existing `project.godot` modification is not mine and I did not touch it.** The
uncommitted deletion of

```
-[rendering]
-mesh_lod/lod_change/threshold_pixels=1.0
```

carries mtime `00:08`, **29 minutes before the lab directory existed**. It is L-J residue #3
(an editor open is a write). Left exactly as found.

## §7 — Residue outside the lab: one escape, named

**`~/.dotnet/` received 14 files and 17 directories from this lap** — workload-advertising
metadata under `sdk-advertising/8.0.400/` plus `.workloadAdvertisingUpdates8.0.400`.

`DOTNET_ROOT` and `NUGET_PACKAGES` were redirected into the lab; **`DOTNET_CLI_HOME` was
not**, so the CLI wrote to the home directory regardless. `rm -rf ~/Games/mcp-lab` does not
remove these. Exact removal commands are in `UNINSTALL.md` §3.

**`~/.nuget/` — zero files with mtime ≥ 2026-07-25.** The `NUGET_PACKAGES` redirect held.

Small, non-destructive, and reported rather than rounded down — TCP-18 constraint 1 says
*everything* lands in the lab, and 31 filesystem entries did not. **For L4, add
`export DOTNET_CLI_HOME="$LAB/dotnet-home"` to `env.sh`** and the escape closes.

## §8 — Launch procedure for L4 (executable)

```bash
# 0. Preconditions — assert, do not assume.
pgrep -fl 'Godot|gamedev-mcp-server'     # MUST be empty. If not, reap before continuing.
lsof -nP -iTCP:27435                     # MUST be empty.

cd ~/Games/mcp-lab && source env.sh      # sets DOTNET_ROOT, NUGET_PACKAGES, GODOT_NET
# RECOMMENDED ADDITION (see §7):
export DOTNET_CLI_HOME="$LAB/dotnet-home"

# 1. Start the MCP relay FRESH. Never reuse one that outlived an editor (§4.7).
#    It detaches and orphans to PID 1 — capture the PID.
nohup ./project/.ai-game-dev/server/osx-arm64/gamedev-mcp-server > logs/server.log 2>&1 &
echo $! > logs/server.pid

# 2. Start EXACTLY ONE editor, headless, Q45-enforced, ping-polled.
#    editor_up.sh sets GODOT_MCP_CONNECTION_MODE/AUTH_OPTION/HOST and refuses to stack.
./bin/editor_up.sh headless 150
#    Ready in ~4 s. On failure it reaps itself and exits non-zero — do NOT relaunch;
#    read logs/editor-l3b-headless.log and assert this line:
grep 'connecting (mode=' logs/editor-l3b-headless.log   # MUST say mode=Custom, localhost

# 3. Confirm the wire is live BEFORE trusting any tool list (§4.3).
node bin/mur_mcp_client.mjs --list 2>/dev/null | python3 -c \
  "import sys,json; print('tools:', json.load(sys.stdin)['count'])"   # MUST be 39, not 0

# 4. Drive the wire with the client, not session-wiring (§P-D).
node bin/mur_mcp_client.mjs --plan plans/l4_step1.jsonl

# 5. Render with OUR rig (TCP-8), not screenshot-* (headless has no GPU).
"$GODOT_NET" --rendering-driver metal --path project --quit-after 300 \
    tcp_l3b_shoot.tscn -- res://<scene>.tscn /abs/out.png

# 6. Reap. Both processes. Every time.
./bin/editor_down.sh && kill "$(cat logs/server.pid)"
pgrep -fl 'Godot|gamedev-mcp-server' || echo CLEAN
```

**Calling conventions L4 must know before writing its first plan:**

- Properties are **C# names**: `Position`, `RotationDegrees`, `Mesh` — and `X`/`Y`/`Z`.
  snake_case silently no-ops (§4.5).
- Resource-valued properties take a **ResourceRef object**:
  `{"Mesh":{"instanceId":0,"resourcePath":"res://…tres"}}` (§4.6).
- **`scene-save` is required.** Node mutations live in editor memory until it is called
  (§4.10). Nothing warns you.
- **Read `result[].Type == "Error"`, not `isError`** (§4.5).
- **`node-create` does not take a mesh.** Create → `node-modify` mesh → `scene-save`.
- Extension tools (GridMap/CSG/Particles) are **not installed** (P-C). Budget the installs.
- **Prefer W→H for assembly** (§4.9): have Murzak write the builder, run it headless.

## §9 — For the conductor

**No HALT was triggered.** No `sudo`, no machine-wide install, no write into a product repo,
no Gatekeeper block, and the editor came up on the second *diagnosed* route with the first
already reaped.

**Three things I think are worth a ruling or a ledger entry:**

1. **The Cloud default (§4.1) is a Q45 matter and I think it is Matt's, not mine.** Two
   separate components of a tool we are evaluating dial a third party by default, and one
   of them transmits machine and project identity **before any tool call**. Self-hosting
   holds only because we set four environment variables. That is a real property of the
   instrument and it should be on the record when Murzak is scored, not buried in a
   launch procedure.
2. **The latency correction (§4.4) supersedes a banked L3 finding and touches TCP-15.**
   "14× spread between instruments" is withdrawn. Murzak ≈ Pro ≈ 8 ms. Someone should
   decide whether TCP-15 gets amended or a TCP-19 gets written; that is above my seam.
3. **Charter defect §5.1 generalizes past this lap.** Every future lap that touches
   `Assets/` inherits a blast-radius predicate that cannot see the writes it most needs to
   see. The fingerprint check is cheap and I would make it standing.

**Honorable-fallback status (L-F/L-G):** nothing hit a ceiling that needed one. The two
things that *did* fail — the Cloud default and the ResourceRef schema gap — are named with
their exact blocking artifacts (§4.1 verbatim log lines, §4.6 verbatim error text) and both
were routed around rather than worked around.

---

## Artifact index

**Report:** `agentic_orchestration/drax/notes/2026-07-24-tcp-l3-murzak-standup-run-report.md`

| Artifact | Path (all under `~/Games/mcp-lab/`) |
|---|---|
| Live manifest, L3a GUI | `evidence/MUR_LIVE_MANIFEST.json`, `evidence/MUR_LIVE_TOOLNAMES.txt` |
| Live manifest, L3b headless | `evidence/MUR_LIVE_MANIFEST_L3b_headless.json` |
| Extension catalog (P-C) | `evidence/extension_catalog_summary.txt` |
| Cloud default — client config | `evidence/mcp.json.setup-mcp-DEFAULT-CLOUD` |
| Cloud default — addon boot | `evidence/CLOUD_DEFAULT_addon_boot.txt` |
| Latency ledger | `evidence/LATENCY_L3b_headless.txt` |
| Blast-radius baseline | `evidence/BLAST_BASELINE_reincarnated-godot.txt` |
| Asset fingerprint (P-E) | `evidence/PE_pack_fingerprint_BEFORE.txt` |
| **Frames** | `evidence/frames/BUILT_wire_authored_builder.png`, `PROOF_wire_node_crud.png`, `CLEAN_wire_node_crud.png` |
| Single-editor launcher / reaper | `bin/editor_up.sh`, `bin/editor_down.sh` |
| MCP client | `bin/mur_mcp_client.mjs` |
| Authoring plans | `bin/proof_stage_a.jsonl`, `bin/proof_stage_b.jsonl`, `bin/script_probe.jsonl`, `bin/burst.jsonl`, `bin/mesh_persist.jsonl` |
| **Murzak-authored builder (W→H)** | `project/tcp_l3b_builder.gd` |
| Builder output | `project/tcp_l3b_built.tscn` |
| Wire-authored scenes | `project/tcp_l3b_proof.tscn`, `tcp_l3b_clean.tscn`, `tcp_l3b_burst.tscn` |
| Capture rig (drax-authored) | `project/tcp_l3b_shoot.gd`, `tcp_l3b_shoot.tscn` |
| Import timings (P-E) | `logs/pe_import_timing.txt`, `logs/pe_import_warm_timing.txt` |
| Uninstall procedure | `UNINSTALL.md` |

**Signed:** drax, 2026-07-25 (presentation seam).
