# KR sequencing record — Path B 1c is a THREE-STRAND coupled calibration (elemental resist ↔ physical recal ↔ proxy army-soak)

**Author:** knight-rider (orchestration). **Status:** durable sequencing record — captured so the coupled calibrations are NOT authored or scheduled as independent dispatches in any future session. **Triggers:** gandalf cross-thread recognition `2026-06-22-path-b-defensive-axis-homogenization-reconciliation.md` (commit `2543222`) established the 2-axis compound; gandalf proxy-W3 tee-up `2026-06-22-proxy-w3-encounter-model-teeup.md` (commit `e80696b`) added the third strand.

## The coupling (the fact this record exists to preserve)

**Three defensive demands now converge on the same 1c Gate-2 test**, all feeding off (or bypassing) the same post-1a sim Loadout + gear budget:

1. **Path B Step 1c** — budget recalibration of the **elemental** defensive axis (resist, ~9 gear slots). Gated on 1a + 1b. (spec `2026-06-22-path-b-resist-design-spec.md` §15)
2. **Defensive-axis recal wave** — `MOB_DAMAGE_SCALE` 0.40→4.0 + armor/HP, the **physical/general** defensive axis. Matt-ruled (B) "death is a core pillar"; currently **Matt-gated**, not yet authorized as its own workstream. (diagnose `simulation/math/defensive-axis-calibration-diagnose-2026-06-21.md`, jack-ryan Gate-2 PASS-WITH-INFO)
3. **Proxy-W3 army-soak** — the summoner's minion-wall as a defensive LAYER. **This is the structurally-different strand:** strands 1 and 2 are bought with the **same currency offense is** (gear slots) so they COMPETE with offense (the costed trade that makes §11.3(b) a *good* property). The army is bought with a **non-gear currency** (summon-allocation / trait / T4) so it does NOT compete with the gear budget — it can substitute for BOTH personal axes (resist + armor) at zero gear cost. That inverts the guard: it leaks from the **optional-bypass** direction (a free defense one archetype gets to skip the costed game with), not the **mandatory-tax** direction §11.3 was written against. Proxy-W3 SIM wave is itself **Matt-gated** + needs jack-ryan DESIGN-MODE Gate-1 before build; gandalf's SHAPE ruling (army = costed layer, NOT free substitute) is pre-framed (`e80696b` §4) and fires when gamora's calibration evidence lands.

Strands 1 and 2 are **separate axes** (spec §14: `armor/(armor+3000)` ≠ the resist dict — separateness is good for build space); strand 3 is a non-gear bypass of both. The §11.3 homogenization guard was validated by gamora **on the physical axis alone** — it has NOT been validated on the **compound** (elemental + physical), let alone the **triple** (+ army-soak).

## The four obligations that now land at ONE 1c Gate-2

