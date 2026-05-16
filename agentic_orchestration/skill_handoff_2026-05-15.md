# Skill handoff — 2026-05-15 (Day 2)

**Audience:** knight-rider on first invocation of the next session.
**Purpose:** Full team state at end of Day 2. Read this, then run first-invocation checks.

**Day 2 was substantively heavier than Day 1.** Five parallel streams ran simultaneously at peak (gamora B10.4, drax v0.5.1+v0.6.5, star-lord gear-pool-stats + telemetry research, knight-rider doc 37 + dispatch authoring, jack-ryan Gate 1 reviews). Multiple substantial design decisions surfaced and were partly resolved; several remain open and prominent.

---

## 🔴 Matt's priority design questions (LOG — affect multiple work streams)

These two questions surfaced at the end of Day 2 and connect directly to the View A/B/C AOE-philosophy lock currently gating the B10.4 milestone tag. They are not yet resolved and need to be raised before the View lock so they can inform it.

### Q1 — Geospatial convergence / divergence framing

Matt's articulation: *"Strip those five out and what's left isn't 'maximize divergence.' It's something like:*

- *Each class should be clearly differentiated from its archetype-mates (divergence above a floor — distinct enough to feel like its own thing),*
- *while every class retains a playable floor in every content type (divergence below a ceiling — no helpless matchups),*
- *with rough parity of total experienced cost, not just count."*

**Why this matters for the View lock:** Pure View A says AOE classes earn pack-dominance "for free" with parity 1v1 throughput. But under Matt's actual-objective framing, **single-target classes must retain a playable floor in pack content** (no helpless matchups). Pure View A may not satisfy this — if single-target classes are *helpless* against packs, View A as locked produces a metagame the design philosophy doesn't endorse.

**Implication:** Before locking View A, we need to know whether single-target classes are *helpless* or *less efficient* against packs. The KPM data from B10.4 (non-pack -25%, aggregate +75%) doesn't directly answer this — it tells us about clear-speed, not about whether classes are mechanically helpless.

**Operational candidates surfacing from this framing:**
- A "divergence floor + ceiling" metric: distance between class centroids must be `≥ floor` (distinct) and `≤ ceiling` (no helpless matchups). Could be a hard constraint in the convergence loop or a soft tuning variable for kit composition.
- An "experienced cost parity" metric: total time × resource investment to complete a content slot, normalized across content types per class.

**Action needed:** Discussion before View lock. Knight-rider proposes a focused design conversation that explicitly frames the View decision as *"does locked View satisfy the divergence-floor + playable-floor + experienced-cost-parity objective?"*

### Q2 — Movement speed in simulation

Matt's articulation: *"Is movement speed coded at all? If basic/level 1 movement speed is used, single target struggles more in the AOE gauntlet vs end-game movement speed potential. Have we tested monster kill speed versus the 100 monsters per minute gate? If we are using basic movement speed right now, we should probably adjust it from basic early game move speed to anticipated end game movement speed so that we get monsters per minute AND monster pack kiting right in these simulations."*

**Why this matters for the View lock:** Single-target viability against packs depends heavily on **kiting and positioning**. If the simulation doesn't model movement (or models it at L1 speed when the engine is balanced against L50 endgame per file 29), single-target classes are unfairly handicapped in pack content. That's a measurement artifact, not a class deficiency. View A may look operative empirically while the underlying physics is wrong.

**Specific investigation needed (rocket + gamora):**
1. Does the simulation model movement at all? If yes, at what speed?
2. If movement is modeled but uses L1 speed, what's the L50 endgame speed projection?
3. Is the file 29 ~80-100 mobs/min ARPG-genre KPM target tested against the current simulation? If not, what does the current sim actually produce? (Per gamora's B10.4 finding, non-pack KPM is 1.2 — but per-fight KPM and gauntlet-completion KPM aren't the same metric.)

**Connection to other work:**
- Directly affects B10 V2 (sequential rooms) — kiting / movement is core to that simulation
- Affects the v0.7 centroid viz interpretation — if single-target classes look bad in pack content, is that View A operating as designed OR an artifact of bad movement modeling?
- May invalidate the empirical basis of jack-ryan's View A finding if movement isn't being simulated faithfully

