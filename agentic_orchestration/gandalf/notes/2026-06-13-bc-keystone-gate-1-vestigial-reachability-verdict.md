# Gate 1 — BC-Keystone Vestigial-Label Reachability Verdict

**STATUS:** CURRENT — Pattern A-deep terminal gate on the BC-measurement keystone
**Author:** gandalf (story-and-design steward)
**Date:** 2026-06-13
**Mode:** Pattern A-deep (terminal Gate-1 read; KR-orchestrated, Matt acts on it)
**Predecessor:** `gandalf/notes/2026-06-13-session-close-handoff-flag-queue-and-bc-keystone-orchestration.md` (§ 5 set this gate's criterion: "substrate evidence, not bugs — do NOT reorder to force")
**Source chain:** rocket gen → gamora MEASURED Axis-4/3B → rocket Items 7/8 → jack-ryan Gate-2 PASS-WITH-INFO (`qa/findings/2026-06-13-gamora-bc-measurement-pipeline-and-full-run.md`)
**Anchors:** `qd-engine-bc-axes-lock-2026-05-20.md` §§ 3.6/3.7; `vestigial_labels.py` (committed code); commit `f2fee41` (the Berserker rule I authored)

---

## TOP-LINE VERDICT

**Gate 1: PASS-ON-CLEAN / DEFER-CONTAMINATED — with one load-bearing correction to the dispatch's framing that changes the Berserker answer entirely.**

The framing-audit (OP § 3.7 Q1/Q2) caught it: the dispatch's three-way split is *correct in shape* but its FIRST bucket is mislabeled. **Berserker is NOT structurally-vestigial-by-construction. It is a spec-vs-code divergence — a stale-code bug.** I authored the Berserker rule into canon last session (commit `f2fee41`, S4 § 2.3 rule 10: `close + rage + front-loaded + Axis-3B spiky → Berserker`). rocket's committed `vestigial_labels.py` does NOT contain that rule — rule 10 in code (line 189) is still the OLD pre-`f2fee41` form (`close+rage+front-loaded → Ravager`), and Berserker is hardcoded into `STRUCTURALLY_UNREACHABLE_LABELS` (line 68-69). rocket's math note says "I implement the rules VERBATIM" — but the spec rocket transcribed predates my Berserker authoring. So this corpus could not have fired Berserker no matter what it drew, because the rule isn't in the code that ran.

This does not weaken the keystone. It is exactly what a terminal gate is for: the keystone surfaced a real divergence between authored design and shipped code before it baked in. Per Matt 2026-05-27 ("stagnant vestigial logic baked into the engine across time" is the worst outcome), catching this here is the win.

**The corrected three-way adjudication:**

| Dispatch's bucket | My corrected verdict | Disposition |
|---|---|---|
| **Berserker** "structurally vestigial" | **Stale-code bug** — rule exists in canon (`f2fee41`), absent in shipped code | rocket re-syncs code to spec; re-run; THEN re-judge reachability |
| **Conduit** "structurally vestigial" | **CONFIRMED truth-to-design-around** — intentionally RETIRED, name-only by design | Keep as name-only; no rule; correct as-is |
| **Windrunner / Phantom** "bug-blocked (Axis-4 collapse)" | **CONFIRMED bug-blocked** — verdict on these MUST WAIT for the defensive-bridge fix + re-run | Defer; unjudgeable on contaminated Axis-4 |
| **Control/terrain/hybrid/Axis-1 labels** "corpus-construction" | **CONFIRMED clean** — deliberate corpus scope, not a bug | Gate-1 PASSES on these now |
| **6 fired labels** | **CONFIRMED reachable** | Clean |

**Bridge-fix recommendation (Matt ratifies):** WIRE IT, don't redesign. `defensive_vitality_scale` et al. are sound design intent with zero generation-side consumers — a missing wire, not a wrong model. Recommendation detail in Q3.

---

## Q1 — Truth-to-design-around vs. bug-blocked: the core call

### Berserker — NOT structural. Stale code. (The dispatch's load-bearing miss.)

The dispatch inherited "Berserker is structurally unreachable, vestigial-by-construction" from rocket's Item-8 report. **That was true of the code that ran, and false of the canonical design.** Verified four ways this session:

1. `vestigial_labels.py:39` — `BERSERKER = "Berserker"  # taxonomy label; NO assignment rule (structurally unreachable)`
2. `vestigial_labels.py:68-69` — Berserker hardcoded into `STRUCTURALLY_UNREACHABLE_LABELS`, asserted == `{BERSERKER, CONDUIT}`
3. `vestigial_labels.py:189` — rule 10 reads `if a1=="close" and energy=="rage" and front: return RAVAGER` — the OLD rule, no spiky test, no Berserker branch
4. `git show f2fee41` — the rule I authored: rule 10 `close AND rage AND front-loaded AND Axis-3B=spiky → Berserker` else Ravager (non-spiky) else Striker; "17 primary labels, all structurally reachable"

**Conclusion:** Berserker's unreachability in *this* report is an artifact of code lagging canon by one session. It is NOT substrate evidence about the design. My Gate-1 criterion ("substrate evidence, not bugs") classifies this squarely as a bug. **rocket must re-sync `vestigial_labels.py` rule 10 to the `f2fee41` spec, then re-run reachability.** Only the re-run tells us whether Berserker is genuinely rare (a real substrate finding) or healthy — and that re-run also needs Axis-3B, which IS measured here, so the Berserker test is *recoverable without the defensive bridge* once the rule is in code. (Note: Berserker also needs Axis-1, which is unmeasured in this corpus — see Q1 corpus-construction. So even post-sync, Berserker can't fire over THIS corpus; its real reachability test needs an Axis-1-measured corpus. Two separate gaps stack on Berserker.)

