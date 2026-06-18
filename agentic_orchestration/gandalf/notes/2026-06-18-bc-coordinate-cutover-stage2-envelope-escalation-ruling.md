# gandalf ruling — BC-coordinate cutover Stage-2 WARN-1a envelope escalation + A1 re-confirm

**STATUS:** RULED — **ACCEPT** the `damage_long_collapse` over-wide envelope; **A1 RE-CONFIRMED** (earth_caster case=2). Clears the gandalf design gate on BC-coordinate cutover **Stage-2 Unit-2+**. Decisions-log ratification routes Matt-approve → KR-draft → jack-ryan-review. jack-ryan Gate-2 on the implementation is a separate downstream gate; Stage-3 (prove-then-delete of the legacy archetype tables) becomes gated-but-unblocked.
**Date:** 2026-06-18
**Author:** gandalf (story-and-design steward)
**Resolves:** the WARN-1a escalation (`escalate=True`) in `reincarnated-engine/output/stage-2-bc-keying-equivalence-2026-06-14.txt` L25, routed to gandalf per the math note §3.1.1 step 3 ("over-wide collapse → fresh gandalf gate"); AND the §3.2.1 forward-guard ("gandalf re-confirms A1 against this artifact at the implementation gate", math note L186).
**Method discipline:** ruled against the ARTIFACT, not the survey summary. Read the equivalence table + the §3.1.1 WARN-1a definition + the §3.2.1 A1 verdict directly; the per-archetype gate data flips the escalation from "looks alarming (24% spread)" to "clean-accept (the spread is element-intrinsic, exactly preserved)."
**Companions:**
- `reincarnated-engine/output/stage-2-bc-keying-equivalence-2026-06-14.txt` — the milestone gate artifact (N=1120/arm/archetype). The escalated envelope block is L24-25.
- `reincarnated-engine/src/reincarnated/simulation/math/bc-coordinate-cutover-stage-2-ai-bin-keying-2026-06-14.md` — §3.1.1 (WARN-1a envelope cap), §3.2.1 (A1 verdict + forward-guard), §4 (tri-state demote-not-delete).
- `canonical/37-form-bias-diagnosis-and-recovery.md` — the form-bias pathology this ruling's A1 half is an instrument-level cure of.

---

## 0. The ruling in one line

**ACCEPT the collapse.** The over-wide `damage_long_collapse` envelope (water/earth/holy/shadow spanning **W_ttk=24.42%** under legacy) is **element-intrinsic flavor spread that the cutover preserves EXACTLY** — proven by all four archetypes passing the per-archetype gate at `wr_d=0.00 / ttk_d=0.00 / rf_L1=0.000`. It is NOT ordering-driven differentiation that the bin-collapse would flatten. The WARN-1a "envelope-laundering" hole is **not triggered**, because preservation here rests on exact per-archetype equality, not on a within-the-envelope band claim.

## 1. What the escalation actually is (and why the headline 24% is not the danger it looks)

WARN-1a (math note §3.1.1) caps the **legacy intra-group envelope width** at the per-archetype tolerance band (W_wr ≤ 3pp, W_ttk ≤ 5%, W_rf L1 ≤ 0.10). The hole it closes: if a collapse group's preservation claim is only "the bin ordering's outcome lands *within the envelope* spanned by the member legacy outcomes," then a WIDE legacy envelope makes that band so loose a genuinely mis-piloted ordering trivially passes — the dispersed baseline launders a regression.

The artifact escalates `damage_long_collapse ['water','earth','holy','shadow']` because `W_ttk=24.42% > 5%` cap (and `W_wr=3.84pp > 3pp`, `W_rf=0.254 > 0.10`). Mechanically `escalate=True`. By design that routes to me — NOT to auto-pass.

**But the danger the hole guards against requires the per-archetype gate to be failing or unmeasured. It is neither.** The same artifact shows every one of water / earth / holy / shadow **individually** at:

```
water_mage     0.00  0.00  0.000  PASS
earth_caster   0.00  0.00  0.000  PASS   (case=2(accept); control_freq_label_keyed=0.0000)
holy_caster    0.00  0.00  0.000  PASS
shadow_mage    0.00  0.00  0.000  PASS
```

The bin-keyed pilot reproduces each archetype's legacy fight **byte-identically** — the *strongest* form of preservation, not the within-envelope *weak* form. There is no laundering: each archetype is independently certified at delta=0.

## 2. Why the wide envelope is benign — the load-bearing logic

A single canonical bc role-priority ordering `O` is what all four "damage_long" archetypes collapse onto. The per-archetype gate proves `O` piloting each archetype reproduces its legacy outcome at delta=0:

- `O` ∘ water → legacy_water (exact)
- `O` ∘ earth → legacy_earth (exact)
- `O` ∘ holy → legacy_holy (exact)
- `O` ∘ shadow → legacy_shadow (exact)

The four legacy outcomes differ by 24.42% TTK. But **the same ordering `O` produces all four.** Therefore the 24.42% spread **cannot be attributed to the ordering** (the ordering is constant across all four) — it is driven entirely by the per-kit factors the cutover leaves untouched: **element** (water/earth/holy/shadow → different damage types, resistance interactions, DoT-vs-burst profiles), base stats, and skill composition. The collapse unifies only the role-priority keying source; it does not touch element or skills. So the spread **survives the collapse intact** (arm B still spans 24.42%, matching arm A), and it survives because it is exactly the differentiation we WANT.

