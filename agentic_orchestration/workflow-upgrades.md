# Project Workflow Upgrades — living backlog

> **STATUS:** LIVING (born 2026-08-23, Matt directive: *"I need to see, historically, what happened so I can work towards improvements on scope, cost, prompt success/efficiency, model success/efficiency"*).
> **Owner:** gandalf (proposals + curation) · **Matt rules adoption** · **KR sequences builds** · jack-ryan ratifies anything that graduates to governance.
> **Law of this doc:** every item names (a) the improvement LEVER it pulls (scope / cost / prompt-efficiency / model-efficiency), (b) the historical evidence or gap motivating it, (c) the EMPIRICAL CRITERION that gates adoption or measures success. No item advances on vibes.
> **Session lineage:** born from the 2026-08-23 Codex seam-substitution review (three research lanes + machine recon) and the Godot AI-tooling review (verification lane + repo recon). Verdicts of record: `gandalf/notes/` this date.

---

## U-1 — Fleet flight-recorder + read-only board (TOP PRIORITY — Matt 2026-08-23)

**Lever:** ALL FOUR — this is the measurement substrate every other lever needs.
**The gap (historical evidence):** the team's history is rich but *narrative* — git messages, ledgers, CHANGELOG prose. There is NO row-shaped record of what any unit of work COST (tokens, wall-time, retries) or how it PERFORMED (first-pass gate rate, rework count). The late-July token exhaustion could not be attributed (genuine demand vs. cache thrash) because nothing recorded per-workstream burn. We cannot improve scope/cost/prompt/model efficiency against data we do not capture.
**The build (two halves + one law):**
- **(a) Flight recorder (forward capture):** per-dispatch lifecycle telemetry — enqueue → start → gate events → close timestamps; token usage where surfaceable (`/usage` attribution per skill/subagent/MCP now exists; Codex lane emits per-turn usage natively via `codex exec --json` JSONL); retry/rework flags; verdict outcomes (PASS / PASS-with-findings / BLOCK / refusal). Logged as append-only JSONL beside the dispatch artifacts. The Codex queue lane (U-4) logs this from birth as its flight recorder.
- **(b) Board (projection):** a read-only kanban rendered FROM disk truth — columns from dispatch/queue state (QUEUED · IN-FLIGHT · AT GATE · AWAITING MATT · SEALED), cards from the dispatch files, history from git log + the JSONL. Local render only (the corpus is the moat; no deployed surface). Rebuilt from disk on refresh — cannot desync.
- **(c) THE LAW (welded on, non-negotiable):** the board is a VIEW, never a second truth source; **zero authority, read-only, never in the data path** (per § 4.8 queue-rows-are-views precedent and the Q3 staleness failure case). A watcher that carries traffic is a middleman, not a monitor.
**Empirical criterion:** after one full wave under the recorder, Matt can answer from rows (not prose): what did this wave cost, where did the time go, what got reworked and why.
**Seam:** harness logging = star-lord-adjacent factory work; board render = bounded drax-class build (or a Codex-lane job post-F2). KR sequences.
**Status:** OPEN — awaiting Matt adoption ruling.

## U-2 — Historical retrospective mining (the backward half of U-1)

**Lever:** all four (baseline-setting).
**What:** one-time mining pass over what history IS reconstructible: git logs across all repos (wave durations from commit timestamps, rework visible as repair-commit chains), CHANGELOG, qa/findings (gate outcomes: PASS/BLOCK/WARN counts per wave), refusal records, ledger row counts. Produces the FIRST baseline table: per-wave duration, gate outcome, rework incidence. Token costs are NOT recoverable retroactively — name that honestly; the table starts sparse and U-1 fills it forward.
**Empirical criterion:** a baseline table Matt can eyeball; the U-1 recorder's first wave then has something to compare against.
**Seam:** bounded read-only analysis — legolas or Explore-class; gandalf synthesizes.
**Status:** OPEN.

## U-3 — Cache-policy fix + usage attribution audit

