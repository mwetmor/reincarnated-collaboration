# Spike — `godot-lsp-cli diagnostics` + gdtoolkit as a pre-freeze static gate for the burst lane

**Date:** 2026-09-19 · **Author:** drax (presentation seam) · **Status:** CURRENT (spike finding; recommendation for conductor)
**Dispatch:** `agentic_orchestration/drax/dispatches/2026-09-19-godot-lsp-cli-gate-spike.md`
**Authorization:** Matt 2026-09-19, R-C7-15 (2) — adoption 2 of `agentic_orchestration/gandalf/notes/2026-09-19-reddit-harness-thread-assessment.md`
**Captures:** `agentic_orchestration/drax/captures/2026-09-19-lsp-spike/`

---

## 0. Top line

**Neither outside tool catches either defect shape this run found late.** gdlint caught **0 of 4** probes. The Godot LSP caught **1 of 4** — and the one it caught is `preload()`, which is *not* the form F-C7-2 took (our kits emit `load()`).

The finding that pays for the spike is a different one: **`godot-lsp-cli diagnostics --project <dir>` returns `{}` on every project. It is a no-op**, and would have installed a silently-passing gate. Godot's LSP does answer the question — but only over a `textDocument/didOpen` sweep the CLI never performs.

---

## 1. Tooling installed (global only; nothing entered any repo)

| Tool | Version | Install |
|---|---|---|
| `gdtoolkit` (`gdlint` / `gdformat` / `gdparse`) | 4.5.0 | `pip3 install gdtoolkit` (no pipx on host) |
| `godot-lsp-cli` | 0.2.1 (SomniGameStudios) | `npm i -g --prefix ~/.npm-global` — `/usr/local/lib/node_modules` is root-owned; a user-level global prefix avoided `sudo` |
| Godot | `/Applications/Godot.app/Contents/MacOS/Godot` | already present |

---

## 2. Results table

Targets: **v45** = `astra_test_01/burst/runs/C-7/cliffside_v45` (70 `.gd`, run against a scratch copy; original byte-verified untouched) · **RG** = `~/Games/reincarnated-godot` (648 `.gd`).

| Tool | Target | Errors | Warnings | Wall time | F-C7-1 shape? | F-C7-2 shape? |
|---|---|---:|---:|---:|---|---|
| `gdlint` | v45 | 973 | 0 | **2.5 s** | **NO** | **NO** |
| `gdlint` | RG | 9 917 | 0 | **17.3 s** | **NO** | **NO** |
| `gdformat --check` | v45 | 70/70 files "would reformat" | — | 2.4 s | n/a | n/a |
| `gdparse` | v45 probes | 0 (exit 0) | — | <1 s | **NO** | **NO** |
| `godot-lsp-cli diagnostics --project … --json` | v45 | **0 — returns `{}`** | 0 | 2.5 s | **NO (no-op)** | **NO (no-op)** |
| `godot-lsp-cli diagnostics --project … --json` | RG | **0 — returns `{}`** | 0 | 2.5 s | **NO (no-op)** | **NO (no-op)** |
| LSP `didOpen` sweep (own driver) | v45 | 1 | 63 | **68 s** (4 s boot + 54 s sweep) | **NO** | **preload only** |
| LSP `didOpen` sweep (own driver) | RG | 566 | 324 | **591 s** (219 s boot + 357 s sweep) | **NO** | **preload only** |

**gdlint severity is a single class.** Every one of the 973 / 9 917 lines prints as `Error:`, and every one is a **style** rule. v45 breakdown: `max-line-length` 715, `class-definitions-order` 254, `max-returns` 2, `trailing-whitespace` 1. **Zero semantic findings on either project.**

**`gdformat --check` is 70/70 red on v45.** As a gate it is a constant fail until the lane is formatted once; it carries no defect signal at all.

### Named files the dispatch asked for (LSP sweep, v45, clean run)

| File | LSP diagnostics |
|---|---|
| `scripts/vfx_g2.gd` | 4 warnings — 2× `SHADOWED_VARIABLE_BASE_CLASS`, 1× `INCOMPATIBLE_TERNARY` (L210), 1× shadowed `for` iterator |
| `scripts/vfx_g2_flipbook.gd` | 2 warnings — `SHADOWED_VARIABLE_BASE_CLASS` (L103), `INCOMPATIBLE_TERNARY` (L159) |
| `scripts/keeper.gd` | **clean** |
| `scripts/vfx_g1_fl4.gd` / `_fl6.gd` / `_painted.gd` | 2 × `INTEGER_DIVISION` each |
| `scripts/vfx_g1.gd`, `vfx_g1_orb*.gd` | clean |

