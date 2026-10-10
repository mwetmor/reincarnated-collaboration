# Barrow arena web repair — 2026-10-10

Authority: Matt asked Codex to finish Claude's fixes after Claude credits ran out. Codex adopted drax's implementation seam. This is the completion record for the Claude-to-Codex handoff; no internal subagents were used.

The web export now mounts the auxiliary packs before selecting the site's painted manifest. Downloads drain in 1 MiB chunks, report their status, and stop visibly on a failed request or mount. The presentation session explicitly chooses the runtime's GDScript contact solver only for the specific Web.wasm32 native-library-unavailable refusal. The generated PCK extension startup list is empty on Web; sealed native-extension files are still present and unchanged. Enemy effects ship their existing atlas bytes in a separate pack, with page digests checked before decoding. The arena removes the exploration scene's inherited touch controls.

Sealed inputs remain pinned and byte-verified at launch:

- Runtime tree: `a0e75469a78b3b81d979d9d525e0bbf1c5324459260c62110192878c33a53f1c`
- Model pack: `997117278c1e28dac0da9a6cf64ddaf72111347094a7ac5e3b4c03590507d788`

Verification uses an empty project folder with the exported PCK and an actual Chrome/WebAssembly launch. The browser harness waits for shader warm-up and observes opt-in `?probe=1` state while exercising movement, held/released Whirlwind, skills and zoom. It covers desktop mouse/keyboard, emulated landscape touch, and an intercepted HTTP 404. Screenshots and full console/network records are saved beside each test. This is touch emulation on a Mac, not a physical phone test.

Known limitations: the pinned runtime emits the same non-fatal `Unexpected NUL character` decoder messages in its earlier native launch log and the web build. The harness records those exact messages and rejects other errors. Initial boot includes a substantial runtime/model load and shader warm-up (roughly 45–50 seconds on this Mac on localhost); this repair does not establish phone performance or native/reference solver parity. Export size is 385,183,671 bytes across the page and ten auxiliary packs; largest file is `vfx_0.pck`, 41,429,056 bytes.

A clean rebuild is `bash tools/build_web_arena.sh`; it retains the existing 26 GiB disk gate and heavy-process lock. For this repair, existing byte-verified asset packs were retained and the main/VFX packs re-exported under the lock. The whole clean script was not rerun because available disk had fallen below its gate. Syntax checks, the isolated packed-input check, actual browser tests, and the loadout Vite production build cover the repaired output.

The Windows ZIP is feasible as a separate native export, but is not produced by this web repair. It still needs Windows solver selection and portable leech-table/runtime paths, then a Windows launch test. The current native library is macOS.arm64 only.

Protected-preview testing uses the linked loadout project's development OIDC credentials. AudioWorklet fetches do not inherit the browser automation's custom headers, so the optional `VERCEL_CLI_PATH` hook uses `vercel curl` to obtain an ordinary same-origin bypass session cookie in memory. Tokens/cookies are never written to evidence or source. Use `VERCEL_CLI_USE_NATIVE_BINARY=0` with CLI 63.1.2's `env run`: the native variant incorrectly re-entered its deploy command when asked to run Node. The incidental `barrow-oidc-check` project was deleted and its deletion confirmed by HTTP 404.

Final hosted verification: Vercel preview `dpl_8CGFbFqDzh9E1g42MjFSnPP7Ww8B`, loadout branch `codex/c9-arena-web` at `5aa8673`. URL: https://reincarnated-loadout-5i1cmo8xq-matthew-wetmore-s-projects.vercel.app/playtest/barrow-arena/ . The hosted desktop test passed, including audio module loading. The downloaded main PCK and audio worklet hash-equal the staged build. Local desktop, landscape touch and missing-pack tests passed; the isolated pack probe reported bundle intact. Evidence is retained in `web_arena/build/logs/verified/` (generated, gitignored). This is a preview deployment; production main was not changed.
