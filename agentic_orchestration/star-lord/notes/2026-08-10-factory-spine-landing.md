# FACTORY SPINE v1 — landing note

**Author:** star-lord (builder, ruling D4)
**Date:** 2026-08-10
**Build contract:** `agentic_orchestration/gandalf/notes/2026-08-10-factory-spine-spec.md` (Spec A)
**Strategy of record:** `agentic_orchestration/operating-procedures/software-factory.md`
**Landed at:** `agentic_orchestration/factory/` — commit `339c7216`
**For:** gandalf (DRIFT-CRITIC, reviews on landing) · jack-ryan (Gate-2, before the
first compiled workflow) · Matt

---

## 1. Top line

The spine is built, it runs, and it is honest about what it does not do.

Spec A § 11 acceptance items 1–4 are **mechanically proven** (not asserted in prose).
Item 5 — jack-ryan Gate-2 — is **queued and blocking**: no compiled *agentic* workflow
fires before it. The mechanical lane is already exercised, because a mechanical cell
spends no tokens and invokes no model.

136 tests, all green. The live run and the determinism assertion are reproducible from
the shipped workflow file:

```
./factory run workflows/kc2-baton-mechanical.yaml
./factory determinism workflows/kc2-baton-mechanical.yaml
```

## 2. Acceptance, item by item

| # | Spec A § 11 item | Status | Evidence |
|---|---|---|---|
| 1 | Baton-scene mechanical cells run end-to-end | **PROVEN** | 3 phases, 14 gate verdicts, all green. Digest pin `d7ecd866…` @ 1,065,632 B. `BR2W_C9.mp4` ffprobe-verified at 40.37 s, video+audio, ≥1280×720. The engine's baton test wall exited 0. |
| 2 | Determinism assertion | **PROVEN** | `DETERMINISM: EXACT — 14 gate verdicts identical across two laps.` |
| 3 | Zero stub gates (grep-provable) | **PROVEN** | `tests/test_no_stub_gates.py`, three independent proofs (§ 4 below). |
| 4 | Synced-triad green; permissions breach ⇒ rollback + abort | **PROVEN** | `tests/test_envelope_triad.py` (9 tests); `tests/test_permissions.py` plants an undeclared write and asserts ABORT + quarantine + clean tree + **zero retries consumed**. |
| 5 | jack-ryan Gate-2 PASS on the landing | **QUEUED — BLOCKING** | See § 6. |

## 3. The § 13 open items — resolved, with one delta

All four were probed **live before any code was written** (claude 2.1.119, Python
3.12.0, this host, 2026-08-10). Three confirmed the spec. One did not.

- **O1 — flag co-support: CONFIRMED, with a load-bearing addition.**
  `--agent` + `-p` + `--output-format stream-json` co-support works. **`--verbose` is
  MANDATORY** alongside stream-json in print mode — without it the CLI exits 1 *before
  any API call*. An adapter that forgot this would burn a phase for nothing and report
  a harness failure with no result frame. Passed unconditionally now.
  Also observed: SessionStart hooks DO fire in headless mode; their frames appear in
  the stream and are recorded, not suppressed.

- **O2 — usage fields: CONFIRMED.** The `result` frame carries `input_tokens`,
  `output_tokens`, `cache_read_input_tokens`, `cache_creation_input_tokens`,
  `total_cost_usd`, `modelUsage{}`. **No `reasoning_tokens` key was present** in the
  probe sample → reasoning is recorded as NULL with a reason, never folded into output.
  The recorded frame ships as `fixtures/claude_stream_probe.jsonl` and the usage tests
  assert against it, so a future harness change that starts reporting reasoning will
  red a test rather than pass silently.

- **O3 — PyYAML: CONFIRMED.** 6.0.3 present. `.json` workflows load through the same
  validator if it ever goes missing.

- **O4 — dollars: SPEC DELTA. Flagged for DRIFT-CRITIC.**
  Spec A expected `total_cost_usd` to be NULL on a subscription lane. **It is
  populated** — $0.0672 for a call that produced 4 output tokens. It is a
  harness-computed **list-price imputation**, not an amount billed; the Max
  subscription is flat.

  Resolution taken: record the figure **and** record `dollars_source`
  (`"harness_reported_imputed"`), stamped at parse time, carried through the receipts
  schema, and rendered with its label by `report.py`. A downstream surface therefore
  cannot show this number as money spent without also showing that it wasn't.

  **Why this matters beyond the field:** the strategy's cost discipline assumes a
  subscription lane reports nothing. It reports something plausible-looking instead.
  That is a worse failure mode than silence, because a dashboard would render it
  without a second thought. This is the kind of number that becomes a "we spent $X on
  the factory" claim three sessions from now. It is now impossible to make that claim
  from the receipts without the label attached. **Gandalf: this is the one place the
  build did not simply implement the spec, and it deserves a ruling on whether the
  labeling is sufficient or whether the figure should be dropped entirely.**