**Action needed:** Knight-rider authors a small rocket/gamora research-pass dispatch (read-only, ~30 min) to answer the three questions above before the View lock.

---

## What shipped over the past 2 days

### Day 1 (2026-05-14)

| Tag | Seam | What |
|---|---|---|
| `v1.3-b10-2-pack-proxy` | gamora | PackProxy entity + AOE N× multiplier + swarm gauntlet composition (Model C) + recompose gauntlet isolation |
| `gamora/v1.3-b10-2-pre-impl` | gamora | Pre-implementation checkpoint |
| `v0.4-gear-effects` | drax | Gear effects rendering via effect_pool with FlavorTip modal |
| `v0.4.1-gear-display` | drax | 7 UI fixes |
| *(star-lord, untagged)* | star-lord | Yomi `gear_pool.json` exported |

### Day 2 (2026-05-15)

| Tag | Seam | What |
|---|---|---|
| `drax/v0.5-real-gear` (commit 24669c7) | drax | Real Yomi gear consumption; retired synthesis layer |
| `drax/v0.6-encounter-viz` | drax | Static SVG encounter-viz tier 1 (mechanism illustration). **Milestone `v0.6-encounter-viz` HELD** — scope-expansion to v0.7-encounter-analytics pending |
| `drax/v0.5.1-bug-fixes` (commit d715116) | drax | 4 bug fixes: tier diversity, hide power_score, slot labels, /loadout leak. **Milestone `v0.5.1` pending Matt visual QA + knight-rider confirmation** |
| `drax/v0.6.5-analytics-tier3` | drax | 3 Tier 3 analytics charts + Tailwind safelist trim + CC-BY footer. Non-dispatch housekeeping from AGENT_STATE queue. **No milestone tag intent unless Matt approves** |
| `star-lord/season-002328-gear-pool-stats` (commit 4897023) | star-lord | gear_pool.json re-exported with per-item stats + rolled_effects + ability_modifiers. MIGRATION.md authored. Deterministic-replay approach (seed + 999) |
| (commits 18e45ef, 6653666, 4d159d6, d6002bf — gamora) | gamora | B10.4 swarm calibration: code change (eff_attr 0→7), math note, §14 gauntlet analysis, two decisions-log entries (calibration + KPM metric interpretation). **Milestone `v1.3-b10-4-swarm-calibration` BLOCKED** — see § B10.4 below |

**Preview URLs live:**
- drax v0.5.1 + v0.6.5: `https://reincarnated-loadout-606gj5w7p-matthew-wetmore-s-projects.vercel.app`
- (Earlier preview URLs from v0.5 / v0.6 superseded)

---

## 🔴 Decisions blocking next-step work

### Decision 1 — B10.4 tag gated on View A/B/C lock + Option 2 implementation

**Status:** Jack-ryan Gate 1 returned PASS WITH FLAGS. Two preconditions before `v1.3-b10-4-swarm-calibration` can cut:

1. **Matt locks AOE philosophy.** Jack-ryan empirical finding: View A is *operative* (compound — 0.6× per-hit reduction exists but is overwhelmed by lower energy costs, shorter cooldowns, and N=8× pack multiplier). But the three governing parameters in `math_model.py`, `role_constraints.py`, `damage_resolver.py` have **never been analyzed as a joint system**. Knight-rider's read: **Lock View A** (genre-aligned; matches ARPG fantasy of AOE classes clearing trash content). But Matt's Q1 (divergence-floor + playable-floor objective) and Q2 (movement speed) may shift this read — those questions should be discussed before the View lock.
2. **Option 2 implemented + full regen confirms convergence.** Two decisions-log entries required:
   - **B10.2 Two-Gauntlet Pattern entry SUPERSEDED** — its *"Convergence = full fidelity"* clause directly contradicts Option 2. Without supersession, decisions-log is internally inconsistent.
   - **New entry codifying** *"non-pack WR = 50%"* as the operative modifier definition + the locked AOE philosophy view.

**Findings file:** `agentic_orchestration/qa/findings/2026-05-15-b10-4-option-2-and-aoe-philosophy.md`

