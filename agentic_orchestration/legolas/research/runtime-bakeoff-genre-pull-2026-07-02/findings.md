# Runtime Bake-off Genre Pull — findings (legolas, Mode A)

> **CAPTURE NOTE (gandalf, 2026-07-02):** legolas (sub-agent, Mode A) returned these findings as text with
> the directory created but the file unwritten (environment policy blocked the sub-agent write — same
> behavior as the proxy-pairing pull earlier this session). gandalf durable-captured verbatim; authority is
> legolas-authored. Commission: Matt-approved 2026-07-02, briefed by gandalf during the runtime/bake-off
> Pattern-B dialogue (Godot vs three.js/R3F+Rapier web stack; spatial-assembly tooling; web-on-Steam
> postmortems; agent-in-editor corroboration; Godot headless/CI state).

---

# Research — Runtime Bake-off Genre Pull — 2026-07-02

**Mode:** A (analytical)
**Commissioner:** gandalf (design steward)
**Authorization:** Matt-approved 2026-07-02
**Sources consulted:** See Source List. Web search conducted 2026-07-02.

---

## Summary

The web/three.js ecosystem has credible spatial-assembly tooling (Theatre.js, GodotIQ-class patterns, Babylon.js Editor) but none closes the gap with Godot's in-editor MCP loop for bone-attachment and walking-pace work — the decisive advantage remains with a live editor that can render and verify in real time. Web-tech-on-Steam has a clear shipping track record (CrossCode via NW.js, Vampire Survivors via Electron, then migrated off), but player-visible performance ceilings are documented and Steamworks integration requires a specific thin-bridge library (steamworks.js is now preferred over the semi-abandoned greenworks). three.js/R3F + Rapier is viable for ARPG-density gameplay but skeletal animation retargeting for Synty FBX rigs is a solved-but-manual step with no out-of-the-box tooling equivalent to Godot's import pipeline. The agent-in-editor pattern is well-corroborated externally for structural scene work; the evidence is thinner for fine-grained spatial tasks (bone attachment, shading iteration). Godot's headless/CI tooling has a known gap: `--headless` disables rendering, so `--write-movie` and screenshot-diff regression require a virtual display (xvfb) workaround that has documented Vulkan compatibility problems.

---

## Item 1: Spatial-Assembly Tooling in the Web/three.js Ecosystem

### drei (TransformControls / PivotControls)

drei's `<TransformControls>` wraps THREE.TransformControls and exposes translate/rotate/scale gizmos inside a React Three Fiber scene. It auto-disables orbit controls during drag, supports object-prop targeting, and is the de-facto gizmo layer for R3F scenes [source 1, 2]. PivotControls (also drei) provides per-axis handle widgets for precise positioning. Both operate at runtime in a browser tab — they are interactive but not persisted; state must be read back via `onChange` and serialized manually. There is no built-in "export to file" step.

EVIDENCE: These tools are designed for runtime interaction, not authoring-session persistence. An agent or human can drag objects and read back transform matrices, but writing those values into a scene file is an additional implementation step.

INFERENCE: Drei gizmos are suitable for rough placement passes but not a drop-in replacement for Godot's `.tscn` scene round-trip, which persists automatically.

### Theatre.js

Theatre.js is a motion-design editor that overlays a timeline Studio UI on a running three.js or R3F scene. It serializes its state to a JSON project file (`.theatre-project-state.json`) that is plain text and version-controllable [source 3, 4, 5, 6]. Programmatic state export is supported via `IProject.exportState()`. An agent can read and write the JSON file directly without ever opening the browser Studio. The Studio can be embedded (`@theatre/studio`) in development builds and stripped from production.

EVIDENCE: The JSON state file is a clean-text artifact; it records object transforms, animation keyframes, and tweakable props. An agent writing JSON can modify these values without a browser UI.

INFERENCE: Theatre.js is the closest the web ecosystem comes to an agent-editable, persisted spatial-state format. However, it is NOT a scene graph editor — it tweaks values on objects placed by code; it does not place objects itself. Bone-attachment positioning still requires code to implement; Theatre.js could parametrize the offset once coded, but the initial bone-offset discovery still requires visual iteration.

EVIDENCE GAP: No field reports found of agents driving Theatre.js JSON state as part of a game-authoring loop. This is an untested pattern as of this pull.

### three.js Editor (official)

