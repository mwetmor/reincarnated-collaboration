# Research — Codex parallel fan-out on a personal OpenAI account: risk assessment — 2026-08-25

**Mode:** A (analytical)
**Commissioner:** gandalf
**Agent:** legolas (UNKNOWN-RESEARCHER)
**Scope:** Matt's *personal* OpenAI account (Plus/Pro tier) on the project Mac. Enterprise work laptop explicitly out of scope.
**Access posture:** read-only web research. No credentials used, no account state inspected.

---

## 1. Top-line answer

**Compliance risk: LOW. Economics risk: HIGH — and the economics risk is real, current, and unresolved.**

The two halves of the question separate cleanly, and they do not have the same answer.

| Dimension | Verdict | Confidence |
|---|---|---|
| **Compliance / ToS / account-action risk** | Not prohibited. Parallel agent execution is a *first-party shipped feature* of Codex with its own config surface. No ToS clause forbids concurrency. No evidence found of any account actioned for parallel Codex use. | **HIGH** |
| **Economics / quota risk** | Severe and live. Multiple 2026 reports of full weekly quotas draining in hours-to-overnight under parallel subagents, including on Pro 20x + `gpt-5.6-sol` — Matt's exact configuration. Metering bugs still OPEN. | **HIGH** |
| **Superlinear burn (worse than N×)** | Contested. OpenAI's stated expectation is *roughly linear*; user reports claim far worse; at least one careful audit shows part of the reported excess is a telemetry double-count artifact. Genuinely unsettled. | **MEDIUM** |

**The headline distinction that drives everything below:** the severe quota incidents are concentrated in **Codex's own internal recursive subagent feature** (`spawn_agent`, MultiAgent V2, fork trees nesting 4 levels deep), *not* in flat parallel invocation of independent `codex exec` processes. Matt's described pattern — Claude fanning out N parallel Codex sub-agents — is closer to the second, which carries materially less of the documented blast radius. **This distinction is load-bearing for the decision and is the single most decision-relevant thing in this note.**

---

## 2. Evidence by source

### 2a. Primary — OpenAI Terms of Use (consumer)

**Source:** OpenAI Terms of Use, **Effective January 1, 2026**, retrieved 2026-08-25 via Wayback snapshot `20260823143939` (openai.com serves 403 to non-browser clients; see § 3).
<http://web.archive.org/web/20260823143939/https://openai.com/policies/row-terms-of-use/>

The complete "What you cannot do" list, verbatim. You may not:

> Use our Services in a way that infringes, misappropriates or violates anyone's rights.
> Modify, copy, lease, sell or distribute any of our Services.
> Attempt to or assist anyone to reverse engineer, decompile or discover the source code or underlying components of our Services…
> **Automatically or programmatically extract data or Output** (defined below).
> Represent that Output was human-generated when it was not.
> **Interfere with or disrupt our Services, including circumvent any rate limits or restrictions** or bypass any protective measures or safety mitigations we put on our Services.
> Use Output to develop models that compete with OpenAI.

And from Registration:

> You may not share your account credentials or make your account available to anyone else and are responsible for all activities that occur under your account.

**Adjudication of the three clauses that could plausibly bite:**

1. **"Automatically or programmatically extract data or Output."** This is a *scraping/exfiltration* clause — its neighbours in the list are reverse-engineering and competing-model training, which fixes its sense. Using OpenAI's own first-party CLI, in a mode OpenAI ships and documents, to receive Output you then use in your own project, is not "extraction" in this sense. **Does not bite.**
2. **"Circumvent any rate limits or restrictions."** The operative verb is *circumvent* — evade, bypass. Consuming your allowance quickly is the precise opposite: it is honouring the limiter until it stops you. Parallel fan-out hits the limit sooner; it does not route around it. **Does not bite** — provided no retry-hammering, no multi-account rotation, no proxying to dodge a 429.
3. **"Not share credentials / not make your account available to anyone else."** One human (Matt), one account, one machine. Parallel *processes* are not parallel *people*. **Does not bite.**

**Critically: there is no clause anywhere in the consumer ToS restricting concurrent sessions, simultaneous requests, or automation as such.** The document is silent on concurrency. Some secondary commentary asserts a "ChatGPT Plus is restricted to a single individual and concurrent sessions can trigger flags" rule — I could **not** substantiate that against the terms text; it appears to be SEO-blog inference conflating *account sharing* with *concurrent processes*. Treat it as unsupported.