**Path to unblock:**
1. (Optional but recommended) Matt discusses Q1/Q2 with knight-rider; may invoke rocket/gamora movement-speed research first
2. Matt locks View (A / B / C)
3. Knight-rider drafts both decisions-log entries; jack-ryan reviews (quick Gate 1)
4. Gamora dispatch — Option 2 implementation + full regen confirmation + decisions-log entries written
5. Tag cuts

### Decision 2 — v0.5.1 milestone tag gated on Matt visual QA

Drax couldn't capture screenshots (no screen access in his session — acceptable deviation noted). Matt verifies four things at the preview URL:
- `/sample` shows tier diversity (not all legendary)
- No `Power X.XXX` text on gear cards
- Slot labels human-readable
- `/loadout` is empty placeholder

Once Matt confirms → knight-rider confirms tag → drax cuts `v0.5.1`. Drax session may have closed; relaunch needed to cut tag.

### Decision 3 — v0.6.5 milestone tag — Matt's call

Drax shipped Tier 3 analytics + housekeeping under intermediate tag `drax/v0.6.5-analytics-tier3`. No milestone tag intent unless Matt explicitly approves promotion. Whether to promote is purely Matt's call — work is small and additive, not a major milestone.

### Decision 4 — Form-bias work cadence (Option I / II / III)

From doc 37 § "Status and next steps." Three paths:
- **(I) Interleaved with B-series.** Decisions-log + disciplines this session; medium-stakes opens later; etc. Multi-week elapsed.
- **(II) Parked until B-series stabilizes.** Risk: Discipline #13 violation if any developer touches affected seams while locks aren't formally enforced.
- **(III) Push hard now.** Sequential 1-3 over next session or two.

Knight-rider's recommendation: **(I), with the decisions-log entry + Discipline #13/#14 executed before the next session closes** to avoid violating the discipline we just defined. Items 2-3 then in cadence.

---

## Active dispatches (ready to execute — files exist, not yet picked up)

### star-lord telemetry Tier 1 extension
**File:** `agentic_orchestration/dispatches/2026-05-14-star-lord-telemetry-tier1.md`
**Status:** Authored 2026-05-14. **Not yet picked up.** Star-lord's gear-pool-stats session may have closed without scanning for parallel dispatches.
**What:** Persist `duration_seconds`, `a_heals_received`, `a_potions_used` on `class_fight_loadouts` table. Cross-seam authorization granted (touches gamora-owned files). MIGRATION.md required.
**Tag:** `star-lord/telemetry-tier1-extension` intermediate; `v1.3-telemetry-tier1` milestone (Matt approval required).
**Risk:** Same grep-heuristic dispatch-pickup miss that drax originally hit; star-lord may need explicit redirect when relaunched.

### drax stats wiring (no dispatch file yet)
**Status:** Star-lord's gear-pool-stats has shipped (intermediate-tagged). Drax should now consume the new `stats` / `rolled_effects` / `ability_modifiers` fields per the MIGRATION.md in `reincarnated-engine/src/reincarnated/export/MIGRATION.md`. Knight-rider needs to author this dispatch — `2026-05-15-drax-v0-5-2-stats-display.md` likely scope. Could roll into v0.7 instead.

---

## Held / blocked dispatches

### v0.7-encounter-analytics drax dispatch
**File (scoping):** `agentic_orchestration/dispatches/2026-05-14-v0-7-scoping-notes.md`
**Status:** **HELD** on multiple preconditions:
1. Star-lord telemetry Tier 1 must ship
2. Fresh Yomi regen with Tier 1 telemetry must populate the new columns
3. **AOE-philosophy lock** must complete (View A / B / C) so v0.7 viz interpretation guidance can be baked into the dispatch
4. Q2 (movement speed) may need resolution if it affects the empirical basis of View A

When dispatch is authored, must include Matt's three sharpenings (feature space, centroid+stdev ellipses, "encounter slot" not "room") plus the locked-AOE-philosophy interpretation hook (now captured in scoping notes).

---

## Gate 2 pending

