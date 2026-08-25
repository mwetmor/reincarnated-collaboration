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

---

# ADDENDUM — 2026-08-24 (later same day) — RE-RATIFICATION of the U-4 Grok clause under AM-2

**Reviewer:** jack-ryan (DEV-MODE, ratification authority) · **Artifact:** spec § 10 (AM-2), commit `91de6444`
**Trigger:** Matt exercised the AM-1 § 13.3 release valve and ruled the selection order verbatim. AM-2 supersedes **my own ratified U-4 text**, so only a re-ratification moves it.
**Verdict: RATIFIED-WITH-AMENDMENTS (G, H, I)** — sequence continues A–F, which remain binding. **No BLOCK. D-6…D-8 are build-authorized on star-lord as of this addendum.**

## 1 · What is being waived — stated plainly, because a ratification that hides its own reversal is worthless

My clause read *"Not a general research lane unless the judge pilot proves out."* AM-2 grants general admission **and the pilot has not run**. The proves-out condition is **waived by directive, not satisfied by evidence**. Matt owns that call — the scope of a vendor lane is his surface, not mine, and the clause named the valve itself. What I rule is whether the waiver is carried honestly and mitigated adequately.

**It is carried honestly.** § 10.4(1)'s *"this pin is declared, not banked"* is the sentence I would have required had it been absent. § 10.3(2) grounds Codex primacy on the banked-vs-banking asymmetry rather than on preference. § 10.6 fences what AM-2 does not do. Nothing borrows authority it does not have — the same standard § 9.3 met on serial-by-choice.

**The mitigation is adequate but incomplete.** Codex-primary deterministic order means Grok takes spillover only, so exposure is bounded by Codex's occupancy rather than by an untested judgment. Every early Grok job doubling as a banking measurement is the right instinct. What is missing is the *close*: a waived proof condition replaced by a banking practice with **no named point at which anyone asks whether the widening proved out**. U-4's router got an empirical criterion; this widening got none. → **Amendment I.**

