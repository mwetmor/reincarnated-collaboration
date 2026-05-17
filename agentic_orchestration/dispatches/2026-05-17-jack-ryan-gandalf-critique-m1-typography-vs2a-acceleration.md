# 2026-05-17 — jack-ryan + gandalf (critique pair) — Phase M1 typography VS2a acceleration review

**Authority:** Matt L3 2026-05-17 (~18:00 EDT): *"Agree with drax on addition of the fix below, but will defer to hive thinking."*
**Type:** Pattern A — critique pair (parallel, ~30 min each, independent advisories).
**Predecessor:** drax v1.6 mobile UX execution plan (`drax/v1.6-mobile-ux-research-and-plan-1`).
**Outcome:** joint advisory — does Phase M1 ship in VS2a (accelerated) or hold post-VS2a (default)?

---

## The decision

Drax's mobile UX execution plan identifies the demo1 "nothing readable on mobile" bug as a **math root cause**:
- Canvas is 1800px wide; CSS-downscales 4.8× to ~375px on a typical phone
- All current `fontSize: N` values are 8-20px **canvas-space**, which renders at 1.6-4.2 **CSS-space pixels** on a phone — genuinely invisible
- Fix: new `src/ui/typography.ts` with `MOBILE_FONT_SCALE = 4.8`; one `font(N)` helper; replace all hardcoded `fontSize: N` with `font(N)`
- Behavior: returns `N * 4.8` on mobile (Mobile.isActive), returns `N` on desktop

Drax's claim: **purely additive; zero desktop behavior change.**

Matt is inclined to accept and pull Phase M1 into VS2a scope (currently planned post-VS2a). Asking for hive validation before commit.

---

## Required reading