**Suspension clause** (for completeness) — OpenAI may suspend/terminate if you breached the Terms or Usage Policies, if legally required, or if "your use of our Services could cause risk or harm to OpenAI, our users, or anyone else." The third limb is broad, but nothing in the parallel-fan-out pattern engages it.

### 2b. Primary — parallelism is an official, shipped Codex feature

**Source:** Codex docs, Subagents — <https://learn.chatgpt.com/docs/agent-configuration/subagents> (retrieved 2026-08-25)

Codex ships first-class multi-agent orchestration: `spawn_agent`, `send_message`, `followup_task`, `wait_agent`, `list_agents`, `close_agent`. Config surface under `[agents]` includes `agents.enabled` (default `true`) and **`agents.max_concurrent_threads_per_session`** ("caps concurrently open spawned-agent threads, excluding the primary"; `agents.max_threads` retained as a legacy alias). When unset, "Codex chooses the default."

**This is the strongest compliance evidence in the file.** A vendor does not ship a concurrency *governor* for a behaviour it forbids. The existence of `max_concurrent_threads_per_session` presupposes that concurrent threads are a sanctioned thing to have.

The docs carry an explicit economics warning, stated twice:

> Because each subagent does its own model and tool work, subagent workflows consume more tokens than comparable single-agent runs.

Note what that warning is and is not: a **cost** advisory, not a **permission** advisory.

### 2c. Primary — OpenAI staff response to exactly this question

**Source:** openai/codex issue **#9748**, "Subagent feature: Launching concurrent subagents instantly drains entire Pro plan usage quota", opened 2026-01-23, **CLOSED COMPLETED 2026-02-02**. <https://github.com/openai/codex/issues/9748>

A Pro subscriber on `gpt-5.2-xhigh` launched ~6–8 concurrent subagents and watched the full 5-hour quota vanish in ~1 minute. **OpenAI engineer `etraut-openai` replied:**

> The subagent feature is still under development, but you should assume that even in its final form, it will consume tokens much faster than a single agent. **The consumption rate should scale roughly linearly with the number of concurrent agents.** You'll need to decide whether that additional consumption is worth it for your personal use cases. If you require additional capacity beyond what's included in your subscription, we recently added the ability to purchase additional credits.

**This is the single most decisive piece of evidence in the commission.** An OpenAI engineer, told directly that a *personal Pro subscription* was being used to run 6–8 concurrent agents, responded with cost guidance and an upsell — **not** with a policy warning. Had personal-account concurrency been a terms problem, this was the moment to say so, in the vendor's own issue tracker, on the record.

Same engineer, second comment, on the `429 Too Many Requests` errors several users hit:

> The error you're seeing here is not the normal "usage limit hit" error. You're hitting a different rate limiter that is (presumably) in place to mitigate DDOS attacks. Users with pro subscriptions have priority request processing and more throughput.

**Two distinct limiters therefore exist:** (i) the subscription usage/quota meter, and (ii) an infrastructure-protection throughput limiter that returns 429. Fan-out can trip (ii) as well as (i). Tripping (ii) is an availability annoyance, and — importantly — nothing in the evidence suggests it is treated as abuse; but *hammering retries against it* is the one behaviour that could arguably approach the "interfere with or disrupt our Services" clause. Bound your retries.

### 2d. Primary — the live, unresolved economics risk (matches Matt's exact config)

**Source:** openai/codex issue **#35463**, "Codex subagents drain full week quota overnight — usage counting broken", opened 2026-07-26, **STILL OPEN as of 2026-08-25**. <https://github.com/openai/codex/issues/35463>

Reporter's environment: **Pro 20x, `gpt-5.6-sol`, `reasoning_effort: xhigh`, macOS, CLI 0.145.0** — i.e. materially identical to our standing provision pin. Entire weekly Pro quota drained to 0% overnight, correlated specifically with MultiAgent V2 subagent use, and *not* occurring on days without subagents. Audit of `~/.codex/sessions` found 129 sessions from one root thread, **fork trees up to 4 levels deep** (subagent's subagent's subagent's subagent), which the reporter did not request. Reported root causes include every subagent fork replaying its entire ancestor lineage's bookkeeping verbatim, and — the reporter's claim — that **"there is currently no way to bound nesting depth under MultiAgent V2 at all."**