**Lever:** COST (possibly the largest single lever, and it's a config line).
**Evidence:** on Claude subscriptions, prompt-cache TTL silently drops 1 h → 5 min once usage credits engage, unless `ENABLE_PROMPT_CACHING_1H=1` is set. A 2.5-day throttled multi-arm run tipping into credits reprocesses full context at every >5-min gap. Part of the late-July burn may be cache thrash, not demand. (Research of record 2026-08-23; Anthropic docs primary.)
**Action:** set the env var machine-wide; run a `/usage` attribution audit; measure post-fix burn on comparable work.
**Empirical criterion (also gates U-4's scale):** how much of the July-class burn survives the cache fix.
**Status:** OPEN — Matt action (host-level env). Candidate for `matt_to_do/`.

## U-4 — Serialized Codex worker lane (the ruled F2 pilot, generalized)

**Lever:** COST + capacity (second subscription already authenticated; marginal cost ~zero).
**Shape (verdict of record, 2026-08-23):** ONE serialized queue in `agentic_orchestration/factory/harness/codex.py` (interface already pinned) — never parallel streams on one `auth.json` (OpenAI CI/CD-auth precondition: "one machine or serialized job stream"). No DSH, no third-party router — REJECTED on machine evidence (not installed, misidentified, duplicates the factory harness). Names stay ours; identity binds via AGENTS.md + brief; provider resolution is one line in the harness.
**Pilot:** F2 baton-consumer (already Matt-ruled), differential-judged — this IS the G-S3 behavioral-equivalence test. Gates G-S0–G-S6 from the seam-substitution doc adopted as the lane's standing gate set, esp. G-S4 (delegation rate is first-class — a lane that never fires has failed) and G-S5 (rubber-stamp detector).
**Sequencing law:** discipline-heavy seams (gamora law-stack, jack-ryan gate authority, orchestrator) HOLD permanently; Godot seam only after G-S1 (MCP into `CODEX_HOME`) + G-S2 (skill→AGENTS.md port) close AND SB-1 reaches a seam boundary.
**Empirical criterion:** F2 differential verdict vs `baton_v1_stub_consumer.py`.
**Status:** OPEN — F2 staged, blocked on D5 containment revisit (pre-existing); queue build awaits KR sequencing.

## U-5 — Dispatch outcome scorecard (prompt + model efficiency, made measurable)

**Lever:** PROMPT-EFFICIENCY + MODEL-EFFICIENCY.
**What:** standing per-dispatch metrics riding on U-1 telemetry: first-pass gate rate · rework count · tokens per accepted artifact · refusal/HALT incidence · wall-time to seal. Once captured, prompt-format A/B (brief shapes, pinning styles) and model A/B (Claude vs Codex lane on comparable work classes) become differential measurements instead of impressions — the house method (judge externally, never self-report) applied to our own process.
**Empirical criterion:** two comparable dispatches scored end-to-end from rows alone.
**Depends on:** U-1(a).
**Status:** OPEN.

## U-6 — AGENTS.md portability layer (G-S2 groundwork, repo by repo)

**Lever:** SCOPE + model-portability (and it de-risks U-4's later seams).
**What:** adopt the vendor-neutral instruction pattern — per-repo `AGENTS.md` as the canonical behavioral contract; `CLAUDE.md` becomes a thin importer (`@AGENTS.md` + Claude-specific notes). Start with `reincarnated-godot/` (CLAUDE.md exists, 6.1 KB, high-quality discipline content; AGENTS.md absent — recon 2026-08-23). Claude-native skills stay Claude-side; the *portable* discipline lands in AGENTS.md so any future provider reads the same contract.
**Empirical criterion:** a Codex smoke invocation in the repo demonstrably honoring the AGENTS.md contract (read-only task).
**Seam:** each repo's owner ports their own; gandalf reviews contract fidelity.
**Status:** OPEN.

## U-7 — Godot toolchain hardening (from the 2026-08-23 Godot-AI-tooling review)

**Lever:** SCOPE (assurance floor) + cost (cheaper failure detection).
Verdict of record: the Codex research doc's architecture is a good general-purpose FLOOR; our gate-based evidence harness (Metal off-screen renders, SHA-256 determinism ×2, ffprobe gates, galadriel receipts) is ABOVE that floor for visual work — adopt the doc's portability items, reject regressions. Itemized:
- **(a) Pin the Godot version** — one env/config point (scripts already honor `$GODOT`); currently unpinned (4.6.3 inferred). Cheap, do it.
- **(b) `./dev/check` parse-check wrapper** — `--check-only` over changed `.gd` before render cycles; catches parse errors pre-render at near-zero cost. Do NOT flatten the bespoke `run_*.sh` instruments into generic wrappers — they are pre-registered gates, not boilerplate.
- **(c) GdUnit4 for the LOGIC layer** (baton consumer, harness math, non-visual scripts) — verified healthy (v6.2.1 2026-08-20, green 4.3→4.7). NOT GUT (75 issues, fragmented branches).
- **(d) gdlint/gdtoolkit: DO NOT adopt now** — stale ~10.5 months, open correctness bugs (`static func` AST miss; gdformat emits Godot-rejected indentation), targets 4.5 grammar. Re-check on its next release.
- **(e) satelliteoflove/godot-mcp: KEEP, at tip** (we run 4.1.0 = upstream tip; freeze/step/screenshot/input surface code-verified real; 4.6 satisfies 4.5 floor). WATCH item: feature-stalled since 2026-06-20 (dependabot-only since).
- **(f) Coding-Solo/godot-mcp: PERMANENTLY DISQUALIFIED** — npm `0.1.1` (2026-02-03) lacks the git-only RCE hardening (GHSA-8jx2-rhfh-q928 class; unpublished 2026-04-16 fix); maintainer absent 4+ months. Recorded so nobody ever npx-installs it on star-count.
- **(g) hi-godot/godot-ai: BANKED behind an empirical trigger, not installed** — the credible broad-construction bridge (1.9k★, active, Claude+Codex config documented) but heavy (addon + Python/uv server, mcp 2.x incompat, release churn) and would contend with our incumbent bridge (one-comprehensive-bridge rule, which the research doc itself states). **Trigger:** when scene/content ASSEMBLY volume becomes the measured bottleneck (One-Realm MVP floor-assembly phase), pilot it in a disposable project first.
- **(h) minimal-godot-mcp diagnostic bridge: OPTIONAL** — no addon needed, LSP-version-agnostic, semi-dormant but honest scope. Adopt only if (b) proves insufficient for diagnostics.
- **(i) First-party watch:** NO official Godot/W4 AI-MCP effort exists (verified 2026-08-23) — community bridges remain the only path; no wait-for-official argument. regiellis/godot-mcp-go = re-check in ~3 months (best design, one month old).
**Status:** (a)+(b) ready for drax whenever KR sequences; (c) queued; rest are standing rulings/watches.

## U-8 — Cross-vendor judge (galadriel ADD, never replace)

**Lever:** MODEL-EFFICIENCY (correlated-bias attack on our judging layer).
**What:** a second-vendor judge scoring the same artifacts galadriel scores — vendor diversity in judgment is the point (the one unambiguously good idea in the original seam-swap doc). Rides the U-4 lane once serialized capacity exists.
**Empirical criterion:** inter-judge agreement/divergence table on one capture set.
**Status:** OPEN — queued behind U-4 pilot.

## U-9 — Synty pack-level license ledger + AI-clearance stop-gate (from the 2026-08-23 Codex-QA comparison — the audit's one genuinely-new catch)

**Lever:** SCOPE (legal assurance floor — the cheapest possible insurance against the most expensive possible surprise).
**Evidence:** Codex STRATEGIC §4 flags July-2026 Synty EULA revisions around AI/editor use. Canon check 2026-08-23: `business-platform-strategy.md:52` is the ONLY license-shape sentence in canon (strategy-level, predates the AI-terms question); `ensemble-asset-pipeline-spec.md` carries ZERO license/EULA/clearance rows while its Stage-4 plans an image→3D vendor call (Tripo slot) on Synty-derived captures — i.e., we are one dispatch away from sending licensed assets into a third-party AI service with no clearance on file.
**The build (three parts):** (a) ✓ **DONE 2026-08-23** — legolas primary-source read landed: `agentic_orchestration/legolas/notes/2026-08-23-synty-eula-primary-source-read.md`. Revision claim CONFIRMED but narrower than flagged (9 Jul 2026 added exactly two 3D-gen clauses; the editor ban is ~4 years old and unchanged). **The finding under the finding:** the 3 Jun 2026 revision DELETED the 2022-era blanket "as inputs to Generative AI Programs" ban, and the OTP's rights ratchet pins the governing version to PURCHASE DATE — so the ledger schema is now **pack → purchase channel → purchase date → governing EULA version → notes** (channel is decisive: Unity-Asset-Store packs sit under Unity's stricter still-live AI-input ban; Humble inherits the Synty OTP at one seat). (b) **ledger** — schema above; blocked only on Matt's channel+date disclosure (T18 Step 0). (c) ✓ **stop-gate WRITTEN into ensemble spec Stage-4 (2026-08-23)** — reshaped by the findings into a **LINEAGE gate**: 3D-model generation FROM Synty assets is Grade-A prohibited under current terms regardless of input form (activity-scoped clause), but Stage-4's designed inputs are *generated* images, so the gate is "no Synty-derived pixels/meshes anywhere in the input chain to a 3D-gen service" + a one-time style-bible/trailer lineage audit (were Synty captures ever image-prompts upstream?). Pairs with `matt_to_do/` **T18** (Step 0 channel+dates; Step 1 the 12-item letter, note § 5).
**Empirical criterion:** ledger row with channel + purchase date + governing version for every pack the pipeline touches BEFORE the first Stage-4 vendor call; trailer-lineage audit verdict recorded; T18's written answer attached when it lands.
**Status:** (a) DONE · (c) gate landed · (b) awaiting T18 Step 0 (Matt: channels + dates, one sentence).

## U-10 — Cross-seam contract index (contract-proliferation guard; candidate)

**Lever:** SCOPE (Codex §23 "contract proliferation" — the one risk-name we lacked).
**Evidence:** our contracts are individually strong but index-less: baton v1 + GL-6..GL-12 law, export bundle contract, atlas manifest, receipts schema (factory Spec A). A consumer today learns the contract surface by folklore or grep.
**What:** ONE versioned index doc enumerating cross-seam artifact schemas — name, version, owner seam, consumers, pointer — consumers cite the index; schema changes land with an index bump. NOT a rewrite of any contract; an index only.
**Empirical criterion:** index exists; two real consumers cite it; one schema change demonstrably lands with its index bump.
**Seam:** star-lord + KR concurrence REQUIRED before this advances (their surfaces); gandalf drafts on their nod.
**Status:** OPEN — candidate, gated on seam-owner concurrence.

---

## Adoption protocol

New items: any agent proposes; gandalf curates in; each item lands with lever + evidence + empirical criterion or it doesn't land. Items graduate OUT to: `matt_to_do/` (host-level actions), KR dispatches (builds), engineering-disciplines via jack-ryan (anything that becomes law). Collapse-on-adoption per OP § 4.9 — adopted items compress to one-line entries with their outcome.

**Signed:** gandalf, 2026-08-23.
