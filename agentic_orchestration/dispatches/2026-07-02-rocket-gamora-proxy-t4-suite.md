# Dispatch — 2026-07-02 — rocket (+ gamora) — dormant-T4 revival + PROXY-T4 SUITE (B1, Lane B)

**From:** knight-rider
**To:** rocket (strategy classes + η integration + dormant-five revival) · gamora (sim-eval + final magnitudes)
**Approved by:** Matt 2026-07-02 (relay §2 ruling 4 — DEMO-CRITICAL; ledger D.1 #9; one-realm §5 ask 4). Verbatim: *"Summon-focused kits MUST have a proxy-focused T4… make all of the dormant T4 capstones alive in the engine (including proxyspawn) and… a full suite of proxy-T4's for the demo, so decent proxy kits can be emitted for selection."*
**Estimated effort:** 4–7 days (two-phase engine work; rocket architecture → gamora numbers)
**Acceptance:** the five v1.1-dormant strategies are ALIVE in the engine (sim_prerequisite strings cleared/re-named per revival) + the six-member proxy-T4 family (S1–S6) exists with tier-aware magnitudes and η wired so summon kits draw proxy-family capstones. gandalf's canonical spec is the authority.
**Status:** Lane B critical path (B4 demo emission depends on this). **GATE OPEN** — gandalf proxy-T4 suite design spec AUTHORED (`c764f40`, canonical at `reap-die-rise-engine/proxy-t4-suite-spec-2026-07-02.md`). Two-phase, same-repo → SERIAL: rocket architecture first, gamora sim-eval + magnitudes second. Gate-1 critique-pair (jack-ryan DESIGN-MODE + gandalf design-fit against the spec's A1–A6) required before execution.

## Context

Every live T4 amplifies the **caster's own body** (DDA 1.75× — `mechanic_alteration.py:664`). W2 measured a summoner's body at **WR 0.000 caster-alone**; proxies carry 100% of the kill. A summon kit drawn under the current T4 set gets a capstone multiplying its *smallest* surface — mechanically dead weight at the exact genre-promised fantasy peak. The fix is a **family, not a node** (PoE/D2/Last Epoch precedent). Matt's doubt — *"will only one T4 work for all Proxies?"* — is answered mechanically: **different decl shapes draw different family members via axis_match** (spec §4/A3). The two D3-certified fixtures MUST rank different top members.

**gandalf's spec (`proxy-t4-suite-spec-2026-07-02.md`) governs.** It owns the design; **gamora owns final numbers** (math-note-first Disc #18, single-param-isolated sweeps Disc #24, fresh seeds 53M+, boss anchor FIXED per D3 harness); **rocket owns strategy-class architecture + η integration + the dormant revival**.

## Required reading before starting

- `canonical/reap-die-rise-engine/proxy-t4-suite-spec-2026-07-02.md` — THE authority (six members §2 · tier table §3 · η integration §4 · rulings R1–R5 §5 · dormant-five dispositions §6 · acceptance A1–A6 §7)
- `canonical/current-to-end-state/current-to-end-state-serial-content-emission.md` D.1 #9 (the gate this closes)
- `src/reincarnated/generation/mechanic_alteration.py` — η architecture (:65/:69/:338), ABC (:255), v1.1-deferred list (:45-46), `sim_prerequisite` (:266-271), DDA (:664), blood-magic element-resonance precedent (:325-334)
- `src/reincarnated/.../proxy_vocabulary_bridge.py` — the four scaffold levers (:68 HP / :77 / :232 damage_multiplier / :255 attack-interval) — R2 says these stay untouched DEFAULTS
- `src/reincarnated/.../proxy_commander.py:59-70` — Set-#6 calibrated contribution constants (R2 HARD BOUNDARY — T4 multiplies on top, never edits)
- gamora D3 cert (`gamora/v-proxy-fight-calibration-1` @ `abb010d`; `simulation/AGENT_STATE.md`) — the certified fixtures + `PROXY_TIER_MAX_ACTIVE` {minimal:3, mid:2, full:1}

## Cross-seam contract change? (Principle 6 gate)

Intra-engine (generation strategy classes + simulation eval). The T4 decls surface on existing kit records (`t4_candidates`/`primary_t4`); the demo bundle consumes them at B4 emission. No new cross-seam schema — but **flag star-lord** if the emission surface needs a new field to carry a family-member primary_t4.
- `Round-trip: intra-engine (rocket generation + gamora simulation); T4 decls ride existing kit-record surfaces into B4's emission. If a new emitted field is needed, MIGRATION coordination with star-lord before B4.`

## Scope — PHASE 1 (rocket: architecture)

- [ ] Author the six strategy classes S1–S6 per spec §2 (ProxyDamageAmplification / ProxyBulwark / ProxyLegion / ProxySurge / ProxyDeathConversion / ProxySpawn-revived)
- [ ] **η integration** (spec §4): hard eligibility gate — S1–S5 `opportunity_scan()` → 0.0 for empty-decl kits; S6 inverts (empty-decl only). axis_match keys off DECL SHAPE (count>max_active→S3; count==1+full→S2/S1; long cadence→S4; high-lethality pref→S5). thematic per element-resonance. Manifestation ladder: S1/S2/S4/S5 continuous scale-down at rank2/3; **S3 integer axis is T4_active-only** (η=0 below tier 3)
- [ ] **Dormant-five revival** (spec §6): clear/re-name each `sim_prerequisite` with a one-line justification (ProxySpawn→S6; ZoneControl; ConditionalModifier; ResourceBuffer; MechanicReplacement). Any prerequisite genuinely still absent → NAMED residual (no silent re-defer — Disc: no deferral-as-disposition)
- [ ] **Rulings asserted** (spec §5): R1 no-DDA-propagation (separate surfaces); R2 decl-surface-only (bridge constants + Set-#6 untouched); R3 one primary_t4; R4 count-wall (S3 raises max_active + count floor together, ceiling 3); R5 S1–S5 zero-effect on solo-bin
- [ ] **Phase-1 EXIT GATE (jack-ryan Gate-1 fold B1-1):** answer "does the family-member `primary_t4` fit the EXISTING emitted surface, or need a NEW emitted field?" BEFORE Phase-2 closes — if new, coordinate MIGRATION with star-lord NOW (not discovered mid-B4-emission). This is the cross-seam variant of Disc #1 (contract-before-code); cheap now, expensive at B4
- [ ] **Tag-commit body requirement (jack-ryan Gate-1 fold B1-2):** the five dormant-revival `sim_prerequisite` one-line justifications (spec §6) are a REQUIRED artifact in rocket's tag-commit body — so the "no silent re-defer" discipline is auditable at Gate-2, not merely asserted (the item most likely to be skipped under wave pressure)
- [ ] Tag: `rocket/v-proxy-t4-suite-strategies-1`

## Scope — PHASE 2 (gamora: sim-eval + magnitudes)

- [ ] **Final magnitudes** for the 10-cell tier table (spec §3) — math-note-first (Disc #18), single-parameter-isolated sweeps (Disc #24), fresh seed range 53M+ (D3 consumed 52M), boss anchor FIXED per D3 harness
- [ ] **A2 sim delta:** each S1–S4 on a D3-certified fixture produces a measurable build-floor delta in its axis (kill-time↓ S1/S3/S4; survival-margin↑ S2) vs no-T4 baseline; NO member makes caster-alone viable (amplify proxy, not body)
- [ ] **A3 differentiation (THE Matt-doubt test):** on the two certified fixtures, η ranks DIFFERENT family members top (bone-acolyte count-2→S3/S4 lean; crypt-lieutenant count-1 full→S2/S1 lean). Same-top → axis_match under-differentiated → rework before ship
- [ ] **A5/A6 boundary+invariance assertions:** R1 (no DDA propagation) + R2 (Set-#6 untouched) explicit test assertions; S1–S5 solo-invariance asserted; dormant-four solo effects validated per-strategy
- [ ] Tag: `gamora/v-proxy-t4-suite-eval-1`

## Acceptance criteria (spec §7 — Gate-1 checks against these)

- [ ] **A1** post-un-gate emission: every proxy-bin kit carries ≥1 family member in `t4_candidates`; primary_t4 family-share ≥90% heavy / ≥60% light (measured at B4, not forced)
- [ ] **A2** sim delta measured for S1–S4; no member makes caster-alone viable
- [ ] **A3** the two fixtures rank different top members (THE differentiation test)
- [ ] **A4** each member's on-screen read is nameable in one clause (feeds D5)
- [ ] **A5** R1 + R2 boundaries asserted in tests
- [ ] **A6** S1–S5 solo-invariance asserted; dormant-four solo effects validated

## Out of scope (explicit non-goals)

- Final T4 flavor NAMING/narration — rides the phase-5 T4 narration pass (`phase-5-t4-narration-amendment-2026-05-26.md`), NOT this dispatch
- The demo emission run (B4) — this makes the suite EXIST; B4 emits with it live
- Editing bridge module constants or Set-#6 calibrated constants (R2 HARD BOUNDARY)
- The ranged-proxy NAV question (separate PART E fork — spec §8 notes count=2 delivers a content-level mitigation; nav fix is post-demo)
- **Named descope valve:** if the wave must cut, **S5 is the cut** (only member needing new trigger plumbing) — defers to launch, the other five stand

## Quality criterion

**Game-quality goal:** summon-focused kits get a capstone that amplifies the thing that actually kills (the proxies), so the demo can emit "decent proxy kits for selection" (Matt) and the necromancer fantasy peaks at the capstone instead of going dead. The differentiation (A3) is what makes "400 unique heroes" credible at the T4 layer — not one proxy-T4 reskinned six ways.

**Refutation conditions (surface if any apply):**
- A3 fails — both fixtures draw the same top member (axis_match under-differentiated; the Matt-doubt is REAL and unaddressed — surface before ship)
- A dormant strategy's sim_prerequisite genuinely still doesn't exist post-spatial-sim (NAMED residual, not silent re-defer)
- A family member makes caster-alone viable (spec violation — the T4 amplifies proxy contribution, not the body)
- Magnitudes set without math-note-first / without single-param isolation (Disc #18/#24 violation)
- The suite edits the certified scaffold or Set-#6 constants (R2 HARD BOUNDARY breach — the D3 cert must not be re-tuned underneath)

## Open questions for the agent to resolve (document; escalate to KR)

- Per-strategy dormant-revival feasibility (spec §6 — the v1.1 labels predate the spatial sim; several may be cheap now; NAME any genuinely-still-blocked)
- Whether S5 (DeathConversion trigger plumbing) fits the wave or takes the named descope valve — rocket+gamora assess cost; surface to KR if the cut is warranted
- Whether the emission surface needs a new field to carry a family-member primary_t4 (flag star-lord → MIGRATION before B4)

## References

- proxy-t4-suite-spec-2026-07-02.md (THE authority) · serial-emission ledger D.1 #9 · relay §2 ruling 4
- gamora D3 cert `abb010d` · mechanic_alteration.py / proxy_vocabulary_bridge.py / proxy_commander.py
- MASTER: `2026-07-02-one-realm-mvp-build-MASTER.md` (Lane B)

## Completion record — PHASE 2 (gamora sim-eval + magnitudes) — 2026-07-02

**Status:** COMPLETE. Tag `gamora/v-proxy-t4-suite-eval-1`. Closes B1 (Phase 1 rocket + Phase 2 gamora both land). B4 demo-emission unblocks once the star-lord `export/` primary_t4 widening (rocket fold B1-1 blocker) also lands.

**Math note (Disc #18, math-before-code):** `reincarnated-engine/src/reincarnated/simulation/math/proxy-t4-suite-eval-2026-07-02.md`.
**Harness:** `reincarnated-engine/scripts/gamora_proxy_t4_suite_eval_2026_07_02.py` (a3 / a5a6 / smoke / full).
**Test pins:** `reincarnated-engine/tests/test_proxy_t4_suite_eval.py` (9 pins; 27 green with rocket's 18 architecture tests).
**Raw:** `agentic_orchestration/cycle-14-wave-5-season-001/b1-proxy-t4-suite-eval-2026-07-02-full.json`. **Seed base 53,000,017 → next free 54M+.**

**Final magnitudes (spec §3 10-cell table — gamora-owned, sweep-CONFIRMED HOLD, no re-tune):**
| Strategy | proxy-light | proxy-heavy |
|---|---|---|
| S1 DamageAmp | 1.75× | 1.5× |
| S2 Bulwark | HP ×3.0 | HP ×2.0 |
| S3 Legion | +1 | +2 (ceiling 3) |
| S4 Surge | −30% | −40% |
| S5 DeathConv | ~4s burst | ~2s burst (band only; new plumbing, not sim-run) |
| S6 ProxySpawn | 0.5× (sub-summoner) | — |

The current `_PROXY_SCAFFOLD_MAGNITUDES` in `mechanic_alteration.py` already equals these final values → rocket's dict is correct as-landed; a SCAFFOLD→CONFIRMED comment flip is a trivial rocket follow-on (values unchanged).

**A2 measured deltas (S1-S4, both certified fixtures, both boss shells — ALL PASS):**
- S1: kill-time 60→40s (bone) / 60→35s (crypt), army-DPS up.
- S3 (strongest lever): 60→20s (bone +2) / 60→30s (crypt +1).
- S4: 60→37s (bone) / 60→43s (crypt) via attack-interval shave.
- S2: wall soaks 2-3× boss slams, WR holds 1.0 (survival-margin↑; no-death-risk boss → WR 1.0 both, margin is the read).
- **NO member makes caster-alone viable:** proxy_decls=[] WR 0.0 baseline AND under every T4 (delta is proxy-borne only). R1 amplify-proxy-not-body proven.

**A3 (THE Matt-doubt test) — PASS on the REAL certified fixtures. The two draw DIFFERENT tops:**
- `demo_bone_acolyte` (count-2 horde) → **PROXY_LEGION** (η 0.704, clean margin).
- `demo_crypt_lieutenant` (count-1 full) → **PROXY_BULWARK** (η 0.679).
- **NAMED FRAGILITY (surfaced, not smoothed):** on crypt, BULWARK ties SURGE at η 0.679 — top by family-order tie-break, not margin. NOT a rework trigger (fixtures rank different tops, both crypt candidates are spec-predicted). Flagged for phase-5 axis_match review if crypt top must be margin-robust; gamora does NOT self-re-tune rocket's axis_match (Phase-1 seam).

**A5/A6 — PASS.** R1 (DDA keys disjoint from proxy intent keys + sim invariance); R2 (no Set-#6/certified constant in code + certified baseline byte-unchanged under T4 apply, G-SCAFFOLD); A6 (S1-S5 zero on solo; S6 intended crossing-member grant on solo non-summoner).

**Residual (carried from D3, unchanged):** `demo_gravecaller` ranged caster-summoner still uncertified (ranged-proxy NAV gap — a T4 multiplier cannot fix an archer that never reaches the boss). A2/A3 run on the 2 MELEE certified fixtures only. Same fold-D residual D3 surfaced to KR; Phase 2 does not re-open it.