Corroborating comment (`Sachinart`, 2026-07-27): "It burnt my quota within 4 hours (SOL ULTRA Standard 100% to 0%)."

⚠ **Note a documentation/reality tension I could not resolve:** secondary sources describe a `max_depth` setting alongside `max_threads`, but the official subagents page I retrieved lists only `max_concurrent_threads_per_session` and no depth control — which is consistent with #35463's claim that nesting is unbounded. **Depth, not width, appears to be the un-governed axis.** Recorded as a contradiction rather than averaged away.

### 2e. Primary — the token-amplification claim is partly rebutted

**Source:** openai/codex issue **#33196**, "Parallel subagents cause extreme token amplification and repeated compaction", opened 2026-07-15, OPEN. <https://github.com/openai/codex/issues/33196>

Original report: two parallel review subagents, ~340M cumulative tokens each in ~2 minutes, ~1.4B aggregate.

**But** commenter `cansitki` (2026-07-21) audited 59 child rollouts and found the measurement itself is inflated:

> a child rollout JSONL contains a large replayed prefix of the parent/shared history at spawn. Counting every token_count or compacted event in each child file, then summing child files, therefore double-counts the same cumulative telemetry.

Separating replayed prefix from child-specific events: replayed prefix 80,217 `token_count` events / 1,236 compaction markers, versus child-specific 3,592 / 44. **A ~22× measurement inflation.**

**Reported honestly because it cuts against the alarming reading:** a meaningful share of the "parallel agents burn tokens superlinearly" folklore is an artifact of naïvely summing per-child logs that each embed a copy of the parent's history. This does not make #35463's drained quota unreal — that was measured at the *dashboard*, not the logs — but it does mean the *magnitude* claims circulating in community reports are unreliable, and OpenAI's "roughly linear" position (§ 2c) has not been cleanly falsified.

### 2f. Primary — current limit structure and metering

**Source:** Codex pricing docs, <https://learn.chatgpt.com/docs/pricing> (retrieved 2026-08-25)

Local messages per 5-hour window:

| Model | Plus | Pro 5x | Pro 20x | Business |
|---|---|---|---|---|
| GPT-5.6 Sol | 10–100 | 50–500 | 200–2,000 | 10–100 |
| GPT-5.6 Terra | 25–200 | 125–1,000 | 500–4,000 | 25–200 |
| GPT-5.6 Luna | 250–2,000 | 1,250–10,000 | 5,000–40,000 | 250–2,000 |

Key metering facts:
- **"Local messages and cloud chats share a five-hour window. Additional weekly limits may apply."** One shared pool — CLI work and any ChatGPT-side Codex/Work usage draw down the same budget. Fan-out therefore also taxes Matt's non-Codex ChatGPT usage.
- Underlying accounting is credits per million input / cached-input / output tokens.
- Plus and Pro users hitting the cap **can purchase additional credits** rather than upgrade — the documented escape valve, and the one OpenAI's own engineer pointed to.
- Note `gpt-5.6-sol` is the **most expensive** row by an order of magnitude vs Luna. Our standing `sol` @ `xhigh` pin is the costliest possible fan-out substrate.

**Contradiction resolved:** community reporting disagrees on whether the 5-hour window still exists — it was temporarily removed 2026-07-12 for Plus/Pro/Business, with one source claiming restoration 2026-07-30 and another claiming no published end date. **The official pricing page presents the 5-hour window as current, and openai/codex issues #40725 and #40650 filed *today* (2026-08-25) both request changes to the live 5-hour quota window.** The window is in force. Weekly caps also apply and are the harder ceiling.

### 2g. Primary — automation auth guidance

**Source:** Codex docs, Non-interactive mode, <https://learn.chatgpt.com/docs/non-interactive-mode> (retrieved 2026-08-25)

> API keys are the right default for automation because they are simpler to provision and rotate.

…with the ChatGPT-account path documented as an explicit supported alternative: *"Use this path only if you specifically need to run as your Codex account."*