### Conduit — CONFIRMED truth-to-design-around. Keep name-only.

This one IS the intended design. I retired Conduit last session (`f2fee41`, S4 § 2.2): resource-generation as a *primary* identity is non-viable in solo-only play (no allies to feed; the Resource Conduit *proxy* survives as economy DUAL_PROXY + convergence parent). Conduit having no §2.3 rule is *correct and intentional* — it is a name in the taxonomy with no generative path, by design. This is the genuine "name-only label, no generative path" case the dispatch's Q1 asks about. **Disposition: keep as-is. No rule. Not a gap.**

This gives the clean answer to the dispatch's framing question "is name-only-with-no-generative-path the intended design, or a gap?" — **both exist, and they're different cases.** Conduit is intended name-only (retired identity, kept for taxonomy/telemetry completeness). Berserker is a gap (rule authored, code stale). The dispatch collapsed them into one bucket; they are opposites.

### Windrunner / Phantom — CONFIRMED bug-blocked. Verdict MUST WAIT.

Both gate on Axis-4 = dodger (rule 7: `wind AND dodger → Windrunner`; rule 9: `dodger AND single-target AND shadow → Phantom`). The MEASURED Axis-4 distribution is glass 94 / mitigator 2 / **dodger 0 / tank 0**. With zero dodger kits in the corpus, neither rule can fire — not because the labels are vestigial, but because the bin they gate on was annihilated by the missing-bridge collapse. **These are unjudgeable on this corpus.** Any reachability verdict on Windrunner/Phantom from this run would be reading a bug as a design fact — the precise failure my Gate-1 criterion forbids. **Disposition: DEFER both pending the defensive-bridge fix + re-run.** Phantom additionally needs single-target (Axis-2) and shadow; it is "rare-not-dead" even in a healthy corpus, so expect it to stay rare — but that's a post-fix judgment, not a now-judgment.

---

## Q2 — Is this report usable as Gate-1 substrate evidence AT ALL?

**YES — partitioned.** The report is usable for the portions NOT downstream of the contaminated Axis-4, and unusable for the portions that are. The clean/contaminated line is sharp because the missing bridge contaminates exactly one axis:

**CLEAN — Gate-1 PASSES on these now:**
- **Conduit** structurally-unreachable-by-design: confirmed independent of any axis (no rule exists; intentional). PASS.
- **Corpus-construction unreachables** (Shadowcaller, Warden, Templar, Reaver, Earthshaper, Striker, Ravager, Ranger): these are unreachable because of deliberate corpus scope — Axis-2B held all-`damage-pure` (kills control-gated rules 4/11), no hybrids (kills Reaver rule 15), no terrain skills (kills Earthshaper rule 6), and **Axis-1 entirely unmeasured** (kills rules 10/12 → Striker/Ravager/Ranger/Berserker regardless). These are corpus-design facts, not bugs and not Axis-4-contaminated. The reachability machinery correctly reports them as `empirically_unfired`. PASS — this is the report working as intended.
- **6 fired labels** (Arcanist 68, Pact-holder 12, Stormbringer 8, Invoker 6, Threshold 1, Sentinel 1): these fired on axes upstream of the contamination (proxy-family, COMPANION/MONSTER_PACT, charge-stack, element+Axis-2). Reachable, confirmed. PASS. The Arcanist 68/96 dominance is itself a clean finding worth flagging (see § Player-experience) — it's the rule-16 default catching a homogeneous mana-caster corpus, not a bug.

