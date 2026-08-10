# Factory Spine — build contract (Spec A)

**Date:** 2026-08-10 · **Author:** gandalf (SPEC-AUTHOR) · **Builder:** star-lord (ruling D4)
**Review:** gandalf DRIFT-CRITIC on landing · jack-ryan Gate-2 before first compiled workflow
**Governing strategy:** `operating-procedures/software-factory.md` (read § 1–6 before building)
**Status:** BUILD-CONTRACT — awaiting KR dispatch sequencing. gandalf writes no production code;
this spec is the contract the build is judged against.

---

## 1 · Scope

Python package at `agentic_orchestration/factory/` (meta-repo). Dependency posture: stdlib-lean
— `sqlite3`, `subprocess`, `json`, `pathlib`, `dataclasses`; `yaml` via PyYAML (verify
availability at build, § 13). No daemon in v1: `factory run <workflow.yaml>` and
`factory status` are terminal commands. `factory/sessions/` and `factory/receipts.db` are
**git-ignored working state**; committed artifacts are code, configs, and deliberately promoted
run reports.

## 2 · Phase runner — default-fail

A phase is a context manager that ENTERS as FAILED and stays FAILED unless exactly one
`finish(status, summary, artifacts, notes_for_next_agent)` collapses it. Unhandled exception →
FAILED with traceback recorded in receipts. There is no "assume success" path and **no override
parameter** — the KC2 emit wall's posture (`no_override`) is the ancestor and the law.

## 3 · Envelopes — the synced triad

`EnvelopeBase`: `status: PASS | FAIL | PARTIAL` · `summary: str` · `artifacts: list[path]` ·
`notes_for_next_agent: str`. The dataclass, its JSON schema, and the prompt-block text that
describes it to a worker live in **one module**, and a test asserts the three agree
(field-for-field). Drift between what the code accepts and what the prompt promises is the
first bug this architecture exists to kill.

## 4 · Claim gates v1

Signature: `gate(envelope, run) -> GateReport`. Gates run **post-hoc against artifacts on
disk** — never against the envelope's own word (per-landing law, compiled).

| Gate | Verdict source |
|---|---|
| `artifacts_exist` | every declared artifact path exists |
| `files_non_empty` | no zero-byte deliverables |
| `json_parses` | declared JSON artifacts parse |
| `diff_matches_claims` | git change-set ⊆ what the envelope claims touched |
| `verdict_consistent` | envelope status vs gate outcomes: a PASS envelope with red gates is itself a red |
| `tests_pass(command)` | run the command; exit code is the verdict; **only failures travel** into any subsequent prompt |

**No stub gates, ever.** A gate that cannot execute returns `FAIL / NOT-RUNNABLE` with reason —
never green. (SSSF's echo-exit-0 stubs are the named anti-pattern; strategy doc § 6.)

## 5 · Harness adapters

- **Claude Code headless (v1, live lane):** `claude --agent <seam> -p '<prompt>'
  --output-format stream-json`, stdin from `/dev/null`, cwd per config. Named seam agents ONLY
  (the discipline stack loads with the name — routing rule § 4.10). Parse stream-json for
  result + usage.
- **Codex CLI (F2, honestly stubbed):** interface pinned now (`run(prompt, cwd, config) ->
  RawResult`), body raises `NotImplementedError("F2 — blocked on T16")`. An honest stub in an
  ADAPTER is legal; a stub in a GATE is not — the distinction is load-bearing.

## 6 · Receipts — SQLite, WAL mode

Tables: `sessions` · `phases` · `events` · `envelopes` · `gate_results` · `processes` ·
`agent_sessions`. Usage columns per phase (`UsageBreakdown`): `input_tokens`, `output_tokens`,
`cache_read_tokens`, `cache_write_tokens`, `reasoning_tokens`, `dollars` (nullable —
subscription lanes may not price; **record tokens always**). **Reasoning tokens are a share of
output tokens, never a fifth addend** — a summation bug here poisons every cost report
downstream.

## 7 · Session dirs

`factory/sessions/{run_id}/` → `context_handoff/` (envelopes as JSON) · `prompts/` (the exact
prompt each worker received) · `{phase}/raw_output.jsonl` · `{phase}/envelope.json`. The dir is
the run's forensic record: any receipts row must be reproducible from it.

## 8 · Permissions fingerprinting (v1 containment, per D5)

Fingerprint the working tree before/after each phase (git status porcelain + hash of tracked
diffs). Any write outside the phase's `writes` allowlist → **rollback the excess + ABORT the
run** (breach = evidence, never retry). Protected paths regardless of config: `factory/` itself
(no self-modification), `canonical/`, `.claude/`, and the engine tree from any godot-cell
workflow (read-only proof pattern per the WR3 owner-eye cell).

## 9 · Workflow config (YAML)

Per phase: `agent` (named seam) · `tools` (allowlist) · `writes` (path allowlist) · `gates`
(list + args) · `retries` (int; retry re-prompts with failures-only context). **No `model`
field in v1** — model policy belongs to the launcher/harness session, not the workflow file.

## 10 · Tier-0 surface

`factory status` (live phases, last gate results, token totals) + a generated per-run markdown
report from receipts (the run's mechanical shadow of a wind-down note). This ships WITH the
spine — strategy § 7 Tier 0.

## 11 · Acceptance (what Gate-2 judges)

1. The baton-scene **mechanical cells run end-to-end under the spine**: digest gate (verify
   `d7ecd866…` before load), ffprobe gate (R-BR-56 — promote no render unverified), headless
   test wall (`tests_pass`) — receipts + usage recorded for each.
2. **Determinism assertion:** re-run of an identical phase config produces identical gate
   verdicts (R-BR-51 — the instrument asserts its own determinism).
3. **Zero stub gates** anywhere in the tree (grep-provable).
4. Synced-triad test green; permissions-breach test proves rollback+abort on a planted
   out-of-allowlist write.
5. jack-ryan Gate-2 PASS on the landing.

## 12 · Non-goals (v1)

No router agent · no Kanban/autonomy loop · no sandboxes (D5) · no cloud · no UI beyond
Tier-0 · no Codex execution (adapter interface only) · no engine-side code.

## 13 · Open items (ARCHITECT table — resolve-or-surface at build)

| # | Item | Disposition |
|---|---|---|
| O1 | Exact `claude` CLI flag surface at installed version (`--agent` + `-p` + `--output-format stream-json` co-support) | VERIFY-AT-BUILD; if absent, surface before workaround |
| O2 | Usage-stats availability in stream-json result frames | VERIFY-AT-BUILD; if absent, tokens go NULL-with-reason, never invented |
| O3 | PyYAML availability in the Mac Python env | VERIFY-AT-BUILD; stdlib-JSON configs are the fallback |
| O4 | Dollar pricing on subscription lanes | Expected NULL; column stays nullable |

**Signed:** gandalf, 2026-08-10.