gdlint's counts for the same files are entirely line-length and member-ordering: `keeper.gd` 57, `vfx_g2.gd` 54, `vfx_g2_flipbook.gd` 41.

---

## 3. The defect-shape test

Four isolated probes in the scratch copy (`captures/…/defect_probes/`), each pointed at a `res://` path that genuinely does not exist in the kit (`lightning_blast_e3` and `zeus_chain_e3` are two of the three v45 kits that emit no `Additive.tres`):

| # | Shape | gdlint | gdparse | LSP sweep | `godot --check-only` |
|---|---|---|---|---|---|
| 1a | **F-C7-1 as it actually occurred** — null instance, *valid* method, down a branch never taken | no | no | **no** | no |
| 1b | adjacent — *unknown* method on a typed `Node2D`, same untaken branch | no | no | **no** | no |
| 2a | **F-C7-2 as it actually occurred** — `load()` of a missing `res://` | no | no | **no** | no |
| 2b | adjacent — `preload()` of the same missing path | no | no | **YES**, severity 1: `Preload file "…" does not exist.` | yes (stderr) |

gdlint's verdict on all four probe files was literally `Success: no problems found`.

**1a is unreachable by static analysis in principle** — the method exists on the type, and only flow analysis over an untaken branch would find it. No tool here claims that capability, and none should be expected to.

**1b is the surprise.** An unknown method on a *typed* variable is exactly what a GDScript analyzer should reject, and neither the LSP nor `godot --headless --check-only` reported it. Whatever depth F-C7-1's neighbourhood needs, this suite does not have it.

**2a vs 2b is the whole story for F-C7-2.** Godot resolves `preload()` at parse time and errors; `load()` is a runtime call over an opaque string and nothing inspects it. **Our kits emit `load()`.** So the one catch the suite does own sits on the form our lane does not use — and the existing dangling-`res://` fence, however narrow its `.gdshader` walk, is closer to the real defect than either new tool.

---

## 4. Gate-design findings (the part that would have bitten)

1. **`godot-lsp-cli diagnostics` never opens a file.** v0.2.1 `dist/cli.js` case `"diagnostics"` sleeps 2 s and reads whatever the server pushed unprompted — it does not call `ensureOpen()`, which is the only path that sends `textDocument/didOpen`. Godot publishes diagnostics *on open*. So the command returns `{}` **whether or not the project is broken**, and it exits **0**. Wiring the dispatch's literal command line into `verify.sh` would have added a gate that can never fail. Every number in the LSP rows above comes from a 120-line driver I wrote for this spike (`captures/…/spike_lsp.py`), not from the CLI.

2. **`godot --headless --check-only` exits 0 on a parse error.** Measured directly: `RC_ON_PARSE_ERROR=0`, `RC_ON_CLEAN=0`. Any gate built on it must parse stderr; exit code carries no signal.

3. **`res://` resolution is project-root-relative, so nested projects produce mass false positives.** All 41 `Preload file … does not exist` errors in the RG sweep are false — they come from `web/cliffside/`, a staged sub-project with **its own `project.godot`**, whose `res://scripts/vfx_g1.gd` resolves against *its* root, not the parent's. Scanned from the parent root every intra-subproject path looks dangling. A gate must point `--project` at the true project root of the thing being frozen.

4. **RG's raw error count is not a quality signal.** Of 566 errors, **509 are vendored** (`Assets/` Binbun VFX packs duplicated across `assets-2` … `assets-20`, plus `addons/`). First-party is 57 errors / 297 warnings, and the 41 false preloads are inside that 57. Any adopted gate needs a vendor-path exclusion before its number means anything.

5. **Indentation mix aborts the whole file, and cascades.** My first injection used tabs in a space-indented file. Result: `vfx_g2.gd` returned *only* 8 tab errors — every semantic check on the file was skipped — and `keeper.gd` then reported `Could not resolve script "res://scripts/vfx_g2.gd"`, a defect in a file nobody had touched. I re-ran clean rather than report the contaminated table (that run is kept as `v45scratch_lsp_tabcontaminated.json`). **A red gate line can mean "the file could not be read," not "the file is wrong"** — and one unparseable file poisons its dependents' results.

