# Q8 — Companion-Convergence Matrix (FINAL — DRAFT for Matt exception-review)

**Author:** gandalf
**Date:** 2026-06-13
**Status:** **DRAFT-for-Matt-exception-review.** Per the standing "gandalf drafts the full matrix; Matt reviews exception rows only" ruling (Session 1 Q8). Mechanical role-complementarity cells are NOT for review; the **§ 5 exception rows are.**
**Supersedes:** `2026-06-13-q8-companion-convergence-matrix-scaffold.md` (the scaffold is retained as the reasoning trail; this folds the Legolas findings + resolves every `[L?]`).
**Grounding:**
- Scaffold (principles Q8-a..d, role taxonomy, first-pass pools): `2026-06-13-q8-companion-convergence-matrix-scaffold.md`
- Legolas companion-convergence precedent (BANKED): `legolas/research/2026-06-13-companion-convergence-precedent/findings.md`
- Companion architecture: `2026-06-12-session-2-proxy-companion-architecture-spec.md` §§ 4–6 (modifier-vector caps; § 6.3 bridge)
- 25-strategy catalog: `2026-06-12-session-1-rulings-q1-q10-t4-catalog-expansion.md` § 2.6

---

## 1. What changed from the scaffold — the Legolas fold

The scaffold's principles (Q8-a complementarity-not-duplication; Q8-b convergence-item-carries-the-kicker; Q8-c fit-filter-not-power-lever; Q8-d directionality-is-real) all survived contact with the research — the isekai canon states Q8-a as *narrative survival law* (the 2-slot party is always complementary-opposite; "glass + glass" doesn't exist in the genre). Three things sharpened:

