# Autonomous-Run Plan v2 — Engine-Completion + Pipeline Tracks

> **STATUS:** CURRENT (load-bearing as of 2026-06-17) — see `canonical/00-ground-state.md` § 1. The active charter for the next autonomous run. **SUPERSEDES** `canonical/story/2026-06-16-engine-state-and-autonomous-run-plan.md` (v1), now stamped HISTORICAL-SUPERSEDED — v1's frontier was a single convergent gate; the real frontier is two parallel tracks (engine-completion + pipeline). v1 was also found **stale on 3 items and silent on 3** by the post-run review (`agentic_orchestration/gandalf/notes/2026-06-16-autonomous-run-review-and-completion-frontier.md`). That failure is the discipline this charter is built to not repeat — see § 0.1.

**Date:** 2026-06-17
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-17 — *"pre-author what you can and draft a new autonomous … session for the next engine and pipeline steps that are unblocked or can be."* This doc is the draft; the pre-authored gandalf bottleneck-removers are §2 + the StyleProfile ruling (`canonical/story/styleprofile-output-shape-ruling-2026-06-17.md`).
**Orchestrator at run-time:** knight-rider (engine + cross-cutting); gandalf orchestrates the in-flight descent run-to-green load-path gate (Track B sub-track, separate Matt auth).
**Companions:**
- `agentic_orchestration/gandalf/notes/2026-06-16-autonomous-run-review-and-completion-frontier.md` — the verified-against-disk review of the prior run; § 5 two-completion-bars; § 7 deferred-work empirical criteria.
- `agentic_orchestration/autonomous-run-2026-06-16-RETURN-PACKAGE.md` — the prior run-log (Waves 1/1.5/2/4) + § 2 parking lot.
- `agentic_orchestration/skill_handoff_2026-06-16.md` — most-current state (1D+b6 retired, KPM closed, §6=6b).

---

## 0. TL;DR — the frontier is TWO tracks, not one gate

The prior run + the sessions since closed the convergent middle. **§6 set-bonus magnitude is RULED (= 6b, Matt 2026-06-16). 1D sim + b6 are RETIRED outright — 2D spatial is the sole battle sim. KPM-band recalibration is CLOSED (Gate-2 PASS-WITH-INFO).** None of those is a gate anymore. What remains is two independent tracks that can run in parallel:

- **Track A — engine completion.** Drive the spatial 2D sim from "certified" toward "shipped loadout-faithful + proxy-complete + production-ready." Keystone live-integration is the unblocked head of this track (§6=6b ruled removes its last design dependency).
- **Track B — pipeline / Synty.** The Synty corpus is **downloaded** (136 zips, 8.8 GB) and the gear-spec **resumption gate just cleared** (galadriel slice-verification YES/YES). The deferred gear-spec system is now resumable; the descent render run-to-green is already in flight; the procgen options matrix is delivered (adoption deferred, Matt-gated).

**What I pre-authored to remove gandalf as a bottleneck:**
1. **The StyleProfile output-shape ruling** (`canonical/story/styleprofile-output-shape-ruling-2026-06-17.md`) — the §7.6 canon call whose empirical gate just resolved. rocket/elrond/drax/star-lord consume it without waiting on me.
2. **Pre-registered gandalf endorse-criteria** (§ 2 below) — the design-side acceptance gates for every Track-A wave, written as PASS/PARK criteria the critique-pair can evaluate without me. The run parks for me only on the explicit exceptions named in each criterion.

### 0.1 The run-start discipline (NON-NEGOTIABLE — the v1-staleness lesson)

**This plan is a starting hypothesis, NOT ground truth.** v1 failed precisely because it was consumed as truth after the board had moved under it. At run-start, knight-rider MUST reconcile this plan against disk before firing any wave:
- `git log --oneline -20` since this commit — what landed?
- For each wave below, the named precondition is a *claim to verify*, not a fact to trust. Verify the flag state / file existence / gate status on disk.
- If a wave's precondition is already satisfied (work landed) → mark it done, advance. If a precondition dissolved (the thing it depended on was retired) → drop the wave, note it.
- **Trust-but-verify beats trust.** The cheapest refutation (a grep, a SQL count, a Pattern-A query to the seam owner) precedes any wave that depends on a claim in this doc.