**Genre anchor (the distinction made concrete):** this is the Diablo/PoE principle that a Fireball and a Frostbolt fired on the *same* "cast-on-cooldown" priority still feel completely different — the element carries the feel (burn DoT vs chill/freeze/shatter), not the cast logic. Homogenizing the cast-priority does not homogenize the spells as long as the elements differ. The 24% TTK spread is holy-smite vs shadow-DoT vs water-chill vs earth-crush doing their genuinely distinct things; collapsing the AI ordering they share leaves that element-flavor untouched. Flattening would require the spread to live in the ordering. It does not.

## 3. The A1 re-confirm (the second half of this gate)

§3.2.1 requires gandalf re-confirm the earth_caster A1 verdict against this artifact. The artifact row 9 carries `case=2(accept); control_freq_label_keyed=0.0000` — **exactly** the A1 prediction: earth_caster's legacy label LED with `control`, but its `area_damage` composition produces zero control skills, so control fires at frequency **exactly 0.0** under both pilots. Dropping the never-honored control-lead is behavior-identical (`ttk_d=0.00`), not a regression. **A1 RE-CONFIRMED.**

This composes with the form-bias diagnosis (doc 37): the flat `earth_caster` label asserted a control identity the composed mechanics never delivered — the form-bias pathology itself. The coordinate correctly carries only what the kit *does*, not what the label *claimed*. The cutover is the form-bias cure applied at the AI instrument: aspirational-label text is dropped; real mechanical behavior is preserved exact. **This is a reason to accept, not a reason to hold.**

## 4. Framing-audit (OP §4.1) — clearing my own ruling

- **Q1 (load-bearing assumption):** "per-archetype delta=0.00 ⟹ envelope spread is element-intrinsic, not ordering-driven." Logically tight: one ordering reproducing four distinct outcomes exactly means the outcomes' mutual differences are non-ordering-attributable.
- **Q2 (refuting evidence in scope):** Could the 0.00 deltas be a dead harness (not exercising the difference)? No — WARN-1b (§3.1.2) powers the gate at N≈1120/arm/archetype against a *boss-tier* panel chosen precisely because standard/elite opponents die to opening burst (0 incoming → eHP/role-frequency unmeasurable). Boss-tier is the panel that DOES exercise TTK + role-firing-frequency. The 0.00 is resolved above the binomial noise floor (±3pp half-width at N≈1120), not a sampling artifact. No refutation in scope.
- **Q3 (refine rather than execute):** No refinement — the evidence is dispositive both ways (envelope benign; A1 confirmed). Clean-accept.

## 5. What this unblocks — and what it explicitly does NOT

**UNBLOCKS:**
- The **gandalf design gate** on BC-coordinate cutover **Stage-2 Unit-2+** clears. (Per MIGRATION v1.70 the implementation — `CombatantState.bc_target`, propagation, `bc_target_role_priority()`, tri-state routing — is already landed; this ruling removes the gandalf hold on certifying it.)
- **Stage-3** (prove-then-delete of `ARCHETYPE_ROLE_PRIORITY` / `_PLAYER_CONTROLLER_ARCHETYPES` / `ARCHETYPE_TEMPLATES` / `legacy_archetype_shim`) becomes **gated-but-unblocked** — its own future gate, no longer waiting on this design question.

**DOES NOT unblock / still gated:**
- **jack-ryan Gate-2 on the implementation** — separate gate (the math note §3.3 INFO-4 commits the table as the Gate-2 evidence; the JSON companion `output/stage-2-bc-keying-equivalence-2026-06-14.json` is the on-disk artifact). My design gate ≠ jack-ryan's QA gate.
- **Stage-3 deletion itself** — prove-then-delete is a deliberate separate step (math note §4 L208); this ruling does not fire it, it only removes the design blocker in front of it.
- The **tri-state must NOT collapse** — FALLBACK (legacy physical / pre-cutover kits ride `ARCHETYPE_ROLE_PRIORITY` unchanged) + LOUD-DEFAULT survive per §4 (Disc #12 / Disc #39). Nothing here authorizes deleting the tables before Stage-3's own gate.

## 6. Routing + sign-off

**gandalf design gate: ACCEPT (envelope) + CONFIRMED (A1).** Decisions-log ratification of the Stage-2 cutover (semantic-shift per Disc #12: bc_target-present kits re-key from `ARCHETYPE_ROLE_PRIORITY[label]` to bin-derivation, §3-proven behavior-equivalent) routes the standard path: gandalf recommends → Matt approves → knight-rider drafts → jack-ryan reviews. jack-ryan owns the Gate-2 on the implementation independently.

**Recognition → validate → commit honored:** the empirical criterion that gated this ruling was the milestone equivalence artifact (already on disk, N≈1120/arm/archetype, powered above noise) — read directly, which is what flipped the framing from "24% spread is alarming" to "24% spread is element-flavor, exactly preserved." No code change from this ruling (the implementation is already landed behind its gate); the ruling releases the gandalf hold.

**Signed:** gandalf (story-and-design steward), 2026-06-18.