**Read this carefully, because it is the one soft signal pointing away from our pattern — and it is weaker than it first looks.** The stated rationale is **provisioning and rotation ergonomics**, not permission. The subscription-auth path is documented, supported, and given a legitimate use case. This is a recommendation about *what is convenient for CI*, not a rule about *what is allowed*. It also aims at unattended CI/CD pipelines; Matt's pattern is attended developer work on his own workstation, which is squarely the subscription's intended use.

`--ephemeral` is documented ("use when you don't want to persist session rollout files to disk"). Secondary sources report that **parallel `codex exec` instances without `--ephemeral` can collide via shared session-restore files** — an operational mitigation worth carrying if fan-out is adopted. The official page does not address parallel invocation, collisions, or concurrency limits at all.

### 2h. Account-action evidence — searched hard, found nothing attributable

Systematic search of openai/codex issues for ban/suspension terms returned **zero** results. Community ban reports do exist and were examined:

- **"Codex + ChatGPT Pro account banned with no warning — 18-month subscriber"**, community.openai.com thread 1381906, 2026-05-27/28. User was a heavy daily Codex user. **Parallel/concurrent usage is never mentioned.** User and community converged on **datacenter/transit egress IP reputation** (a clinical network whose public IP resolves to a Google LLC datacenter range) as the probable trigger. OpenAI_Support engaged and moved it to a private ticket; outcome not published.
- Secondary aggregators (qcode.cc, 4sapi blog — low-tier SEO sources, weighted accordingly) list ban triggers as: datacenter/shared IPs, rapid VPN region-switching, virtual/prepaid cards, **account sharing or reselling**, and "routing bots or a whole team through one consumer account." **The consistent theme is many *humans* or resale behind one subscription, plus network-reputation signals — not one human running many processes.**

**Negative finding, stated as such: across the codex issue tracker and the OpenAI developer community, I found no case where an account action was attributed to parallel Codex sessions on a personal plan.** Absence of evidence is not proof of safety, but the search space here is large, loud, and highly motivated to complain — and this complaint does not appear in it, while quota complaints appear constantly.

### 2i. Practitioner norm (secondary, weighted low but directionally useful)

Simon Willison, "Embracing the parallel coding agent lifestyle", 2025-10-06 — <https://simonw.substack.com/p/embracing-the-parallel-coding-agent>

> I frequently have multiple terminal windows open running different coding agents in different directories. These are currently a mixture of Claude Code and Codex CLI, running in YOLO mode (no approvals)…

A prominent, highly-visible practitioner describes exactly this pattern in public, with no ToS caveat. Corroborates that the norm is unremarkable. **Caveat: dated 2025-10, predates the 2026 subagent-metering incidents entirely, and says nothing about tier or quota.** Norm evidence only; carries no weight on economics.

### 2j. Ergonomics finding (bears on N)

openai/codex **#37827**, 2026-08-10, OPEN — a user running two parallel Codex sessions in separate git worktrees reports that **approval prompts serialize the operator**: "Even with only two concurrent sessions, I had to stay in front of the screen and continuously respond to approval requests… the parallel workflow turned into managing approval requests."

Relevant because it means fan-out's *realised* benefit depends entirely on the approval posture. Fan-out under interactive approvals may cost quota without buying wall-clock. This argues that N should be chosen against a sandbox/approval configuration, not in isolation.

---

## 3. What is UNKNOWN or unfindable — stated honestly