The official three.js editor (editor.threejs.org) is a full-featured browser scene editor — objects, lights, materials, geometry, scripts — exporting to a JSON scene format. It is architecturally separate from the R3F ecosystem and does not integrate with React component trees. No documented agent/MCP integration was found.

### Babylon.js Editor / Sandbox

Babylon.js Editor (editor.babylonjs.com) is a full production scene editor with drag-and-drop asset placement, material editors, animation editors, and script attachment [source 9]. Per the Babylon.js 9.0 blog post (Windows Developer Blog, April 2026): "the entire game was created 100% with the Babylon.js Editor" [source 10] — confirmed shipped-game use. The Node Render Graph Editor supports visual or programmatic pipeline composition. Babylon.js 9.0 released April 2026 with OpenPBR and improved API ergonomics.

EVIDENCE: If the project were on Babylon.js rather than three.js/R3F, the editor gap would be substantially smaller. This is corroboration that the web lane carries a real spatial-tooling cost relative to Godot — the best native-web editor requires adopting a different renderer.

### Needle Engine

Needle Engine exports Unity scenes (hierarchy, bones, materials, animations) to glTF bundles, running on a three.js-based web runtime [source 7, 8]. Authoring happens inside Unity Editor with full inspector, bone-attachment UI, and Unity's tooling surface. The glTF export includes skeletal animation, lightmaps, PBR materials, and custom TypeScript components.

EVIDENCE: Needle Engine is the only currently-maintained solution that provides Unity-editor-level spatial authoring ergonomics outputting to a web runtime. Authoring is human-in-Unity-Editor; the TypeScript component side is scriptable. It does not solve agent-driven spatial authoring — it solves human spatial authoring.

### Sub-question answers

**(a) Bone-attachment / walking-pace / shading-tweak with live feedback:** The web ecosystem has no peer to Godot MCP's live editor loop for these tasks. Theatre.js + drei + custom tooling can approximate it but requires assembly work the team would build. Needle Engine via Unity provides it but adds Unity as a required tool. Babylon.js Editor provides the closest native-web equivalent but requires adopting Babylon.js as the renderer.

**(b) Agent-driven programmatically:** Theatre.js JSON state is agent-writable. Babylon.js and three.js have JavaScript APIs accessible from Node/headless contexts, but no documented MCP server for either was found. No web-renderer MCP server equivalent to Godot MCP Pro / GodotIQ was found.

**(c) Persists as clean text an agent can also edit:** Theatre.js project state JSON is the only clean-text artifact found in an active R3F-compatible workflow. The three.js editor JSON scene format is a second candidate but is not part of an R3F production stack.

---

## Item 2: Web-Tech-on-Steam Shipping Postmortems

### CrossCode (Radical Fish Games, NW.js)

CrossCode shipped on Steam using a custom engine originally based on impact.js (heavily modified) running under NW.js. Rendering is pure canvas2D — no WebGL [source 12, 13, 14, 15]. NW.js was actively updated post-ship. Performance issues and framerate drops are documented in Steam community discussions, particularly in fullscreen mode and on certain GPU configurations.

Console porting was the known hard wall: Deck13 compiled the JavaScript codebase to C++ ahead-of-time (AOT) to achieve 60fps on Switch — a significant R&D investment, not a commodity workflow [source 16].

EVIDENCE: CrossCode proves a web-tech game can ship on Steam and succeed commercially. It also proves that AOT JS-to-native is the console port path — not just a deploy to native renderer.

### Vampire Survivors (poncle, Electron → migrated off)

Vampire Survivors shipped on Steam built on Electron. Performance issues were documented by players — framedrops and slowdown despite simple 2D graphics [source 17]. poncle publicly migrated to a new engine with the stated motivation of "increased performance and compatibility for more machines," keeping the old Electron build as opt-in.

EVIDENCE: This is the most prominent public case of Electron performance ceiling being the direct motivation for engine migration on a commercially successful Steam title. If Electron struggles with low-complexity 2D at scale, a 3D ARPG is a materially more demanding ask.

### Steamworks Integration: steamworks.js vs greenworks

Greenworks is semi-abandoned and not up to date with the current Steamworks SDK [source 19]. steamworks.js (written in Rust) is the actively maintained successor, with the creator's explicit motivation being that greenworks was "not maintained anymore and not up to date" [source 18, 20].

