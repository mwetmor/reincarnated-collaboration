# Q8 — Companion-Convergence Matrix (SCAFFOLD)

**Author:** gandalf
**Date:** 2026-06-13
**Mode:** offline matrix drafting (Pattern B follow-on; process ruled Session 1, principles + matrix drafted here)
**Status:** **DRAFT SCAFFOLD** — principles + role taxonomy + first-pass complementarity pools complete; valid-pair confidence calls + exception rows + convergence-item kickers PENDING the Legolas companion-convergence pull (`legolas/research/2026-06-13-companion-convergence-precedent/`, fired 2026-06-13).
**Grounding:**
- Session 1 ruling (process): `gandalf/notes/2026-06-12-session-1-rulings-q1-q10-t4-catalog-expansion.md` § 1 (Q6/Q7/Q8 row), § 2.6 (25-strategy catalog)
- Q6/Q7 predecessor: `gandalf/notes/2026-06-12-q6-q7-convergence-matrix-dual-proxy-pools.md` (the proxy-layer matrix; Q8 inherits its Q7-a/Q6-b principles, re-aimed at the companion layer)
- Companion architecture: `gandalf/notes/2026-06-12-session-2-proxy-companion-architecture-spec.md` §§ 4–6 (Tier-2/3 companions = pre-fight modifier vectors; convergence item = 4th gear slot; § 6.3 archetype→modifier-vector bridge)
- Legolas companion-convergence precedent (PENDING; fired 2026-06-13)

---

## 0. The load-bearing distinction — Q8 is NOT Q6/Q7

| | Q6 / Q7 | **Q8** |
|---|---|---|
| Layer | **Proxy** — entities *inside* one summoner kit | **Companion** — a *separate full kit* fighting alongside the player |
| Objects paired | proxy-type × proxy-type (14 types) | **player-strategy × companion-strategy (25 T4 strategies)** |
| Fight model | ProxyCombatant entities in `simulate_fight` | pre-fight **modifier vector** applied to the player (Session 2 § 6; capped) |
| Matrix shape | 14×14 → cross-family → 33 valid | **directional 25×25 = 625 → ~60–80 valid** |
| Binding mechanism | the merge / the dual-pool | the **convergence item** (4th gear slot) |

**Directional, not symmetric.** Row = the PLAYER's primary strategy; column = the COMPANION's strategy. `(glass-player, tank-companion)` and `(tank-player, glass-companion)` are *different cells* — both can be valid, because complementarity runs both ways (a tank completes a glass player; a damage-finisher completes a tank player). That asymmetry is why the space is 625 ordered pairs, not 325 unordered. Budget ~60–80 ≈ **25 rows × ~3 complementary columns each** (mirrors the Q7 "3–4 secondaries per primary" budget).

---

## 1. Governing principles (Q8-a … Q8-d) — inherited + adapted

These extend the **ratified** Q6-b / Q7-a principles (Q6/Q7 doc § 1) from the proxy layer to the companion layer. The inheritance is deliberate: it is the *same anti-pattern guard* one level up.