The 1c Gate-2 test is the convergence point for all four (gandalf-owned shapes; gamora's numbers; jack-ryan ratifies):
- **§11.3 reconciliation** — Path B guard-compliant by construction (RATIFIED; calibration-conditional on §13.4).
- **§13.4 / CONCERN-2** — the three elemental shapes (uniform / concentrated / full-cap) viable + non-dominant.
- **§5 compound obligation** — no (resist-floor, armor/HP-floor) pair strictly mandatory; offense-substitution holds against the SUMMED elemental+physical demand.
- **Proxy third-axis read (NEW, `e80696b` §5)** — a proxy kit buying **zero personal resist + zero personal armor** must survive the boss at **glass-cannon variance (~0.6–0.8), NOT bruiser-safety (~0.95+)**, and must die in the resummon gap. If it survives at bruiser-safety with no personal defense, the wall is a free bypass (clause-1/2 violation) → recalibrate (lower `base_hp` / `proxy_max_active`, lengthen the exposure gap). The four W3 SCAFFOLD magnitudes map to clauses: `base_hp` + `proxy_max_active` → does the slam evaporate the wall (good) or hold (leak); `attack_interval_s` → is the exposure gap real; `damage_multiplier` → does the army double as the kill-speed answer (worst case).

## Why they cannot be calibrated independently

The risk is a **compound defensive tax neither axis exhibits alone**: each individually satisfies §11.3 (offense substitutes; no single mandatory floor), yet *summed* they can force the player to cap resist AND hit the armor/HP threshold before any offense is affordable. At that point §11.3(b) (offense-substitution) fails on the compound — the build screen becomes a checklist (the D4-launch one-shot-meta / PoE "mandatory defensive layers" creep). Calibrating 1c and the recal independently is precisely how that slips in.

## The two clean options (gandalf §4 — KR routes the choice to Matt; calibration is gamora's, ratify is jack-ryan's)

- **(A) Co-calibrate — both stewards' lean, 3-strand-reinforced.** Run Step 1c + the defensive-axis recal (+ the proxy army-soak when its W3 evidence is in) as ONE joint calibration against the compound guard. One validation over the real (elemental + physical + army) surface. B's window-of-incompleteness widens with each added strand.
- **(B) Sequence with the compound guard as an explicit entry condition on each subsequent strand.** Whichever calibrates later must hold the compound criterion against the prior's locked values, not just its own axis.

## Binding constraints on whoever authors these dispatches (KR-self / future session)

1. **Do NOT author Step 1c, the defensive-axis recal, and the proxy-W3 caster-threat calibration as independent calibration dispatches.** They are one coupled (3-strand) calibration problem.
2. The **compound proof obligation** (gandalf §5, extends Path B §13 + defensive-axis §11.3) is an explicit 1c/recal Gate-2 acceptance criterion: *no (resist-floor, armor/HP-floor) pair is strictly mandatory; offense-substitution holds against the **summed** defensive demand; the viable-build set includes kits that under-invest in ONE axis and compensate via offense or the other axis (glass viable; tank the opposite extreme; the spread is now a 3-way build space, not 2-way).* Numeric thresholds are gamora's; jack-ryan ratifies.
3. **Independence elsewhere holds:** the coupling binds ONLY at the calibration step. Path B Step 1a (sim Loadout widening) and 1b (breadth-affix mint) are unaffected — they build machinery; the compound guard binds only when the numbers are set. So 1a/1b proceed on the existing sequence; the coupling is a 1c-and-later concern.

## What the 1c dispatch MUST close (jack-ryan Gate-1 addendum, registered into 1c Gate-2 acceptance)

jack-ryan ratified §2 (RECONCILIATION RATIFIED) and registered §5 as GATE-ABLE, with three specification items the 1c dispatch must pin (same posture as the §13.4 delegation — numbers are gamora's, shape is gate-able):

1. **The 2-axis reference-corner set is undefined and must be enumerated.** §13.4 names three *elemental* shapes; the compound obligation implies a 2-axis grid but does not pin the kit corners. Minimally: {glass-both, tank-both, resist-heavy/armor-light, armor-heavy/resist-light, ≥1 offense-compensating mid}. gamora proposes the corner set; jack-ryan ratifies it populates the 3-way space. Without it, "viable set includes single-axis-under-investing kits" is not testable.
2. **The dominance margin Y must extend to the compound, or a distinct compound-Y defined**, and the 1c dispatch must state *which composite* (e.g. survive-rate × clear-time over the 2-axis sweep) Y is measured on — so it isn't silently inherited from the per-axis §13.4 Y.
3. **"Strictly mandatory pair" needs an operational definition that reuses the existing survive+kill bar** (§13.1/§13.3), NOT a new threshold: a (resist-floor, armor-floor) pair is "strictly mandatory" iff no kit omitting either floor clears survive+kill against the non-counter enum portion. Keeps the compound from introducing a fourth distinct number.

## Routing status

- **Gate-1 fold (gandalf):** §13.5 cross-reference + compound proof obligation #5 folded into Path B spec — **DONE** (commit `7901379`).
- **Gate-1 record (jack-ryan):** §2 RATIFIED as the answer to the §11.3 objection (one INFO: compliance is calibration-conditional via §13.4 — correctly routed to the same 1c Gate-2, not a residual); §5 compound obligation GATE-ABLE, three specification items above carried into 1c Gate-2 acceptance. **DONE.**
- **Proxy-W3 third strand (gandalf `e80696b`):** folded — the proxy caster-threat read cannot be set in isolation; the army-soak can bypass both gear-axes, so calibrating it against a caster *assumed* to carry resist+armor (when the dominant proxy build skips both) sets the army knob against a fiction. Extends the coupling to a triple; converges at the same 1c Gate-2.
- **Steward lean (both): co-calibrate (option A), now 3-strand-reinforced.** Matt's framing: B (sequence-with-entry-condition) leaves a window where a value passed a per-axis guard but never the compound — the exact crack the compound tax slips through, and it **widens with three strands**. A (one joint validation over the real elemental+physical+army surface) absorbs the third strand cleanly. jack-ryan's QA observation concurs: option B Gate-2-PASSes the first calibration against a guard validated only per-axis. **Record the lean; the formal bind stays at 1c-authoring with 1a+1b outputs in hand — do NOT lock the calibration structure ahead of the post-1b surface.**
- **Matt decision (open):** option (A) co-calibrate vs (B) sequence-with-entry-condition, now a 3-strand question. Non-blocking now (binds at 1c, downstream of 1a+1b; doesn't gate kickoff); recorded so it is resolved at 1c-authoring. The defensive-axis recal wave's Matt-gate AND the proxy-W3 wave's Matt-gate are now entangled with Path B 1c — authorizing any one implicates the calibration structure of all three.