1. **No documented per-account concurrency cap exists — anywhere.** Neither the ToS, the pricing page, the subagents page, nor the non-interactive page states a maximum number of simultaneous sessions or requests. I searched specifically for this and it is genuinely absent, not merely un-found. The practical ceiling is the undocumented DDoS-mitigation limiter (§ 2c), whose thresholds OpenAI has not published and which "presumably" — the engineer's own hedge — exists for that purpose.
2. **`agents.max_concurrent_threads_per_session` default value is undocumented.** "Codex chooses the default" — the number is not published.
3. **Whether nesting depth can be bounded under MultiAgent V2 is contested** (§ 2d). Docs list no depth control; a detailed bug report asserts none exists; secondary blogs claim `max_depth` works. Unresolved, and it matters — depth is the axis implicated in the worst quota incidents.
4. **openai.com serves HTTP 403 to non-browser clients** (verified: both WebFetch and curl with a browser UA, on both `/policies/row-terms-of-use/` and the Codex help-centre article). **All ToS quotations in § 2a therefore come from a Wayback snapshot dated 2026-08-23 — two days stale.** The document self-describes as "Effective: January 1, 2026" and OpenAI reserves the right to make changes "effective as soon as we post them." A two-day window for a silent amendment is small but non-zero. **If this note is used for a consequential ruling, the terms should be re-read in a browser.** This is the one place where my evidence is not first-hand-current, and I am flagging it rather than letting the quotation marks imply more freshness than they carry.
5. **Whether OpenAI's internal abuse heuristics treat request concurrency as a signal at all** is unknowable from outside. No public documentation, and by nature it would not be published. My compliance verdict rests on the written terms plus the absence of contrary evidence plus a first-party engineer's on-record non-objection — not on visibility into the enforcement system.
6. **The `codex exec`-fan-out-specific economics are un-measured.** Every severe quota report I found involves Codex's *internal* subagents. I found **no** report — good or bad — quantifying quota burn from N independent external `codex exec` processes. Matt's actual pattern is the one the public record is quietest about. Reasoning suggests it should be closer to clean linear (independent sessions, no ancestor-replay pathology), but **that is my inference, not an observation**, and it is the largest genuine gap in this note.
7. **Matt's actual tier is unconfirmed** (Pro 5x vs Pro 20x vs Plus). The gap between Plus and Pro 20x on `sol` is 10–100 vs 200–2,000 messages per window — a 20× difference that materially changes the economics arithmetic. This is checkable locally via `/status` in a Codex session or the usage dashboard; I did not inspect account state, per read-only posture.

---

## 4. The decision-shaped summary — Matt's fork

**This is Matt's ruling. Presented as a fork with the evidence each branch leans on, not as a recommendation.**

The compliance question is, on the evidence, **not the real question** — it comes back low-risk from three independent directions (written terms silent on concurrency; parallelism is a shipped feature with its own governor; OpenAI engineer told directly about 8-way personal-Pro fan-out and answered with pricing, not policy). **The live question is economics, and specifically: what does fan-out do to a shared quota pool that also feeds Matt's ordinary ChatGPT usage?**

### Option 1 — Stay SERIAL (status quo)

*Leans on:* #35463 (OPEN, unresolved, Pro 20x + `sol` + `xhigh` — our exact pin — full weekly quota gone overnight); #9748's "instant drain" class; the shared 5-hour pool meaning a burned Codex window also degrades non-Codex ChatGPT work; `sol` being the most expensive model row by ~10×; #37827 suggesting fan-out may not even buy wall-clock under interactive approvals.

*Costs:* forgoes real throughput on genuinely parallelisable work. Preserves a constraint that the compliance evidence does **not** justify — if serial is retained, it should be retained on **cost-control** grounds, and the policy should say so, because "we stay serial for ToS reasons" is now a claim the evidence does not support.

### Option 2 — Bounded fan-out, N=2–3

*Leans on:* the § 1 headline distinction — external `codex exec` fan-out avoids the recursive-ancestor-replay pathology that drives every severe incident found; OpenAI's stated "roughly linear" scaling makes N=3 a ~3× burn rate, which is budgetable; the #33196 rebuttal (§ 2e) showing the scariest amplification numbers are ~22× inflated by telemetry double-counting; small N stays far from the undocumented DDoS limiter.

*Conditions this option implicitly requires:* set `agents.max_concurrent_threads_per_session` explicitly rather than trusting an undocumented default; **prefer external `codex exec` over internal `spawn_agent`, since depth is the un-governed axis (§ 2d) and external processes cannot nest**; use `--ephemeral` to avoid session-restore collisions (§ 2g); bound retries so a 429 is never hammered (the one behaviour with any ToS exposure at all, § 2c); check `/status` before and after the first few fan-outs to convert inference into measurement.

*Costs:* still multiplies burn on the most expensive model tier; requires a measurement discipline we do not currently run.

### Option 3 — Full fan-out, N=5+ (match the enterprise-laptop pattern)

*Leans on:* the compliance case being genuinely clean; OpenAI's own engineer declining to object to 8 concurrent agents on a personal Pro plan; a documented escape valve (buy credits) that OpenAI itself recommends; the practitioner norm being unremarkable; Pro 20x on `sol` nominally affording 200–2,000 messages per 5-hour window.