### gamora B10.2 — `v1.3-b10-2-pack-proxy`
**Status:** Still pending from Day 1. Note: B10.2's "Convergence = full fidelity" decision is being superseded under Option 2; Gate 2 review should incorporate this supersession.

---

## Open decisions-log items (held)

| Entry | Held on | Author |
|---|---|---|
| **B10.2 Two-Gauntlet Pattern — SUPERSEDED by Option 2** | Matt's View lock + Option 2 implementation | knight-rider drafts |
| **Option 2 + locked AOE philosophy** | Matt's View lock | knight-rider drafts |
| **kit_anchor semantic** | Rocket ships the rename (not yet dispatched) | knight-rider drafts |
| **Trash tier removed from A3 gauntlet** | B10.4 V1/V2 metrics confirm no material change | knight-rider drafts (when metrics clean) |
| **Form-bias structural realignment + locked positions** | Matt picks Option I/II/III cadence | knight-rider drafts |
| **Internal-vs-generative schema separation (architectural pattern)** | Form-bias cadence decision | knight-rider drafts |

## Engineering-discipline candidates (held)

| Discipline | Status | Held on |
|---|---|---|
| **#13 — Implicit-pillar drift** | Drafted in doc 37 §9.1, jack-ryan approved-with-flag | Form-bias cadence decision |
| **#14 — Internal-vs-generative schema separation (reviewable check)** | Drafted in doc 37 §9.2b | Form-bias cadence decision |

---

## Major design work — Day 2

### doc 37 — Form-bias diagnosis and structural realignment

Located at `canonical/37-form-bias-diagnosis-and-recovery.md`. **Draft 2 incorporates jack-ryan PASS WITH FLAGS findings + Matt's position-locks.** Five major positions locked in conversation:

- **Position C** (slot-as-functional-mechanic + embodiment-as-narrative-skin)
- **Position (ii)** (abstracted mechanical signatures; cipher = resistance-translation only)
- **Smart-loot in-season + spirit-conversion post-Phase-0**
- **Three body-swap gear rules** (Trial / doppelganger / death)
- **Ailment-damage-signatures re-activated** as load-bearing dependency

**Open questions remaining** (per doc 37 § 10):
- 3 high-stakes (mechanical-signature pool, pair-structure exposure shape, residual LLM bias)
- 3 medium-stakes (embodiment-variation unit, diegetic vs ambient spirit guide, form library ownership)
- 2 low-stakes follow-on (L1 starter gear, gear→augmentation rename confirmation)

**Next step:** Matt chooses (I)/(II)/(III) cadence; decisions-log + Discipline #13/#14 drafts follow.

### jack-ryan Gate 1 reports — Day 2

| Findings file | Verdict | Date |
|---|---|---|
| `qa/findings/2026-05-14-humanoid-bias-design-mode-review.md` | PASS WITH FLAGS — 2 WARN + 4 INFO, all addressed in doc 37 draft 2 | 2026-05-14 |
| `qa/findings/2026-05-15-b10-4-option-2-and-aoe-philosophy.md` | PASS WITH FLAGS — Option 2 cleared, View A operative empirically | 2026-05-15 |

### Star-lord research pass — fight-log granularity

Returned 2026-05-14. Captured in `agentic_orchestration/dispatches/2026-05-14-v0-7-scoping-notes.md` § "Star-lord research findings." Key insight: Tier 1 extension (~9 lines + migration) unlocks 4 of 6 candidate v0.7 dimensions cheaply; Tier 2 unlocks the 5th but is deferred per Matt's call.

---

## Process events — Day 2

### Permission allowlist consolidated to user-level

`~/.claude/settings.json` updated with comprehensive allow list (98 rules) + deny list (18 rules) + `defaultMode: "acceptEdits"` + `additionalDirectories` covering all four repos. Reduces routine prompts across all agent sessions. **Sessions running at the time of the change did not pick it up** — applies to new sessions only.

### Dispatch grep-heuristic failure mode discovered

Drax's session-start heuristic — `grep -l "## Completion record"` — false-positive-matched the dispatch template's section header. Result: drax silently skipped v0.5.1 dispatch and started Tier 3 housekeeping. Self-corrected after Matt prompted.

