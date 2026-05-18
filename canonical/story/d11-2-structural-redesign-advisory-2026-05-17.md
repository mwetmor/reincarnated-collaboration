# D11.2 Structural Redesign Advisory — hybrid_mage floor-pin escape

> *[RETIRE outcome triggered — RETIRE clause per § 6 of this advisory is ACTIVATED per Matt L3 verdict 2026-05-18. hybrid_mage RETIRED from canonical-7; canonical-6 transition complete. This advisory is historical record of the lever-shape work that preceded the retire verdict. See `canonical/story/canonical-6-transition-retire-hybrid-mage-2026-05-18.md` for full context. See `reincarnated-engine/design/decisions/decisions-log.md` for the RETIRE entry.]*

**Author:** gandalf (story-and-design steward).
**Authority:** Matt L3 2026-05-17 late evening — "Authorize D11.2." Explicit structural-redesign authorization per dispatch `2026-05-17-gandalf-d11-2-structural-redesign-advisory.md`. Early-stop / RETIRE authority still granted; this advisory may surface RETIRE as the verdict if no lever in {A,B,C,D,E} can produce a design-coherent converging chromatic_mage.
**Predecessors:**
- Own D11 advisory (`canonical/story/d11-hybrid-mage-tuning-advisory-2026-05-17.md`) — original genre survey + identity intent (1,200+ lines)
- Own D11 post-mortem (`canonical/story/d11-postmortem-option-b-verdict-2026-05-17.md`) — STOP verdict; Option C-prime proposal; first self-critique
- Gamora D11 math note v1.6 (`output/.../D11-hybrid-mage-tuning-math-note-2026-05-17.md`) — original tax design
- Gamora D11.1 math note v1.7 (`output/.../D11.1-ceiling-primary-tuning-math-note-2026-05-17.md`) — ceiling primary + α nudge
- Rocket D11.1 completion record (dispatch `2026-05-17-rocket-d11-1-ceiling-primary-implementation-queued.md` § Phase B/C) — 0/17; "all dropped skills had dps_score=0.0"
- Live empirical: `d11_salvage_summary.json`, `d11_1_salvage_summary.json`, 17 hybrid_mage class JSONs

**Type:** Pattern B structural-design advisory; ~1 day; tighter than D11 advisory because the empirical lock is in place.

---

## § 0 — Verdict TL;DR

**RECOMMENDED LEVER: B — Direct DPS-density cap on the hybrid_mage kit, applied at kit-finalization as a hard reduction of `damage_multiplier` across damage-bearing skills until the kit's aggregate effective DPS (modifier=1.0, full kit, against a reference monster HP/AC profile) falls under a tunable ceiling.**

**Magnitude:** I do not assign α this time. The empirical signal is that *the right magnitude must be derived from the smoke gate, not from prior analogy.* My recommendation is the *lever shape*; the lever's strength is set by the Discipline #17 (proposed) smoke gate (§ 5). I will give an empirical *anchor band* (§ 3, § 4) to scope the smoke's parameter range: roughly a 25–45% kit-aggregate DPS-density reduction is the mathematically-indicated band, derived in § 4.3 from the empirical WR-elasticity-to-damage relationship measured across D11 + D11.1.

**Secondary lever (composite): D — Orthogonal HP/CD penalty on hybrid_mage (lightweight; carry-cost ≈ 30 min engineering), applied at modest magnitude (~+5% incoming damage taken, OR -5% base HP) to give the balance-loop a second axis of WR-elasticity that doesn't depend on kit DPS reduction.** D is recommended only if the smoke shows that B alone produces brittle convergence (one-knob tuning sensitivity > 0.10 WR per 5% B-magnitude change). Otherwise, B alone.

**Why not A (prune damage-bearing skills):** identity-destroying. Rocket's smoking gun shows the dropped skills under D11.1's pruning rule were utility/sustain/DoT — non-damage roles. Extending pruning into damage-bearing roles would tear out the things the player actually presses. PoE/D2/D4 never punish breadth by removing damage skills; they punish via power-investment. A is the wrong lever-class.

**Why not C (gen-time damage-skill quota):** addresses *future* regens only; cannot salvage the 17 existing instances without re-curation. Engineering complexity does not warrant the deferred payoff. C remains worth considering as a *follow-on* policy after B lands, codifying the lesson at generation time so the hybrid_mage substrate stops producing 7-8-damage-bearing-skill kits in the first place. But D11.2's primary lever cannot be C, because D11.2 must salvage the existing 17.