*Costs:* the § 2d incident is **open, recent, and configuration-matched to ours** — this is not a historical bug. At N=5+ the shared pool can plausibly be exhausted inside one working session, taking non-Codex ChatGPT usage down with it. Nudges the undocumented throughput limiter. And it commits to a burn profile on the pattern (§ 3.6) for which **no public measurement exists in either direction**.

### The one thing I would put in front of the decision

**The enterprise laptop is not evidence about the personal account, and the difference is not compliance — it is metering.** Business/Enterprise plans meter through workspace credits with flexible/overage purchasing, so heavy fan-out there degrades gracefully into spend. A personal Plus/Pro plan meters through a fixed shared window that, when exhausted, **stops Codex and ordinary ChatGPT together** until the window rolls or credits are bought. Matt's untroubled enterprise experience is therefore genuinely uninformative about the personal case — **it is not that the enterprise account is permitted to do something the personal one isn't; it is that the enterprise account fails soft and the personal one fails hard.** That asymmetry, not any terms question, is what the ruling should turn on.

---

## 5. Source list

**Primary — OpenAI official**
- OpenAI Terms of Use (consumer), Effective 2026-01-01 — via Wayback snapshot `20260823143939`, accessed 2026-08-25. <http://web.archive.org/web/20260823143939/https://openai.com/policies/row-terms-of-use/> (live URL 403s to non-browser clients)
- Codex docs — Subagents, accessed 2026-08-25. <https://learn.chatgpt.com/docs/agent-configuration/subagents>
- Codex docs — Pricing / usage limits, accessed 2026-08-25. <https://learn.chatgpt.com/docs/pricing> (redirected from `developers.openai.com/codex/pricing`)
- Codex docs — Non-interactive mode, accessed 2026-08-25. <https://learn.chatgpt.com/docs/non-interactive-mode>

**Primary — openai/codex issue tracker (incl. OpenAI staff statements)**
- #9748 — concurrent subagents drain Pro quota; `etraut-openai` staff replies. Opened 2026-01-23, closed 2026-02-02. <https://github.com/openai/codex/issues/9748>
- #35463 — subagents drain full week quota overnight; Pro 20x / `gpt-5.6-sol` / `xhigh`. Opened 2026-07-26, **OPEN**. <https://github.com/openai/codex/issues/35463>
- #33196 — parallel subagent token amplification + `cansitki` measurement rebuttal. Opened 2026-07-15, OPEN. <https://github.com/openai/codex/issues/33196>
- #22340 — parallel agents vanish on interruption, consuming non-refundable limits. Opened 2026-05-12, OPEN. <https://github.com/openai/codex/issues/22340>
- #37827 — parallel sessions serialized by approval prompts. Opened 2026-08-10, OPEN. <https://github.com/openai/codex/issues/37827>
- #40725, #40650 — 5-hour quota window change requests, both filed 2026-08-25 (used to establish the window is currently in force).

**Secondary — community**
- OpenAI Developer Community thread 1381906, "Codex + ChatGPT Pro account banned…", 2026-05-27/28. <https://community.openai.com/t/codex-chatgpt-pro-account-banned-with-no-warning-no-explanation-18-month-subscriber/1381906>
- OpenAI Developer Community thread 1365010, "Am I allowed to use Codex on my VPS?", 2025-11-04 — question posed, never authoritatively answered. <https://community.openai.com/t/am-i-allowed-to-use-codex-on-my-vps-will-openai-think-im-using-a-vpn/1365010>
- Simon Willison, "Embracing the parallel coding agent lifestyle", 2025-10-06. <https://simonw.substack.com/p/embracing-the-parallel-coding-agent>

**Tertiary — SEO/aggregator (low weight; used only for ban-trigger themes, and one of their claims was checked and rejected in § 2a)**
- qcode.cc Codex ban guide; blog.4sapi.com ChatGPT/Codex ban guide; krater.ai subscription-sharing guide; eesel.ai and winbuzzer.com on the July 2026 5-hour-limit change.

---

*Prepared by legolas (UNKNOWN-RESEARCHER) under Mode A analytical commission from gandalf, 2026-08-25. Read-only research; no account state inspected, no credentials used. Findings are source-anchored; § 3 states the gaps. The ruling is Matt's.*