**Independently verified this session (#19.1(b), zero cost, no model call):** the effort vocabulary claim — `grok --reasoning-effort bogusvalue` returns *"unknown effort level 'bogusvalue'; use one of: xhigh, high, medium, low"*. Vocabulary is **CONFIRMED identical to Codex's** from the CLI's own error surface, not inherited from the spec. `grok 1.0.5 (5115b46bc909) [stable]` unchanged since my first pass.

## 2 · R-A consistency — § 10.3 opens no door R-A closed. CONFIRMED.

I read § 10.3 specifically hunting for the reverse-direction override. It is not there. Step 5 states vendor-first applies **only past the gate**; step 1's parenthetical preserves the Claude-ward override as the one named exception; step 4's Claude-now branch is R-A operating exactly as written (schedule-critical, ledger note, never silent). **No step routes work toward a vendor over a router NO**, and the deterministic order is a choice *between* vendors made after all four questions are YES. R-B is untouched and vendor-generic: no curator, no fire, either lane.

**INFO — the one pressure AM-2 creates, named so it can be watched.** Making vendor-first mandatory gives the dispatcher a standing incentive to answer the four questions YES, because YES is now the cheap path. R-D's standing caution was written for the mirror case (too few NOs = the covered set is too narrow); it generalizes here. The gate's answers are findings about the world and must not be shaped by the lane's cost. Not an amendment — a thing to notice at Gate if the NO rate goes to zero after AM-2.

## 3 · Amendments A–F — survival check, one by one

| # | Status under AM-2 |
|---|---|
| **A** (execution-occupancy union; `queue-pending` ≠ busy) | **SURVIVES, and becomes load-bearing on Matt's floor** — see G and H. |
| **B** (blast radius per-VENDOR) | **SURVIVES, cited by name** at § 10.4(2). Correct. But the § 4 G-3 body still carries the superseded per-host text — see G. |
| **C** (capture the resolved model id) | **HONORED** — § 10.4(1) captures `modelUsage`'s resolved id per call; `grok-4.6` → `grok-4.6-build` recorded as the known resolution. |
| **D** (effort said on the argv) | **HONORED, and improved** — `xhigh` is argv-said from the **first** job, not merely from the pilot. Consistent with P-5's Posture-2 lean. |
| **E** (`--no-leader` asserted, not assumed) | **SURVIVES UNAMENDED — and is now an active build constraint.** § 10.5 says *argv-said*; E requires more: `GrokHarness` preflight **asserts** the flag parses (rc check, no model call), D-5 pins the assertion by literal, and the lane **refuses to fire** if the assertion fails. The flag remains undocumented at the top-level surface; a version bump can remove it with no help-diff to signal it, and the failure mode is silent re-entry through the concurrency door. This mattered least when D-6 was gated; it matters most now that D-6 fires. |
| **F** (probe DISCHARGED) | **EXECUTED BY THIS ADDENDUM.** The U-4 Status paragraph recorded the discharge, but the clause body still asserted *"First step: headless-CLI capability probe — itself a Posture-1 Codex job."* My clause rewrite below carries the discharge into the clause itself. |

**AMENDMENT G — THE A–F FOLD-IN DEBT IS NOW LOAD-BEARING, NOT HOUSEKEEPING.** § 10 cites Amendment B *by number* while § 4's G-3 still reads *"counts busy against ALL lanes on this host"* and § 3's union rule still counts `ENQUEUED` toward busy. One document now contradicts itself, and a reader who lands in § 4 gets the superseded text with no marker. Under the U-8-door scope this was cosmetic. Under AM-2 it is not: an unattributable out-of-band `codex exec` would, on the unamended G-3, close the **Grok** lane too — driving selection-law step 3 straight past spillover into step 4, which is the branch that spends Claude. The widening converted a textual defect into a routing defect. **Ruled: gandalf folds A–F into the spec bodies (§ 3 union rule, § 4 G-3) before the crawl fires through the selection law.** My record remains the ratification of record and star-lord builds from it — so this does **not** gate D-6.

**AMENDMENT H — THE SELECTION LAW MUST SPEAK THE § 3 ANSWER-STATE VOCABULARY. `queue-pending` COUNTS AS *OPEN*.** § 10.3 says *open* and *closed*; § 3 already defines six answer states (`open`, `busy-lock`, `busy-out-of-band`, `queue-pending`, `auth-expired`, `cli-missing`). Two vocabularies for one question means every dispatcher re-derives the mapping, which is exactly the folklore the busy check was built to abolish. Compose the gap with Amendment A's own failure shape and the harm is concrete: one P-9 HELD job on each vendor lane makes both read *closed*, step 4 fires, and **Claude takes vendor-scoped work on backlog alone** — inverting Matt's verbatim floor via a state that means *the lane is free and a drain will take it*. **Ruled: `queue-pending` is OPEN for selection purposes.** *Closed* for steps 1/3/4 means `auth-expired` or `cli-missing` — the lane cannot take the work at all. `busy-lock` / `busy-out-of-band` are **occupied-but-available**: the lane takes the work by enqueue, which is step 4's default, not step 4's Claude branch. The dispatcher binds to the **one named "safe to fire" predicate** Amendment A already required MIGRATION.md to pin (ADR-004); the router's Q3 text — still *"last `_run-log.tsv` row terminal"*, which is leg 3 alone and pre-Amendment-A — binds to that same predicate rather than restating a rule it can drift from.

**AMENDMENT I — THE WAIVED PILOT IS REPLACED BY A DECLARED 10-JOB BANKING WINDOW, NOT BY NOTHING.** A proof condition removed by directive leaves a hole that banking practice alone does not fill, because banking with no close never returns a verdict. **Ruled: the first 10 Grok jobs are a declared banking window.** Every row carries curator (R-B), resolved model id (C), declared effort (D), and the per-call `costUSD` the envelope already provides. At close, the window is compared against Codex's banked baseline on the criteria U-4's model-pin discipline already names — curation WARN rate and URL/claim-verification pass rate. Outcomes, all admissible: rates comparable → the deterministic order is confirmed as a banking artifact and re-ranking becomes a live U-5 question; rates materially worse → Codex primacy holds on evidence rather than on precedence, and Grok's scope is revisited **by amendment, at the same authority level that widened it**; **the window cannot be assembled because Grok never receives spillover** → the widening was inert, which is G-S4's *a lane that never fires has failed* applied to the second vendor, and is a finding, not a non-event. The judge door's information is not lost — § 10.2 keeps judge batches firing both vendors, so the three-way comparison still arrives; AM-2 removed its ordering as a gate, not its existence. 10 matches U-4's own router criterion; I am reusing an existing number rather than inventing one.

## 4 · Rulings carried without amendment

**§ 10.2 widening — RATIFIED.** The U-8 judge role retained *inside* the wider scope is the right shape: disagreement structure remains the product, galadriel stays primary, R-C provenance verbatim. A widening that had dissolved the judge door into general research would have cost the one thing the third vendor was admitted for.

**§ 10.3(2) deterministic order — RATIFIED, and this is the clause I scrutinized hardest.** *Never random* is the load-bearing half. Random vendor assignment is an undeclared A/B experiment running permanently across every measurement the fleet takes — it would make every future comparative statistic unattributable (#10). The banked-vs-banking ground is real and it is the correct ground, because it names a condition under which the order **changes**: U-5 evidence, per-class comparative rows. An order grounded in preference could never be dislodged.

**§ 10.4(2) — CORRECT, and correctly framed as *not a fork*.** Per-credential locking was ratified law from § 9.3; KR's *"strictly better than fallback"* is a reading of the design, not an assumption he was making. Nothing to rule.

**§ 10.5 gate move — RATIFIED.** *A harness with no admitted workload is speculative code* was my endorsed test, and AM-2 admits the workload. The gate's premise is satisfied, not bypassed. **D-6…D-8 build-authorized**, under C, D, and E, composing with A and H.

**§ 10.6 scope guard — RATIFIED.** Sealed and unchanged, verified against the spec text: serial law (Codex, vendor-precondition), serial-by-choice (Grok, § 9.3), THE LAW (U-1), R-B curator law, the Q62 ruling, the four-question router itself, the tier-2 VFX law and its § 6.6 fence, the whirlwind clean-room quarantine. **P-10 applies to Grok from birth — no hand-fire era, and AM-2 does not create one.**

## 5 · Action

- [ ] **gandalf** — Amendment G: fold A–F into the spec bodies (§ 3 union rule, § 4 G-3) before the crawl fires through the selection law; mark H's vocabulary binding into § 10.3 and I's banking window into § 10.4.
- [x] **jack-ryan** — U-4 Grok clause rewritten to the superseding text (this addendum executing; Amendment F discharged in the clause body).
- [ ] **star-lord** — D-6…D-8 **BUILD-AUTHORIZED NOW**. Carry Amendment E as a hard preflight (assert `--no-leader` parses; refuse to fire otherwise; D-5 pins it by literal), C (resolved id per call), D (`xhigh` argv-said from job one), A + H (`queue-pending` is not busy and is *open* for selection; one named safe-to-fire predicate in MIGRATION.md, ADR-004).
- [ ] **KR** — bind the router's Q3 to the named predicate rather than to *"last row terminal"*; open the Amendment I banking window on the first Grok fire and count it.
- [ ] **Matt** — nothing owed. The waiver is yours and is recorded as a waiver.

## 6 · References

- `agentic_orchestration/gandalf/notes/2026-08-24-codex-lane-protocol-and-busy-check-SPEC.md` § 9, § 10 (commit `91de6444`)
- `agentic_orchestration/gandalf/notes/2026-08-24-fleet-flightrecorder-board-spec-DRAFT.md` § 13.3 (AM-1 release valve — verified verbatim)
- `agentic_orchestration/workflow-upgrades.md` § U-4 (clause rewritten by this addendum), § U-5 (re-rank evidence path), § U-8 (judge door, retained)
- Live instrument check this session: `grok --reasoning-effort bogusvalue` parse-error vocabulary enumeration; `grok --version` (read-only, zero cost, no model call)

---

**jack-ryan**, 2026-08-24 — DEV-MODE **RE-RATIFICATION. RATIFIED-WITH-AMENDMENTS G, H, I.** A–F stand. No sealed clause reopened; no BLOCK issued. The waived condition is recorded as waived, and Amendment I gives it a close.

---

# ADDENDUM 2 — 2026-08-24 (night) — GATE-2 on `dddd232d` + RATIFICATION of § 11 (agent-level seam custody)

**Reviewer:** jack-ryan (DEV-MODE, BLOCK authority) · **Targets:** commit `dddd232d` (star-lord, D-1…D-8); spec § 11 (gandalf, commit `61b421e0`)
**Verdicts: GATE-2 = PASS-WITH-FINDINGS. § 11 = RATIFIED-WITH-AMENDMENTS (K, L).** Sequence continues A–I; **J** is issued at Gate-2 and amends the Amendment-H consumer clause. **No BLOCK. Nothing sealed reopened.**
**Principles applied:** REVIEW_PROCESS #2 (smoke-gate), #3 (cross-seam impact), #5 (severity) · Disciplines **#10**, **#11**, **#19.1(b)**, **#62(a)**, **#73** · ADR-002, ADR-004, ADR-006.

---

## 1 · The test run, from my hands (#19.1(b) — I did not accept the count)

| Suite | Result |
|---|---|
| `agentic_orchestration/factory/tests/` | **735 passed, 0 failed** (203 s) |
| `agentic_orchestration/factory/ui/tests/` | **18 passed, 0 failed** (11 s) |
| **Total** | **753 passed, 0 failed** — reproduces star-lord's reported count **exactly** |

No network reached; no vendor CLI invoked by any test. Separately: `agentic_orchestration/flight/tests/` is **2 failed / 74 passed** — those are the two reds star-lord *declared* in `ca3ec471`, which post-dates `dddd232d` and belongs to the U1-BUILD workstream. **Out of this gate's scope**, recorded so nobody later reads my 753 as a whole-repo claim.

---

## 2 · Amendment compliance — audited one by one

| # | Ruling | Evidence |
|---|---|---|
| **A** | **PASS** | `SAFE_TO_FIRE_STATES = frozenset({"open", "queue-pending"})`; `read_runlog` sets `executing` only for `START`/unrecognised markers; the P-9 × leg-3 row exists by name — `test_AMENDMENT_A_a_HELD_job_answers_queue_pending_and_is_SAFE_TO_FIRE`. MIGRATION § 1 explains *why* `is_idle()` was the wrong composite and keeps it exported as correct-about-what-it-measures. |
| **B** | **PASS** | `classify_processes(cfg, procs)` keys every match to a per-vendor `LaneConfig`. Held by **two** rows, both directions, plus `test_the_argv_patterns_are_ANCHORED_and_do_not_convict_a_MENTION` — which is the row I would have asked for and did not have to. |
| **C** | **PASS** | Live finish row carries `resolved_model=grok-4.6-build`; telemetry carries `declared_model`, `resolved_model_ids`, `model_resolution_captured`. Declared pin and resolved id are both on the record, separately. |
| **D** | **PARTIAL → FINDING G2-1 (WARN)** | argv-said (`--reasoning-effort xhigh`) and telemetry (`reasoning_effort: "xhigh"`) — **yes**. Run-log row — **no**. See § 4. |
| **E** | **PASS** | `assert_no_leader_parses()` is a parse-level rc check with no model call, pinned by literal `NO_LEADER_FLAG`, evaluated **before the lock is taken** so a refused lane never holds it, and returning `PREFLIGHT REFUSED (lane spec Amendment E)` rather than raising. Stronger than I ruled: I asked for refuse-to-fire, he also made the refusal not-take-the-lock. |
| **H** | **PASS inside `factory/`; violated in fact outside it → AMENDMENT J** | MIGRATION § 1 pins the predicate **by state name** in a blockquote, `SAFE_TO_FIRE_STATES` is pinned by equality in `test_vocabularies.py`, and the three dispositions are asserted to **partition** the vocabulary so a state deleted from one set and not added to another reds a row instead of leaving the denominator. See § 5. |
| **THE LAW** | **PASS, and the test is REAL** | Three rows, not one. `_tree_fingerprint` digests **content and mtime_ns** for every file under the queue root across three status calls and compares the whole dict — a behavioural claim, not a tautology. A second row counts telemetry events. A third refuses `RunLog`/`Telemetry` imports and filesystem-mutating calls **over the AST**. The docstring records that the coarse first version (*"no call named `append`"*) failed on a local `signals.append` and was replaced — a test that reports its own false-positive history is a test somebody actually exercised. Plus `test_THE_LAW_asking_does_not_CREATE_the_lock_file`, which catches the O_CREAT trap I had not thought of. |
| **Serial law** | **INTACT** | Exactly one `subprocess.run` site in `grok.py::run`; `SerialLaneLock(...).acquire()` immediately precedes it, `pass_fds=(lock.fd,)` gives the child the fd, `finally: lock.release()`. `TimeoutExpired` kills the **child** and returns `ok=False` — it does **not** break the lock. No `--force`, no reaper. The `force=` parameter on `assert_no_leader_parses` is a preflight-**cache** bypass, verified by reading it, not a lock-break. |

**INFO (not an amendment).** The AST leg of THE LAW refuses `ImportFrom` of `RunLog`/`Telemetry` and a named set of mutating attribute calls. It would not catch `import jobqueue` + `jobqueue.RunLog(...)`, nor `os.remove` / `os.rename` / `os.makedirs`, nor `.open("w")` reached as an attribute. I am **not** ruling on it: the behavioural fingerprint row tests the actual claim, and the AST row is the structural belt, not the braces. Recorded so a future reader does not mistake the belt for a proof.

---

## 3 · The three named deviations — ruled

### Deviation 1 — `busy-unknown` as a seventh answer state: **RATIFIED — and it is not a new deviation.**

I ruled this **RATIFY** earlier today at `agentic_orchestration/qa/findings/2026-08-24-u1-schema-law-ratification.md` § 6, on the flight-recorder's degraded card, with a WARN-3 carry-forward. Nothing has changed in its favour or against it, and I do not re-litigate my own ruling twelve hours later.

**Yes, false-open is the alternative**, and it is the one direction G-2's FALSE-BUSY ruling forbids. An unreachable leg coerced into an existing label is the semantic-shift failure; a lane whose lock could not be read rendering `open` is the failure that fires a second job at an occupied credential. `STATE_PRECEDENCE` places it above `auth-expired`/`cli-missing` and above `open` — ambiguity outranks a credential state, which is the right ordering. Exit `22` sits in the occupied band, and `exit_code_for()` returns **22 for any state nobody named**, pinned by `test_the_exit_code_for_an_UNNAMED_state_is_busy_unknown_NEVER_zero`. That fail-closed default is the part I care about most: the vocabulary can grow wrong without the exit code going fire-safe.

**It belongs in the spec by amendment: § 3's answer-state list goes from six to SEVEN.** Editorial debt on gandalf, folded with the outstanding Amendment-G fold-in. The spelling is genuinely shared with the board (`flight/bin/flight_report:98`) — see Amendment J for why *shared spelling* is not yet *shared definition*.

### Deviation 2 — per-state exit codes vs. `0 = open`: **RATIFIED AS BUILT. This is the only correct reconciliation.**

The two constraints really do pull apart: the spec imposed `0 = open`, Amendment A required `open` and `queue-pending` **separately identifiable by exit code**. One integer cannot satisfy both. The resolution — **two questions, two surfaces** — is right: the default exit answers *what state*, `--safe-to-fire` answers *may I fire*, and neither has to lie for the other.

The load-bearing addition is the one star-lord made and I did not ask for: **the band.** `[ $? -lt 20 ]` lets a shell caller bind to the **predicate** without knowing the vocabulary at all — which is Amendment H satisfied at the shell boundary, where I had only pinned it at the Python boundary. A future eighth state cannot be handed a number that reads fire-safe to a band-checker, and `test_lane_status.py` asserts the banding separately from the table so the two cannot drift. `--lane all` returning the **worst** lane's code under fail-closed precedence is correct — a caller reading only the exit code is never told *open* while a lane is occupied. Exit `2` reserved to argparse and documented as *not ours* is the right kind of honesty about a number we do not control.

### Deviation 3 — the `test_JR24` adjudication: **IT WAS ADJUDICATION. VERIFIED, NOT ACCEPTED.**

I did not take the inherited claim. I built a clean worktree at **`dddd232d^`** and ran the row:

```
FAILED test_vocabularies.py::test_JR24_the_classifier_ADJUDICATES_what_it_cannot_CLASSIFY
AssertionError: public UPPERCASE names the classifier cannot place:
['ui/board.py:AO_DIR', 'ui/board.py:FACTORY_DIR', 'ui/board.py:FLIGHT_DIR', 'ui/board.py:HERE',
 'ui/board.py:REPO_ROOT', 'ui/tests/test_board.py:AO_DIR', 'ui/tests/test_board.py:FACTORY_DIR',
 'ui/tests/test_board.py:FLIGHT_DIR', 'ui/tests/test_board.py:NOW',
 'ui/tests/test_board.py:REPO_ROOT', 'ui/tests/test_board.py:UI_DIR']
```

**RED at the parent commit, on exactly those eleven names, no more and no fewer.** The claim is true and the scope is exact.

**And the remedy applied is the remedy the test itself prescribes**, in its own docstring: *"the third exit reds this row, and clearing it means writing the name into `NOT_A_VOCABULARY` with a reason — which is the adjudication, performed by a human, exactly once."* That is what was done. He did **not** widen `_classify_module`, did **not** add a subtree exemption, did **not** touch `FACTORY_RUNTIME_FILES`, and did **not** edit drax's files. Authoring-around would have looked like any of those four; none is present.

I checked the eleven **reasons** against source rather than trusting the labels: `ui/board.py:60–64` and `ui/tests/test_board.py:30–34` are all `os.path.dirname` / `os.path.join` expressions, and `test_board.py:41` `NOW` is `datetime.datetime(2026, 8, 25, 0, 0, 0, tzinfo=utc)` — a fixed clock reading. **All eleven reasons are true.** Ruled **CORRECT**.

**INFO, and it is a positive one.** This is a cross-seam classification made unilaterally on drax's names. It is the right call — the alternative was leaving a red nobody wrote down, and *a suite that is red for a reason nobody wrote down is a suite people learn to scroll past* is the correct governing sentence. What makes it clean is the in-file header: **"ADJUDICATED HERE, NOT AUTHORED HERE."** That is precisely the source/authorship-provenance discipline I accepted the draft assignment for at § 6.2. I am recording it as a **fourth instance — the first positive one**, showing the rule already has a practised shape to codify rather than one to invent.

---

## 4 · FINDINGS

### G2-1 — **WARN. Amendment D is honoured on the argv and in telemetry; it is NOT honoured on the run-log row, and MIGRATION asserts that it is.**

My Amendment D reads: *"the pilot declares its effort value explicitly on the argv **and records it in the run-log row**."* The live finish row is

```
2026-08-25T00:36:20Z  smoke-grok-lane-2026-08-24  rc=0  attempt=1 elapsed_s=5.1 tokens=30645 resolved_model=grok-4.6-build cost_usd=0.00983  curator=star-lord  event=finish
```

No `effort=` token. § 7's detail-token table lists three conventions (`router=`, `resolved_model=`, `cost_usd=`) and effort is not among them — but **MIGRATION § 5 asserts "every row carries curator + resolved model id + declared effort + per-call `cost_usd`."** A document asserting a property the artifact does not carry is **#73 arriving in the MIGRATION doc that pins #73's own build constraint** — the same shape as Amendment F, one layer up.

Nothing is lost (`telemetry.jsonl` has it), so this is WARN and not BLOCK. But the surface Amendment I names for the banking window is the **run-log**, and effort is one of the three things the window must attribute against. **Action, star-lord:** add `effort=<value>` to the finish row and to § 7's table, or strike the claim from § 5. One of the two, not neither.

### G2-2 — **WARN. The smoke job's real finding — a ~28K-token per-job floor — did not survive into the cost expectations.**

MIGRATION § 10 settles the token *arithmetic* exactly right, by the vendor's own numbers rather than by inference (`28,170 + 2,432 + 0 + 43 = 30,645`; the subset reading gives 28,213, which matches nothing). That is model work and I endorse it.

What is **absent** is the operational fact the same measurement exposed: **28,170 input tokens on a one-line prompt.** That is not the prompt; it is a fixed context the CLI injects on every call. It is a **per-job cost floor**, and it is material to Amendment I, whose whole purpose is to compare Grok's banking window against Codex's banked baseline. An unrecorded fixed overhead makes every per-job cost comparison mis-attribute CLI overhead to the model or to the effort pin — **#10, change one thing and measure one thing**, defeated before the window opens. `$0.00983` for 43 output tokens is a number that will mislead anyone who meets it without the floor beside it.

**Action, star-lord:** record the floor in MIGRATION § 10 as a named quantity with its measurement (job `smoke-grok-lane-2026-08-24`), so the banking window's cost column is read against it. **Verified separately and correctly:** the smoke row carries `router=SMOKE` / `job_class=smoke` and is properly outside the Amendment-I window, which counts the first ten **production** jobs.

### AMENDMENT J (BINDING) — **THE RATIFIED PREDICATE HAS TWO IMPLEMENTATIONS AND NOTHING BINDS THEM.**

`agentic_orchestration/flight/bin/flight_report` carries its own `STATE_PRECEDENCE`, `SAFE_TO_FIRE_STATES`, `OCCUPIED_STATES`, `CLOSED_STATES` and `lane_answer()`. I grepped: **`lane_status` appears zero times anywhere under `flight/` or `factory/ui/`.**

I compared them member-for-member and order-for-order: **they agree today, exactly.** `lane_status.py` even says so in a comment — *"Identical ordering to the fleet board's `STATE_PRECEDENCE`, deliberately: one question, one answer, two renderers."*

**Deliberately identical by hand-copy is not bound.** Amendment H's sentence is *consumers bind to the predicate by name, never re-derive it*; this is the **largest consumer**, re-deriving it in full. The blast radius is not abstract: the fleet board is Matt's decision surface, and § 11.3 now instructs a dispatcher to consult it before spawning. An eighth state added to `lane_status.py` — `busy-unknown` was a seventh, so this is a demonstrated growth path, not a hypothetical — renders on that board through a classifier that has never heard of it, and `flight_report:137`'s `if ans["state"] in CLOSED_STATES or ans["state"] == "busy-unknown"` will colour it by falling through. The duplicate was written honestly, when D-2 **did not exist** and the card was declared *degraded — D-2 CLI pending*. **That justification expired at `dddd232d`.**

**Ruled: one test asserts the four vocabularies AND `STATE_PRECEDENCE` are EQUAL across the two modules, and reds on any divergence.** I am **not** ordering a refactor — `flight_report`'s standalone-script shape is a deliberate G-4 property and importing `factory` into it would trade away more than it buys. A test is enough. It is cheap, it converts a comment into a mechanism, and it is exactly what `test_vocabularies.py` already does for every other pin in the package. **Owner: star-lord** (both files sit on his seam). **WARN, not BLOCK** — they agree today, so nothing is presently wrong; the amendment exists so that stays true by mechanism rather than by memory.

---

## 5 · § 11 — agent-level seam custody

### 5.1 · The #73 question: **gandalf's argument HOLDS.** Checked, not accepted.

The defect #73 names is a **status header asserting state** — true when written, false by mtime, with nobody able to tell which. That is not an analogy to the founding incident; it **is** the founding incident, in KR's own words: *knowledge true when formed and false by mtime 20:32.*

A CLAIM row does not have that property. It is a statement about a **past event** — *at time T, dispatcher D spawned into seam S* — and a past event cannot become false by the passage of time. Occupancy is never read off a row; it is the derivation `last CLAIM without RELEASE, per seam × holder-session process liveness`. **Leg 2 is kernel state in exactly G-1's sense:** sessions ARE host processes, `ps` is the kernel's answer, and nobody writes it. That is the same reasoning I independently concurred with for `flock`, applied one level up, and it survives the same test. **No TTL** is correct for the § 2 P-2 reason and I do not reopen it: a TTL is a timeout-based lock break wearing a different word, and it would silently free a claim whose holder is alive and mid-flight.

### 5.2 · Hand-append before D-9: **SOUND. RATIFIED.**

The vendor lane's own lesson is applied correctly — *the record's schema was the gap, not the tooling*. I verified both seeded rows are **6-column**, matching the declared format family. Starting the habit before the tool exists is right, and it is why this ratification has a ledgered claim to close.

### AMENDMENT K (BINDING) — **THE LEDGER BUYS VISIBILITY, NOT MUTUAL EXCLUSION. SAY SO — AND CLOSE THE RACE AT D-9.**

§ 11.3's rule is **check, then claim**. That is a time-of-check/time-of-use race: two dispatchers may both read *free*, both append CLAIM, and both spawn. **That is the founding incident, unprevented by the mechanism built to prevent it.** The vendor lane does not have this problem because `flock` is an **atomic test-and-set**; the custody ledger has no atomicity whatsoever.

This does not sink § 11, and I want to be precise about why: **visibility alone would have stopped the founding incident.** KR would have seen gandalf's row and stood down twenty-eight minutes earlier, without coordination, without a conversation. That is a real and sufficient win. What must not happen is § 11 **spending flock's authority on a mechanism that does not have it** — the same defect § 9.3 avoided so carefully when it refused to let the Grok serial policy borrow the Codex law's grounding. A rule whose strength is misdescribed cannot be reasoned about later.

**Ruled:**
1. § 11 states plainly that the hand-append era provides **visibility, not exclusion**, and that the exclusion is a **dispatcher discipline** resting on it.
2. **D-9's `custody claim` performs check-and-append ATOMICALLY, under an `flock` on the ledger file.** The primitive already exists at `factory/lane.py::SerialLaneLock` and costs nothing to reuse; G-1's grounding carries over unchanged (derived kernel state, content never trusted, released by the kernel on holder exit).
3. **D-10 gains the row:** two concurrent claims on one seam — exactly one wins, and the loser is told who holds it.

### AMENDMENT L (BINDING) — **A RUN-SCOPED CONDUCTOR CLAIM NAMES ITS SEAMS AND ITS RELEASE CONDITION. NO WILDCARDS, NO BLANKET ROWS.**

Yes — the door is real, and it is the one I was asked to hunt for. Compose three ratified clauses: *a RUN-CONDUCTOR charter claims its seams FOR THE RUN* + *no TTL* + *occupied seam → DO NOT SPAWN*. A multi-day charter over eight seams then holds the fleet for days, with **no expiry, no named end, and OVERRIDE unavailable because the holder is alive**. § 11.5's *custody is dispatch exclusivity, never seam ownership* is a statement of intent with no mechanism behind it — and the practical effect of an unbounded live claim is indistinguishable from ownership, which is the thing the sentence promises it is not.

The spec already solved this exact problem one level down, and I am reusing its answer rather than inventing one: **P-9 requires a hold to name the condition that ends it.** That is what makes a hold governance instead of drift, and it is what makes a claim governance instead of a lock.

**Ruled:**
1. A run-scoped claim writes **one row per seam** — never a wildcard, never a blanket row — so a dispatcher checking seam X finds a row **about seam X**, and a partial release is expressible.
2. **Every CLAIM row's `intent` names the condition whose satisfaction produces the RELEASE.** A claim whose release condition cannot be stated is a claim that should not be written.
3. D-9's `custody claim` **refuses a claim with no stated release condition**, the same way the Grok harness refuses an undeclared vendor rather than defaulting one.

This is P-9 at the agent level, and it is what turns *custody ≠ ownership* from asserted into checkable.

### 5.3 · Ratified without amendment

**The routing rule itself — RATIFIED.** *Check before spawning; occupied = do not spawn; standing down gets a ledger row, not a shrug* is correct, and making the stand-down **ledgered** is the load-bearing half: an unrecorded stand-down teaches nobody, and KR's was the finding that produced this section. **Custody does not replace KR's sequencing authority** — right, and the distinction is clean: custody is how two live routers see each other, not a third router. **Matt outranks custody** — right, and § 11.5's observation that his presence is visible via leg 2 regardless means the exemption costs no blindness. **Grain = agent name, widening only by amendment on an instance** — right, and it is the same evidence discipline U-4's router criterion uses.

**Build delta D-9 / D-10 — AUTHORIZED on star-lord**, under K and L, with `check` held to the same emits-nothing discipline as § 3 and banded exit codes pinned in MIGRATION.md. The eventual SEAMS board card is a **VIEW** per THE LAW — and per **Amendment J**, it binds to the custody predicate by name rather than re-deriving it. That is J's whole point arriving before the second instance instead of after it.

**INFO — RELEASE authorship is unspecified.** § 11.2 says CLAIM is written by the dispatcher; it does not say who writes RELEASE. Both seeded rows carry the same holder (`gandalf-session-85515`) for two different seams, which is correct — the holder column names the **session that must be alive**, not the agent — but a crashed sub-agent whose dispatcher also dies leaves a claim that only OVERRIDE can clear. Leg 2 covers that case, so this is not an amendment. Name it in D-9.

**INFO — holder ids are PIDs, and PIDs recycle.** A dead session whose PID is reassigned reads **alive**, which fails in the FALSE-BUSY direction and is therefore G-2-consistent and safe. But an OVERRIDE refused by a recycled PID will look wrong to the operator at the moment they most need the ledger to make sense. **D-9's liveness leg should compare process START TIME as well as PID** (`ps -o lstart=`). Cheap, not blocking, not an amendment.

---

## 6 · Action

- [ ] **star-lord** — **G2-1**: put `effort=` on the run-log finish row and in MIGRATION § 7, or strike the claim from § 5. **G2-2**: record the ~28,170-token per-job floor in MIGRATION § 10 as a named measured quantity, before the Amendment-I window closes. **AMENDMENT J**: one test binding `flight/bin/flight_report`'s four vocabularies + `STATE_PRECEDENCE` to `factory/lane_status.py`'s, red on divergence. **D-9 / D-10 authorized** under K (atomic check-and-claim under an flock on the ledger; concurrency row in D-10) and L (one row per seam; refuse a claim with no stated release condition).
- [ ] **gandalf** — § 3's answer-state list goes from **six to seven** (`busy-unknown`, already ruled at the U1 finding § 6); fold K's *visibility-not-exclusion* sentence and L's naming rule into § 11.2/§ 11.3. Carries with the outstanding Amendment-G fold-in debt.
- [ ] **KR** — nothing new. The Q3 binding and the Amendment-I count stand from Addendum 1.
- [ ] **Matt** — nothing owed by this addendum. § 11 is fleet law as ratified, and it is yours to veto at will; Q62 is ruled and § 6.4 remains in your queue.

## 7 · References

- `agentic_orchestration/factory/lane_status.py`, `factory/harness/grok.py`, `factory/cli.py`, `factory/MIGRATION.md` (§ 1, § 2, § 5, § 7, § 10)
- `agentic_orchestration/factory/tests/test_lane_status.py`, `test_grok_harness.py`, `test_vocabularies.py`
- `agentic_orchestration/flight/bin/flight_report:98–117, 137, 466–560` (the second derivation — Amendment J)
- `agentic_orchestration/lanes/grok/_run-log.tsv`, `lanes/grok/telemetry.jsonl`, `lanes/README.md`
- `agentic_orchestration/lanes/agents/_custody.tsv` (both seeded rows verified 6-column)
- `agentic_orchestration/qa/findings/2026-08-24-u1-schema-law-ratification.md` § 6 (`busy-unknown` — my earlier RATIFY, WARN-3)
- `agentic_orchestration/gandalf/notes/2026-08-24-codex-lane-protocol-and-busy-check-SPEC.md` § 11 (commit `61b421e0`)
- Live checks this session: full suite from a clean run (753/753); **`test_JR24` reproduced RED in a throwaway worktree at `dddd232d^`** on exactly eleven names; all eleven adjudication reasons verified against `ui/board.py:60–64` and `ui/tests/test_board.py:30–34, 41`; vocabulary comparison across both derivations. Zero cost, no vendor call.

---

**jack-ryan**, 2026-08-24 — DEV-MODE. **GATE-2 on `dddd232d`: PASS-WITH-FINDINGS** (G2-1, G2-2, Amendment J). **§ 11: RATIFIED-WITH-AMENDMENTS K, L.** A–I stand. No sealed clause reopened; no BLOCK issued. Custody RELEASE row appended — the first ledgered claim/release cycle closes on its own record.