---

## 1. Verified state reconciliation (disk-truth as of 2026-06-17, commit `8da65d1`)

| Item | Prior framing | VERIFIED current state | Source |
|---|---|---|---|
| §6 set-bonus magnitude | open decision | **RULED = 6b** (reference-set instrument; 6a = eventual shipped form) | skill_handoff line 39; Matt 2026-06-16 |
| 1D sim / b6 | parity fork pending | **RETIRED outright**; 2D spatial sole sim; v1 skipped, v1.1 current | skill_handoff; b6-stack outright-deletion dispatch |
| KPM-band recalibration | divergent (5–55×) | **CLOSED** — numerator fix rooms/min→mobs/min collapsed to 0.63–4.74×; bands wired (6 cohorts) | KR Gate-2 PASS-WITH-INFO |
| Keystone gear-materialization + node-wire | to-build | **BUILT** (additive, flag-gated); `apply_max_profile_investment` default **False** — LIVE-INTEGRATION queued | combatant.py:436 (verified False); contract `c7b0de5` |
| Proxy-Commander Set #6 | to-spec | **SPEC'D + COMMITTED** — proxy-add spec + #6 capstone (`17b80d5`) | both files on disk |
| Synty FBX corpus | long-pole download | **COMPLETE** — 136/136 zips, 8.8 GB, verified; crawl method cracked + 157-collection enum | `4772b99`, `1c07aaa` |
| Gear-spec resumption gate | deferred behind slice | **CLEARED** (geometry half) — galadriel #2+#3 YES; §7.6 ruling now fired | `8da65d1`; ruling doc 2026-06-17 |
| elrond Synty gear-substrate catalogue | — | **DISPATCHED** (Gate-1 cleared), in flight | `837dd7f` |
| legolas Godot procgen options matrix | active commission | **DELIVERED** (top-3: GridMap / SimpleDungeons / WFC — all engine-authority-PASS) | `efd66f3`; findings.md |
| Audit camera | proposed | **ACCEPTED**; validator re-scoped to both-ends-land load-path | `8216264` |
| Descent render run-to-green | — | **IN FLIGHT** (round 1 fired; drax + galadriel parallel; gandalf orchestrating) | `c490f51` |

**Net:** the convergent gate is gone. Two tracks remain. v1's three blocker-lists are obsolete; this table replaces them.

---

## 2. Pre-registered gandalf endorse-criteria (the bottleneck-remover)

For each Track-A wave that would normally park for a gandalf design-endorse, the criterion below is the PASS test. **If the criterion is met, the critique-pair (jack-ryan Gate-2 + this criterion) terminates the wave on clean pass — no park for gandalf.** The run parks for me ONLY on the explicit exception in each.

### 2.1 Keystone live-integration (Wave A1)
**ENDORSE if ALL hold:**
- Re-measured archive validates the contract's § 8 predictions directionally (full 15-point node investment + real Legendary T1 main-hand + 4-piece Set raises measured kit power vs the stripped baseline; the ~0.35× zero-investment penalty is gone).
- The measured main-hand is the **kit's own `selected_weapon`** at Legendary T1 (contract § 3.3 weapon-as-identity-surface), not a synthetic stopgap.
- Set bonus is measured at the **6b reference instrument** (Matt-ruled), not a generated-kit-aligned 6a.
- Rank ordering across the archive is preserved or improves in coherence (no kit inverts implausibly).

**PARK for Matt if:** the re-measure inverts the archive's rank order in a way that implies a balance defect (not just a level shift), OR the full-investment profile pushes any cohort outside its just-wired KPM band by >1 band-width (the keystone and the KPM bands were calibrated on different gear assumptions — a collision is a genuine new question).

