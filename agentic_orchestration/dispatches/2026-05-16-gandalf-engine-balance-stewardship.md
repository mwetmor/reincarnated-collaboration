# Commission — gandalf engine-balance stewardship doc

**Status:** COMPLETE — `canonical/story/engine-balance-stewardship.md` filed; informs View A lock + multi-dimensional divergence framework (decisions-log 2026-05-16)
**Target:** gandalf (generative-side design steward — Tier A)
**Branch:** main (collaboration repo)
**Type:** Knight-rider commission to gandalf for design-canonical authoring
**Direction:** knight-rider → gandalf (reverse of `agentic_orchestration/gandalf/requests/` which is gandalf → knight-rider)

## Context

Two seam-owners are currently blocked on engine-balance design decisions that gandalf's Legolas-research-grounded design instinct is best positioned to inform:

- **Gamora B10.4 milestone tag** (`v1.3-b10-4-swarm-calibration`) is held pending AOE-philosophy View A/B/C lock. Jack-ryan Gate 1 returned PASS WITH FLAGS on Option 2 (exclude pack fights from convergence binary search). Empirical finding: View A is operative (compound — 0.6× per-hit reduction exists but is overwhelmed by lower energy cost + shorter cooldown + N=8× pack multiplier). Matt asked for gandalf-informed design opinion before locking.
- **Drax v0.7-encounter-analytics dispatch** is held pending the same View decision (the viz interpretation hook depends on whether View A is locked or View B/C overridden).

Matt's two priority design questions surfaced 2026-05-15:

- **Q1 — Divergence floor / ceiling.** Matt's articulation: *"Each class should be clearly differentiated from its archetype-mates (divergence above a floor — distinct enough to feel like its own thing), while every class retains a playable floor in every content type (divergence below a ceiling — no helpless matchups), with rough parity of total experienced cost, not just count."*
- **Q2 — Movement speed in simulation.** Matt's framing: if the simulation models movement at L1 speed (or not at all), single-target classes are unfairly handicapped against packs because kiting/positioning is the genre's standard mitigation. The engine is supposed to balance against L50 endgame per file 29; the simulation calibration may not match. Pertinent for both AOE balance AND the file-29 ~80-100 mobs/min KPM target.

Per Matt's 2026-05-16 deferral: *"Legolas' research into current ARPG design will inform Gandalf with the opinions needed to design movement speed per Q1/Q2. This will also help for gamora's block on AOE gauntlet strategy decisions."*

Legolas's 5-pass research is now filed (`research/knowledge/` — isekai / Diablo / PoE / ARPG community / adjacent ARPGs). The research base is ready; what's needed is **gandalf's design opinion drawing on it.**

## Recommended sequencing — complete season-feel + drift-audit FIRST

Per Matt 2026-05-16: **complete `season-feel-rubric.md` and `drift-audit.md` BEFORE authoring engine-balance-stewardship.md.** Rationale:

- **`season-feel-rubric.md`** defines what makes a season distinct in player experience — this is the foundation for understanding *what kind of game we're balancing for*. Engine-balance decisions without season-feel grounding are mechanically-tuned-for-nothing-specific.
- **`drift-audit.md`** inventories load-bearing pillars and verifies structural enforcement — gives engine-balance work a stable foundation of locked decisions. Without it, balance recommendations may be authored against unlocked or drifted pillars.
- **`engine-balance-stewardship.md`** is the load-bearing third piece — builds on both.

This sequence respects Matt's directive AND produces a more coherent end-state. Engine-balance stewardship that's grounded in season-feel + drift-audit will read as informed-by-the-whole rather than as isolated mechanical opinion.

If your authoring rhythm differs (e.g., you find that engine-balance work emerges naturally during the season-feel or drift-audit authoring), exercise design judgment. The sequencing is a recommendation, not a hard gate.

## What's being requested

A canonical-story doc at `canonical/story/engine-balance-stewardship.md` that addresses three specific gates with structured recommendations, citations from Legolas research, and locked-or-deferred status per question. Roughly 3-5 pages.

### Gate 1 — AOE-philosophy View A / B / C lean

Articulate which view the project should lock, and why, drawing on:

- **Legolas Pass 4 ARPG community discourse** — especially the documented community-pattern *"encounter design is the real lever, not flat damage ratios"* (per the per-pass headlines you received). This is directly relevant to whether View A's "AOE earns pack-clear-identity for free" is genre-correct or whether View B/C compensatory mechanics are required.
- **Jack-ryan's Q3 empirical finding** (`qa/findings/2026-05-15-b10-4-option-2-and-aoe-philosophy.md`): View A is operative empirically; the engine's current implementation is compound View-A-with-partial-View-B-damage-reduction.
- **File 29's locked "shaped balance over numeric scaling" philosophy** — does View A satisfy this? Or does the free-pack-clear upside contradict "classes differ by COMPOSITION first, by NUMBERS last"?
- **Q1's playable-floor constraint** — does View A satisfy *"every class retains a playable floor in every content type"*, or do single-target classes become helpless against packs under pure View A?

Output: a recommendation (View A / View B / View C / hybrid), with rationale and named consequences. If the recommendation is View A, address Q1's playable-floor concern explicitly. If View B or C, specify what compensation mechanism is recommended and why.

### Gate 2 — Divergence floor / ceiling framing

Articulate the operational form of Matt's Q1 framing. Specifically:

