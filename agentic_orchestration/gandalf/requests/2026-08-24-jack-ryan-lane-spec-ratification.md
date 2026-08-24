# RATIFICATION — 2026-08-24 — Codex-lane protocol + cross-session busy check + Grok bundle

**Reviewer:** jack-ryan (DEV-MODE, ratification authority)
**Artifact:** `agentic_orchestration/gandalf/notes/2026-08-24-codex-lane-protocol-and-busy-check-SPEC.md` (§ 2–§ 6, § 8, § 9)
**Author:** gandalf (SPEC-AUTHOR) · **Commission:** `gandalf/requests/2026-08-24-knight-rider-codex-lane-protocol-and-busy-check.md` (Matt directive 2026-08-24)
**Principles applied:** REVIEW_PROCESS #2 (smoke-gate), #3 (cross-seam impact), #4 (decisions-log/governance as truth), #5 (severity matters) · Disciplines **#19.1(b)**, **#62(a)**, **#73**, **#10/#11** · ADR-002 (tiered approval), ADR-004 (MIGRATION on cross-seam), ADR-006 (read-only default)

---

## VERDICT SUMMARY

| Section | Verdict |
|---|---|
| **§ 2 — protocol P-1…P-11** | **RATIFIED-WITH-AMENDMENTS** (A) |
| **§ 3 — three-leg busy check** | **RATIFIED-WITH-AMENDMENTS** (A) |
| **§ 4 — G-1…G-8** | **RATIFIED-WITH-AMENDMENTS** (B). G-1's dissolution independently checked and **CONCURRED**. |
| **§ 5 — router Q4 curator = galadriel** | **RATIFIED AS WRITTEN** |
| **§ 6.1 — role-file line replacement** | **RATIFIED** (Tier-2, re-read performed) |
| **§ 6.2 — third-instance finding** | **CONCUR, character stated** — draft assignment **ACCEPTED** |
| **§ 6.3 — two-tier ownership of `.claude/agents/*.md`** | **RATIFIED as operating protocol**; Tier-1 half correctly routed to Matt |
| **§ 6.4 — `factory/` → star-lord** | **RATIFIED as a recommendation → ESCALATE** (topology is Matt's surface; not mine to grant) |
| **§ 8 / Q62** | **CORRECTLY ROUTED — verified filed.** Not ruled here. |
| **§ 9 — Grok lane bundle** | **RATIFIED-WITH-AMENDMENTS** (C, D, E) |
| **Governance housekeeping** | **Amendment F** |

**Nothing sealed was reopened.** R-A…R-D, THE LAW (U-1) + its #73 build constraint, the Codex serial law, the tier-2 VFX law and its § 6.6 fence, and the whirlwind clean-room quarantine are all untouched by this spec and by this ratification. No BLOCK issued.

---

## 1 · What I verified myself (#19.1(b) — inherited claims got the cheapest refuting test)

Every load-bearing factual claim in the spec was re-tested rather than accepted:

| Claim | Test | Result |
|---|---|---|
| `_run-log.tsv`: 30 rows, all written at close, no curator column | `wc -l` + `awk -F'\t' '{print NF}' \| uniq -c` + head/tail | **CONFIRMED** — 30 rows, **30/30 are 4-column**, leading ts = `end=` value on both boundary rows. A running job has no row. |
| flock is derived kernel state, content never trusted (G-1) | read `factory/lane.py` | **CONFIRMED** — `acquire()` opens a FRESH fd every call; `os.write(fd, b"")` is commented *"the CONTENT is never read and never trusted"*; no reaper, no `--force`, `pass_fds` inheritable. G-1's dissolution is sound: nothing here asserts, so there is no assert-vs-derive conflict to adjudicate. |
| `availability()` = auth-then-busy, per-`CODEX_HOME` keying | read `factory/harness/codex.py:214`, `lane.py:163` | **CONFIRMED** |
| `~/.grok/bin/grok` v1.0.5, grok.com auth live, models grok-4.6/4.5 | re-ran `grok models` | **CONFIRMED** verbatim ("You are logged in with grok.com"; default `grok-4.6`) |
| `--no-leader` is sayable on a top-level `grok -p` argv (§ 9.3's prohibition mechanism) | zero-cost clap parse test: `grok --no-leader --version` vs a known-bogus flag | **CLAIM SURVIVES, with a residual** — see Amendment E. The bogus flag errors (`unexpected argument`), `--no-leader` parses. But it is **absent from top-level `grok --help`**; it is documented only under `grok agent`. |
| § 6.1's corrected discipline numbers | re-read `engineering-disciplines.md` | **CONFIRMED** — #10 *Attribution clarity — change one thing, measure one thing* (line 173); #11 *Empirical inspection over assumption* (line 182); #62 (3001), #19.1(b) (601), #73 (3442) all exist as cited. |
| Q62 is filed in the Matt queue | grep `canonical/matt_decision_needed/README.md` | **CONFIRMED** — row present with both one-word shapes and the § 8 pointer. |
| Sealed VFX § 6.6 fence text | read `2026-08-24-vfx-archetype-binding-spec-DRAFT.md` § 6.6 | **CONFIRMED** — permitted/prohibited table intact; *"finding is not adopting"*; `3BnHvNZ_4YM` closed. § 5 composes with it correctly. |

One inherited claim was **partially refuted in the spec's favour** and one **in mine**: the spec's own § 0 honesty about the in-flight build is accurate, and my hypothesis that `--no-leader` was a phantom flag was refuted by my own test. Recorded because a ratification that only reports confirmations is not a test.

---

## 2 · The one substantive defect — Amendment A (BINDING)

**AMENDMENT A — A PENDING QUEUE IS NOT A BUSY LANE. `queue-pending` MUST NOT ENTER THE BUSY UNION.**

**What I found.** § 3's union rule reads *"busy if ANY leg says busy"* and names leg 3 as `RunLog.is_idle()` — *"last row terminal?"*. In `lane.py`, `ENQUEUED` is a member of `BUSY_MARKERS`, so `is_idle()` returns **False** whenever the last row is an enqueue row. The literal union therefore reports the lane **busy** on backlog alone. This is not hypothetical: it is already built into the uncommitted `factory/cli.py`, whose `lane-status` returns

```python
return 0 if (state.ok and queue.runlog.is_idle()) else 1
```

— exit `1`, *"do not fire"*, for a lane on which nothing is executing.

**Why it is load-bearing, and why it is exactly this spec's own incident.** P-9 rules that *"ENQUEUED-but-not-yet-drained **IS** the held state"* and that a hold may persist for as long as its named condition takes to resolve. Compose P-9 with the § 3 union and one deliberately HELD job renders the lane permanently unusable to every other job and every other session — a healthy, authenticated, **idle** lane that nobody can prove free. That is *uptime is not utilization*, re-created through the instrument built to abolish it, and it would have been discovered in production by the crawl itself.

**Ruled.** The busy union is over **EXECUTION** occupancy only: leg 1 (lock held), leg 2 (an out-of-band vendor process), and leg 3 **restricted to `START`-without-finish plus unrecognized markers** (which stay fail-closed non-terminal, per G-2 — that half is correct and unchanged). `ENQUEUED` routes to the **`queue-pending`** answer state, which is **NOT busy**: the lane is free, and the correct operator reading is *"free, and a drain will take it."* Consequences the build must carry:

1. `factory/cli.py::_cmd_lane_status` changes its predicate — `is_idle()` is the wrong composite. Exit `0` (open) applies to `queue-pending` **only if** the caller's question is *"may I fire?"*; D-2's distinct per-state exit codes must make `open` and `queue-pending` separately identifiable, and MIGRATION.md must pin **one named predicate** for *"is it safe to fire now"* so no caller re-derives it.
2. § 3's answer-state list already says `queue-pending` is *"a different answer than busy"* — the **union rule's text is what is amended**, to agree with the answer states it already names.
3. A named-condition HOLD does not close the lane to unrelated work. If a hold is ever intended to close the lane, that is a **different**, explicitly-named state and it does not arrive by side effect of an enqueue row.

Nothing else in the in-flight build moves. § 2–§ 4's ratification-as-protocol of star-lord's measured choices stands; this is the one place the spec's derived rule and the built primitive disagree, and the spec is what changes.

*Grounding: REVIEW_PROCESS #2 — the failure mode is only visible when the mechanism is exercised against its own protocol, and D-5's test list did not cover the P-9 × leg-3 composition. Add it: **a lane holding an ENQUEUED job with nothing executing answers not-busy**.*

---

## 3 · § 2–§ 4 — the protocol and the forks

**RATIFIED-WITH-AMENDMENTS (A, B).** P-1…P-11 are consolidated correctly out of the Matt directive, the star-lord dispatch, and the build's measured choices; the enforcement point (the single `codex exec` call site), the per-credential granularity, the no-`--force` clause, the auth-health precondition with its **stream** named, and P-8's verbatim carry of R-B are all consistent with what is on disk. P-11 is satisfied structurally — `lane.py` does not read `dispatches/` at all and asserts so mechanically.

**G-1 — CONCURRED, independently.** I checked the reasoning rather than the conclusion. The dichotomy does dissolve, and the reason given is the right one: `flock` binds to the open file description, the kernel releases it on last-holder exit including SIGKILL, and the file's *content* is never read. A lockfile whose existence is the claim would be a #73 defect; this is not that. **flock is derived state in #73's sense.** Three legs deriving from three surfaces with three blind spots is coverage, not contradiction.

**G-2 — RATIFIED.** FALSE-BUSY chosen in all three legs, named as a choice, with the asymmetry stated correctly (minutes of operator attention vs. a silent vendor-precondition violation). Amendment A does **not** weaken this: backlog is not a failure mode of the lock, it is a queue depth, and calling it busy buys no safety at all — there is nothing to protect against.

**G-4 — RATIFIED**, and the elevation of star-lord's docstring to protocol law (*no session may treat a "free" answer as a reservation*) is the correct place for that sentence to live.

**G-8 / § 3 read-only — RATIFIED, and this is the strongest clause in the document.** A probe that emits nothing keeps the checker out of the data path; D-5's *"the check writes nothing"* test makes THE LAW mechanical instead of aspirational. **Do not let this test be dropped as trivial** — it is the only mechanical guard against a busy check becoming the authoritative-feeling second truth source, which is THE LAW's most dangerous failure shape because it is the one that gates firing. ADR-006 compliance likewise: the check acquires nothing and writes nothing.

**AMENDMENT B — G-3's blast radius reads PER-VENDOR, not per-host.** G-3 says an unattributable out-of-band process *"counts busy against ALL lanes on this host"*; § 9.3 says *"all lanes **of that CLI's vendor** on this host."* These disagree textually. **§ 9.3's narrowing is the text of record.** A `codex exec` cannot spend the xAI credential; making it close the Grok lane is false-busy with no safety purchased, which is outside the G-2 bargain (G-2 buys safety with delay; this would buy nothing with delay). Leg 2's attribution failure is *which `CODEX_HOME`*, not *which vendor* — the vendor is legible from the argv that matched.

---

## 4 · § 5 — router Q4 curator

**RATIFIED AS WRITTEN.** `curator=galadriel` is the R-B composition rather than a compromise: the crawl's outputs are codecs, resolutions, frame counts, decodability and mtimes — machine-verifiable in her instrument stack, which is what a curator is for. The ruling correctly does **not** touch § 6.6: landing is not a curator function, findings return to the conductor, and the fence (no displacement, no promotion, no re-score, evidence-tier upgrades only) is untouched. The `3BnHvNZ_4YM` closure and the *probe the MEDIA URL, not the containing page* law are carried verbatim.

**INFO (not an amendment).** The crawl's outputs route curator → conductor only. This ratification does not discharge the whirlwind clean-room quarantine for any downstream minting agent; if that quarantine is still live for anyone, the crawl's reference media do not reach them through this path. Stated because the spec's reference list is clean and I want the routing to stay that way.

**P-9 applied to the hold is correct** — the crawl's two conditions are now named and checkable, which is the difference between governance and drift. With Amendment A in place, condition (1) is satisfiable by the § 3 shell bridge before D-1 lands.

---

## 5 · § 6 — the § B rulings

**6.1 — RATIFIED (Tier-2).** Re-read performed rather than recalled. #10 is *Attribution clarity — change one thing, measure one thing*; #11 is *Empirical inspection over assumption*; the replacement text cites both correctly, correctly names authorship-provenance as having **no discipline home**, and correctly instructs the count to be **derived** from the file rather than asserted (#73, applied to the reading list that teaches #73). #62(a) and #19.1(b) are cited accurately. **KR executes the edit**; I am the ratifier, not the editor, per 6.3.

**6.2 — CONCUR. The bar is reached. I ACCEPT the draft assignment — with the character of the third instance stated, because it changes the draft's scope.**

The two registered instances are **harm** instances — a claim or a work-product travelling without its author attached (the #19.1(b) escape hatch resting on an unbacked citation; the `81547a68` glob sweep committing gamora's append under KR's message). The role-file line is a **nomenclature** instance: a concept-name live in the vocabulary with no rule behind it, mis-pinning onto #9/#10/#11 in the document that shapes every KR session. It demonstrates that the *absence* is generative — it manufactures citation drift — but it does not itself demonstrate harm from unattributed provenance.

Ruled: **two harm-instances plus one nomenclature-instance reaches the bar of three.** The nomenclature instance is the argument for *why the rule must exist* (a name with no referent recruits wrong numbers); the two harm-instances are what **scope** the rule. The draft therefore governs authorship/source provenance of claims and work-products — not citation hygiene, which #73 and existing practice already cover. I will draft it on my own seam and it lands through the normal path (`engineering-disciplines.md`, ratified per the adoption protocol). Third instance recorded here so the draft's evidence base is on file at three, dated, and not reconstructed later.

**6.3 — RATIFIED as operating protocol, immediately.** The two-tier split is correct and the reasoning is the same conflict seam as gandalf's CANON-STEWARD → jack-ryan ratifier switch: **proposer ≠ sole-ratifier-on-self**. KR's decline-to-self-edit is confirmed as the right instinct. Steward-of-record attribution — *obliged to surface defects, never entitled to be one's own ratifier* — is the load-bearing sentence. Tier-1 (charter substance) stays Matt-gated and is correctly **not** ruled by this spec. Under ADR-002 the Tier-2 lane is documentation-class and mine to approve; Tier-1 is not, and this ratification does not touch it.

**6.4 — RATIFIED AS A RECOMMENDATION → ESCALATE to Matt.** star-lord owning `factory/` is right on the evidence (spine, harness contract, lane, queue) and the durable-queue dispatch already addresses him as that seam. But `AGENTS.md` topology is Matt's surface and a seam-ownership row is not a documentation-class change under ADR-002 — **I do not grant it.** KR drafts the row; Matt nods. A standing seam with no owner is a real gap and it should not sit long.

---

## 6 · § 8 / Q62 — routing only

**CORRECTLY ROUTED. Verified filed** at `canonical/matt_decision_needed/README.md` (row Q62), carrying both one-word shapes, gandalf's lean, the cost of each branch, and pointers to § 8 and the commission. § 9.3's generalization of the fork to **vendor-generic** (one ruling covering interactive `codex` and interactive `grok` presence) is a correct scope move — it is the same question about the same working habit, and splitting it would produce two rulings that can disagree.

**I do not rule Q62 and neither does gandalf.** Recorded: whether Matt's own presence at a terminal pauses the fleet is a call about his working posture. The advisory state `interactive-vendor-cli-present` is implementable and reportable **now**, independent of the ruling — the build should ship it as advisory (D-1 already says so) and the ruling only decides whether it also gates.

---

## 7 · § 9 — the Grok lane bundle

**RATIFIED-WITH-AMENDMENTS (C, D, E).**

**§ 9.2's seal claim — VERIFIED TRUE.** U-4's Grok clause reads *"admitted-in-principle via the U-8 judge door ONLY … Pilot = one From/To judge batch, three-way verdict comparison (galadriel primary). Not a general research lane unless the judge pilot proves out."* § 9 governs the lane's **operating law**; it admits no workload U-4 did not already admit. **The door is not widened.** D-6 is correctly gated behind U-8 pilot authorization — *a harness with no admitted workload is speculative code* is the right test and I endorse it as the gate.

**§ 9.3's serial-by-CHOICE framing — RATIFIED, and this is the passage I scrutinized hardest.** Codex's serial law cites a **verified vendor precondition**; no equivalent xAI statement has been verified, and the spec says so rather than borrowing Codex's authority. That honesty is the whole point: a rule that quietly inherits someone else's grounding cannot be falsified later, because nobody can find what it rests on. Applying G-2's FALSE-BUSY ruling at the **policy** level is the correct disposition — serial costs delay, parallel-on-an-unknown-constraint risks an account-level fault — and the loosening clause is well-formed: **loosening requires the evidence NAMED, by amendment to this spec.** The cost/rate-limit half of P-3's granularity reasoning holds independently of the CI/CD precondition, so per-credential keying is right regardless of how the vendor question resolves. **The distinction between a law and a policy must survive into the code comments** — a future reader who finds `SerialLaneLock` on both lanes must be able to tell which one is a vendor precondition and which one is our choice, or the Grok policy will be defended as if it were the Codex law.

**Leader-mode prohibition — RATIFIED.** A shared backend multiplexing clients is a concurrency door around the serial lock, and closing it is correct. A live `leader.sock` process reading `busy-out-of-band` is the right fail-closed disposition.

**Cross-vendor parallelism — RATIFIED.** *"The law was never one vendor process per host"* follows directly from P-3's per-credential grounding. Parallel Codex+Grok is LEGAL; see Amendment B for the leg-2 consequence.

**P-7 / P-8 / P-9 / P-11 verbatim, no lane-specific variation — RATIFIED.** R-C applying doubly (a Grok verdict inside a galadriel judgment named inline as Grok-sourced) is correct and is my own amendment operating as intended. P-10's *no hand-fire era at all* is the right lesson drawn from the Codex lane's own history.

**AMENDMENT C — PIN THE DECLARED MODEL; RECORD THE RESOLVED ONE.** § 9.1 measures that the argv value `grok-4.6` **resolves to `grok-4.6-build`** in headless mode. A pin whose resolved target is chosen by a vendor-side rule is not a pin — it is a request, and P-5's grounding (*every banked lane statistic was measured at this config*) fails silently if the resolution moves under a CLI update. Ruled: the lane declares `grok-4.6` on the argv **and** captures the **resolved model identifier** from the JSON envelope's `modelUsage` key into the run-log detail column and the telemetry record, per call. A change in the resolved identifier at an unchanged declared pin is a **lane event that must be visible**, not a silent substitution. The envelope already carries it; this costs one field.

**AMENDMENT D — THE PILOT SAYS ITS REASONING-EFFORT ON THE ARGV, EVEN THOUGH NO PIN EXISTS YET.** § 9.3 correctly states that reasoning-effort is **UNPINNED** because no statistics are banked at any config — but leaving it unpinned means the banking measurement runs at whatever the vendor default is, which is exactly P-5's *"never left to ambient config"* defect arriving at the one run whose entire purpose is to establish the baseline. `--reasoning-effort` exists on both the top-level and `grok agent` surfaces (verified in `--help`). Ruled: the U-8 pilot **declares its effort value explicitly on the argv and records it in the run-log row**; that declared value becomes the pin, and A/B discipline applies from then on. The spec's Posture-2 logic (*a shallow second opinion launders confidence*) leans this high; the pilot names the number.

**AMENDMENT E — `--no-leader` IS ACCEPTED BUT UNDOCUMENTED AT THE TOP-LEVEL SURFACE; ASSERT IT, DO NOT ASSUME IT.** My parse test confirms the flag is accepted on a top-level `grok -p` argv (a known-bogus flag errors with `unexpected argument`; `--no-leader` does not). But it appears **only** in `grok agent --help`, not in `grok --help` — it is a hidden flag at the posture-of-record surface, and leader mode's default is `[cli] use_leader` in `~/.grok/config.toml` (currently absent, so ambient default is off — but it is ambient, which is the point). A protocol clause resting on an undocumented flag can be removed by a version bump with no help-diff to signal it, and the failure would be **silent re-entry through the concurrency door the lock exists to close**. Ruled: `GrokHarness` preflight **asserts** the flag is accepted (a parse-level rc check, no model call, no cost), and D-5's per-lane test suite **pins the assertion by literal** — the same treatment `lane.py` already gives its closed vocabularies. Refuse to fire the lane if the assertion fails, rather than firing with an ignored flag.

**AMENDMENT F — GOVERNANCE HOUSEKEEPING (documentation-class; ADR-002, mine to approve).** U-4's Grok clause still reads *"First step: headless-CLI capability probe — itself a Posture-1 Codex job."* That step is **DONE**, executed directly under Matt's direction rather than through the Codex lane. The routing supersession is properly disclosed in § 9.1 and is within Matt's authority; the U-4 block must be updated to read **DISCHARGED 2026-08-24 (Matt-directed live probe, not routed as a Codex job)** so the governance doc stops asserting an owed step that is complete. A block that asserts stale state is #73 arriving in the document that ratifies #73's build constraint.

---

## 8 · Action

- [ ] **gandalf** — mark Amendments A–F into the SPEC (A rewrites § 3's union-rule sentence; B replaces G-3's blast-radius clause with § 9.3's wording; C/D/E ride § 9.3 and § 9.4; F edits `workflow-upgrades.md` § U-4).
- [ ] **star-lord** — build D-1…D-5 under Amendment A: `queue-pending` is not busy; `_cmd_lane_status`'s `is_idle()` predicate changes; MIGRATION.md pins the per-state exit codes **and** the single named *"safe to fire"* predicate (ADR-004). D-5 gains the P-9 × leg-3 case. D-6…D-8 stay behind the U-8 pilot gate, under C/D/E.
- [ ] **KR** — execute the § 6.1 Tier-2 edit at `.claude/agents/knight-rider.md:68` (ratified above); draft the `AGENTS.md` `factory/` ownership row for Matt.
- [ ] **jack-ryan** — draft the source/authorship-provenance discipline candidate (§ 6.2 accepted; scope set by the two harm-instances, argued by the third).
- [ ] **Matt** — **Q62** (interactive vendor-CLI presence: advise / block; vendor-generic); **§ 6.4** `factory/` seam-ownership row; **§ 6.3 Tier-1** stands as your gate, unchanged.

## 9 · References

- `agentic_orchestration/gandalf/notes/2026-08-24-codex-lane-protocol-and-busy-check-SPEC.md`
- `agentic_orchestration/gandalf/requests/2026-08-24-knight-rider-codex-lane-protocol-and-busy-check.md`
- `agentic_orchestration/workflow-upgrades.md` § U-1 (THE LAW + #73 build constraint), § U-4 (R-A…R-D, Grok-via-U-8-door)
- `agentic_orchestration/factory/lane.py`, `factory/jobqueue.py`, `factory/harness/codex.py`, `factory/cli.py` (uncommitted working tree, read in full; **not staged by this commit** — #62(a))
- `agentic_orchestration/research/vfx-p2-dossiers/usage/_run-log.tsv` (30 rows, 30/30 four-column — verified)
- `agentic_orchestration/gandalf/notes/2026-08-24-vfx-archetype-binding-spec-DRAFT.md` § 6.6 (sealed fence — untouched)
- `canonical/matt_decision_needed/README.md` (Q62 row — verified filed)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` #10 (173), #11 (182), #19.1(b) (601), #62 (3001), #73 (3442)
- Live instrument checks this session: `grok models`, `grok --help`, `grok agent --help`, argv parse-acceptance test (read-only; no model call, no cost)

---

**jack-ryan**, 2026-08-24 — DEV-MODE ratification. **RATIFIED-WITH-AMENDMENTS A–F.** No sealed clause reopened; no BLOCK issued.