### 2.2 Proxy-Commander Set #6 forward-work (Wave A2)
**ENDORSE if ALL hold:**
- `proxy_primary` selector flags sensible membership: proxies whose contribution ≈ 0.5 of player offense flag as commander-set-eligible; **Beast-Taming hunters correctly do NOT flag** (the named negative case — pets are not proxies).
- 2pc friction-accelerate + 4pc Clause A (parity-bounded count/power/duration) measure within the parity books they reference (no clause exceeds its parity bound).
- 4pc Clause B offense-inheritance holds `s < 1` (non-negotiable — verify the coefficient, not just the behavior).
- `proxy_primary` is measured at the neutral 6b instrument (resolves the capstone's measurement circularity).

**PARK for Matt if:** the LIVE-ONLY command-amplification (`effective_s(t)`) is being promoted from live-only into the parity books (that is a production semantic shift — Tier 3), OR the selector flags a class the design did not intend (membership surprise = new design question).

### 2.3 F1 production-readiness re-measure (Wave A3)
**ENDORSE the BUILD if:** the geometry-corrected outcomes match the design intent recorded for F1 (the fix produces spatially-correct results, not just different numbers).
**PARK for Matt (Tier 3) on:** the **production semantic-shift ratification** — flipping F1 from "fixed in sim" to "this is the shipped behavior" is a ratification Matt holds, not a gate the run closes. Build + measure autonomously; ratify with Matt.

### 2.4 D4 proxy-port flag-flip (Wave A3)
**ENDORSE the BUILD + measure if:** the port behaves per the proxy-add spec under the flag.
**PARK for Matt (Tier 3) on:** flipping the production default (same semantic-shift principle as F1).

### 2.5 Gear-spec rocket §7.2 build (Track B, Wave B2)
**ENDORSE if:** the L2 restyle-leaf shader + accent-attachment system are built per the StyleProfile ruling (per_region 5-zone path + whole_tint degrade path; sockets per galadriel's verified set) AND consume the manifest's real field set + elrond's real values.
**PARK for gandalf (design, NOT Matt) if:** the build surfaces a substrate reality that contradicts the ruling's schema (e.g., a pack with a zone count the additive-nullable shape can't express) — that is a ruling-amendment, my seam. **Do NOT park for Matt** on this; route to gandalf.

---

## 3. Track A — engine completion (wave queue, dependency-ordered)

> Reconcile each precondition against disk before firing (§ 0.1).

### Wave A1 — Keystone LIVE-INTEGRATION  **[HEAD — unblocked]**
- **Precondition (verify):** `apply_max_profile_investment` default `False` (verified) + §6=6b ruled (verified) + gear-materialization & node-wire built (verified).
- **Do:** flip `apply_max_profile_investment` ON in the measurement path; consume the kit's real selected gear (real Legendary T1 main-hand = kit's `selected_weapon`); swap 4 slots to the 6b reference Set; re-measure the archive.
- **Gate:** jack-ryan Gate-2 + gandalf endorse-criterion § 2.1. **Tier 2** (fire on clean; park on the § 2.1 exceptions).
- **Owner:** gamora (measurement path) + rocket (gear materialization) as the contract § 7 hooks name.

### Wave A2 — Proxy-Commander Set #6 forward-work
- **Precondition (verify):** proxy-add spec + #6 capstone committed (verified `17b80d5`); keystone re-measure landed (A1) so proxy_primary measures against a faithful baseline.
- **Do:** build the proxy-add (skills + gear modifiers + `proxy_primary` selector) per spec; implement #6 capstone (2pc + 4pc Clause A/B; command-amplification LIVE-ONLY).
- **Gate:** jack-ryan Gate-2 + gandalf endorse-criterion § 2.2. **Tier 2**.
- **Owner:** rocket (generation: skills, gear modifiers, selector) + gamora (simulation: proxy combat behavior).

### Wave A3 — F1 fix + D4 proxy-port (production-readiness, BUILD autonomous / RATIFY parks)
- **Precondition (verify):** F1 defect + D4 flag still open in the § 2 parking lot of the return package.
- **Do:** build the F1 geometry fix + re-measure; flip the D4 proxy-port flag + measure.
- **Gate:** § 2.3 / § 2.4 — **BUILD is Tier 2; production semantic-shift RATIFICATION is Tier 3 (parks for Matt).**
- **Owner:** gamora / rocket per defect locus.