## 4. Zero stub gates — how it is proven

"No stubs" fails in three different ways, so there are three proofs:

1. **Marker scan.** No TODO / FIXME / NotImplementedError / placeholder anywhere in the
   gate tree. The scanner tokenizes string literals away and keeps comments, so the
   modules can *describe* the no-stub law in their docstrings without tripping the
   scanner that enforces it. (A law that cannot be written down is a law nobody reads.)
2. **Red-path proof.** Every registered gate's source can reach `failed` or
   `not_runnable`. A gate that can only return `passed` is a stub wearing a gate's name.
3. **Evidence proof.** Every gate touches disk, a subprocess, or the measured
   change-set. A gate that reads only the envelope is taking the agent's word, which is
   the thing gates exist to refuse.

Plus a registry-coverage assertion: every gate in the registry has a falsification test
that shows it reds when its subject is broken. Adding a gate without one reds the suite.

**The one stub in the tree** is the Codex adapter. It declares `HONEST_STUB = True`,
names **T16** (Matt action: ChatGPT subscription + Codex CLI install + login) as its
blocker, and **raises** rather than returning a green. A test asserts it is the only
module in the package containing `NotImplementedError` in executable code. An honest
stub in an *adapter* is a lane saying it is not open. A stub in a *gate* would be
observability theater. The line between them is now enforced, not remembered.

## 5. Two holes found and closed during the build

Both self-caught, both recorded because the next builder will be tempted the same way:

- **Single-fingerprint containment hole.** The runner fingerprinted before and after
  execution — but a mechanical cell does its work *inside* a gate command
  (`tests_pass` / `command_succeeds`), so the command's own writes landed *after* the
  post-execution snapshot and escaped containment entirely. Every mechanical phase was
  effectively unfenced. Now fingerprinted a second time after gates, with the breach
  receipt naming which side of the boundary it came from (`during="gate execution"`).

- **Fingerprint cost and a false-breach trap.** Content-hashing dirty paths would have
  hashed ~2,800 engine paths per snapshot, twice per phase. Worse, rglob-based
  directory signatures counted the factory's *own* gitignored `sessions/` writes as
  modifications to `agentic_orchestration/factory/` — a PROTECTED path — which would
  have aborted every run as a self-breach. Now: stat signatures grouped by
  `git ls-files --others --exclude-standard`, so gitignored writes are invisible to the
  fingerprint. A test pins that behavior specifically.

## 6. What is queued, and what gates it

| Item | Owner | Gating criterion |
|---|---|---|
| **Gate-2 on this landing** | jack-ryan | Blocking. No compiled *agentic* workflow fires until PASS. Mechanical workflows are already exercised (no model invoked, no tokens spent). |
| **DRIFT-CRITIC review** | gandalf | Especially the O4 delta (§ 3) — the one place the build departed from the spec. |
| **F2 — Codex lane** | star-lord | Blocked on **T16** (Matt). Interface is pinned so the pilot is a body-fill, not a redesign. |
| **First agentic workflow** | knight-rider dispatch | Downstream of Gate-2. The spine will not author its own first real run. |
| **Receipts schema v2** | star-lord | Only on a demonstrated consumer need. `SCHEMA_VERSION` is stamped so a consumer can refuse an unknown version rather than guess; a change ships with a MIGRATION note first. |
| **UI tier > 0** | deferred by doctrine | No dashboard before receipts. Receipts now exist; the tier ladder still advances on evidence, not on appetite. |

## 7. Scope compliance

Meta-repo writes only, as directed. The engine tree was **read** and its baton test wall
was **executed** (exit 0) — no engine-tree writes. The Godot tree was read for the render
artifact only. Both are declared `read_only_trees` in the shipped workflow, so the
fingerprinting would have aborted the run had anything written to them.

One consequence worth naming: my usual session-end checkpoint lives at
`reincarnated-engine/src/reincarnated/export/AGENT_STATE.md`, which is an engine-tree
write and therefore **out of scope for this session**. This note is the checkpoint
instead. The next star-lord session should fold the factory-spine state into
AGENT_STATE.md when an engine-tree write is in scope.

---

**Signed:** star-lord — operational-pipeline seam (export · output · telemetry · LLM),
builder of the spine per ruling D4.