EVIDENCE GAP: Tauri is NOT listed as a supported target for either greenworks or the main steamworks.js distribution in the search results. No confirmed shipped Steam title using Tauri + steamworks.js was found. This is a real integration risk for the web lane if Tauri is chosen.

### Tauri vs Electron

Tauri 2.0 (late 2024) produces ~10MB installers and ~30–50MB RAM vs Electron's 80–150MB installers and 150–300MB RAM [source 21, 22]. Three.js/R3F with WebGL should work in Tauri's WebKit WebView, but WebKit's WebGL2 support has historically lagged Chromium's, and Electron ships Chromium — a known-good WebGL2 runtime. For a 3D ARPG demo targeting precise rendering parity, Electron's Chromium provides a more predictable baseline.

INFERENCE: For this bake-off, Electron + steamworks.js is the lower-risk web-lane wrapper stack. Tauri's bundle/RAM advantage is real but its Steamworks integration path is unproven and its WebKit WebGL2 behavior under the Metal renderer on macOS needs empirical verification before committing.

---

## Item 3: three.js/R3F + Rapier Maturity for ARPG-Density Gameplay

### Skeletal Animation: AnimationMixer

three.js AnimationMixer handles glTF skeletal animation natively [source 29]. Synty's default export format is FBX; conversion to glTF requires fbx2gltf or Blender's FBX→glTF pipeline. Synty rigs follow Unity/Humanoid-convention skeleton topology; retargeting to a different skeleton in three.js requires manual bone-mapping — there is no built-in retargeter equivalent to Unity's Humanoid Retargeting. A lightweight library for Mixamo→VRM retargeting exists [source 30] but there is no Synty-to-arbitrary-rig library ready to use.

EVIDENCE: The FBX→glTF conversion step is mature and documented. The retargeting step for Synty rigs specifically has no ready-made library — it is a one-time authoring cost per character set, not a structural blocker, but real work the team would need to do.

### Rapier Determinism

Rapier's WASM/TS/JS build is documented as cross-platform deterministic under a fixed timestep loop [source 23]. Variable frame rates prevent full determinism. For a 60s bake-off play loop using `fixedUpdate` pattern, the determinism claim holds.

### NavMesh: recast-navigation-js

recast-navigation-js is a WebAssembly port of Recast Navigation (the industry-standard navmesh toolkit used in Unity and Unreal) [source 24]. The `@recast-navigation/three` integration package provides DebugDrawer and three.js helpers [source 25]. The library is active and cross-framework (also referenced in Babylon.js forums). This is the correct navmesh solution for a three.js ARPG.

### VFX / Particles

- **vfx-composer** (hmans/composer-suite): GPU-side InstancedMesh particle system, compiles to shaders via Shader Composer, R3F-idiomatic [source 26].
- **Three.Quarks**: High-performance general-purpose VFX library, cross-framework, with an online particle system designer at quarks.art [source 27]. Most full-featured option.
- **wawa-vfx**: Modular R3F VFX system designed for production use [source 28].
- **three-nebula**: Older widely-referenced particle system, less actively maintained.
- **three-vfx** (nikolai-sim): Explicitly WIP; not production-ready.

INFERENCE: Three.Quarks is the most full-featured option with an out-of-browser designer. vfx-composer is most R3F-idiomatic. Neither matches Godot's visual VFX node editor, but both can produce hit/cast effects for a proxy ARPG demo.

### Shipped ARPG Precedent

No commercially shipped 3D ARPG on R3F + Rapier was found. The closest: an isometric browser RPG ("Eidolon," alpha v0.17, December 2025) built with three.js [source 31]. Educational shooters and puzzle games on R3F are documented; multiplayer games using R3F + WebSockets have been presented at conference talks. The 6-monster ARPG density scale is well within THREE.InstancedMesh capability; the bake-off would be generating the first known vertical-slice evidence for this class.

---

## Item 4: Agent-in-Editor Precedent (External Corroboration)

### Godot MCP Landscape (2026)