### Wave A4 — MOB_HP baseline (PRODUCE autonomous / READ parks)
- **Precondition (verify):** KPM recalibration closed (verified) so the bimodality source (`MOB_HP_DIFFICULTY_MULTIPLIER=1.5`) is isolated as the second defect.
- **Do:** the run PRODUCES the MOB_HP baseline measurement as a normal output of A1–A3 re-measures. **Do NOT decide the MOB_HP reconciliation in-run.**
- **Gate:** **Tier 3 — the reconciliation READING/decision parks for Matt POST-baseline** (Discipline #18 refinement: extension methodology consultation fires AFTER baseline empirical data lands, not before; D3-Inferno precedent). The run banks the diagnostic question, not the answer.

### Wave A5 — star-lord export reinterpret (KPM open item #3)
- **Precondition (verify):** the export still emits the pre-recalibration KPM semantics.
- **Do:** reinterpret the export to consume mobs/min cohort-band semantics (additive; the old read is wrong, the new read is correct).
- **Gate:** jack-ryan Gate-2; additive/correctness fix. **Tier 1** (runs fully; Matt only on gate fail).
- **Owner:** star-lord.

---

## 4. Track B — pipeline / Synty (wave queue)

### Wave B0 — Descent render run-to-green  **[IN FLIGHT — continue, do not re-queue]**
- **State:** round 1 fired (drax sanctum-stair fix + audit-camera extension + both-ends-land scan; galadriel register-2 baseline). Awaiting both completion notifications. **Separately Matt-authorized** ("run until every still passes per galadriel and drax").
- **Do:** on round-1 returns → gandalf rules drax's load-path flags (canon call on the both-ends-land Tier-1 check) + folds galadriel's scores into the matrix → triage → fix rounds until **dual-gate GREEN** (Gate A aesthetic ≥~4.0 + Gate B load-path both-ends-land for every still).
- **Gate:** gandalf canon call on Gate B; galadriel CV on Gate A. gandalf orchestrates this sub-track directly.

### Wave B1 — elrond Synty gear-substrate catalogue  **[IN FLIGHT — continue]**
- **State:** dispatched, Gate-1 cleared (`837dd7f`).
- **Do:** elrond materializes the substrate-half manifest (per-mesh: mode + zone count + provisional region labels + socket inventory) feeding the StyleProfile ruling's field set. Consumes the verified slice.
- **Gate:** elrond seam; jack-ryan Gate-2 on schema. **Tier 1/2** (substrate curation).

### Wave B2 — Gear-spec rocket §7.2 build  **[gated on B1 + ruling]**
- **Precondition (verify):** StyleProfile ruling fired (verified — this commit) AND B1 manifest design-owned half + substrate slice landed.
- **Do:** rocket builds the L2 restyle-leaf master ShaderMaterial (per_region + whole_tint paths) + accent-attachment system per the ruling.
- **Gate:** jack-ryan Gate-2 + gandalf endorse-criterion § 2.5 (**park routes to gandalf, NOT Matt**, on schema-contradiction). **Tier-2-gated-on-manifest** — do NOT fire before B1.

### Wave B3 — procgen adoption  **[NOT in run scope — named for completeness]**
- **State:** legolas options matrix delivered (top-3: GridMap pure-receiver / SimpleDungeons room-prefab CC0 / WFC seam-filling — all engine-authority-PASS).
- **Disposition:** the ADOPTION decision is a **future Matt-gated call** (a later modularization phase per the research brief). **Tier 3 — does not fire in this run.** Nothing in A or B depends on it.

### The UE packet (Track B terminus — parks)
- **State:** PC integration/playtest node specs documented (`SYSTEM_SPECS_FOR_PIPELINE.md`: RTX 4060 Ti / 8 GB VRAM constraint / i7-14700F). The end-to-end pipeline (gen→balance→name→export→render→UE) is Bar 2, further out.
- **Disposition:** **Tier 3** — UE-packet requirements name PC-seam interfaces (mantis/radagast); parks on cross-host naming. Not in this run.

---

## 5. Three-tier pre-authorization envelope (carried from v1, Matt-ratified)

| Tier | Behavior | Applies to (this run) |
|---|---|---|
| **Tier 1** | Runs fully; Matt only if a gate FAILS | A5 star-lord export; B1 elrond curation; additive/correctness fixes |
| **Tier 2** | Pre-authorized to FIRE on the pre-registered clean criterion (§ 2); **park on ambiguity** | A1 keystone; A2 proxy; A3 builds; B2 gear-spec build (gated on B1) |
| **Tier 3** | ALWAYS parks for Matt | A3 F1/D4 production semantic-shift ratification; A4 MOB_HP reconciliation decision (post-baseline); B3 procgen adoption; UE packet; any scope amendment; any gate-fail on a destructive step |

**Safety invariant:** every deletion / flag-flip is git-revertible. Park-and-advance over block-and-wait: a parked wave does not stall the other track.

---

## 6. What parks for Matt (the consolidated list)

1. **F1 / D4 production semantic-shift ratification** — "this is the shipped behavior" is Matt's call, not the run's (build + measure autonomously).
2. **MOB_HP reconciliation decision** — POST-baseline (the run produces the data; the decision waits for Matt with the data in hand; Discipline #18 refinement).
3. **Keystone × KPM-band collision** (§ 2.1 exception) — if full-investment profiles push cohorts out of band.
4. **Proxy selector membership surprise / command-amplification promotion to parity books** (§ 2.2 exceptions).
5. **Procgen tool adoption** (B3) + **UE packet** (PC-seam naming).
6. **Any scope amendment, any new design question, any gate-fail on a destructive step.**

Everything else fires autonomously on the § 2 criteria. **gandalf does not need to be woken for the Track-A gates** — the criteria are pre-registered; the StyleProfile ruling is pre-fired. Route Track-B gear-spec schema-contradictions to gandalf (design), not Matt.

---

## 7. knight-rider kickoff prompt

> **Autonomous run v2 — engine-completion + pipeline.** Charter: `canonical/story/2026-06-17-autonomous-run-plan-v2.md`. **FIRST: reconcile against disk per § 0.1** — `git log` since `8da65d1`, verify each wave's precondition before firing; this charter is a hypothesis, not truth (v1 went stale and that is the failure this run must not repeat).
>
> Run two parallel tracks. **Track A (engine):** A1 keystone live-integration (head, unblocked) → A2 proxy Set #6 forward-work → A3 F1/D4 (build autonomous, ratification parks) → A4 MOB_HP (produce baseline; reconciliation parks post-baseline) → A5 star-lord export reinterpret. **Track B (pipeline):** B0 descent run-to-green is in flight under gandalf — continue to dual-gate green; B1 elrond catalogue continues; B2 gear-spec rocket build gated on B1 + the now-fired StyleProfile ruling; B3 procgen adoption + UE packet are Tier-3, do not fire.
>
> Gates: jack-ryan Gate-2 + the **pre-registered gandalf endorse-criteria in § 2** — terminate Track-A waves on clean pass, NO park for gandalf. Park for Matt only on the § 6 list. Park Track-B gear-spec schema-contradictions to **gandalf** (design), not Matt. Three-tier envelope § 5. Auto-commit in-scope work; **push stays Matt-ask** (or per any standing wave-close pattern Matt sets for this run). Return a package mirroring the prior run's: per-wave log + § 2-style parking lot + what reconciliation against disk changed from this charter.

---

## 8. Sign-off

This charter encodes the verified frontier (§ 1, disk-truth), pre-fires the one gandalf canon call whose gate resolved (the StyleProfile ruling), pre-registers the design-side acceptance criteria so the run does not park for gandalf on Track A (§ 2), and carries the v1-staleness lesson as a run-start non-negotiable (§ 0.1). The two completion bars stand: A drives Bar 1 (spatial sim → shipped-faithful) toward Bar 2; B builds the pipeline toward the same Bar 2 from the presentation side. They meet at the UE packet, which parks.

**Signed:** gandalf, 2026-06-17. Supersedes v1 (`2026-06-16-engine-state-and-autonomous-run-plan.md`).