**CONTAMINATED — DEFER:**
- **Windrunner, Phantom** (Axis-4=dodger gated): unjudgeable, per Q1.
- **Sentinel's count is suspect** (rule 14: `Axis-4 ∈ {mitigator,tank} AND damage-pure`): fired exactly once, and only because 2 kits measured `mitigator` instead of glass. With a healthy Axis-4 distribution, Sentinel's rate would differ. So Sentinel *fired* (reachable — clean) but its *frequency* is bridge-contaminated. Reachability PASS; frequency DEFER.

**Verdict on Q2:** Gate 1 does NOT block the whole read, and does NOT pass the whole read. It **PASSES on the clean partition** (Conduit disposition, corpus-construction unreachables, the 6 fired labels' reachability) and **DEFERS the Axis-4-gated partition** (Windrunner/Phantom reachability; Sentinel/dodger-gated frequencies) pending the bridge fix + re-run. The Berserker stale-code finding is the third outcome — neither pass nor defer but **bounce-back-to-rocket** (sync code to canon).

The keystone is NOT a failed keystone. It did its job: it produced a real substrate signal (the inversion), surfaced a stale-code divergence (Berserker), and cleanly partitioned what's trustworthy from what's contaminated. A terminal gate that catches a code-lags-canon bug before it bakes in is a keystone succeeding, not failing.

---

## Q3 — Defensive-bridge fix: wire it, don't redesign

**Recommendation: WIRE `defensive_vitality_scale` (+ `shield_buffer_est`, `regen_per_sec_est`, `is_dodge_built`) into the stat allocator. Generation fix → rocket. Do NOT redesign the defensive-target model.** (Matt ratifies; this is a design-direction call.)

**Why wire, not redesign:**

1. **The model is sound; only the wire is missing.** rocket's own diagnosis (jack-ryan-corroborated): these four fields are WRITTEN into `substrate_trace` with ZERO generation-side consumers. The design intent — defensive target should drive defensive stats — is correct. The defect is a disconnected wire, not a wrong circuit. Redesigning a model whose only fault is that nobody reads it would be discarding good work to fix a plumbing gap.

2. **The inversion proves the wire's absence is the whole story.** jack-ryan independently reproduced: simulated vitality is driven entirely by energy/element priors (rage>mana, physical>lightning), fully decoupled from the defensive label. Glass-target kits drew high-vitality energies → measured tankiest (+16% raw HP). Wire `defensive_vitality_scale` (1.8 tank → 0.55 glass) into the allocator and the +16% glass HP advantage inverts toward the intended ordering. This is ONE fix for BOTH the collapse and the inversion — the dispatch is right that it's a single root cause.

3. **Genre precedent says the model is the right one.** Every mature ARPG ties a defensive archetype to actual defensive stats: D2 Barbarian's BO+Iron Skin is real eHP, not a cosmetic label; PoE Juggernaut vs. Trickster are mechanically different survivability models; D4 Werebear-Druid genuinely eats hits. A defensive-target field that doesn't move defensive stats is the cosmetic-archetype anti-pattern (think early D3 where "tanky" was a tooltip, not a build). The fix restores the genre's defensive-identity contract.

**The fix scope (rocket's seam — I describe the WHAT; rocket implements the HOW):**
- Stat allocator reads `defensive_vitality_scale` and scales the HP/vitality allocation by it (the 1.8→0.55 range is the intended spread).
- `shield_buffer_est` feeds shield_pool; `regen_per_sec_est` feeds regen telemetry; `is_dodge_built` feeds avoidance allocation (this is what will repopulate the dodger bin → unblocks Windrunner/Phantom).
- jack-ryan's INFO-1 is a *guardrail on the fix, not a redirect of it*: the bridge must move eHP toward the intended ordering WITHOUT relying on "glass takes less damage" (it doesn't — glass takes the HIGHEST damage on the full 8-fight basis; the current inversion survives only because HP dominates). So the wire should differentiate eHP through HP/mitigation/avoidance allocation, and the validation criterion is the MEASURED Axis-4 distribution approaching 24/24/24/24 — NOT a damage-taken proxy.

**Sequencing (KR's call; my input):** the bridge fix is a prerequisite for re-judging Windrunner/Phantom AND for trusting Sentinel/dodger frequencies. It does NOT block the Berserker re-sync (independent) or the clean-partition PASS (already clean). So: (a) rocket re-syncs the Berserker rule [independent, cheap]; (b) rocket wires the defensive bridge [the real fix]; (c) re-run with the bridge live AND an Axis-1-measured corpus → re-judge the deferred partition + Berserker's true reachability. Items (a) and (b) can be one rocket work-unit.

**Empirical criterion that closes the deferred Gate-1 partition:** a re-run where MEASURED Axis-4 populates all four bins (target ≥ ~15/24 hit-rate per bin, not the current 0 in two bins) AND Axis-1 is measured. At that point Windrunner/Phantom/Berserker reachability becomes substrate evidence rather than bug-shadow.

---

## Q4 — Thematic / player-experience stakes

**The defensive archetype labels are currently cosmetic, and that is a player-facing coherence failure of the exact kind the genre punishes.** Flagging the stakes plainly:

1. **"Glass is tankiest" breaks the build-identity contract.** In any ARPG, a player who builds glass-cannon accepts a deal: massive damage, paper defense, die-if-touched. That fragility is the *point* — it's the risk that makes the burst feel earned (D2 hardcore summoner glass-cannons, PoE no-defense pure-damage). If the engine generates a "glass" kit that is secretly the tankiest thing in the corpus, the deal is a lie. The player's mental model of their own build is wrong. This is worse than imbalance — it's incoherence. A player can adapt to a strong build; they cannot adapt to a build that does the opposite of what its identity promises.

2. **The defensive axis is one of the four pillars of build feel.** Axis-4 (tank/mitigator/dodger/glass) is how a build *survives* — and survival style is half of how an ARPG build feels to pilot. A dodge-roll Rogue (D4) plays nothing like a Werebear (D4) even at identical clear speed, because the moment-to-moment defensive texture differs. With the bridge absent, every kit collapses to one defensive texture (glass-by-label, tank-by-accident) — the build-variety the whole BC system exists to deliver is invisible on this axis. The keystone measuring this is what made the failure legible; that's the keystone earning its place.

3. **Why this is a "design around the right thing" caution, per jack-ryan INFO-1.** It would be tempting to read "glass takes lowest damage (on physical)" as a feature and lean into it. Do not. On the full 8-fight basis glass takes the HIGHEST damage; the survivability is pure HP-bloat, and HP-bloat-as-defense is the least interesting defensive model in the genre (it's why D3 launch toughness felt flat — eHP without active mitigation/avoidance texture is a number, not a playstyle). The fix should restore *differentiated* defensive textures (mitigation, avoidance, true tankiness), not entrench undifferentiated HP.

4. **The Arcanist 68/96 dominance is a separate, clean coherence flag.** Two-thirds of the corpus defaulted to Arcanist (rule-16 catch-all). On a homogeneous mana-caster corpus this is expected, but it foreshadows a real risk for production: if the live game's kit distribution skews mana-caster, the player sees "Arcanist, Arcanist, Arcanist" and the 17-label identity system reads as theater. This is NOT bridge-related and NOT a Gate-1 blocker — it's a corpus-diversity flag for the eventual production-distribution gate (the Session-5 hypothesis tests). Logging it here so it isn't lost: **identity-label diversity needs a corpus that exercises non-caster archetypes**, which is the same Axis-1-measured, defensive-bridge-live corpus the deferred partition needs. Three reasons now point at the same re-run.

---

## DISPOSITION SUMMARY (for KR + Matt)

- **Gate 1 verdict: PASS-ON-CLEAN / DEFER-CONTAMINATED / BOUNCE-BERSERKER.**
- **PASS now:** Conduit (intended name-only — keep as-is); corpus-construction unreachables (deliberate scope); 6 fired labels' reachability. The clean partition is trustworthy Gate-1 substrate evidence.
- **DEFER:** Windrunner + Phantom reachability; Sentinel/dodger-gated frequencies. Gated on defensive-bridge fix + re-run. Do NOT judge these on contaminated Axis-4.
- **BOUNCE to rocket:** Berserker — stale-code divergence (rule authored `f2fee41`, absent in shipped `vestigial_labels.py`). Re-sync rule 10 to canon. NOT a vestigial finding.
- **Bridge fix:** WIRE `defensive_vitality_scale` et al. into the stat allocator (rocket's seam; generation fix). Do NOT redesign the model. Matt ratifies the direction.
- **Re-run criterion that closes the deferred partition:** MEASURED Axis-4 populates all four bins + Axis-1 measured. Same re-run also tests Berserker's true reachability and corpus-identity-diversity. Three deferred questions, one re-run.
- **Player-experience stakes:** glass-as-tankiest breaks the build-identity contract; defensive labels are currently cosmetic; fix must restore differentiated defensive texture (not entrench HP-bloat). Flagged, not blocking.

The keystone delivered. It produced a real inversion signal, surfaced a stale-code bug, and cleanly told us what to trust and what to re-run. That is a terminal gate doing exactly what it's for.

---

**Author:** gandalf, 2026-06-13. Gate 1 — BC-keystone vestigial reachability. Pattern A-deep terminal gate. Reported to KR; not pushed (Matt's keystone-close gate). Framing-audit caught the Berserker stale-code divergence (OP § 3.7 Q1/Q2) — the load-bearing correction to the dispatch's framing.