Four active Godot MCP servers found:
- **Coding-Solo/godot-mcp** [source 35]: Free, open-source; launches editor, runs projects, captures debug output.
- **IvanMurzak/Godot-MCP** [source 36]: 39 tools across 11 families; scene/node control, script attachment, visual feedback, C# + GDScript.
- **godot-mcp-pro** (youichi-uda) [source 37]: 162 tools across 23 categories ($15); covers scene, animation, 3D, physics, particles, audio, shader, input simulation, runtime analysis, navigation, testing.
- **GodotIQ** (salvo10f) [source 32, 33, 34]: 35–38 tools with explicit "spatial intelligence" framing. Smart Placement finds designer-intended Marker3D slots first (95% confidence), falls back to constraint-solving grid search. Screenshot + camera controls provide a visual verification loop. Demo: agent given one prompt built a "living city" in Godot 4.

EVIDENCE: GodotIQ's Smart Placement is direct external corroboration that spatial assembly is a solvable MCP tool class when the editor returns visual state (screenshots) as feedback signals. The ecosystem expanded from a handful to 11+ serious options in 18 months (per Ziva 2026 comparison, source 41).

### In-Editor vs File-Authoring Distinction (External)

Josh English (Medium, "Advanced Agentic Game Development in Unity with MCP") [source 38]: "when Unity is put behind MCP, the agent can query the project rather than hallucinate it — the difference between AI-assisted coding and AI-native game development. MCP turns the Unity Editor into an addressable tool surface where actions are explicit, inputs are structured, outputs are inspectable."

Codex CLI article (April 2026) [source 40]: "Game-engine MCP servers expose editor APIs as tools agents call, allowing agents to invoke operations like 'create scene' and 'attach script' via JSON-RPC instead of hand-writing code."

mcp.directory 2026 comparison [source 39]: Godot MCP produces `.tscn` + `.gd`; Unity MCP produces `.unity` + `.cs`. Both require a running editor process.

EVIDENCE: External literature unanimously frames in-editor agent operation as qualitatively superior to file-authoring for scene work. No published comparison found arguing for file-authoring winning on spatial tasks.

### Bone Attachment / Fine-Grained Spatial (Specific)

godot-mcp-pro lists 3D and animation as tool categories; GodotIQ demonstrates constraint-solving object placement. However, no published case study or postmortem documenting an agent successfully completing bone-attachment work (e.g., placing a weapon into a specific skeleton bone socket) purely through an MCP loop without human verification was found.

INFERENCE: External corroboration is strong for broad structural scene assembly; it is weaker (evidence gap, not refutation) for fine-grained skeletal attachment tasks. Our project's internal finding that the editor wins for spatial-perceptual work is consistent with all external evidence found; no refutation was found.

---

## Item 5: Godot Headless/CI Regression Tooling

### What Works: Logic-Layer Testing

`godot --headless` (Godot 4.x) uses the dummy display server and audio driver; runs on agents with no GPU or display. Well-suited for: GDScript unit tests (GUT, GdUnit4), resource validation, scene instantiation smoke tests, export pipeline checks. GUT + CI (GitHub Actions) is documented and in production use [source 42, 43, 48].

EVIDENCE: Logic-layer CI is mature and reliable.

### The Rendering Gap

`--headless` explicitly disables all rendering code. Consequences:
- `--write-movie` (MovieWriter) requires a rendered window — incompatible with `--headless`.
- Screenshot capture (`get_viewport().get_texture().get_image()`) requires a rendered frame, which requires a display.
- 3D scene visual regression (pixel-diff) cannot run in pure headless mode.

This gap is tracked upstream in godot-proposals issue #5790, which requests an `--offscreen` CLI argument for render farms, automated benchmarking, and CI visual regression [source 44]. As of this pull, the proposal is open — the feature has not shipped in stable.

### xvfb Workaround and Its Limits

Running Godot under xvfb (virtual X11 framebuffer) with a software Vulkan fallback (lavapipe) on Linux CI is the documented workaround. However, compatibility is documented as problematic: Godot 4.x (Vulkan) with `xvfb-run + lavapipe` on Ubuntu has confirmed issues [source 45]. The workaround works on some configurations and fails on others. An alternative (`--rendering-driver opengl3` + xvfb) sidesteps the Vulkan issue but differs from the Forward+/Metal renderer used in the production scene (the project targets macOS).

### MovieWriter (`--write-movie`) Practical Use

MovieWriter records a scene to disk (PNG frames or video) at non-real-time rates (each frame fully rendered before advancing). Requires a spawned window — cannot be used in true headless mode [source 46]. On macOS (Metal/Forward+) it operates normally in a standard windowed run. The team can use `--write-movie` for manual capture passes but not for headless CI automation.

### Practical Gap Summary for the Bake-off