1. `canonical/story/mobile-ux-execution-plan-2026-05-17.md` — drax's plan; Phase M1 details
2. `agentic_orchestration/dispatches/2026-05-17-drax-demo-mobile-ux-research-and-plan-commission.md` — commission completion record (the headline finding)
3. Drax v1.5/v1.4/v1.3 ship history (last week's velocity baseline)
4. `canonical/16-project-roadmap.md` § VS2a — current punch-list and ship-gating items
5. `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #11 (attribution), #12 (semantic shifting), #15 (demo as renderer)

---

## Stream A — jack-ryan critique (technical/process steward)

### Questions for you

1. **"Purely additive" claim verification:** drax says zero desktop behavior change. Stress-test:
   - Does `font(N)` on desktop return exactly `N` (no rounding, no DPR side effects)?
   - Is there any code path where `Mobile.isActive` could be wrong at the moment `font()` is called (e.g., during init before mobile detection completes)?
   - Are there any third-party Pixi.js or font-rendering interactions where 4.8× could trigger sub-pixel artifacts on desktop?
   - Could the change introduce regressions in screenshot-diff tests, snapshot tests, or any layout-dependent tests?

2. **Engineering-discipline alignment:**
   - Discipline #11 (attribution): does typography.ts touch any cross-seam contract? (My read: no — it's a demo-internal concern; star-lord export untouched; gamora sim untouched.)
   - Discipline #12 (semantic shifting): would any consumer of the demo's rendered text experience a meaning-change? (My read: no — visible text is rendered, not consumed by other systems.)
   - Discipline #15 (demo as renderer): does typography.ts respect the seam? (My read: yes — it's pure rendering; engine-side is untouched.)

3. **VS2a punch-list impact:** does adding M1 to VS2a delay other VS2a-gating items? Currently in flight VS2a-gating items:
   - Gamora regen (in progress; seasons 3-5 remaining)
   - Drax v1.x demo polish series (active iteration)
   - Pool × VFX-catalogue mapping audit (Drift-14 closure; legolas+gandalf+rocket)
   - Environment tileset catalogue sweep (Drift-15 closure)
   - Gate-3b sim consumption (gamora)
   
   M1 is a single drax dispatch (~200 lines changed; ~30 new). Does it fit in drax's current bandwidth without delaying anything above?

4. **Risk of partial M1:** if M1 ships in VS2a but Phases M2-M7 stay post-VS2a, does that produce any user-confusing partial-state on mobile? (E.g., text suddenly large, but joystick still tiny — does that mismatch confuse?)

5. **Tag protocol recommendation:** M1 in VS2a would tag as `drax/v1.7-mobile-typography-foundation-1` (per the mobile-execution-plan phasing). Suitable for a Matt-approved milestone tag (no prefix) at VS2a ship, or stays seam-prefixed?

6. **Gate-2 implications:** if M1 ships pre-VS2a, what would your Gate-2 review look for? Pre-flag any blocking criteria so drax can build to them.

### Your output

A short advisory (~200-400 words) in this dispatch's "Jack-ryan advisory" section below:
- Recommendation: **ACCELERATE TO VS2A** / **HOLD POST-VS2A** / **CONDITIONAL** (with conditions)
- Top 1-3 risks if accelerated
- Top 1-3 mitigations if accelerated
- Gate-2 pre-flags

---

## Stream B — gandalf critique (design/experience steward)

### Questions for you

1. **Playtest readability — is M1-absence a VS2a-shippable state?** VS2a is the playtest-validatable demo; if mobile readability is "genuinely invisible" per drax's math, can VS2a ship with mobile-illegible text? Or does mobile-illegibility undermine the VS2a playtest value?
   - The form-bias cadence + strategic-axis lock framed VS2a as desktop-primary. Is mobile readability genuinely needed for VS2a's playtest, or is mobile a VS2b-onwards concern?
   - If a Group-2 player (centered overlay map preference; per your map overlay commission) tries the demo on mobile and can't read anything, what's the player-experience cost?

2. **Aesthetic risk of 4.8× scale:** does scaling fonts 4.8× on mobile produce any specific design-canon violation?
   - Pixel-art register: the 1800×944 canvas is designed at HD-2D-pixel register (per `canonical/story/style-register.md`). Does 4.8× font scaling break that register on mobile, or does the CSS-downscale-then-Pixi-upscale chain preserve it?
   - Substrate-color readability: gandalf's perception-engineering principles from the map overlay research (in flight — Stream A) emphasize legibility over realism. Does M1 fit those principles?

3. **Strategic-axis-lock interaction:**
   - The form-bias cadence Option II + sub-lock (b) Isekai-canon-primary at narrative-skin lock — does early mobile typography work pre-empt any strategic-axis commitment?
   - My read: no — typography is platform-render, not narrative-skin. But you've caught these earlier than me.

4. **Hive-thinking input on the 5 deferred mobile open questions** (your v1.7 § 7 Q1/Q2/Q4/Q5; Matt deferred today): does pulling M1 into VS2a affect any of those deferrals? E.g., if M1 lands without Q4 resolved (1080p vs 1440p baseline), is that a problem?

### Your output

A short advisory (~200-400 words) in this dispatch's "Gandalf advisory" section below:
- Recommendation: **ACCELERATE TO VS2A** / **HOLD POST-VS2A** / **CONDITIONAL** (with conditions)
- Top 1-3 player-experience considerations
- Any aesthetic or strategic-axis flags
- Recommendation on whether VS2a-shippable WITHOUT M1 (mobile-illegible) is acceptable

---

## Joint synthesis (knight-rider authors after both stream advisories land)

Once both advisories are in:
- Knight-rider synthesizes the joint hive verdict
- Surfaces to Matt for final sign-off
- If GO: drax dispatch for Phase M1 fires under standard Pattern A rules
- If HOLD: M1 stays at post-VS2a as originally planned

---

## Out of scope

- ❌ DO NOT debate Phases M2-M7 — only M1 is on the table for VS2a acceleration
- ❌ DO NOT re-litigate dual-stick lock (Matt-locked today)
- ❌ DO NOT touch drax's plan artifact — that doc is authoritative as authored
- ❌ DO NOT block on the 4 deferred mobile open questions (Matt explicitly deferred)

---

## Acceptance criteria

- [ ] Jack-ryan advisory authored (~200-400 words; recommendation + risks + mitigations + Gate-2 pre-flags)
- [ ] Gandalf advisory authored (~200-400 words; recommendation + PX considerations + strategic-axis flags)
- [ ] Both tagged: `jack-ryan/v1.2-m1-vs2a-acceleration-critique-1` + `gandalf/v1.9-m1-vs2a-acceleration-critique-1`
- [ ] Hive-log STATE entries (CRITICAL: § 14.1.1 race-condition discipline — two parallel agents writing same hive log)

---

## Coordination notes

- **Two parallel agents** writing this same dispatch file — append your advisory to the section below, separated clearly
- **Race-condition discipline (§ 14.1.1):** PRE-SIGNAL before hive-log appends; pull-rebase before commits; explicit-path staging
- **Gandalf:** you have map overlay Stream A in flight; this critique is small (~30 min). Pause map overlay if needed; resume after.
- **Jack-ryan:** you're currently idle; this is the active critique commission.

---

## Jack-ryan advisory

**Recommendation: CONDITIONAL ACCELERATE TO VS2A**

Drax's "purely additive; zero desktop behavior change" claim is substantially correct but warrants three conditional requirements before the dispatch fires.

---

### Q1 — "Purely additive" verification

The claim holds under normal conditions with two caveats.

`font(N)` on desktop returns `N` identically only if the implementation is a clean ternary with no rounding (`Mobile.isActive ? N * 4.8 : N`). Any `Math.round()` or integer cast inside the helper would silently alter desktop font sizes by ±1px on non-integer base values (e.g., `fontSize: 9.5` exists in combatLog.ts). **Gate-2 pre-flag #1: verify the helper is a pass-through with no numeric transform on the desktop branch.**

`Mobile.isActive` is resolved at the moment of TextStyle construction, which happens at panel-init or spawn time, not at module-eval time. The detection uses `pointer: coarse` + UA string check (`mobile.ts`) — both are synchronous at page load; no async gate. No race risk identified for standard rendering paths.

Pixi.js Text objects do not auto-apply devicePixelRatio, but the 4.8x scale is applied only when `Mobile.isActive` is true, so desktop Text objects are never touched. Sub-pixel artifact risk on desktop is nil. On mobile, very large canvas-space fonts (72–96px) can produce GPU texture atlasing overhead — Pixi's TextStyle `resolution` property mitigates this; the smoke test must verify no visible aliasing on an actual phone.

Screenshot-diff or snapshot tests are at low but non-zero risk: any test that renders a panel on a mock-mobile viewport (or that sets `Mobile.isActive = true` in test setup) will see size changes. **Gate-2 pre-flag #2: drax confirms no test suite fixture forces `Mobile.isActive` true for desktop-context assertions.**

---

### Q2 — Engineering-discipline alignment

- Discipline #11 (attribution): `typography.ts` is demo-internal; zero cross-seam contract exposure. Star-lord export, gamora sim, rocket schema: all untouched. MIGRATION.md not required per ADR-004.
- Discipline #12 (semantic shifting): font size is presentation only; no downstream system consumes rendered text as data. No semantic shift.
- Discipline #15 (demo as renderer): `src/ui/typography.ts` is a rendering concern entirely. Engine-side seam boundary is respected.

No discipline violations identified.

---

### Q3 — VS2a punch-list impact

M1 scope is ~200 lines changed (one-line replacements) + 30 lines new. This is a single drax dispatch, well within a one-session execution window. Drax is the binding-constraint seam on VS2a; the relevant question is whether M1 displaces higher-priority gating items.

Current drax VS2a-gating queue: B11 VFX integration (iterating), character-track rendering (dispatch authored), B6 skill-tree UI surface (open gap), cipher migration drax-side (sequenced behind star-lord Stage 3), and perception-test session-runner (Deliverable 27). M1 is ~0.5 days at most. It fits inside drax's bandwidth IF it is sequenced AFTER or CONCURRENT WITH Deliverable 27 (perception-test runner readiness), which is the current highest-urgency drax item per coordination matrix.

**Condition 1 (scheduling gate): M1 does not displace Deliverable 27 or the Drift-14 pool-cull VFX work. Drax slots M1 as a parallel or immediately-following task, not a replacement.**

---

### Q4 — Risk of partial M1 (text large, other mobile UX still broken)

Text suddenly legible but joystick undersized and no dash button is a known partial-state. This mismatch is acceptable at the VS2a milestone IF the milestone framing is explicitly "desktop-primary playtest; mobile is improved but not complete." The mismatch is NOT acceptable if VS2a is used as a mobile-primary playtest vehicle.

Roadmap (doc 16) confirms VS2a is desktop-primary (end-game-anchored Gauntlet playtest). Mobile-primary playtest is post-VS2b at earliest. The partial-M1 mismatch is therefore within bounds for VS2a scope — players who try mobile will see readable text, which is strictly better than before, even though other mobile gaps persist.

**Condition 2 (framing gate): VS2a ship notes explicitly state "M1 typography foundation shipped; M2-M7 mobile phases deferred to VS2b." No false impression that mobile is complete.**

---

### Q5 — Tag protocol

M1 as a drax dispatch should tag `drax/v1.7-mobile-typography-foundation-1` (seam-prefixed per ADR-003). It is NOT a candidate for a Matt-approved milestone tag (`v<X.Y>`) at VS2a ship — M1 is a foundational module within a larger unreleased phase series. The VS2a milestone tag encompasses the full gauntlet playtest slice; M1 ships as a contained drax sub-tag within that window.

---

### Q6 — Gate-2 pre-flags (build these into acceptance criteria when drax executes)

1. `npm run build` PASSES with 0 TypeScript errors. Any implicit `any` introduced by the helper function is a BLOCK.
2. Desktop visual regression confirmed: launch demo at desktop viewport; verify HUD, combat log, panels are pixel-identical to pre-M1 baseline (manual smoke + screenshot compare if available).
3. Mobile legibility confirmed on 375px viewport (Chrome DevTools or real device): damage numbers, class names, combat log lines, gear names are all readable at normal reading distance.
4. `font(N)` implementation inspection: desktop branch is a pure pass-through (no rounding, no type coercion). Flag if `Math.round`, `parseInt`, `|0`, or `~~` are present in the desktop branch.
5. Test suite green: `npm test` (or equivalent) passes with no regressions. Any test exercising font sizes against specific numeric values must be updated to use `font(N)` expectations.
6. Word-wrap widths: M1 does NOT need to fix word-wrap widths on mobile (that is Phase M5 scope per the plan). Gate-2 BLOCKS any M1 commit that also modifies `wordWrapWidth` values — scope creep would conflate M1 and M5.

---

### Summary

Three conditions before dispatch fires:
- **Condition 1:** M1 is sequenced after or concurrent with Deliverable 27; does not displace VS2a-gating drax work.
- **Condition 2:** VS2a ship notes include explicit "M2-M7 deferred" framing.
- **Condition 3:** Gate-2 checklist items 1-6 built into M1 dispatch acceptance criteria.

All three are operationally lightweight. On net, M1 is a clean acceleration candidate. The "purely additive" claim survives scrutiny at the architecture level; the residual risks are implementation-surface (rounding, test fixtures) catchable at Gate-2 with the pre-flags above.

Cite: Discipline #11, #12, #15; ADR-003, ADR-004; Review Principle 2 (scope containment).

**jack-ryan / 2026-05-17**

---

## Gandalf advisory

**Recommendation: ACCELERATE TO VS2A.**

Read alongside jack-ryan's CONDITIONAL ACCELERATE — his three implementation gates (no-rounding pass-through; non-displacing schedule; M2-M7-deferred ship-notes framing) are the right guards. From the design / player-experience side, the case for acceleration is stronger than "no objection."

**Player-experience considerations (three).**

1. **Reputational asymmetry on a pitch-positioned product.** VS2a is desktop-primary as a balance-validation playtest — the form-bias work and `movement-speed-baseline.md` both anchor on desktop. But the one-pager pitches Reincarnated as an *"isekai mobile ARPG."* Any playtester who reads the pitch then opens the demo on their phone — some fraction will, unprompted — sees 1.6–4.2 CSS-pixel text. That isn't "VS2a doesn't cover mobile yet"; that is "the product positioned itself as mobile-first and the mobile build is illegible." Diablo Immortal took its initial credibility damage in the first 48 hours of player contact, not in patch cycles. Same risk shape here at a smaller blast radius. ~200 lines of additive code closes the hole.

2. **Group-2 / overlay-map cohort cost.** From map-overlay research Stream A (in flight): a meaningful slice of the ARPG mobile audience reads the world primarily through HUD/text affordances rather than spatial chrome. A Group-2 player on mobile today cannot read damage numbers, combat log, or gear names — they get the gauntlet without the *information layer the gauntlet exists to teach.* The end-game-anchored playtest's pedagogical purpose collapses for that cohort.

3. **Phase-cascade unlock.** M1 is the prerequisite for M4 (damage text), M5 (panels), and the rest of M2–M7. Shipping M1 in VS2a doesn't just make mobile readable today — it lets the M2–M7 chain run alongside VS2b instead of behind it. Holding M1 holds the whole chain.

**Aesthetic / strategic-axis flags: NONE.**

- **Style register (HD-2D-pixel, Matt-locked 2026-05-15):** unaffected. The register governs *world rendering* — sprites, environments, VFX. UI typography is chrome. Octopath Traveler, Triangle Strategy, and Live A Live HD-2D Remake all pair pixel-art world with non-pixel-art readable UI text; that is HD-2D canon, not a violation. 4.8× font scale on mobile preserves the register.
- **Form-bias sub-lock (b) — Isekai-canon-primary at narrative-skin:** unaffected. Typography is platform-render layer, not narrative-skin. Drax's read is correct; no strategic-axis pre-emption.
- **Deferred mobile open questions (gandalf v1.7 § 7 Q1/Q2/Q4/Q5):** none gate M1. Skill-name-vs-element-abbreviation (Q4) and HP/MP globe merge (Q1) are post-M1 decisions; M1 only makes whatever text is rendered legible.

**Verdict on VS2a-shippable WITHOUT M1: NO — unless mobile is hard-gated.** Acceptable only if VS2a hard-gates phone detection with a literal "mobile not supported in this playtest" splash. Anything less — including current silent-mobile-failure — risks contaminating the desktop-anchored playtest sample with "I tried it on my phone and it was broken" first-contact data that pollutes the gauntlet findings the milestone exists to produce.

The cleaner path is to ship M1 inside VS2a and remove the question.

— gandalf (`gandalf/v1.9-m1-vs2a-acceleration-critique-1`)

---

## Knight-rider synthesis

**Joint verdict: ACCELERATE Phase M1 into VS2a scope** with jack-ryan's 3 conditions + 6 Gate-2 pre-flags operationalized at M1 dispatch time.

**Convergence:**
- **Jack-ryan (technical/process):** CONDITIONAL ACCELERATE. Claim survives stress-test; disciplines #11/#12/#15 respected; no MIGRATION.md needed (demo-internal); only real risk is desktop-branch pass-through purity (no `Math.round`/`parseInt`/`|0`/`~~` — `combatLog.ts` has `fontSize: 9.5` that would silently shift desktop rendering by 1px under any integer coercion).
- **Gandalf (design/experience):** ACCELERATE — "actively beneficial, not merely no objection." Three PX drivers: (1) reputational asymmetry — playtesters opening unprompted on phones see 1.6-4.2 CSS-pixel text at first contact ("Diablo-Immortal-launch-pattern credibility damage"); (2) Group-2 overlay-map cohort cost — gauntlet's pedagogical purpose collapses on mobile for cohorts that read the world through HUD/text; (3) phase-cascade unlock — M1 is precondition for M2-M7. Style register unaffected; form-bias sub-lock (b) unaffected.

**Critical gandalf finding on the binary:** VS2a-shippable WITHOUT M1 is shippable ONLY IF mobile is hard-gated with explicit "mobile not supported in this playtest" splash on phone detection. Anything less contaminates the desktop-anchored playtest sample with "I tried on my phone and it was broken" first-contact data.

**Implication:** the actual binary is:
- **Option A (recommended by both stewards): ACCELERATE M1** — ~200 lines additive code; mobile becomes playtest-viable
- **Option B: NO M1 + hard-gate mobile** — adds a splash screen + phone detection; preserves desktop-anchored sample purity but caps playtest reach

Both options are valid. Both stewards prefer A.

**If Matt approves A (ACCELERATE):** knight-rider authors M1 dispatch under standard Pattern A. Drax executes with jack-ryan's 6 Gate-2 pre-flags as acceptance criteria. Tag `drax/v1.7-mobile-typography-foundation-1` (seam-prefixed; Matt may promote to milestone tag at VS2a ship).

**If Matt approves B (HOLD + splash):** knight-rider authors small drax dispatch for the phone-detection splash screen; M1 stays at original post-VS2a slot.

**Awaiting Matt L3 sign-off.**

— knight-rider 2026-05-17 ~18:30 EDT

---

*Dispatched 2026-05-17 by knight-rider per Matt L3 "defer to hive thinking." Two parallel ~30-min advisories.*