6. **The headless editor WRITES INTO THE PROJECT IT SCANS.** The scratch copy came back with two new files the original does not have — `probe_cast_ab.gd.uid` and `probe_events.gd.uid`, minted by Godot for the two scripts that lacked a `.uid` sidecar. Small and benign, but it settles the dispatch's "copy it if the LSP writes anything" clause as a real requirement, not a precaution: **any adopted gate must run against a copy, or it mutates the artifact being frozen.** (`.godot/` churn is expected and was excluded from the comparison; the `.uid` files are not in `.godot/` — they sit beside the scripts.)

7. **Memory-law behaviour was clean.** Every Godot instance ran under `heavy_lock.py drax`, one at a time, the lock held for the instance's whole lifetime (the driver spawns, sweeps, and terminates inside the hold; `godot-lsp-cli serve` would instead detach and drop the lock while Godot lives). `df -h /` unchanged across all four runs (76–77 Gi free). **No stray `godot` processes**, and in `reincarnated-godot` — which has a warm import cache — zero tracked files and zero `.godot/` writes. The v45 *original* is untouched: `diff -rq` against the pre-run copy reports nothing on the original side.

---

## 5. Recommendation — **ADVISORY ONLY. Do not make it a freeze gate.**

**The reason:** the suite does not catch what we asked it to catch. 0 of 4 for gdtoolkit, 1 of 4 for the LSP, and that one is a `preload()` form our kits do not emit. Against the two defects that actually cost us this run it would have been **silent** — and worse than silent, because a green line in `verify.sh` would have read as evidence the lane was clean. A gate that cannot fail on your real defect classes doesn't reduce risk; it launders it.

The cost side compounds it: 591 s and a 219 s Godot boot on RG for a number whose 90 % is vendored asset packs, plus a mandatory one-time format pass before `gdformat --check` stops being 70/70 red, plus a vendor-exclusion list and a per-subproject root map to suppress the false positives in § 4.3/4.4. That is real conductor maintenance for signal we have not yet seen it produce.

**What to do instead — one line, advisory, on the staged kit project only:**

```bash
# advisory: prints, never blocks; run from the staged project root (the dir holding project.godot)
gdlint --config <repo>/tools/gdlintrc.advisory $(find . -name '*.gd' -not -path './.godot/*') 2>&1 | tee gdlint.advisory.txt || true
```

with `gdlintrc.advisory` disabling `max-line-length`, `class-definitions-order`, `trailing-whitespace` and `max-returns` — the four rules that are 100 % of v45's 973 lines and carry no defect signal for generated kit code. What remains (`unused-argument`, `expression-not-assigned`, `duplicated-load`, `mixed-tabs-and-spaces`) is small, fast (2.5 s), needs no Godot instance, no lock, and no disk. Let it print for a few freezes; if it ever flags something a runtime probe later confirms, revisit promotion then — on that evidence, not on the tool's reputation.

**Do not wire `godot-lsp-cli diagnostics` into `verify.sh` in any form.** Until upstream opens documents before reading diagnostics, it reports `{}` and exits 0 on a broken project.

**The F-C7-2 class is better served by extending the fence we already own.** Our dangling-`res://` check walks `.gdshader` only. Widening it to `.tres` / `.material` / `.png` across both `load("res://…")` and `preload("res://…")` string literals is a grep-and-resolve pass — no Godot, no lock, milliseconds — and unlike every tool measured here it catches the **`load()`** form, which is the one the kits emit. That is the cheapest refuting test for the defect class that actually bit us, and it is squarely inside the conductor's existing machinery.

---

## 6. What this spike did not answer

- Whether the LSP's first-party RG findings (57 errors / 297 warnings, minus 41 false preloads) contain anything real. **Empirical criterion for revisiting:** a triage pass over that residual, separately dispatched — not folded into a gate decision.
- Why `godot --headless --check-only` misses an unknown method on a typed variable (probe 1b). Worth knowing before anyone proposes `--check-only` as the freeze gate instead.

**Signed:** drax — presentation seam. `astra_test_01/burst/` and `reincarnated-godot` both unmodified; all Godot work ran against a scratch copy (see § 4.6 for why that mattered).