"Headless capture" of the Godot lane is not achievable with `--headless` today. Options ranked by friction:
1. MovieWriter in windowed mode on the Mac dev machine — manual, not CI-automated; low friction for a bake-off.
2. GdScript screenshot capture to disk at frame checkpoints in windowed mode — scriptable, not truly headless.
3. xvfb + lavapipe on a Linux CI agent — requires testing for Godot 4.x/Vulkan compatibility before trusting results.
4. Wait for the `--offscreen` proposal to land in Godot stable — timeline unknown.

For the bake-off specifically (a one-time 60s loop capture), option 1 is the pragmatic path. The CI regression gap is a production concern rather than a bake-off blocker.

---

## Knowledge Gaps Not Resolved

1. **No shipped 3D ARPG on R3F + Rapier found.** The bake-off would be generating first-known vertical-slice evidence for this class.

2. **Tauri + steamworks.js integration unverified.** No confirmed shipped Steam title using this wrapper combination was found. Real risk if Tauri is chosen over Electron.

3. **Synty FBX → glTF + three.js skeletal retargeting.** No Synty-specific pipeline guide found for three.js. Bone-name mapping for Synty's humanoid convention would need hands-on verification.

4. **Agent-driven bone attachment via MCP (fine-grained).** No published case study found. Corroboration exists for broad structural placement, not skeletal socket attachment specifically.

5. **Theatre.js as agent spatial-state layer.** JSON-editable state is documented; no agent-authoring loop using it for game-scene spatial work found in the literature.

