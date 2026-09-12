# Painted-2D Art Pipeline — MECHANICAL PROCESS (agent-facing twin)

> **STATUS:** CURRENT (load-bearing as of 2026-09-11) — see `canonical/00-ground-state.md`. Twin of `00-system.md` (human-readable); both are views over the executable sources listed in `00-system.md § 7 SYNC` — same-commit rule.

**Date:** 2026-09-11
**Author:** gandalf (CANON-STEWARD / RUN-CONDUCTOR)
**Status:** v1.0
**Authority:** Matt 2026-09-11 — *"add hooks into ChatGPT's AGENTS.md or some other system that can ensure that Astra (who is doing the work) follows the mechanical processes as built"*; charter rulings F7/F7c/F8
**Companion docs:**
- `canonical/reap-die-rise-game/painted-2d-pipeline/00-system.md` — the human-readable twin
- `astra_test_01/burst/BURST_RULES.md` · `REGISTER_CARD.md` · `JUDGE_RUBRIC.md` · `receipt.schema.json` · `SPEC.md` — the executable sources (Astra reads these, not this doc)
- `AGENTS.md` (repo root) § "Painted 2D / Astra work" — the Codex routing hook

---

## 0. TL;DR

Astra never reads *this* document during a burst — a burst's entire instruction set is the rendered brief (card + rules row + task + references + return schema), and the process holds because the **wrapper audits the burst after the fact and voids violations**. This doc exists for (a) interactive Codex sessions in the repo (routed here by root `AGENTS.md`), (b) Claude agents who need to invoke or reason about the lane, (c) the sync check.

## 1. Invariants (the rules that make it a lane, not a session)

1. **Every generation is a burst:** fresh `codex exec`, `--ephemeral`, profile `astra-burst`, workdir `~/astra-burst/runs/<run>/<burst-id>/` (outside the repo), `</dev/null`, `--json`, `--output-schema receipt.schema.json`. Never an interactive Codex session; never a resumed thread.
2. **Typed bursts, typed caps:** TOOLING (writes code under `astra_test_01/burst/` only; ≤40 min/≤60 calls; then FROZEN via `MANIFEST.sha256`) · GENERATE (images only; ≤12; no code; writes only `out/`) · CHECK (frozen tools; 0 images) · JUDGE / TRANSCRIBE (separate instance; `view_image` only; 0 images; controls in every batch) · LABEL (edit, ≤2 images) · ANNOTATE · PACK. Rows: `BURST_RULES.md`.
3. **No PASS vocabulary in any receipt.** Verdicts come from the conductor's gates (`checks.json`) and the comparator; JUDGE produces scores.
4. **Intent is conductor-owned:** REGISTER_CARD, bible, ledger. A burst cannot edit them (sandbox: repo is read-only from a burst except declared `--add-dir`s, which only TOOLING receives).
5. **Two-attempt rule with scope guard:** one diagnosed retry in-burst; then the conductor may change *method within the hypothesis*, never *medium* (no rigs/meshes/renderers/textures-on-geometry) — medium changes are Matt's.
6. **HALT to Matt** on: two consecutive experiment FAILs · two VOIDs in a row · a JUDGE passing its control twice · three rate-limit backoffs · any write outside `out/` · run image cap (250) · any medium or bar change.

## 2. How to run a burst (conductor recipe)

```
cd astra_test_01/burst
python3 lane/run_burst.py --run C-1 --burst-id <EXP>-<type>-<nn> --type <TYPE> --task <task.json> [--dry-run]
#   task.json: {"text","references":[{"path","role"}],"image_cap","minutes_cap","tool_call_cap","outputs":[],"effort","add_dirs":[]}
#   exit 0 DELIVERED · 2 VOID (audit/receipt/hash) · 3 FAILED (codex error/timeout)
#   artifacts → runs/C-1/artifacts/<burst-id>/ ; ledger → runs/C-1/ledger.json (append-only, conductor-owned)
```
Dry-run first on any new task shape; read the rendered brief. After a TOOLING burst: run the tests, review the diff, regenerate `MANIFEST.sha256`, append the ledger entry, commit with `--only` over `astra_test_01/burst`.

## 3. Enforcement hooks (four surfaces; one is research-gated)

| Surface | Mechanism | Covers |
|---|---|---|
| **Wrapper audit** (`lane/audit.py`) | event-stream census + filesystem diff vs snapshot + caps + forbidden tools (`web`, `collaboration`, `spawn`) → VOID | every burst — the real enforcement |
| **Root `AGENTS.md`** § "Painted 2D / Astra work" | routes any interactive Codex session in this repo here; forbids generating painted assets outside the lane; declares `astra_test_01/design/` HISTORICAL (do not resume `PROGRESS.json`) | Matt's own Codex sessions; any Codex agent in the repo |
| **Profile** `~/.codex/astra-burst.config.toml` | no plugins, no MCP servers, sandbox workspace-write, approvals never | burst context hygiene |
| **Codex hooks** (`hooks.json` session_start) | **OPEN — legolas R2** must verify the hook API in Codex 0.153.x before this is relied on | would cover interactive sessions mechanically |

## 4. Drift alarms

- `00-system.md § 7` hash mismatch on any source → the process documents are stale (fix in the same commit as the source change; never silently).
- `MANIFEST.sha256` mismatch → tools were changed outside a TOOLING burst → treat all downstream results as VOID until re-frozen.
- Ledger `bursts[].audit.violations` non-empty on a DELIVERED burst → the wrapper let something through; file it.
- A receipt containing `PASS`/`FAIL` → the schema drifted; VOID.

## 5. Cross-references

`00-system.md` (twin) · charter `agentic_orchestration/gandalf/notes/2026-09-11-astra-burst-lane-run-charter.md` · `astra_test_01/burst/SPEC.md` · `canonical-doc-format § 6.8` (twin-sync rule) · `AGENTS.md § 3` (Codex-lane standing provisions: one lane, no internal sub-agents)

Tracker-delta: none beyond `00-system.md`'s (registered together).

---

**Signed:** gandalf (CANON-STEWARD)
**For:** the agent-facing mechanical twin of the painted-2D pipeline — invariants, the burst recipe, the enforcement surfaces, the drift alarms.