| # | Principle | Statement |
|---|---|---|
| **Q8-a** | **Complementarity, not duplication** (inherits Q7-a) | A pairing is a valid convergence only when the companion **fills a role the player's strategy lacks** (tank / control / sustain / zone / economy) OR **amplifies a payoff the player sets up** (control→finish; ramp→spike-cover). NEVER a co-equal second source of the player's own damage axis. The genre's universal companion-failure state is "two damage dealers that don't synergize." |
| **Q8-b** | **The convergence item carries the emergent kicker** (inherits Q6-b at the item layer) | Where Q6-b put the "third thing neither parent does alone" in the merged proxy, Q8 puts it in the **convergence item**: when player+companion are an aligned pairing, the item grants a small synergy proc — a behavior, not a number — *within the § 6.2 modifier caps*. This is what makes a valid pairing read as *designed*, not arbitrary. (Examples PENDING Legolas Q3 — the D4-reinforcement-bond / set-keys-off-follower precedent.) |
| **Q8-c** | **The matrix is a fit-and-fantasy filter, not a power lever** | Raw companion power is already bounded by the Session 2 § 6.2 modifier caps (≤15% dmg amp, ≤25% CC, etc.) regardless of pairing. So Q8 valid-pairs select for **synergy, theme, and player-fantasy coherence**, NOT for balance. A "non-valid" cell isn't underpowered — it's *uncomposed* (generation won't surface it as a rewarded pairing). |
| **Q8-d** | **Directionality is real and meaningful** | The role a strategy plays *as a companion* (its modifier-vector contribution) is not the role it plays *as a player* (its need-profile). The taxonomy (§ 2) tags both columns separately. Pairs are evaluated row→column. |

**Composition with Session 2 § 6.3 (the runtime bridge):** Q8 (this matrix, generation-time, strategy-level) is the **selection filter** — "is this pairing a valid convergence to surface/reward?" Session 2 § 6.3 (runtime, measured-archetype-level) is the **magnitude derivation** — "and here is the modifier vector it contributes." They compose: Q8 says *whether*, § 6.3 says *how much*.

---

## 2. Role taxonomy — the 25 strategies, dual-tagged

Each strategy tagged by **as-PLAYER need-profile** (what gap it has when it's the row) and **as-COMPANION contribution-role** (what modifier-vector role it brings when it's the column). This is the backbone the pools (§ 3) are derived from.

| # | Strategy | Family | As-PLAYER: primary need (the gap) | As-COMPANION: contribution-role |
|---|---|---|---|---|
| 1 | ELEMENT_CONVERSION_MONO | ELEMENT | survivability / control (pure offense) | damage_amp (elemental) |
| 2 | ELEMENT_CONVERSION_HYBRID | ELEMENT | survivability / control | damage_amp (elemental, flex) |
| 3 | ELEMENT_CONVERSION_PHYSICAL | ELEMENT | control / sustain (bruiser offense) | damage_amp (phys-element) |
| 4 | ELEMENTAL_ECHO | ELEMENT/COMBAT | survivability (proc-reliant) | damage_amp (echo/proc) |
| 5 | DEFENSIVE_TRADEOFF | DEFENSE | **damage finish** (durable, low kill-speed) | **survivability_mod** (mitigator/shield) |
| 6 | SACRIFICE_ASCENDANCY | DEFENSE | **survivability / sustain** (glass-by-choice) | damage_amp at self-cost (risky) |
| 7 | RETRIBUTION_ENGINE | DEFENSE | control of incoming / **damage finish** | **survivability_mod** + retaliation (tank) |
| 8 | PHASE_MOMENTUM | DEFENSE | aggro-sink to stay unhit | survivability (avoidance/dodger) |
| 9 | GEOMETRY_COLLAPSE | GEOMETRY | AoE coverage / survivability (single-target spike) | damage_amp (concentrated) |
| 10 | GEOMETRY_INVERSION | GEOMETRY | survivability / control | damage_amp + aoe_radius_mod |
| 11 | GEOMETRY_PROPAGATION | GEOMETRY | **single-target / boss finish** (density-gated; ≈0 vs lone boss) + survivability | aoe_radius_mod (clear) |
| 12 | RESOURCE_CONVERSION | RESOURCE | **resource fuel** / sustain (overflow-hungry) | resource_gen_mod |
| 13 | TEMPORAL_CHARGE | RESOURCE | survivability through charge-up / **fuel** | resource_gen_mod (tempo) |
| 14 | MOMENTUM_CASCADE | RESOURCE | survivability / CC to survive the ramp | tempo buff (ramp-enabler) |
| 15 | PROXY_ASCENSION | PROXY | **buff / tank-anchor** for the army (NOT more dmg) | army presence (see § 3 note) |
| 16 | PROXY_SOVEREIGNTY | PROXY | buff / control (autonomous army) | army presence |
| 17 | PROXY_FISSION | PROXY | tank-anchor / zone (fragile swarm) | army presence (transient) |
| 18 | PROXY_INVERSION | PROXY | damage finish (army flips to utility) | debuff/utility |
| 19 | PROXY_CONVERGENCE | PROXY | buff / sustain (one concentrated body) | single strong body |
| 20 | DUAL_PROXY | PROXY | buff / economy (already role-paired internally) | mixed |
| 21 | COMPANION_CONTRACT | COMPANION | **(the bond strategy itself)** — see § 4 | nested sub-companion (rare) |
| 22 | MONSTER_PACT | COMPANION | **(the bond strategy itself)** — see § 4 | **cc_duration / enemy_cc_mult** (control) |
| 23 | NETWORK_AMPLIFIER | COMBAT | survivability / control (scaling glass) | damage_amp (network) |
| 24 | RESONANCE_LOOP | COMBAT | **forgiveness** — sustain / no added cog-load (HIGH-load rotation) | damage_amp (but adds cog-load if active) |
| 25 | PERSISTENCE_ENGINE | COMBAT | **burst / spike-cover** (even, no-burst DoT) + safety to hold uptime | flat/sustained damage_amp |

**Reading the need column:** offense-family strategies (ELEMENT, GEOMETRY, NETWORK, ELEMENTAL_ECHO) almost all need *survivability or control* — they kill but are exposed. Defense-family strategies (DEFENSIVE_TRADEOFF, RETRIBUTION) invert it — they endure but need a *finisher*. This offense↔defense inversion is the spine of the matrix (Q8-d directionality made concrete).

---

## 3. The complementarity pools — first pass (per player-strategy)

Sparse-matrix representation (mirrors Q7's per-primary pools — cleaner than a 25×25 grid for ~60–80 of 625). Each row lists the **valid companion-strategy complements** for that player. **HIGH-confidence** = role-complementarity is unambiguous (drafted now). **[L?]** = marginal / genre-precedent-dependent → confidence call PENDING Legolas. Pools target ~3 columns each.

> Convention: I list companion strategies by the ROLE they bring (§ 2 right column), choosing the cleanest exemplar(s) of that role. Final pools may swap an exemplar within a role once Legolas's canonical-fit data lands.

### Offense players → want SURVIVABILITY / CONTROL (never more damage)

| Player (row) | Valid companion complements (col) | Logic |
|---|---|---|
| ELEMENT_CONVERSION_MONO | DEFENSIVE_TRADEOFF (tank), MONSTER_PACT (CC), RETRIBUTION_ENGINE (tank) | pure elemental glass wants a wall + crowd control |
| ELEMENT_CONVERSION_HYBRID | DEFENSIVE_TRADEOFF, MONSTER_PACT, PERSISTENCE_ENGINE [L?] (sustained chip while player spikes) | flex offense + protection + optional chip-floor |
| ELEMENT_CONVERSION_PHYSICAL | RETRIBUTION_ENGINE (bruiser-tank), MONSTER_PACT, PHASE_MOMENTUM [L?] | phys-bruiser pairs with a tankier anchor |
| ELEMENTAL_ECHO | DEFENSIVE_TRADEOFF, MONSTER_PACT, RESOURCE_CONVERSION [L?] (fuel the procs) | proc-glass wants protection; fuel is marginal |
| GEOMETRY_COLLAPSE | DEFENSIVE_TRADEOFF, MONSTER_PACT, GEOMETRY_PROPAGATION [L?] (AoE-cover the single-target spike) | single-target spike wants a wall + AoE coverage for trash |
| GEOMETRY_INVERSION | DEFENSIVE_TRADEOFF, MONSTER_PACT, RETRIBUTION_ENGINE | shape-shift offense + protection/control |
| NETWORK_AMPLIFIER | DEFENSIVE_TRADEOFF, MONSTER_PACT, PERSISTENCE_ENGINE [L?] | scaling glass wants survivability + a damage floor |

### Defense / sustain players → want a FINISHER / SPIKE (the inversion)

| Player (row) | Valid companion complements (col) | Logic |
|---|---|---|
| DEFENSIVE_TRADEOFF | ELEMENT_CONVERSION_MONO (burst), GEOMETRY_COLLAPSE (spike), NETWORK_AMPLIFIER | the wall needs a kill-speed source |
| RETRIBUTION_ENGINE | ELEMENT_CONVERSION_MONO, GEOMETRY_COLLAPSE, MONSTER_PACT [L?] (control the incoming it converts) | tank-bruiser wants a finisher; CC-the-incoming is a thematic [L?] |
| PERSISTENCE_ENGINE | GEOMETRY_COLLAPSE (the burst it lacks), ELEMENT_CONVERSION_MONO, MONSTER_PACT [L?] | even-DoT wants a spike for priority targets + CC to hold uptime |
| PHASE_MOMENTUM | GOLEM-role tank? → **RETRIBUTION_ENGINE** (aggro-sink), ELEMENT_CONVERSION_MONO (finish), MONSTER_PACT [L?] | dodger wants something to hold aggro so it stays unhit + a finisher |

### Resource / tempo players → want FUEL or SUSTAIN

| Player (row) | Valid companion complements (col) | Logic |
|---|---|---|
| RESOURCE_CONVERSION | RESOURCE_CONVERSION? **no** (dup) → TEMPORAL_CHARGE [L?], DEFENSIVE_TRADEOFF, PERSISTENCE_ENGINE [L?] | overflow-hungry wants fuel/sustain — but fuel-on-fuel risks dup; flag |
| TEMPORAL_CHARGE | DEFENSIVE_TRADEOFF (survive charge-up), ELEMENT_CONVERSION_MONO (spend the charge into a partner-spike) [L?], MONSTER_PACT | charge-tempo wants protection during wind-up |
| MOMENTUM_CASCADE | DEFENSIVE_TRADEOFF, MONSTER_PACT (CC buys ramp-time), PERSISTENCE_ENGINE [L?] | ramp wants safety + time-to-ramp |

### Summoner players (PROXY) → want a ROLE THE ARMY LACKS (Q7-a one level up; NOT a damage-army companion)

| Player (row) | Valid companion complements (col) | Logic |
|---|---|---|
| PROXY_ASCENSION | DEFENSIVE_TRADEOFF (anchor), MONSTER_PACT (control), PERSISTENCE_ENGINE [L?] | army + a wall/control the bodies don't provide |
| PROXY_SOVEREIGNTY | DEFENSIVE_TRADEOFF, MONSTER_PACT, RETRIBUTION_ENGINE [L?] | autonomous army + protection/control |
| PROXY_FISSION | DEFENSIVE_TRADEOFF, MONSTER_PACT, RETRIBUTION_ENGINE | fragile swarm badly wants an anchor |
| PROXY_INVERSION | ELEMENT_CONVERSION_MONO [L?] (army goes utility, needs a finisher), DEFENSIVE_TRADEOFF, MONSTER_PACT | inverted (utility) army wants a damage source — a controlled exception to "summoner never wants damage" |
| PROXY_CONVERGENCE | DEFENSIVE_TRADEOFF, MONSTER_PACT, PERSISTENCE_ENGINE [L?] | one concentrated body + protection/control/floor |
| DUAL_PROXY | MONSTER_PACT, DEFENSIVE_TRADEOFF, [one more PENDING] | already internally role-paired; wants the outermost gap |

### Bond-strategy players (COMPANION family) → § 4

---

## 4. The COMPANION_CONTRACT / MONSTER_PACT rows — special handling

These two strategies ARE the companion-bond made primary — the player's whole identity is "I fight with a bound companion/monster." Two consequences:

1. **As a ROW (player on COMPANION_CONTRACT / MONSTER_PACT):** the convergence matrix is *most* expressive here — this player is built to converge. Their pool should be the **widest** (4 columns, top of the budget), spanning the role-gaps a companion-centric player most wants filled. PENDING Legolas Q5 (isekai party-composition) for the canonical "what does the companion-bonded hero most want in a second companion" read.
2. **As a COLUMN (companion built on COMPANION_CONTRACT / MONSTER_PACT):** Session 2 § 9.1 notes a COMPANION_CONTRACT companion is a *nested sub-companion* — "rare but valid." A nested bond is recursion-adjacent; cap at one level (a companion's companion does not itself bear a companion), same bounding discipline as proxies-of-proxies (Session 1 ruling § 4). MONSTER_PACT as a column is the **cleanest control-companion** in the catalog (§ 2: cc_duration / enemy_cc_mult) — it appears in many pools above for exactly that reason.

---

## 5. Exception rows flagged for Matt review (preliminary — grows when Legolas lands)

Per the standing "Matt reviews exception rows only" ruling. Mechanical role-complementarity applications are NOT flagged; these are the judgment calls:

1. **Summoner-wants-damage exceptions (PROXY_INVERSION row).** The blanket rule is "summoner never wants a damage companion" (Q7-a). PROXY_INVERSION flips the army to utility, which *legitimately* re-opens a damage-companion slot. Confirm this is the one sanctioned summoner-damage exception (parallels PROXY_FISSION being the one sanctioned proxies-of-proxies exception).
2. **Fuel-on-fuel dup risk (RESOURCE_CONVERSION row).** A resource player taking a resource companion risks the dual-redundancy Q8-a guards against (two economy engines, no payoff). Flagged: is resource+resource ever a valid convergence, or always a dup? Lean: dup — cut it.
3. **Same-strategy diagonal (the 25 `(X, X)` cells).** Does a player ever validly take a companion of their *own* strategy? Per Q8-a this is the purest duplication — default **all 25 diagonal cells INVALID**. Possible exception: defensive/control strategies where "two walls" or "two controllers" is genre-valid (D2 two-aura stacking). PENDING Legolas Q2.
4. **The convergence-item kicker examples (Q8-b).** The actual emergent procs per valid pair — PENDING Legolas Q3 (bond-mechanism precedent).
5. **Budget landing.** First-pass pools sum to ~70 columns across 25 rows (in range). Final count + the [L?] resolutions land the 60–80 target after Legolas.

---

## 6. What completes when Legolas returns

The pull (`legolas/research/2026-06-13-companion-convergence-precedent/`) resolves:
- **[L?] confidence calls** in § 3 (marginal pairs → keep or cut) — Q2 archetype-pairing canon
- **Exception rows 1–4** (§ 5) — Q2 (diagonal), Q3 (kicker), Q5 (isekai party-comp for the COMPANION-family rows)
- **The convergence-item emergent kickers** (Q8-b) — Q3 bond-mechanism precedent
- **Anti-pattern guardrails** — Q4 (the "companion you ignore," the mandatory-tax, the dual-damage failure) → these sharpen the INVALID side of the matrix
- **Isekai party-fantasy framing** — Q5 → the thematic naming/identity layer (companions are form-library ascended spirits; the Baby Good Mimic precedent showed identity-as-theme is valued)

After folding: produce the FINAL Q8 matrix (DRAFT-for-Matt-exception-review), seam-handoff to rocket (the valid-pair gate as a generation/selection filter) + the Session 5 companion-balance gauntlet (40K pairings sample from the valid space).

---

*Sign-off: gandalf, 2026-06-13 (scaffold). The genre never let the hero's companion be a second sword — the companion held the shield the hero could not, or healed the wound the hero would take. We are only writing down which hand reaches for which.*