6. **Godot `--offscreen` proposal (issue #5790).** Open as of this pull. Check current godotengine.org changelog — may have landed in a 4.x dot release since the search date.

---

## Source List

| # | Source | URL | Type |
|---|--------|-----|------|
| 1 | drei TransformControls docs | https://drei.docs.pmnd.rs/gizmos/transform-controls | Primary |
| 2 | three.js TransformControls docs | https://threejs.org/docs/pages/TransformControls.html | Primary |
| 3 | Theatre.js Projects docs | https://www.theatrejs.com/docs/latest/manual/projects | Primary |
| 4 | Theatre.js @theatre/core API | https://www.theatrejs.com/docs/latest/api/core | Primary |
| 5 | Theatre.js Studio docs | https://www.theatrejs.com/docs/latest/manual/studio | Primary |
| 6 | Theatre.js GitHub | https://github.com/theatre-js/theatre | Primary |
| 7 | Needle Engine docs | https://engine.needle.tools/docs/unity/ | Primary |
| 8 | Needle Engine GitHub | https://github.com/needle-tools/needle-engine-support | Primary |
| 9 | Babylon.js Editor | https://editor.babylonjs.com/ | Primary |
| 10 | Babylon.js 9.0 (Windows Dev Blog, April 2026) | https://blogs.windows.com/windowsdeveloper/2026/04/02/part-3-babylon-js-9-0-openpbr-and-additional-engine-updates/ | Primary |
| 11 | three.js vs Babylon.js 2026 | https://www.utsubo.com/blog/threejs-vs-babylonjs-vs-playcanvas-comparison | Secondary |
| 12 | CrossCode PCGamingWiki | https://www.pcgamingwiki.com/wiki/CrossCode | Secondary |
| 13 | CrossCode NW.js update (Radical Fish Games blog) | https://www.radicalfishgames.com/?p=6904 | Primary |
| 14 | CrossCode tech discussion (Steam community) | https://steamcommunity.com/app/368340/discussions/0/1291817208507901095/ | Community |
| 15 | CrossCode / ImpactJS (devrant) | https://devrant.com/rants/7517787/ | Community |
| 16 | CrossCode console port interview (Siliconera) | https://www.siliconera.com/crosscode-interview-radical-fish-games-on-console-ports-and-whats-next/ | Primary (dev interview) |
| 17 | Vampire Survivors / new engine (PC Gamer, PCGamingWiki) | https://www.pcgamingwiki.com/wiki/Vampire_Survivors | Secondary |
| 18 | steamworks.js GitHub | https://github.com/ceifa/steamworks.js/ | Primary |
| 19 | greenworks GitHub | https://github.com/greenheartgames/greenworks | Primary |
| 20 | Web Game Dev — Desktop publishing | https://www.webgamedev.com/publishing/desktop | Secondary |
| 21 | Tauri vs Electron 2026 | https://tech-insider.org/tauri-vs-electron-2026/ | Secondary |
| 22 | Tauri vs Electron technical (gethopp.app) | https://www.gethopp.app/blog/tauri-vs-electron | Secondary |
| 23 | Rapier determinism docs | https://rapier.rs/docs/user_guides/javascript/determinism/ | Primary |
| 24 | recast-navigation-js GitHub | https://github.com/isaac-mason/recast-navigation-js | Primary |
| 25 | @recast-navigation/three npm | https://www.npmjs.com/package/@recast-navigation/three | Primary |
| 26 | vfx-composer GitHub | https://github.com/hmans/vfx-composer | Primary |
| 27 | Three.Quarks GitHub | https://github.com/Alchemist0823/three.quarks | Primary |
| 28 | wawa-vfx | https://wawasensei.dev/blog/wawa-vfx-open-source-particle-system-for-react-three-fiber-projects | Primary |
| 29 | AnimationMixer three.js docs | https://threejs.org/docs/pages/AnimationMixer.html | Primary |
| 30 | Mixamo→VRM retargeter | https://github.com/saori-eth/vrm-mixamo-retargeter | Primary |
| 31 | Isometric RPG / Eidolon (DEV Community, Dec 2025) | https://dev.to/mendolatech/how-i-built-a-browser-based-isometric-rpg-with-threejs-1j82 | Primary (dev blog) |
| 32 | GodotIQ forum post | https://forum.godotengine.org/t/godotiq-mcp-server-that-gives-ai-agents-spatial-intelligence-for-godot/135304 | Primary |
| 33 | GodotIQ GitHub | https://github.com/salvo10f/godotiq | Primary |
| 34 | GodotIQ living city demo (DEV Community) | https://dev.to/salvo10f/i-gave-an-ai-agent-one-prompt-and-it-built-a-living-city-in-godot-4-3mlm | Primary (dev blog) |
| 35 | Coding-Solo/godot-mcp GitHub | https://github.com/Coding-Solo/godot-mcp | Primary |
| 36 | IvanMurzak/Godot-MCP GitHub | https://github.com/IvanMurzak/Godot-MCP | Primary |
| 37 | godot-mcp-pro GitHub | https://github.com/youichi-uda/godot-mcp-pro | Primary |
| 38 | Unity MCP — Josh English (Medium) | https://medium.com/@jengas/advanced-agentic-game-development-in-unity-with-mcp-5add91c579e9 | Secondary |
| 39 | Godot vs Unity vs Blender MCP 2026 (mcp.directory) | https://mcp.directory/blog/godot-vs-unity-vs-blender-mcp-skills-2026 | Secondary |
| 40 | Codex CLI — Unity/Godot MCP agent workflows (Apr 2026) | https://codex.danielvaughan.com/2026/04/27/codex-cli-game-development-unity-godot-mcp-agent-driven-workflows/ | Secondary |
| 41 | Best AI tools for Godot 2026 (Ziva) | https://ziva.sh/blogs/best-ai-tools-for-godot-2026 | Secondary |
| 42 | Godot CI testing (saltares.com) | https://saltares.com/run-automated-tests-for-your-godot-game-on-ci/ | Secondary |
| 43 | Godot headless test fix (bugnet.io) | https://bugnet.io/blog/how-to-fix-godot-headless-test-run-fails-in-ci | Secondary |
| 44 | Godot offscreen rendering proposal #5790 | https://github.com/godotengine/godot-proposals/issues/5790 | Primary (upstream) |
| 45 | Godot xvfb Vulkan issue #38428 | https://github.com/godotengine/godot/issues/38428 | Primary (upstream) |
| 46 | MovieWriter Godot docs | https://docs.godotengine.org/en/stable/classes/class_moviewriter.html | Primary |
| 47 | Godot regression-test-project | https://github.com/godotengine/regression-test-project | Primary |
| 48 | GdUnit4 Godot Asset Library | https://godotengine.org/asset-library/asset/1522 | Primary |

---

**Note to commissioner (gandalf):** The write call to `agentic_orchestration/legolas/research/runtime-bakeoff-genre-pull-2026-07-02/findings.md` was blocked by environment policy. The directory was created successfully at `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/runtime-bakeoff-genre-pull-2026-07-02/`. The full findings text above is the durable artifact — please capture it per your workflow. Commission is complete.
