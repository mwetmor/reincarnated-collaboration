# Dispatch — spike: `godot-lsp-cli diagnostics` + gdlint as a pre-freeze static gate for the burst lane (Matt-approved R-C7-15 (2))

**From:** gandalf (RUN-CONDUCTOR, Run C-7) · **To:** drax · **Authorization:** Matt 2026-09-19, R-C7-15 (2) — adoption 2 of `agentic_orchestration/gandalf/notes/2026-09-19-reddit-harness-thread-assessment.md`. **Bounded: ≤ 45 minutes of work; read-only against every project; nothing under `astra_test_01/burst/` is modified; no install into any repo — global npm/pip only (`npm i -g godot-lsp-cli`; `pipx install gdtoolkit` or the Somni fork `github.com/SomniGameStudios/godot-gdscript-toolkit`).**

**Question the spike answers:** does a STATIC GDScript pass catch defect classes our runtime probes found late this run — F-C7-1 (null-instance calls down a wrong dispatch path in `vfx_g2.gd`), F-C7-2 (a `load("res://…/materials/Additive.tres")` for a file the kit never emits; our dangling-`res://` fence walks `.gdshader` only) — or anything else the outside suite misses?

**Procedure:**
1. **Memory law:** any Godot instance (the LSP needs one — use `godot-lsp-cli`'s managed headless instance, not the editor GUI) runs under the shared advisory lock: `python3 astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py drax -- <cmd>`. One instance at a time. `df -h /` before and after.
2. Targets: (a) `astra_test_01/burst/runs/C-7/cliffside_v45` (the staged 19-kit project, READ ONLY — copy it to a scratch dir if the LSP writes anything); (b) `~/Games/reincarnated-godot` (your own project).
3. Run `godot-lsp-cli diagnostics --project <dir> --json` over every `.gd`; run `gdlint` over the same set; run `gdformat --check` (report only). Record counts by severity and the exact messages for `vfx_g2.gd`, `vfx_g2_flipbook.gd`, `keeper.gd`, `vfx_g1*.gd`.
4. Deliberately re-introduce F-C7-1's shape in the scratch copy (call a method on a null-typed variable down an untaken branch) and F-C7-2's shape (a `load()` of a non-existent `res://`) and see whether either tool flags them. Revert.
5. Time each command; note whether the managed instance leaves processes or files behind.

**Deliverable:** `agentic_orchestration/drax/notes/2026-09-19-godot-lsp-cli-gate-spike.md` — a table (tool · target · errors · warnings · wall time · caught F-C7-1 shape? · caught F-C7-2 shape?), the raw JSON under `agentic_orchestration/drax/captures/2026-09-19-lsp-spike/`, and ONE recommendation: adopt as a freeze gate (and what exact command line the conductor's `verify.sh` should run), adopt as advisory only, or drop — with the reason. Commit with `git commit --only` on those paths (attribution per the system reminder). Return ≤ 150 words.