- **Divergence above a floor** — what does "distinct enough to feel like its own thing" mean operationally? Some candidate dimensions: feature-space distance between class centroids (a metric for v0.7-encounter-analytics); skill-geometry diversity threshold; archetype-mate distinguishability test.
- **Divergence below a ceiling** — what does "no helpless matchups" mean operationally? Some candidates: minimum win rate per (class, content-type) pair; maximum experienced-cost differential.
- **Rough parity of total experienced cost** — what's the operational measurement? Time × resource expenditure per content slot normalized per class.

This isn't asking for a final spec — it's asking for **the framing language and operational measurement candidates** that v0.7 viz can render and that future balance work can target. The convergence framework currently uses single-number aggregate WR; Q1 implies multi-dimensional constraints. What's the right structural form?

Draw on Legolas Pass 4 (build diversity / class fantasy discourse) and Pass 5 (Last Epoch / Grim Dawn build-diversity-as-design-target patterns).

### Gate 3 — Movement speed framing

Articulate how movement speed should be treated in the simulation. Three sub-questions:

- **Is movement speed currently modeled?** Per the Q2 framing this is genuinely unknown — needs a rocket/gamora research-pass to confirm. If the answer is "no" or "L1-only," what's the recommended path?
- **L50 endgame projection** — per file 29 the engine balances against L50 endgame; if movement is L1 or unmodeled, the simulation is calibration-mismatched. Should movement speed scale per character level or stay constant at endgame value?
- **Kiting / positioning as design lever** — per Legolas Pass 2 (Diablo) and Pass 3 (PoE), movement-and-positioning is a primary genre-mechanic for single-target archetypes against packs. Reincarnated's abstract simulation may not capture this. What's the operational consequence — accept the abstraction limitation, or recommend movement modeling as a B-series item?

Draw on Diablo retrospectives (Pass 2) for how the genre evolved movement-as-balance-lever, and PoE (Pass 3) for the modern endgame-velocity discourse.

## Direct-dialogue option

Same direct-dialogue privilege as the rubric-design work: you can invoke gamora as Pattern A subagent (or schedule Pattern B) for engine-state questions during authoring. Specifically useful:

- For Gate 3, gamora knows whether/how movement is currently modeled (the question is empirical, not design-instinct)
- For Gate 2, gamora knows how the convergence framework computes class differentiation today (and where it's been straining per B10 work)
- For Gate 1, gamora authored the B10.4 empirical findings — direct conversation about edge cases may be useful

Knight-rider does not need to be present. Coordinate timing directly with gamora's session state.

## What this commission unblocks

When this doc lands and Matt approves:

- **Gamora B10.4 milestone tag** can cut after View lock + decisions-log entries (knight-rider drafts; jack-ryan reviews)
- **Drax v0.7-encounter-analytics dispatch** can be authored with viz interpretation correctly bound to locked View
- **Future B-series work** on engine balance has stewardship grounding rather than ad-hoc per-dispatch judgment

## Decisions-log entries expected to follow

Per ADR-002 process: knight-rider drafts decisions-log entries from this canonical work; jack-ryan reviews (or stress-tests if substantial); Matt approves; entries land. Anticipated entries:

- View A/B/C lock (whichever you recommend + Matt approves)
- Divergence floor + ceiling operational framing (if it crystallizes into a named structural commitment)
- Movement speed approach (depending on Gate 3 outcome — may or may not produce a decisions-log entry vs an engine-design.md update)

## Cross-references

- **Required reading first** — your own:
  - `canonical/story/style-register.md`, `court-of-forms.md`, `naming-triad.md`, `cosmology-reincarnated.md`, `enemy-visual-legibility.md` (your existing canonical-story corpus)
  - `gandalf-phase2-bullet-points.md`, `gandalf-design-lineage.md` (your own grounded knowledge)
- **Legolas research** — the empirical base:
  - `research/knowledge/isekai/2026-05-16-isekai-evolution.md`
  - `research/knowledge/diablo/2026-05-16-diablo-design-retrospectives.md`
  - `research/knowledge/poe/2026-05-16-poe-design-philosophy.md`
  - `research/knowledge/arpg-community/2026-05-16-arpg-design-discourse.md` (especially relevant for Gate 1)
  - `research/knowledge/arpg-adjacent/2026-05-16-adjacent-arpgs.md`
- **Engine state** —
  - `canonical/37-form-bias-diagnosis-and-recovery.md` (especially § 10.1 high-stakes opens and § 4 Position C)
  - `canonical/29-design-overview.md` (locked "shaped balance over numeric scaling" + ~80-100 mobs/min KPM target)
  - `reincarnated-engine/design/decisions/decisions-log.md` (latest entries — B10.2 PackProxy + Two-Gauntlet Pattern + B10.4 calibration)
  - `qa/findings/2026-05-15-b10-4-option-2-and-aoe-philosophy.md` (jack-ryan's Gate 1 empirical finding)

## Acceptance

- `canonical/story/engine-balance-stewardship.md` filed
- Three gates addressed with structured recommendations + rationale + citations
- Open questions explicitly parked (any that can't be locked yet)
- If gamora-dialogue was invoked, summary captured in the doc
- Knight-rider notified at completion: doc path, headline recommendations per gate, readiness signal for decisions-log entries

## Priority

**Active but sequenced.** Recommended order: season-feel-rubric → drift-audit → engine-balance-stewardship. The B10.4 milestone tag and drax v0.7 dispatch are held pending this; not urgent enough to skip the prerequisite docs. Realistic timeline: 1-3 sessions of focused work.
