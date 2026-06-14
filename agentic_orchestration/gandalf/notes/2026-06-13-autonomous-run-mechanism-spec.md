# Autonomous-run mechanism spec — for KR

**Type:** mechanism spec (gandalf → knight-rider, who operationalizes the run-launch).
**Date:** 2026-06-13
**Author:** gandalf
**Authority:** Matt-authorized 2026-06-13 ("a one-paragraph autonomous-run mechanism spec KR").
**Durable home flag:** this mechanism belongs as an **engineering-discipline** — jack-ryan canonicalizes; KR operationalizes the launch.

---

## The mechanism (one paragraph)

A sound autonomous run is **not** a wake-up-loop heartbeat poll wrapping a backgrounded task — that pattern is retired for three failure modes: **coupling** (the poll loop's death kills the in-flight build), **redundancy** (a background-completion notification already fires on done, so the poll adds nothing), and **silent stall** (a poll confirms "still running" without confirming "still making progress"). The sound mechanism is three primitives: **(1) incremental checkpointing** — the run commits intermediate state at each completed sub-unit so a mid-run failure *resumes* from the last checkpoint rather than restarting, and a partial run still banks reviewable work; **(2) event-driven completion** — the run signals done via the background-Task completion notification, never a poll, so the orchestrator is woken by the event, not by a timer; **(3) a watchdog / liveness probe** on any long thread — a progress assertion (checkpoint-advanced-since-last-tick), not a heartbeat, so a *silent stall* surfaces as a distinct failure from a clean completion. Parallelism is safe **only across different seams** (gamora-simulation vs rocket-generation vs star-lord-pipeline) where there is **zero file-collision**; the **concurrent-instance discipline** (one writer per artifact per round; git-log/grep before re-authoring) is what keeps two runs — or a run and a live orchestrator session — from racing the same doc. The load-bearing boundary is **the review line**: autonomous covers **build + checkpointed authoring**; **irreversible gates stay human / critique-paired** — the **W-F 1D-delete gate**, **Gate-2 certifications**, and **push-to-remote** (ADR-006). Autonomous runs **FEED** the review queue (each produces work-products + a Gate-1 self-review), they do **NOT BYPASS** it — the Gate-2 close and Matt-ratify happen at re-engagement, against the checkpointed artifacts the run banked.

---

## Topology for the current batch (KR launches)

**Two parallel runs, different seams, collision-free. Proxy-port (D4) is NOT in this batch.**

| Run | Seam | Contents | Notes |
|---|---|---|---|
| **Run A** | gamora (simulation) | **W-E throughput** build [wave critical path] + **displacement-histogram emit** [cheap; unblocks gandalf's mobility lock-edge re-cal] + her **2 Gate-2 doc-lines** [trivial, clears the W-D WARN→PASS] | W-E *build* is autonomous; its **close** returns to the critique pair (jack-ryan Gate-2 + gandalf design + Matt ratify) |
| **Run B** | rocket (generation / foundation) | **D5 reference-kit** (`dispatches/2026-06-13-rocket-reference-kit-coverage.md`) + **D6 grouping-vocab loader fix** (`dispatches/2026-06-13-rocket-grouping-vocab-loader-fix.md`) | Zero overlap with gamora's simulation seam → parallel-safe |

**D4 / Proxy-Port held for a later batch** — three reasons: (1) it is not specced until gamora consumes the §4.C/§4.D density-design contract (`...-density-design-contract-4C-4D-proxy-port.md`) to build the §4.D fixture; (2) it is a movement-AI rework that **must come after Run A banks the displacement histogram** (else it invalidates gandalf's lock-edge re-cal — see the contract's sequencing note); (3) Matt's **W-E-vs-port priority call** is still open. W-D-export (star-lord) is gated on gamora's MIGRATION v1.31, so it sequences off Run A's output rather than launching as a third concurrent run.

---

**Signed:** gandalf, 2026-06-13
**For:** the autonomous-run mechanism (checkpoint + event-driven completion + watchdog; cross-seam parallelism only; review-line preserved — irreversible gates stay critique-paired) and the current-batch topology (two parallel runs, D4 held). Durable home = engineering-discipline (jack-ryan).