**Fix to land:** add explicit `**Status:** PENDING` header to dispatch template; agents check `Status:` field for `PENDING` vs `COMPLETE`, not section-header presence. Captured here; not yet implemented across existing dispatches. ~30 min of template + sweep work for the next session.

### Dispatch HELD-status language ambiguity

v0.6-encounter-viz dispatch was marked **HELD** but drax read it as "wait for the metric data that may inform the mechanism viz" and executed anyway. Held-dispatch language should explicitly state: *"Do not execute. Knight-rider will confirm when this dispatch is active."* Same fix pass as above.

### Form-bias deep dive — substantive design work

Multi-hour design conversation between Matt and knight-rider produced doc 37. Several principles emerged:

- **"Recovery" framing reframed to "structural realignment / realizing latent intent"** per jack-ryan WARN 1
- **Two discipline candidates surfaced** with multiple empirical instances each (#13 implicit-pillar drift, #14 internal-vs-generative schema separation)
- **Cipher architecture proposed** for the canonical-four elements (hide labels from LLM; expose abstract pair structure; per-season vocabulary generates against abstract structure)

---

## Seam-by-seam state

### rocket
- No active dispatch
- Queued (no dispatch yet): kit_anchor rename, D1 pool reconsideration (significant), embodiment-axis addition, pair-structure layer generation, mechanical-signature pool design
- **Movement-speed research pass** is the most likely immediate next item if Matt wants Q2 resolved before View lock

### gamora
- B10.4 partial (code + math + commits + decisions-log entries) — **BLOCKED on View lock + Option 2 implementation**
- B10.2 Gate 2 still pending
- Downstream queued: B10 V2 sequential rooms, B14.5 V2

### star-lord
- gear-pool-stats: **shipped** (intermediate-tagged). MIGRATION.md authored.
- telemetry-tier1: **dispatch ready, not picked up.** May need explicit redirect.
- Downstream queued: LLM prompt-leak audit (form-bias work)

### drax
- v0.5.1: shipped intermediate; milestone tag pending Matt visual QA
- v0.6.5: shipped intermediate (housekeeping)
- v0.5.2 stats display: dispatch needed (knight-rider authors)
- v0.7-encounter-analytics: held on multiple preconditions
- Downstream queued: form-bias display-leak audit; encounter-viz scope expansion

### jack-ryan
- Two Gate 1 reports filed Day 2 (both PASS WITH FLAGS)
- Standing by for: B10.4 decisions-log entry drafts (quick review); form-bias decisions-log + Discipline #13/#14 drafts; v0.5.1 acceptance review when Matt approves tag

---

## For Matt at next session start

### 🔴 Top 3 priority items

1. **Resolve Q1 (divergence floor/ceiling) + Q2 (movement speed) — or explicitly defer them — BEFORE the View A/B/C lock.** These questions may shift the View read. If you want them resolved first, knight-rider's next move is a rocket+gamora movement-speed research-pass dispatch. If you want to lock View A now based on jack-ryan's empirical finding, knight-rider drafts the two decisions-log entries.
2. **Visual QA on drax v0.5.1** at the preview URL. Once confirmed, drax cuts milestone tag `v0.5.1`. Quick.
3. **Pick form-bias cadence Option (I) / (II) / (III).** Knight-rider's recommendation is (I) — decisions-log + Discipline #13/#14 next session.

### Quick actions available

- Launch star-lord with the telemetry-tier1 dispatch — `cd ~/Games/reincarnated-engine && claude --agent star-lord`. Explicit redirect: *"pick up `agentic_orchestration/dispatches/2026-05-14-star-lord-telemetry-tier1.md`."*
- (When v0.5.1 is approved) Launch drax briefly to cut milestone tag.

### Long-running streams

None active at session-end. All work is committed and tagged at intermediate level. Tag-protocol-compliant.

### What I (knight-rider) will do next session unless redirected

1. Read first-invocation checks (per system prompt)
2. Surface this handoff's top 3 priority items immediately
3. Wait for Matt's direction on Q1/Q2/View lock OR form-bias cadence
4. Author decisions-log entries when direction is locked