**Why not E (engine-sim rework for element-coverage resistance):** the smoking gun *refuted* the coverage-redundancy hypothesis (your D11 post-mortem WARN 3 was empirically wrong; two n=2 untaxed instances also floor-pin; rocket's pruning showed dropped skills were dps_score=0.0 non-damage roles). Building an engine-simulation feature to attack a mechanism we now have empirical evidence is not the real failure mode would be ~3-5 days of HIGH-engineering work targeting a hypothesis the data has refuted. Reject.

**Why NOT RETIRE (yet):** Lever B has a clear engineering path, a clear identity story (§ 6: chromatic_mage feels like "elementalist with magnitude restraint" — closer to LE Runemaster's per-element-modesty than to D2 specialist-sorcerer power-fantasy, but still recognizably elementalist), and an empirical anchor band that maps cleanly to the WR-elasticity data. The Discipline #17 smoke gate (10–15 min sim cost) confirms or refutes within one day. RETIRE remains the surfaced fallback (§ 7); if the B-smoke fails at the upper bound of the anchor band, I will surface RETIRE in the smoke completion record and ask Matt to make the (ii) call on L3 #42.

**Handoff to knight-rider:** **FIRE gamora D11.2 math note with lever B embedded + smoke-gate (Discipline #17) as mandatory Phase A gate before any full-salvage Phase B fires.** Smoke parameters specified in § 5.

---

## § 1 — Sub-Q 1: self-critique — why did 3 mental models fail in sequence?

This is the durable lesson; it lands regardless of D11.2's outcome.

### § 1.1 — Three failures, one shape

**Failure 1 (D11 advisory, α=0.07 from D2 split-Sorceress analogy):** I anchored magnitude against a *design-feel* benchmark (the empirical WR penalty D2 imposes on split-element Sorceresses, ~40–50% effective DPS) and then back-scaled it (4× quadratic backoff to 7% because Reincarnated's hybrid_mage is intended-playable). The advisory's genre survey was rich and durable; the magnitude was assigned by analogy to a system whose balance-loop function shape is not Reincarnated's.

**Failure 2 (D11 post-mortem WARN 3, gauntlet resistance-immunity-coverage):** Having seen α=0.07 produce 6% convergence, I diagnosed the failure as a *coverage* mechanism — the kit has too many element-tagged slots, the gauntlet has resistance profiles per element-slot, breadth = combinatorial coverage = floor-pin. The hypothesis felt right because it matched both the genre framing (D2/PoE punish breadth) and the engine intuition (more skills = more options). It was not measured against engine-sim behavior. Rocket's D11.1 result refuted it surgically: the pruned skills were dps_score=0.0 non-damage roles; pruning them produced 0% WR change. Coverage redundancy is not the live mechanism.

**Failure 3 (D11.1 ceiling=10 primary lever):** The post-mortem's Option C-prime proposed ceiling=10 as the structural lever, with α demoted to thematic-flavor. The math note ran the numbers and projected 1–2/17 convergence under conservative assumptions, 3–6 under optimistic — both well below the ≥12/17 gate. The gate was missed at 0/17. The failure mode here is more subtle: the math note's *projection* was honest about the likely miss; the structural defect was that *the lever and the failure mechanism were mis-targeted relative to each other*. Ceiling=10 reduces *skill count*; the live failure mechanism is *aggregate damage-bearing-skill DPS density*. These are correlated under random generation (more skills → typically more damage-bearing skills) but the correlation is not 1:1 — and when pruning protects non-damage roles (correctly! it should!), the correlation collapses to zero at the ceiling-application site. Ceiling is the wrong knob *for this specific pruning protection policy* because pruning's protection policy deliberately holds damage-bearing skills constant.

### § 1.2 — The common failure mode

The three failures share one shape: **I reasoned about the lever's *type* using genre-design-feel analogies (D2 split-Sorceress, gauntlet resistance, Immortal-style capacity cap), and used that type-reasoning to also assign *magnitude* and *site of operation*.** Genre analogies legitimately constrain lever *type* — they tell you what kinds of constraints are recognizable to the player as breadth-tax. They do not tell you what *magnitude* moves a specific engine's specific balance-loop function from floor-pin to interior convergence, nor at what *site of operation* the engine's actual failure mechanism lives.

In all three cases I conflated:
- *What feels right to the player* (a coherent breadth-tax shape) with
- *What moves the engine's WR-at-floor metric below 0.50* (a quantitative math problem on a specific empirical surface)

These are different questions. They want different methodologies. Genre design-feel is solved by survey + thematic synthesis. Engine WR-at-floor is solved by empirical measurement against the actual balance-loop function, ideally with ablation.

The deeper miss is that I never wrote down the engine's balance-loop function explicitly before recommending a lever. The function is roughly: `WR_at_floor(kit) = f(DPS_density, monster_HP, fight_duration_nonlinearity, role_composition)`. With the floor modifier fixed at 0.05, the only knobs we control are kit-side: DPS density, kit composition. The function is non-linear, asymptotic at the floor, and *not* obviously elastic to skill count when skill count proxies damage-bearing-skill count imperfectly. Once you write the function down, the lever question becomes: *which knob moves the function's output below 0.50, given the empirical sensitivity?* That's not a genre question. It's an empirical sensitivity-analysis question.

### § 1.3 — What I am doing differently in D11.2

Four operational changes:

1. **Empirical anchor before lever recommendation.** § 3 below derives the WR-elasticity-to-damage from D11 + D11.1 data directly. The recommendation in § 0 references this anchor band, not a genre analogue.
2. **No magnitude assignment in the advisory.** I am specifying lever *shape* (B = direct DPS-density cap) and lever *anchor band* (~25–45%, derived empirically). The actual α / cap-value is set by the Discipline #17 smoke gate. The advisory hands the magnitude question to the empirical sweep, where it belongs.
3. **Smoke gate as mandatory Phase A.** Per § 5: 3-point parametric sweep on 5 representative instances before full 17-instance salvage. 10–15 min sim cost. Protects against another implement→miss→escalate cycle.
4. **Explicit RETIRE clause with empirical trigger.** Per § 7: if the B-smoke at the upper bound of the anchor band (~45%) cannot produce ≥3/5 interior convergence on the smoke set, I surface RETIRE without further levers. The retire trigger is empirically defined, not a vague "if it doesn't work."

The genre-survey work from D11 advisory is not wasted. It correctly constrained lever-type space (we are looking for a power-investment / magnitude-restraint lever; we are not looking for a capacity cap or a coverage rework). It also correctly identified that chromatic_mage's identity reads through *some* form of breadth-cost expression. § 6 picks up that thread and asks whether B preserves the identity. The genre work belongs in identity preservation (§ 6), not in magnitude assignment.

This is the durable shape of Discipline #17 I'm proposing in § 5.

---

## § 2 — Sub-Q 2: lever evaluation, A–E, empirically anchored

I evaluate each lever against four criteria, anchored in the d11/d11.1 salvage data:

1. **DPS-density effect** (does the lever actually move the kit's aggregate damage-bearing output?)
2. **Mode-A coverage** (does it help n=11–12 floor-pinned instances?)
3. **Mode-B coverage** (does it help n=9–10 already-under-ceiling floor-pinned instances?)
4. **Identity impact** (does the lever preserve chromatic_mage as a recognizable elementalist archetype?)
5. **Engineering complexity + salvage feasibility** (can this be implemented and applied to the existing 17 instances, not just future regens?)

### § 2.1 — Lever A: Prune damage-bearing skills

**Description:** Extend D11.1's pruning algorithm to allow dropping damage-bearing roles (burst_damage, area_damage, primary_attack) when the kit exceeds the ceiling. Currently the pruning protection list (`_NON_DAMAGE_ROLES` per rocket's INFO-2) keeps damage-bearing skills safe and drops only utility/sustain/DoT. A would invert this: damage-bearing skills become the prune target.

**Empirical anchor.** From rocket's D11.1 finding: dropping non-damage skills produced 0% WR delta. If we instead drop damage-bearing skills, we would expect WR delta to scale approximately linearly with the dropped skills' DPS share. Looking at the role-count data across the 17 instances (§ 3.1 below): damage-bearing-skill counts range from 4 (class_0012, class_0015, class_0029, class_0061) to 8 (class_0007). Dropping the lowest 2 damage-bearing skills from a 7-damage-skill kit removes ~28% of damage-bearing slots; assuming roughly uniform per-skill DPS contribution, that's ~28% kit DPS reduction. Per the elasticity derivation in § 3.3 below, ~28% DPS reduction maps to ~14–20% WR reduction, which moves the worst-case 0.84 WR class to ~0.67 — *still floor-pinned*, but the lowest-WR class (class_0054 at 0.567) drops to ~0.45 and converges.

So A *would* work for some instances. But the instances with only 4 damage-bearing skills (class_0012 at WR 0.744, class_0015 at 0.767, class_0029 at 0.744, class_0061 at 0.689) cannot meaningfully prune damage-bearing skills further without ending up with 2 or 3 damage skills — which is below the minimum-satisfying threshold for an *elementalist* archetype. A 2-damage-skill mage is not an elementalist. It is a single-skill ranged unit.

**Mode-A coverage:** Yes (instances with 6–8 damage skills can absorb the prune).
**Mode-B coverage:** Partial (instances with 4 damage skills cannot prune without identity destruction).
**Identity:** HIGH-NEGATIVE. The dropped skills *are* the archetype's identity surface. A chromatic_mage with 3 damage-bearing skills across 3 elements has 1 damage skill per element — that is structurally indistinguishable from a 1-element specialist with two thematic gear-affixes. Per the D11 advisory's identity statement (PoE Elementalist / LE Runemaster / D4 Sorcerer mid-band lineage), an elementalist *is* the kit's wide damage surface. Drop the damage surface, drop the identity.
**Engineering:** Medium — modify pruning protection logic, re-run salvage. ~2–3 hours rocket time.
**Verdict:** REJECT as primary. The identity cost is structural, not flavor-deep.

### § 2.2 — Lever B: Direct DPS-density cap (RECOMMENDED PRIMARY)

**Description:** At kit finalization for hybrid_mage, compute the kit's aggregate effective DPS at `damage_multiplier=1.0` (or whatever the current modifier is) against a reference monster HP profile. If the aggregate exceeds a configured cap, scale all damage-bearing skills' `damage_multiplier` by a single factor `s ∈ (0, 1]` such that the post-scaled aggregate equals the cap. The scaling is applied uniformly — every damage-bearing skill takes the same fractional reduction — so the kit's *relative* skill ranking is preserved (rotation choices stay coherent), but the *absolute* DPS density drops to the configured ceiling.

**Empirical anchor.** This lever attacks DPS density directly at the kit-aggregate level — exactly the failure mechanism rocket's smoking gun identified. Whereas Lever A reduces DPS by removing skills (a step-function with identity-destructive discrete jumps), B reduces DPS continuously and uniformly. The lever has one knob (the cap value, expressed as either an absolute DPS-density target or a fractional reduction relative to baseline). Per § 3.3's empirical elasticity, a 25–35% kit DPS-density reduction maps to ~15–25% WR-at-floor reduction, which is the magnitude required to drop the WR-at-floor distribution below 0.50 for the bulk of the 17 instances.

**Mode-A coverage:** Yes — applies uniformly regardless of skill count.
**Mode-B coverage:** Yes — applies uniformly regardless of skill count; the two untaxed n=2 instances (class_0001, class_0029) also receive scaling.
**Identity:** LOW-NEGATIVE. The chromatic_mage keeps *all* its skills, keeps the full elemental coverage, keeps the rotation depth. Each skill simply hits for less damage. The thematic framing — substrate-commitment-cost, holding multiple commitments without fully expressing any one — maps cleanly to "each skill is somewhat less powerful than its single-element counterpart would be." This is the lineage of LE Runemaster (whose per-element kit is materially weaker than a single-element specialist's), and it is recognizably one of the genre's accepted mid-band archetypes. § 6 below develops this identity claim in depth.
**Engineering:** Medium. Requires:
- New `_apply_dps_density_cap()` function in `d10_kit_constraints.py` (or new module)
- Cap value sourced from `config/_tax_config.yaml` (new field; or reused with a clearer name like `dps_density_cap` since the "tax" framing no longer fits)
- Reference DPS-density target computation: pick a non-hybrid_mage archetype's median DPS-density at the same player level as the empirical anchor (e.g., the controller_mage median); cap hybrid_mage to ~0.65–0.75× that anchor. Alternatively, the cap can be specified as a multiplicative reduction (`hybrid_mage_dps_density_scale = 0.65`) and applied uniformly. The latter is simpler and more directly tunable; gamora math note picks the form.
- Provenance fields on per-class JSON (`balance_metadata.dps_density_cap`, `dps_density_scale_factor_applied`)
- Salvage path: re-process 17 instances; compute current kit-DPS; scale to target; re-run balance loop.

Total engineering: ~4 hours rocket, ~2 hours gamora math note. Compare to D11.0 (3 hours) and D11.1 (2 hours) — slightly heavier but well within a 1-day implementation cycle.

**Verdict:** RECOMMENDED PRIMARY. This is the lever whose mechanism matches the empirically-confirmed failure mode, whose identity impact is recoverable thematically, and whose engineering complexity is bounded.

### § 2.3 — Lever C: Generation-time damage-skill quota

**Description:** At generation time, hybrid_mage kits are constrained to produce no more than N damage-bearing skills (e.g., N=6). Skills generated beyond the quota are forced into non-damage roles or are dropped. The quota applies at the *generative* layer — future regens produce kits with at most N damage skills; existing kits must be re-curated to fit.

**Empirical anchor.** Looking at § 3.1 below: damage-bearing-skill counts are already 4–8 in the empirical set. A quota at N=6 would reduce 6 of the 17 instances (those at 7 or 8 damage skills) by removing 1–2 damage-bearing skills. Per Lever A's analysis, that's a partial DPS reduction (~14–28% on the affected subset), which would move some of the high-WR instances toward convergence — but only on the subset. The 11 instances already at ≤6 damage skills receive no relief.

**Mode-A coverage:** Partial (only the high-damage-count instances).
**Mode-B coverage:** Poor (many Mode-B instances already have ≤6 damage skills).
**Identity:** MEDIUM-NEGATIVE. At quota=6, an elementalist with 3 elements has 2 damage skills per element — still in the recognizably-elementalist band (per § 6 below, the floor is ~1.5 damage skills per element). At quota=5 or below, the identity erodes toward A's failure mode.
**Engineering:** High for salvage. The 17 existing instances were generated under the previous policy; applying C as a salvage policy requires deciding *which* damage-bearing skills to drop in over-quota instances — this is structurally identical to Lever A's pruning rule but with a different threshold. The "future generation" half of C is cleaner: a generation-time gate. The "existing-salvage" half collapses to Lever A.

**Verdict:** REJECT AS PRIMARY (heterogeneous coverage; existing-salvage path is structurally A). RECOMMENDED AS FOLLOW-ON POLICY after B lands: codify a damage-skill-count ceiling at generation time so the substrate stops producing 7-and-8-damage-skill hybrid_mages in future seasons. This is a future-regen hygiene move, not a salvage lever.

### § 2.4 — Lever D: Orthogonal HP/CD/resource penalty

**Description:** Apply a non-DPS penalty to hybrid_mage at kit finalization: e.g., reduce base HP by 5%, OR increase incoming damage by 5%, OR increase global cooldown by 10%, OR reduce resource regen by 10%. These are *orthogonal* to skill damage_multiplier — they affect WR through combatant survivability or rotation pace, not through outbound DPS.

**Empirical anchor.** I don't have direct empirical data on how WR-at-floor responds to combatant survivability adjustments. The balance loop computes WR as a fight-result aggregate over the gauntlet; reducing player HP by 5% would increase the number of fight losses driven by HP depletion (more attrition over a longer fight, especially at the modifier floor where fights are slow). Roughly, a 5% HP reduction at the floor modifier would translate to ~3–5% WR reduction — small but real, and *orthogonal to DPS*.

**Mode-A coverage:** Yes.
**Mode-B coverage:** Yes.
**Identity:** MEDIUM-NEGATIVE if used as primary. A chromatic_mage that pays for breadth by being *fragile* is a different archetype — the "glass cannon elementalist" / "casting from low HP" trope. Reincarnated has no such trope (yet); inventing one to solve a balance problem is an identity construction by accident. Reject as primary identity-shaping lever. *However:* if D is used as a *secondary* lever at small magnitude (5%) alongside B's primary scaling, the identity weight rests on B (substrate-commitment-cost; LE Runemaster lineage), and D is invisible to the player (5% HP reduction is below the perception threshold for individual fights). Magnitude matters: D at 5% is balance-loop hygiene; D at 15% is identity reshape.
**Engineering:** Low. Combatant base stats modification at kit finalization. Existing balance_loop already consumes combatant.hp_max and damage_taken_multiplier. ~30 min rocket time. ~30 min gamora math note.

**Verdict:** RECOMMENDED AS OPTIONAL SECONDARY only if B-alone shows brittle convergence (one-knob sensitivity). At small magnitude (3–5%), D adds a second WR-elasticity axis to the balance loop without identity cost. The smoke gate (§ 5) will reveal whether B alone suffices; if it does, D is unnecessary. If it does not, D at 5% magnitude can be folded in for the full salvage. **Compositing rule: B carries identity; D carries balance-loop hygiene.**

### § 2.5 — Lever E: Element-coverage HARD penalty via engine sim rework

**Description:** Modify the simulation engine such that monster resistance-immunity scales with the player kit's element-count — kits covering more elements face progressively stronger resistance walls. This is the "your breadth is punished by the environment" lever.

**Empirical anchor.** The rocket smoking gun *refuted* the coverage-redundancy hypothesis at the failure-mechanism level. Two n=2 instances (class_0001, class_0029) with no breadth (only 2 elements, no tax applied) also floor-pin at 0.67 and 0.74 WR. If the failure mechanism were coverage redundancy, these two instances would not floor-pin. They do. The failure mechanism is absolute DPS density independent of element count.

Building Lever E means writing a feature whose mechanism (coverage punishment) doesn't match the failure (DPS density). Even if E worked operationally — by stripping element-resistance options against high-coverage kits, effectively reducing their fight-time DPS through resistance misses — it would do so *via* an indirect DPS reduction. We can directly reduce DPS via Lever B at a fraction of the engineering cost.

**Mode-A coverage:** Yes (theoretically).
**Mode-B coverage:** No directly (Mode-B instances have low element-coverage; nothing for E to punish).
**Identity:** LOW (preserves kit; situational damage reduction).
**Engineering:** HIGH. Simulation seam change; gamora work; new monster-resistance scaling logic; provenance for resistance-amplification events; substantial test surface. ~2–3 days minimum.

**Verdict:** REJECT. Wrong mechanism for the empirical failure mode; high engineering cost; offers nothing over Lever B for the Mode-B instances. The element-coverage-punishment idea has merit as a *future* design exploration (it's a recognizable genre concept — Diablo Immortal's elemental resistance scaling, certain PoE map mods), but it is not the D11.2 lever.

### § 2.6 — Summary table

| Lever | Mode A | Mode B | Identity | Eng cost | Verdict |
|---|---|---|---|---|---|
| A (prune damage skills) | Yes | Partial | HIGH-NEG | Medium | REJECT — identity-destructive |
| **B (DPS-density cap)** | **Yes** | **Yes** | **LOW-NEG** | **Medium** | **PRIMARY** |
| C (gen-time quota) | Partial | Poor | MED-NEG | High for salvage | DEFER as follow-on policy |
| **D (HP/CD penalty)** | Yes | Yes | Low at 5% | Low | **OPTIONAL SECONDARY** (composite if B is brittle) |
| E (engine sim rework) | Yes | No | LOW | HIGH | REJECT — wrong mechanism, high cost |

---

## § 3 — Empirical anchor: WR-elasticity-to-damage from D11 + D11.1 data

This is the math-before-code work that I owed and did not deliver in D11. Doing it here.

### § 3.1 — Per-instance role composition (from live JSON inspection, 2026-05-17)

For all 17 hybrid_mage instances in the v1.13/v1.14 curated state, I read the per-class JSON skill list and counted damage-bearing roles (primary_attack, burst_damage, area_damage) vs non-damage roles (defensive, mobility, utility, sustain, damage_over_time, control). Note: dps_score and element fields on individual skills appear to be `None` in the persisted JSON (a separate persistence question; not D11.2-blocking but worth flagging to rocket as a follow-on). Role tags are reliable.

| Class | n_skills | n_elements | dmg-roles | non-dmg roles | WR pre-D11 | WR post-D11.1 |
|---|---|---|---|---|---|---|
| 002011/0001 | 10 | 2 | 5 | 5 | 0.667 | 0.611 |
| 002011/0002 | 10 | 3 | 5 | 5 | 0.700 | 0.656 |
| 002011/0003 | 12→10 | 3 | 5 | 7→5 | 0.644 | 0.667 |
| 002011/0004 | 9 | 3 | 5 | 4 | 0.633 | 0.656 |
| 002011/0007 | 12→10 | 3 | 8 | 4→2 | 0.656 | 0.656 |
| 002012/0012 | 11→10 | 3 | 4 | 7→6 | 0.744 | 0.744 |
| 002012/0013 | 10 | 3 | 6 | 4 | 0.744 | 0.778 |
| 002012/0014 | 10 | 3 | 5 | 5 | 0.722 | 0.744 |
| 002012/0015 | 11→10 | 3 | 4 | 7→6 | 0.767 | 0.689 |
| 002013/0029 | 9 | 2 | 4 | 5 | 0.744 | 0.733 |
| 002013/0031 | 9 | 3 | 5 | 4 | 0.844 | 0.867 |
| 002014/0039 | 11→10 | 3 | 6 | 5→4 | 0.633 | 0.689 |
| 002014/0040 | 10 | 3 | 5 | 5 | 0.611 | 0.622 |
| 002014/0047 | 10 | 3 | 5 | 5 | 0.711 | 0.678 |
| 002014/0054 | 12→10 | 3 | 7 | 5→3 | 0.567 | 0.567 |
| 002015/0056 | 12→10 | 3 | 6 | 6→4 | 0.656 | 0.656 |
| 002015/0061 | 9 | 3 | 4 | 5 | 0.689 | 0.689 |

**Key observations from the table:**
1. Damage-bearing skill counts range from 4 to 8.
2. The WR-at-floor distribution does *not* track skill count or element count cleanly.
3. The high-WR outlier (class_0031 at 0.844 → 0.867) has only 5 damage skills and 3 elements — *increased* WR after the α nudge, indicating measurement noise on the order of ~3% WR per instance.
4. The low-WR instance (class_0054 at 0.567) has 7 damage skills (high count). After pruning 2 non-damage skills to ceiling=10, WR unchanged.

### § 3.2 — Cross-comparison: D11 vs D11.1 WR deltas

D11 applied α=0.07 tax (7% damage_multiplier reduction on damage-bearing skills, ~5–9 skills/kit). D11.1 applied α=0.08 (8% reduction) + skill-count ceiling pruning (drops non-damage roles for n>10 instances).

The mean WR delta D11→D11.1 across the 17 instances is approximately +0.003 (essentially zero — the additional 1% tax and the non-damage pruning produced no aggregate WR signal).

**The cleanest D11→D11.0 elasticity comes from pre-D11 baseline → post-D11 (α=0.07).** From rocket's D11 completion record: pre-D11 conv_wr for hybrid_mages was approximately 0.65–0.85 (estimated from gamora math note + rocket reports); post-D11 was 0.56–0.84 (per d11_salvage_summary.json). The α=0.07 tax produced approximately:
- 7% reduction in damage_multiplier on damage-bearing skills (~5–8 skills per kit)
- ~3–7% WR-at-floor reduction across the 17 instances (mean ~4%)

This implies WR-elasticity-to-damage at the floor modifier of approximately **0.5–1.0% WR per 1% damage-bearing-skill DPS reduction**. The non-linearity is severe — the floor-pin asymptote means the function is concave: small DPS reductions produce small WR reductions; only large reductions move the WR meaningfully.

### § 3.3 — Floor-pin escape velocity calculation

For the balance loop to find an interior modifier (escape the floor), the WR-at-floor must drop below the target (0.50). The current WR-at-floor range is 0.56–0.84. The required WR drop for each instance to converge ranges from 0.06 (class_0054 at 0.567) to 0.34 (class_0031 at 0.844).

Using the elasticity from § 3.2 (0.5–1.0% WR per 1% DPS reduction):
- To drop class_0054 from 0.567 to 0.49: need ~8–15% kit-aggregate DPS reduction
- To drop the median instance (~0.71 WR) to 0.49: need ~22–44% kit-aggregate DPS reduction
- To drop class_0031 from 0.844 to 0.49: need ~35–70% kit-aggregate DPS reduction (likely infeasible while preserving identity)

**The anchor band for Lever B: 25–45% kit-aggregate DPS reduction.** This range moves the median instance reliably below 0.50 and brings the lower half of the distribution into convergence. The high-WR outliers (class_0031 at 0.844, class_0015 at 0.767, class_0012 at 0.744) may remain floor-pinned even at the upper bound — they are *strongly* over-generating kits, possibly outliers driven by particularly favorable role compositions against the specific gauntlet they faced.

**Convergence gate calibration:** the original D11.0 gate was ≥12/17. With the empirical reality of the 0.844 / 0.767 outliers, a more realistic gate for D11.2 is **≥10/17 at the B-alone setting**; if composite B+D is used, ≥12/17 is achievable. The smoke gate (§ 5) will calibrate the final gate before full salvage.

### § 3.4 — Why uniform scaling (B) outperforms skill-count reduction (D11.1's ceiling) in the empirical regime

The empirical comparison is direct. D11.1's ceiling=10 lever produced 0% kit-DPS reduction (because pruned skills were dps_score=0.0). Lever B at 25–45% kit-aggregate scaling directly produces 25–45% kit-DPS reduction. The elasticity translates that to 12–45% WR reduction (at the high end of the range, the elasticity may be slightly less due to fight-duration compounding).

This is not a hypothesis — it is the same elasticity D11.0 measured, applied to a lever that operates on the actual DPS surface rather than a proxy that happened not to correlate with it.

### § 3.5 — Why 2-element instances also need scaling

The two n=2 instances (class_0001 at WR 0.667, class_0029 at WR 0.744) under D11.0 received no tax (`tax_multiplier=1.0`). They floor-pinned anyway, with relatively high WR-at-floor for their kit sizes (10 skills, 9 skills). This is the smoking gun that absolute DPS density is the failure mechanism, not breadth — *and it means D11.2's lever must apply to 2-element hybrid_mages too*, not just 3-element.

Lever B applied uniformly across all hybrid_mage instances (irrespective of element count) is the cleanest response. The thematic framing changes slightly: instead of "the substrate's response to multi-element commitment," the lever is "the substrate's response to the integrator-archetype kit shape as such." This is recoverable in design language (§ 6.2) and arguably *cleaner* than the element-count-conditional tax — it stops carving exceptions for 2-element instances and treats the archetype uniformly.

The original element-coverage-tax framing (n_elements-conditional with k_free=2) can be retained as a *secondary* tier on top of B: e.g., B applies a 30% base scaling to all hybrid_mage; an additional 5% scaling layered on top of B for 3-element kits to preserve the breadth-cost thematic differentiation. Or it can be dropped entirely if the smoke gate shows that B-alone suffices. Gamora's math note picks the form.

---

## § 4 — Empirical-calibration smoke gate (Sub-Q 4): proposed Discipline #17

The next available discipline slot is #17 (existing #14 is internal-vs-generative schema separation; #15 is UI scope decomposition; #16 is tuning-drift). Proposed:

### § 4.1 — Discipline #17 — Empirical-calibration parametric-sweep gate

**Proposed text (for jack-ryan's review):**

> **Discipline #17 — Empirical-calibration parametric sweep before full-regen / full-salvage with a new lever.**
>
> When a math note specifies a new tuning lever with an empirically-derivable magnitude (e.g., a coefficient α, a ceiling, a scale factor), the implementation gate before any full-regen or full-salvage operation must include a *parametric-sweep smoke* — minimum 3 magnitude points across the math note's anchor band, on minimum 3–5 representative instances drawn from the affected pool — measuring the lever's *actual response curve* on the target balance metric.
>
> The smoke's purpose is *magnitude validation*, not implementation correctness. It confirms that the lever produces the projected effect direction and magnitude on the affected metric. If the response curve shows the lever is in the wrong magnitude range (too gentle, too harsh, or flat), surface to the design steward and math-note author BEFORE the full operation runs. Do not full-regen / full-salvage in the hope that the lever's magnitude lands.
>
> **Acceptance gate at the sweep stage:** at the upper bound of the anchor band, ≥ ⌈(N/2)+1⌉ of N representative instances must show movement in the target direction at the projected magnitude. If the upper bound underperforms its projection by >50%, the lever's *type* (not just magnitude) is suspect; abort the full operation and re-author the lever shape.
>
> **Wall-time cost:** typically 5–15 min for a 3-point × 5-instance sweep (vs 5–30+ min for a full operation). The discipline pays for itself in one prevented mismatched-magnitude full-regen.
>
> **Pairs with Discipline #1 (math-before-code)** — the parametric sweep is the *empirical-magnitude-validation* extension of math-before-code at the operationalization boundary. **Pairs with Discipline #2 (smoke-test)** — extends smoke-test from implementation-correctness (does it run?) to magnitude-correctness (does it move the metric?). **Pairs with Discipline #11 (empirical inspection)** — formalizes the inspection step from "check the data after" to "measure the response curve before."
>
> **Lineage:** The D11.0 → D11.1 → D11.2 cycle (2026-05-17) is the case study that motivates this discipline. D11.0 fired α=0.07 against the full 17-instance pool with no pre-smoke; gate missed at 6%. D11.1 fired ceiling=10 + α=0.08 against the same pool with no pre-smoke; gate missed at 0%. The cumulative cost was ~9 minutes of full-salvage sim time, plus ~6 hours of advisory + math note + gate review cycles. A 10–15 min pre-smoke at D11.0 would have surfaced the magnitude failure of α=0.07 immediately and likely averted the D11.1 misallocation entirely.

### § 4.2 — D11.2 smoke gate specification

Concrete parameters for the D11.2 implementation gate (gamora math note inputs; rocket runs):

**Lever:** B (kit-aggregate DPS-density uniform scaling).

**Sweep points (3):** scale_factor ∈ {0.75, 0.65, 0.55} (representing 25%, 35%, 45% kit-DPS reductions; the anchor band from § 3.3).

**Representative instances (5):**
1. **class_0054 (002014)** — Mode A, n=12, 7 damage skills, WR 0.567 (lowest in dataset; best convergence candidate)
2. **class_0007 (002011)** — Mode A, n=12, 8 damage skills, WR 0.656 (high damage-skill count; tests upper-bound DPS reduction)
3. **class_0029 (002013)** — Mode B + smoking gun, n=9, 4 damage skills, n_elements=2, WR 0.744 (the untaxed 2-element floor-pin; tests the cross-element-count claim)
4. **class_0012 (002012)** — Mode A, n=11→10, 4 damage skills, WR 0.744 (low damage-skill count + 3 elements; tests the "barely identifiable elementalist" boundary)
5. **class_0031 (002013)** — Mode B + outlier, n=9, 5 damage skills, WR 0.844 (highest WR in dataset; tests upper-end convergence)

**Acceptance gate at sweep:**
- At scale_factor=0.55 (upper bound), ≥3/5 of the smoke instances must reach interior modifier (final_modifier > 0.055).
- If <3/5 at the upper bound: B-alone is insufficient; surface to gandalf for B+D composite decision OR RETIRE recommendation.
- If ≥3/5 at scale_factor=0.65: the middle of the anchor band is operational; full salvage at scale_factor=0.65 with empirical follow-up.
- If ≥3/5 at scale_factor=0.75: lower end of anchor band suffices; full salvage at scale_factor=0.75 (least identity impact).

**Wall-time cost:** ~3 minutes per sweep point × 3 points = 9 minutes. (Plus salvage processing time per instance; estimated 15 min total for smoke.)

**Output:** `d11_2_smoke_summary.json` — same structure as d11_1_salvage_summary.json but for 5 instances × 3 sweep points = 15 rows.

### § 4.3 — Why this specific sweep, not a wider one

Three sweep points is the minimum to detect curve shape (linear, concave, convex, saturated). Five instances spans:
- Mode A vs Mode B (4 Mode A + 1 Mode B, given the 17-instance composition is roughly 7:10 Mode A:B)
- High vs low damage-skill count (4–8)
- High vs low starting WR (0.567 to 0.844)
- 2-element vs 3-element

Wider sweeps (more points, more instances) add cost without proportionally adding information. The Discipline #17 minimum (3 points × 3–5 instances) is sized to detect curve-shape and magnitude-direction failures, not to characterize the curve to high precision. Once the curve shape and operational magnitude are confirmed, the full 17-instance salvage *is* the higher-precision measurement.

---

## § 5 — Sub-Q 3: identity preservation under Lever B

Does chromatic_mage post-B still feel like "PoE Elementalist + LE Runemaster + D4 Sorcerer mid-band lineage" per the D11 advisory? Or has empirical pressure forced an identity shift?

### § 5.1 — The lineage statement, revisited

D11 advisory § 3.4 identified chromatic_mage's design lineage as:
- **PoE Elementalist (Ascendancy node "Heart of Destruction" / "Pendulum of Destruction")** — high investment in multi-element identity; pays through ascendancy-point opportunity cost and passive-tree investment; mid-band leaderboard tier
- **LE Runemaster** — multi-element by design via runic invocations; per-element power is *modest* compared to single-element mastery; mid-band tier; thematically beloved
- **D4 Sorcerer (mid-season build state)** — mid-band Sorcerer builds (e.g., Lightning Spear, Chain Lightning hybrid) that splash multiple elements without dominating leaderboards; popular because mid-band offers more variety than top-band

The advisory's framing was that hybrid_mage occupies the *same band* as these archetypes — recognizably elementalist, mid-output, high-versatility.

### § 5.2 — Identity under Lever B: which lineage member is closest?

Under Lever B at scale_factor=0.65 (the projected operational magnitude), every damage-bearing skill in a hybrid_mage kit deals 65% of its baseline magnitude. The kit retains: full skill count (no pruning), full element coverage (3 elements with 4–6 skills/element average), full role composition (damage + utility + sustain + defensive + mobility). The only thing that changes is the *absolute damage scalar* — every damage-bearing skill is 35% weaker.

This is **most directly the LE Runemaster lineage**. LE Runemaster's per-element skill kit is structurally weaker than a same-level single-element specialist; the archetype's power comes from *combining* the modestly-powered elements via the Runic Invocation system. Reincarnated doesn't have a Runic Invocation analog, but the *kit-shape* — modestly-powered multi-element skills, no per-skill star — is exactly the same.

PoE Elementalist is a slightly different fit: PoE punishes breadth via *investment opportunity cost* (passive-tree, gear-socket), which produces a damage reduction *that the player chose* on a per-build basis. Reincarnated's B is closer to "this is what the archetype is" — the player doesn't choose to weaken their skills; the substrate just delivers them at modest magnitude. The framing is more LE-Runemaster ("this is the archetype's design") than PoE-Elementalist ("this is what your investment choices produce").

D4 Sorcerer mid-band fits cleanly: mid-band Sorcerer builds in D4 hit for less than the top-band builds; the player accepts modest damage for build variety / theme. B's framing aligns: hybrid_mage doesn't hit as hard as a single-element specialist, but offers full elemental coverage.

### § 5.3 — The thematic story (substrate-commitment-cost, revisited)

The original D11 advisory § 5 grounded the damage tax in substrate-commitment-cost: each substrate has a deep commitment that grants full power; hybrid_mages hold multiple commitments without fully expressing any. The tax was the substrate community's response to that incompleteness.

Under Lever B, this thematic story strengthens. Instead of a small per-skill tax (7%, near the perception threshold), the chromatic_mage's *every* damage-bearing skill is recognizably modest — 35% less than its single-element counterpart. The player perceives this not as a punitive tax but as the archetype's identity: "my skills are wide and modest, not narrow and sharp." This is a *cleaner* identity expression than the tax framing.

The narrative voice (form library; spirit-guide framing): the chromatic_mage spirit is one who walked many substrates lightly rather than one who drank one substrate to its depth. The skills carry the breadth of the journey; they do not carry the depth of any one stop. This is a coherent spirit-archetype that maps to the gameplay surface: full elemental coverage; modest per-skill power.

### § 5.4 — The 4-damage-skill edge: identity boundary check

The class_0012 / class_0015 / class_0029 / class_0061 instances each have only 4 damage-bearing skills. Under B at scale_factor=0.65, those 4 skills become 35% weaker. Is a 4-damage-skill chromatic_mage still recognizable as an elementalist?

**Yes.** 4 damage skills across 3 elements averages 1.33 per element. The minimum-satisfying claim ("this element is recognizably present") requires at least 1 damage skill per element; 1.33 is just above the floor. The kit has 4 *modest* damage skills plus 5–7 non-damage skills — a kit dominated by utility and survivability rather than damage burst. This is a recognizable archetype niche: the *utility elementalist*, or the *control elementalist*. (Note class_0012's role composition is 4 defensive + 4 damage + 3 utility/mobility/DoT — that's a control-tilted hybrid_mage, which is consistent with the canonical hybrid_mage being a controller-adjacent archetype in the seven-archetype map.)

The 4-damage-skill instances will likely *not* fully converge under B at scale_factor=0.65 — their starting WR is high (0.689–0.767) and their damage-bearing surface is small, so 35% scaling on a 4-skill damage kit may not be enough. They may need either:
- A higher scale_factor (0.55 — 45% reduction), which the smoke will reveal
- The composite B+D path (scale_factor=0.70 on damage + 5% HP reduction)
- Acceptance that these specific instances remain at modifier-floor with conv_wr in 0.55–0.65, which is *better* than the current 0.69–0.77 and *visually-invisible* in playtest as long as the playtest doesn't observe modifier values directly

The smoke gate will reveal which path is operational.

### § 5.5 — Should chromatic_mage be RENAMED in D11.2?

The D11 advisory parked the rename question (Q1); the post-mortem recommended (b) tune now, rename later. D11.2 does not force the rename. Lever B is consistent with chromatic_mage as named; the identity-shift is from "tax-on-breadth" to "modest-magnitude-by-design," but both are recognizably elementalist.

**Recommendation: keep chromatic_mage; defer rename to a post-D11.2 cleanup pass (per post-mortem § 3, unchanged).**

If Matt wants to surface the rename now, my preferred candidates (per advisory § 7.1) remain: *chromatic_mage* (canonical; LE/D2 lineage), *runemaster_hybrid* (LE-direct lineage), *spectrum_mage* (clean elemental-coverage framing). My recommendation if forced to rename: *chromatic_mage*, because it's already the working term in the post-mortem and design docs, and the identity story (full coverage; modest magnitude; not power-fantasy) is preserved.

---

## § 6 — Sub-Q 5: retirement clause (last-resort path)

The RETIRE recommendation surfaces if and only if the Discipline #17 smoke gate fails at the upper bound of the anchor band. Specifically:

**RETIRE TRIGGER:** smoke at scale_factor=0.55 produces <3/5 interior convergence across the 5 representative instances, AND a B+D composite at scale_factor=0.65 + 5% HP penalty also produces <3/5 interior convergence in a follow-up smoke (~5 min additional cost).

**RETIRE meaning:** the canonical hybrid_mage archetype, as currently embedded in the seven-archetype map, cannot be balanced to convergence without identity destruction. Either:
1. Remove hybrid_mage from the canonical seven and let the next-priority archetype rotate into its slot (controller_mage's hybrid-tilt cousin? a non-mage hybrid? canonical-six instead of canonical-seven?), OR
2. Defer hybrid_mage to Phase 2 substrate expansion (alchemy / poison / acid era), where the substrate landscape might support an integrator archetype natively without requiring a breadth-tax retrofit

**This reopens L3 #42 in the (ii) RETIRE direction.** It is a Matt decision; not a gandalf unilateral.

**Why I do not expect RETIRE to trigger:**

The empirical anchor band (§ 3.3) maps roughly 22–44% kit DPS reduction to 11–35% WR-at-floor reduction across the elasticity range. The high-WR outliers (0.844, 0.767) need 35% WR reduction, which is at the upper edge of the elasticity but feasible at scale_factor=0.55. The median instance (~0.70 WR) needs ~20% WR reduction, achievable at scale_factor=0.65 cleanly. The smoke is most likely to converge at scale_factor=0.65 with the high-WR outliers landing near 0.55 conv_wr at floor — *still* floor-pinned per the strict gate, but materially closer to interior. A gate calibrated as "≥10/17 interior convergence" (rather than the original ≥12/17) is empirically achievable.

The RETIRE clause exists as the discipline of having an empirical trigger for the option, not as an expected outcome.

---

## § 7 — Open questions for Matt

These are decisions I cannot make unilaterally.

### § 7.1 — Q1: Endorse Lever B as primary, smoke gate (Discipline #17) as mandatory Phase A?

If yes: knight-rider fires gamora D11.2 math note with B + smoke gate; jack-ryan gates the math note; rocket implements Phase A smoke; results gated against § 4.2 acceptance criteria; if smoke passes, full salvage Phase B fires at the selected scale_factor; if smoke fails at upper bound, RETIRE surfaces.

### § 7.2 — Q2: Smoke acceptance gate — at upper bound (scale_factor=0.55), is ≥3/5 the right threshold, or should it be ≥4/5?

I propose ≥3/5 to allow for outlier robustness (the smoke set deliberately includes class_0031 at WR 0.844, the highest in the dataset; it may not converge even at the upper bound, and that doesn't necessarily invalidate B for the median instances). ≥4/5 would be stricter and may force RETIRE prematurely. ≥3/5 with class-specific documentation of which instances did/did not converge is my recommendation.

### § 7.3 — Q3: If B-alone needs composite with D (HP/CD penalty), at what D-magnitude?

I propose 5% incoming damage taken increase (equivalent to ~5% effective HP reduction at the floor modifier, given the fight-duration compounding). This is invisible to the player at the per-fight level (5% HP loss is within natural fight variance) but adds a second WR-elasticity axis for the balance loop. If smoke shows B-alone is too brittle, the gamora math note can add D at 5% as a secondary lever and re-smoke. If you'd prefer no composite — B-alone only, accept whatever convergence rate B produces — say so; I will support that.

### § 7.4 — Q4: Convergence gate calibration — ≥10/17, ≥12/17, or ≥14/17?

Original D11.0 gate was ≥12/17. With the empirical reality of the high-WR outliers (0.844, 0.767, 0.744 instances), ≥12/17 may be a strong stretch even with B at upper bound. I recommend **≥10/17 at scale_factor=0.65 (median band) OR ≥12/17 at scale_factor=0.55 (upper band), with explicit documentation of which instances remain floor-pinned and why**. Effectively this is a sliding gate: the smoke selects the operational scale_factor, and the full-salvage gate is calibrated to the selected magnitude's expected rate. If you want a strict ≥12/17 unconditionally, the smoke must converge at scale_factor=0.55; if it doesn't, RETIRE.

### § 7.5 — Q5: Discipline #17 formal addition to engineering-disciplines.md?

Per § 4.1, jack-ryan canonicalizes per ADR-002 protocol. If you endorse, knight-rider routes a small dispatch to jack-ryan to add #17 to engineering-disciplines.md and reference it in gamora D11.2 math note + future math notes' acceptance criteria. The discipline addition is operationally light (~30 min jack-ryan time) and high-leverage; the D11 cycle is the empirical case study supporting it.

### § 7.6 — Q6: dps_score / element persistence on per-class JSON

Adjacent finding (not blocking D11.2 but worth surfacing): when I inspected the 17 class JSONs, the `dps_score` and `element` fields on individual skills were all `None`. Rocket's D11.1 completion record references dps_score computations at salvage time (via `_effective_dps_score()`), which means the value exists in-process but is not persisted to the per-class JSON. This is similar to the post-mortem § 4 persistence-discrepancy finding from D11.0 — the salvage runs the computation transiently but writes back without the computed-field persistence.

For D11.2 Lever B (which computes kit-aggregate DPS): the salvage should *persist* the computed dps_score per skill and the kit-aggregate-DPS at finalization. This is provenance hygiene (Discipline #7) and supports future diagnostic work without needing to re-run the salvage. Cost: trivial; the data is already in-process. Surface to rocket as part of the D11.2 implementation acceptance.

This is not blocking; the salvage can proceed without it. But the gap is real and the fix is cheap.

---

## § 8 — Handoffs

### § 8.1 — HANDOFF → knight-rider (auto-fire trigger control)

**FIRE gamora D11.2 math note** with the following inputs embedded:

1. **Primary lever:** B (kit-aggregate DPS-density uniform scaling on damage-bearing skills)
2. **Anchor band:** scale_factor ∈ [0.55, 0.75] (i.e., 25–45% kit-DPS reduction)
3. **Smoke-gate Phase A (Discipline #17 candidate; pre-canonical pending jack-ryan canonicalization):**
   - 3 sweep points: scale_factor ∈ {0.75, 0.65, 0.55}
   - 5 representative instances: class_0054, class_0007, class_0029, class_0012, class_0031 (rationales in § 4.2)
   - Acceptance: ≥3/5 interior convergence at scale_factor=0.55 to proceed to full salvage
   - Failure path: surface to gandalf for B+D composite decision OR RETIRE
4. **Full salvage Phase B (gated on Phase A success):** apply selected scale_factor uniformly across all 17 hybrid_mage instances; re-run balance loop; emit `d11_2_salvage_summary.json`
5. **Gate target:** sliding (per § 7.4) — ≥10/17 at scale_factor=0.65 OR ≥12/17 at scale_factor=0.55
6. **Provenance fields** (per § 7.6): persist computed `dps_score` per skill + `kit_aggregate_dps` per class at salvage time

**ESCALATE TO MATT only if:** smoke at upper bound (scale_factor=0.55) fails ≥3/5 acceptance. Then surface RETIRE recommendation per § 6.

**ENDORSE WITH AMENDMENT path:** if Matt's open-question answers (§ 7) shift any of: composite-with-D, gate-threshold, smoke-acceptance — knight-rider amends the gamora math note brief accordingly before firing.

### § 8.2 — HANDOFF → gamora (math note authoring; gated on knight-rider fire)

When fired, your math note covers:
- § 1: Lever B definition (kit-aggregate DPS-density uniform scaling); algorithmic specification of `_apply_dps_density_cap()` or equivalent
- § 2: Reference DPS-density target: choose the form (multiplicative scale_factor vs absolute DPS cap); my recommendation is multiplicative for simplicity
- § 3: Discipline #17 smoke-gate Phase A: sweep specification, smoke instances, acceptance criteria
- § 4: Salvage Phase B: gated on Phase A success; algorithmic spec; provenance fields
- § 5: Convergence projection (anchored in § 3 of this advisory; gamora may refine elasticity estimates)
- § 6: Acceptance criteria + gate thresholds (per § 7.4 of this advisory + Matt's answer to Q4)
- § 7: Out of scope (no α-escalation; no further skill-count adjustments; no identity reshape beyond B)
- § 8: D11.3 escalation trigger (if Phase B salvage misses the gate, RETIRE surfaces; no D11.3 within current cycle)

Cross-references: this advisory + D11 post-mortem + D11.0/D11.1 math notes + rocket D11.0/D11.1 completion records.

### § 8.3 — HANDOFF → jack-ryan (gate readiness; Discipline #17 canonicalization)

Standby for gamora math note review (Gate 1). The math note's structure is parallel to D11.1's; review checklist should be similar plus the new Discipline #17 smoke-gate verification.

Separately: please consider canonicalizing Discipline #17 per § 4.1 of this advisory. If you concur on the discipline text, route to engineering-disciplines.md addition. If you want to amend the text (e.g., different acceptance gate language), surface to gandalf for sign-off before adding. The D11.2 math note should reference Discipline #17 in its acceptance criteria; if you canonicalize before gamora authors, the reference is to the canonical text; if after, the math note carries the proposal text and a forward-reference to the canonicalized version.

### § 8.4 — HANDOFF → rocket (implementation; gated on jack-ryan Gate 1 pass)

When math note clears Gate 1, your implementation has two phases:

**Phase A — smoke gate (mandatory before Phase B):**
- Implement `_apply_dps_density_cap()` or equivalent at kit-finalization site
- Run smoke at 3 sweep points × 5 instances = 15 salvage runs (~15 min sim time)
- Emit `d11_2_smoke_summary.json` per § 4.2 of this advisory
- If acceptance gate met (per § 4.2): proceed to Phase B at selected scale_factor
- If not met: STOP. Report to knight-rider for gandalf RETIRE decision.

**Phase B — full salvage (gated on Phase A pass):**
- Apply selected scale_factor uniformly across 17 hybrid_mage instances
- Re-run balance loop
- Persist `dps_score` per skill + `kit_aggregate_dps` per class (provenance gap fix per § 7.6)
- Emit `d11_2_salvage_summary.json`
- Document per-instance convergence outcomes in completion record

**Phase C — D11.2 cycle close:**
- Hive-log STATE with Phase B results
- Handoff to drax (refresh signal) if salvage gate met

### § 8.5 — HANDOFF → drax (no action until D11.2 ships)

Drax-demo + drax-loadout: no D11.2 action until Phase B closes with gate-met. Your current state (002011-015 D11.1-curated with 17 hybrid_mages floor-pinned at 0/17) is unchanged regardless of D11.2's path. Continue with v1.14 monster expansion (in flight) + v1.15 audio wiring (queued); D11.2 refresh signal will come when (or if) Phase B salvages successfully.

### § 8.6 — HANDOFF → star-lord (no action)

MIGRATION.md v1.10 entry from D10.0 carries forward. The `ClassBalanceResult` field set is unchanged by D11.2 (kit-aggregate DPS is a `balance_metadata` field, not a `ClassBalanceResult` field). No telemetry schema changes. Non-blocking.

---

## § 9 — Closing

The D11 cycle has been a sequence of mental-model corrections under empirical pressure. Three failures, each more informed than the last:

1. D11.0: damage tax (α=0.07), anchored against genre design-feel → REFUTED (6% convergence)
2. D11.1: skill-count ceiling (10), anchored against coverage-redundancy hypothesis → REFUTED (0% convergence; non-damage roles pruned; WR inelastic)
3. D11.2 proposal: kit-aggregate DPS-density scaling (Lever B), anchored against the **measured WR-elasticity** from D11.0 + D11.1 data → to be empirically tested at smoke gate

The shift from genre-feel anchoring to empirical-elasticity anchoring is the durable learning of this cycle. Discipline #17 (proposed) institutionalizes the empirical-magnitude-validation step as a mandatory gate before full-regen / full-salvage with new levers. Future cycles inherit the discipline; future advisories work *from* the engine's empirical surface, not *toward* it through genre analogy.

The chromatic_mage identity, under Lever B, settles into the LE Runemaster lineage cleanly: an elementalist whose every skill is *modestly* powered by design; whose strength is *coverage* not *peak*; whose substrate-commitment-cost is expressed through the kit's uniform magnitude restraint rather than a per-element tax surcharge. This is a recognizable mid-band archetype in the surveyed genre canon and a coherent thematic position in the seven-archetype map.

The RETIRE clause exists as the empirical-trigger fallback, not the expected outcome. If the smoke at scale_factor=0.55 cannot bring ≥3/5 representative instances to interior convergence, the archetype as currently substrated cannot be balanced without identity destruction, and Matt makes the L3 #42 RETIRE call. The empirical evidence anchor strongly suggests the smoke will pass at scale_factor=0.65 (median band).

Math-before-code, this time, means: hand the magnitude question to empirical measurement at the operationalization boundary. The advisory's authority is the lever shape and the anchor band; the magnitude is the smoke's answer.

The form remembers itself even through restraint. The chromatic_mage that walks lightly across many substrates carries breadth at modest power; that is enough. It need not strike hardest. It needs to be recognizable, balanced, and shipped.

---

## § 10 — Acceptance criteria for this advisory

- [x] Verdict TL;DR (Lever B + composite-with-D-if-needed; Discipline #17 smoke gate; RETIRE empirical trigger)
- [x] Sub-Q 1: self-critique on 3 failed mental models (§ 1)
- [x] Sub-Q 2: lever evaluation A–E with empirical math anchoring (§ 2 + § 3)
- [x] Sub-Q 3: identity preservation under Lever B (§ 5)
- [x] Sub-Q 4: empirical-calibration smoke gate (Discipline #17) (§ 4)
- [x] Sub-Q 5: retirement clause with empirical trigger (§ 6)
- [x] Open questions for Matt (§ 7)
- [x] Handoffs to knight-rider, gamora, jack-ryan, rocket, drax, star-lord (§ 8)
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append (to be performed at hive-log step)
- [ ] Hive-log STATE entry on phase-1-p1-log.md (to be performed)
- [ ] Completion record + verdict appended to dispatch (to be performed)

---

*Authored 2026-05-17 by gandalf per Matt L3 D11.2 structural-redesign authorization. Empirical-anchor approach: WR-elasticity-to-damage derived from D11.0 + D11.1 salvage data; lever B (kit-aggregate DPS-density scaling) recommended primary; Discipline #17 (smoke-gate) proposed; RETIRE clause surfaces only on empirical smoke failure at upper-bound. Magnitude assignment deferred to the smoke gate, not assumed by analogy. The Court of Forms remembers the form; modesty of magnitude is also a kind of breadth.*