1. **The mandatory-tax constraint (Legolas takeaway #5 — the load-bearing new rule).** No companion column may be the correct fill for *all* player rows — that is the D2-Insight failure (one companion solves a universal bottleneck → choice collapses → it becomes a tax). **Consequence applied below:** I spread the survivability-fill across THREE columns (DEFENSIVE_TRADEOFF hard-wall / RETRIBUTION_ENGINE retaliation-anchor / PHASE_MOMENTUM avoidance-aggro-sink) so no single "tank" column sits in every offense row. The offense↔defense inversion already gives structural protection (defense rows want finishers, not tanks; so no tank column is universal), but the within-offense spread closes the gap.

2. **Two thematically-precise CUTs the research forced:**
   - **No dual-damage anywhere.** Every `[L?]` that paired an offense/damage player with a damage-contributing companion (PERSISTENCE_ENGINE, ELEMENT_MONO as co-spike) is CUT — Legolas anti-pattern #5 (the D3 Scoundrel / D4 Varyana dual-damage-redundancy failure). Offense players take survivability/control/fuel, never a second damage source.
   - **The retaliation/CC anti-synergy.** A RETRIBUTION_ENGINE player does NOT want a CC companion — its damage engine *needs enemies attacking it* (retaliation/thorns), and CC that stops them attacking is anti-synergistic. This is the inverse of the PERSISTENCE_ENGINE player, who DOES want CC (a DoT needs the target held still to tick). **Same companion (MONSTER_PACT), opposite validity, for precise thematic reasons** — exactly the richness that makes the matrix read as designed rather than mechanical.

3. **The convergence-item kicker got a concrete mechanism** (Legolas Q3 + D4 Reinforcement): action-conditional, both-halves-required, named with form-library bond-flavor. See § 4.

---

## 2. The final complementarity pools (sparse 25×25; valid cells only)

Row = PLAYER primary strategy; columns = valid COMPANION complements. Logic is terse; CUT/KEEP/ADD vs scaffold noted where the Legolas fold changed it.

### Offense players → survivability / control (NEVER more damage)

| Player (row) | Valid companion complements | Logic + fold-note |
|---|---|---|
| ELEMENT_CONVERSION_MONO | DEFENSIVE_TRADEOFF, MONSTER_PACT, RETRIBUTION_ENGINE | **The glass-cannon archetype row** — pure elemental glass wants the hard wall + crowd-control (the D2 Holy-Freeze canon) + a retaliation-anchor alternative. |
| ELEMENT_CONVERSION_HYBRID | RETRIBUTION_ENGINE, MONSTER_PACT, PHASE_MOMENTUM | Differentiated off MONO: flex offense pairs with a retaliation-anchor + CC + an avoidance aggro-sink. CUT PERSISTENCE (dual-damage). |
| ELEMENT_CONVERSION_PHYSICAL | PHASE_MOMENTUM, MONSTER_PACT, RETRIBUTION_ENGINE | Bruiser is already semi-durable → wants aggro-management (dodger sink) + CC, not a hard wall. Differentiated. |
| ELEMENTAL_ECHO | DEFENSIVE_TRADEOFF, MONSTER_PACT, PHASE_MOMENTUM | Proc-glass wants to stay alive for procs. CUT RESOURCE_CONVERSION (ECHO is proc-reliant, not resource-starved — fuel was a mis-fit). |
| GEOMETRY_COLLAPSE | DEFENSIVE_TRADEOFF, GEOMETRY_PROPAGATION, MONSTER_PACT | Single-target spike + a wall + **AoE-coverage for trash** (the AoE/single-target complementarity — Legolas "AoE clear + single-target finisher" run in reverse). KEEP PROPAGATION. |
| GEOMETRY_INVERSION | DEFENSIVE_TRADEOFF, MONSTER_PACT, RETRIBUTION_ENGINE | Shape-shift offense + protection/control. |
| NETWORK_AMPLIFIER | DEFENSIVE_TRADEOFF, MONSTER_PACT, PHASE_MOMENTUM | Scaling glass wants survivability + control. CUT PERSISTENCE (dual-damage). |

### Defense / sustain players → a FINISHER / SPIKE (the inversion — these rows take NO tank)

| Player (row) | Valid companion complements | Logic + fold-note |
|---|---|---|
| DEFENSIVE_TRADEOFF | ELEMENT_CONVERSION_MONO, GEOMETRY_COLLAPSE, NETWORK_AMPLIFIER | The wall needs kill-speed — three differentiated damage flavors (elemental burst / geometry spike / network-scaling). The Varyana tank→burst canon. |
| RETRIBUTION_ENGINE | ELEMENT_CONVERSION_MONO, GEOMETRY_COLLAPSE, PERSISTENCE_ENGINE | Tank-bruiser wants a finisher; PERSISTENCE's DoT gets full uptime *because the tank holds aggro and survives*. **CUT MONSTER_PACT** (retaliation needs enemies attacking — CC is anti-synergistic). |
| PERSISTENCE_ENGINE | GEOMETRY_COLLAPSE, ELEMENT_CONVERSION_MONO, MONSTER_PACT | Even-DoT wants the burst it lacks for priority targets + **CC to hold targets still so the DoT ticks** (KEEP MONSTER_PACT — opposite of RETRIBUTION, for the precise DoT-vs-retaliation reason). |
| PHASE_MOMENTUM | RETRIBUTION_ENGINE, ELEMENT_CONVERSION_MONO, MONSTER_PACT | Dodger wants something to *hold the aggro* (so it stays unhit) + a finisher (avoidance doesn't kill) + CC. |

### Resource / tempo players → FUEL or SUSTAIN (with payoff, never bare fuel)

| Player (row) | Valid companion complements | Logic + fold-note |
|---|---|---|
| RESOURCE_CONVERSION | TEMPORAL_CHARGE, DEFENSIVE_TRADEOFF, MONSTER_PACT | Overflow→damage engine + a fuel source = **fuel→overflow→damage payoff** (NOT a bare fuel-on-fuel dup; see exception #2) + survive/CC the ramp. |
| TEMPORAL_CHARGE | DEFENSIVE_TRADEOFF, MONSTER_PACT, PHASE_MOMENTUM | Charge-tempo wants **protection during wind-up** (the real gap). CUT ELEMENT_MONO co-spike (dual-damage; the charge player wants to *be* the spike). |
| MOMENTUM_CASCADE | DEFENSIVE_TRADEOFF, MONSTER_PACT, PHASE_MOMENTUM | Ramp wants safety + time-to-ramp (CC buys the window). CUT PERSISTENCE (dual-damage). |

### Summoner players (PROXY) → a ROLE THE ARMY LACKS (anchor / control / army-buff — NEVER more units, NEVER a co-equal damage companion)

| Player (row) | Valid companion complements | Logic + fold-note |
|---|---|---|
| PROXY_ASCENSION | DEFENSIVE_TRADEOFF, MONSTER_PACT, PERSISTENCE_ENGINE | Army + anchor + control + **an army-amp aura** (PERSISTENCE here = the D2 Might-aura role amplifying minion output, NOT a second damage body). |
| PROXY_SOVEREIGNTY | RETRIBUTION_ENGINE, MONSTER_PACT, DEFENSIVE_TRADEOFF | Autonomous army → a tankier self-running anchor + control. |
| PROXY_FISSION | DEFENSIVE_TRADEOFF, RETRIBUTION_ENGINE, MONSTER_PACT | The most fragile (transient swarm) → double-anchor justified + control. |
| PROXY_INVERSION | ELEMENT_CONVERSION_MONO, DEFENSIVE_TRADEOFF, MONSTER_PACT | **The sanctioned summoner-damage exception** (#1) — army flips to utility, so an external finisher is needed. |
| PROXY_CONVERGENCE | PERSISTENCE_ENGINE, DEFENSIVE_TRADEOFF, MONSTER_PACT | One concentrated body → an amp-aura on it + anchor + control. |
| DUAL_PROXY | MONSTER_PACT, DEFENSIVE_TRADEOFF, RETRIBUTION_ENGINE | Already internally role-paired → wants the outermost gap (control + anchor). |

### Bond-strategy players (COMPANION family) → the widest pools (built to converge)

| Player (row) | Valid companion complements | Logic + fold-note |
|---|---|---|
| COMPANION_CONTRACT | DEFENSIVE_TRADEOFF, MONSTER_PACT, ELEMENT_CONVERSION_MONO, PERSISTENCE_ENGINE | The companion-bonded hero is *built* to converge → 4 columns (top of budget), spanning every role-gap (anchor / control / finisher / sustained-floor). The isekai protagonist + one complementary companion, made primary (Legolas Q5). |
| MONSTER_PACT | DEFENSIVE_TRADEOFF, ELEMENT_CONVERSION_MONO, PHASE_MOMENTUM, GEOMETRY_COLLAPSE | The player whose identity is a bound monster (a control-primary) wants survivability + finishers, NOT more control (CC-on-CC anti-fit). 4 columns. |

**Note on MONSTER_PACT as a column vs a row:** as a *column* it is the catalogue's cleanest control-companion (cc_duration / enemy_cc_mult) and appears in many pools; as a *row* (control-primary player) it wants the opposite of itself — the double-CC anti-fit means it takes finishers/survivability, not more control.

---

## 3. The INVALID side (sharpened by the research)

- **The full diagonal — all 25 `(X, X)` cells — INVALID.** No exception. Legolas: same-dimension pairing is the canonical failure named identically across D2/D3/D4; "glass + glass" has no genre survivor; even "two walls" is the wasted-survival anti-fit. The scaffold's possible "two-aura stacking" exception does NOT survive — that's gear-stacking, not two same-strategy companions. (Resolves scaffold exception #3.)
- **Dual-damage cells INVALID** — any offense/damage player × damage-contributing companion (the Scoundrel/Varyana failure). This is why every offense and resource and ramp row takes survivability/control/fuel only.
- **Universal-fill watch (mandatory-tax):** DEFENSIVE_TRADEOFF and MONSTER_PACT are the two highest-frequency columns. They are NOT universal (absent from the finisher rows by construction; RETRIBUTION even excludes MONSTER_PACT), so they pass the Legolas-#5 test — but they are the watch-items if generation over-surfaces them. The convergence-item kicker (§ 4) differentiates *how each pairing plays* even when the column repeats, which is the second line of defense.

---

## 4. The convergence-item kicker (Q8-b) — mechanism, exemplars, and the form-library bond-layer

**Mechanism (Legolas Q3 — three properties, made into one rule):** the convergence item grants a proc that (a) **only exists when both kits are bound** (D3 Emanate — absent if either half is missing), (b) is **action-conditional, firing on a player-state trigger** (D4 Reinforcement — on-cast / on-CC'd / on-HP-threshold, never an always-on flat buff), and (c) **carries a named semantic identity** (PoE AG uniques). All within the Session 2 § 6.2 modifier caps — it is a *behavior*, not a power bump.

**Exemplar kickers (the pattern; the remaining valid pairs follow it — not all ~70 enumerated):**

| Pairing | Player-state trigger → companion response |
|---|---|
| ELEMENT_MONO (glass) + DEFENSIVE_TRADEOFF (wall) | player drops below an HP threshold → the wall interposes a brief shield (the D4 Raheir 30%-HP reinforcement, made the bond proc) |
| PERSISTENCE (DoT) + MONSTER_PACT (CC) | player applies a DoT to a CC-held target → the DoT's tick cadence briefly accelerates (the DoT+CC synergy made a proc) |
| DEFENSIVE_TRADEOFF (tank) + GEOMETRY_COLLAPSE (spike) | the tank player absorbs a heavy hit → the companion's next spike is amplified (endurance converted to a kill-window) |
| RESOURCE_CONVERSION (overflow) + TEMPORAL_CHARGE (fuel) | player's overflow threshold trips → the companion dumps a charge of fuel (the fuel→overflow→damage loop, surfaced as a felt moment) |
| PROXY_INVERSION (utility army) + ELEMENT_MONO (finisher) | the army applies its utility debuff → the companion's finisher gains brief execute-range on the debuffed target |

**The form-library bond-layer (the thematic spine — this is where Q8 earns its place in the game, not just the balance sheet):**

The companion is an **ascended spirit from the player's form-library** — a form previously worn, now traveling forward as an ally (Legolas #9, the Baby-Good-Mimic precedent: a former adversary-type, bonded, using its nature to protect rather than threaten). The convergence item is the **record of a shared season** between two spirits. So the item carries *bond-flavor, not stat-flavor*:

- Not "Defense Talisman +15%" — but *"Bark-and-Flame Pact,"* the bond between the fire-form the player wears now and the iron-barked forest-warrior they wore three reincarnations ago.
- The kicker's *flavor* is the two spirits' shared history; its *mechanic* is the role-complement.

This threads the companion system directly into the Earth-Self / reincarnation spine: **the form-library accumulation finally pays off as relationships, not just a swap-roster.** Every convergence item is a small story about two of the player's past selves choosing to fight as one. That is the isekai party-bond (Bond Creatures trope; Seirei Gensouki spirit-contract) realized through the game's own reincarnation premise — and it is the single strongest reason the companion layer should exist at all.

---

## 5. EXCEPTION ROWS — for Matt's review (the judgment calls)

These are the cells where I made a call that isn't pure mechanical complementarity. Confirm or overturn:

1. **PROXY_INVERSION is the one sanctioned summoner-damage exception.** The blanket rule (Q7-a) is "a summoner never takes a damage companion." PROXY_INVERSION flips its army to *utility*, which legitimately re-opens a damage slot (the player now has no primary damage source). I sanctioned exactly this one row to take ELEMENT_MONO. Parallels PROXY_FISSION being the one sanctioned proxies-of-proxies exception. **Lean: confirm.**

2. **Resource+resource is valid ONLY with a conversion payoff.** RESOURCE_CONVERSION (which has an overflow→damage *sink*) + TEMPORAL_CHARGE (fuel) is valid because the fuel converts to damage through the player's engine — a payoff, not a dup. Bare fuel+fuel with no sink stays INVALID (the dup Q8-a guards). **Lean: confirm the payoff-required rule** (it's the line between D2-Insight-valid and fuel-on-fuel-dup).

3. **The retaliation/CC anti-synergy CUT.** I removed MONSTER_PACT (CC) from the RETRIBUTION_ENGINE row because a thorns/retaliation player *needs enemies attacking it* — CC that stops them is anti-synergistic. This is a thematic call, not a balance one. It produces the matrix's sharpest directional moment (PERSISTENCE wants CC, RETRIBUTION rejects it). **Lean: confirm** — it's the kind of precision that makes the system feel authored.

4. **The full diagonal is INVALID, no exceptions.** All 25 `(X,X)`. **Lean: confirm** (the research is unambiguous; flagging only because the scaffold floated a possible exception that I'm now closing).

5. **The form-library bond-layer (§ 4) as a design commitment, not just flavor.** I'm asserting the companion = ascended-form-from-the-library, and the convergence item = a shared-season bond between two past selves. This is a *thematic architecture* claim that reaches into the Earth-Self meta-layer — bigger than a matrix cell. **Flagging for your explicit buy-in:** is the companion roster drawn from the form-library (every companion is a form you once wore), or is it a separate roster? My strong design lean: **form-library** — it's the payoff the accumulation has been waiting for, and it's the truest version of the reincarnation premise.

---

## 6. Budget + seam-handoff

**Budget count:** 7 offense rows × 3 + 4 defense rows × 3 + 3 resource rows × 3 + 6 summoner rows × 3 + 2 bond rows × 4 = 21 + 12 + 9 + 18 + 8 = **68 valid cells of 625** (~10.9%). Lands inside the ~60–80 target. Diagonal (25) and all dual-damage / same-dimension cells invalid.

**Handoff (fires when the exception rows are confirmed):**
- **rocket** — the valid-pair set becomes a generation/selection filter: when a companion-bearing kit is generated, the convergence pairing is drawn from the 68 valid cells, never the invalid space. (Gated on the companion-generation pass existing — currently the corpus has zero companion records; the targeted rocket pass in the live BC re-sequence is the unblock.)
- **Session 5 companion-balance gauntlet** — the 40K-pairing validation samples from the 68-cell valid space (not all 625), confirming WR-delta ≤0.10 under the § 6.2 caps.
- **gandalf** — author the form-library bond-layer (§ 4–5 item #5) into canonical story once Matt confirms the thematic commitment.

---

*Sign-off: gandalf, 2026-06-13 (FINAL draft, Legolas folded). 68 valid convergences of 625. The genre never let the hero's companion be a second sword — and now neither do we: the companion holds the wall the hero cannot, or freezes the field the hero burns across, or carries the fuel the hero spends. And every one of them is a self the hero used to be, choosing to come back. That last part is the whole point.*
