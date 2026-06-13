# Q6 / Q7 — PROXY_CONVERGENCE Matrix + DUAL_PROXY Compatibility Pools

**Author:** gandalf
**Date:** 2026-06-12
**Mode:** offline matrix drafting (Pattern B follow-on; principles ratified in dialogue, matrices drafted here)
**Status:** DRAFT for Matt exception-row review (per ruling record Q6/Q7: "gandalf drafts full matrices offline; Matt reviews exception rows only")
**Grounding:**
- Ratified principles (Matt, 2026-06-12): Q6-a, Q6-b, Q7-a, Q7-b (see § 1)
- Legolas Mode A proxy-summoner genre research (`legolas/research/2026-06-12-proxy-summoner-genre-precedent/findings.md`)
- Proxy type catalog: Session 2 spec § 2.2 (14 confirmed types)
- Strategy mechanics: Session 1 T4 spec § 3.1 (PROXY_CONVERGENCE, DUAL_PROXY)
- Serves: proxy-primary HIGH-centroid type (recognition record § 5.2) — these strategies ARE the proxy-primary composition blueprint

---

## 1. The four ratified principles (Matt, 2026-06-12)

| # | Principle | Ruling |
|---|---|---|
| **Q6-a** | Merge formula | Convergence trades **body-count/coverage for concentration at damage PARITY** — NOT a damage penalty. The genre-backwards `damage = sum × 0.8` merge-cost is RETIRED. |
| **Q6-b** | Convergence output | Each valid pair produces an **emergent named behavior** — a third tool neither parent does alone — NOT "both parents at reduced efficiency" (the discount-bundle model is retired). |
| **Q7-a** | DUAL_PROXY complementarity | "Complement" = **role complementarity.** The secondary is a force-multiplier / coverage type (tank / control / zone / support / utility), **NEVER a second co-equal damage type.** Dodges the genre's universal dual-damage failure state by construction. |
| **Q7-b** | Bridge-type | The Carrion-Golem "stronger-with-diversity" mechanic is **one type's identity**, not a global rule. Assigned to **Golem/Construct** (§ 4.3), capped per PoE scaling discipline. |

---

## 2. Proxy taxonomy — role + family tags (drafting basis)

The 14 Session-2 types, tagged by **combat role** (drives Q7 pools) and **convergence family** (drives Q6 eligibility — convergence requires two DIFFERENT families).

| # | Type | Role | Family |
|---|---|---|---|
| 1 | Passive Fighter (PF) | DAMAGE (melee/engage) | A — Strikers |
| 2 | Autonomous Caster (AC) | DAMAGE (ranged/caster) | A — Strikers |
| 3 | Golem/Construct (GO) | TANK | C — Guardians |
| 4 | Totem/Turret (TT) | DAMAGE (stationary ranged) | B — Emplacements |
| 5 | Bodyguard (BG) | DEFENSE (player-protect) | C — Guardians |
| 6 | Volatile Emitter (VE) | DAMAGE (AoE pulse) | B — Emplacements |
| 7 | Terrain Anchor (TA) | SUPPORT / ZONE | D — Field |
| 8 | Resource Conduit (RC) | UTILITY (economy) | E — Economy |
| 9 | Trap/Mine (TM) | CONTROL + DAMAGE (zone-burst) | B — Emplacements |
| 10 | Warcry/Buff Spirit (WB) | SUPPORT (buff) | D — Field |
| 11 | Fragile Escort (FE) | UTILITY (reward) | E — Economy |
| 12 | Slot-Queue Emitter (SQ) | DAMAGE (burst ranged) | B — Emplacements |
| 13 | Delayed Position Shadow (DS) | DAMAGE (echo) | F — Echo |
| 14 | Charged Threshold Proxy (CT) | DAMAGE + CONTROL (charge-burst) | F — Echo |

Six families: A Strikers {PF, AC} · B Emplacements {TT, VE, TM, SQ} · C Guardians {GO, BG} · D Field {TA, WB} · E Economy {RC, FE} · F Echo {DS, CT}.

---

## 3. Q6 — PROXY_CONVERGENCE matrix

### 3.1 Revised merge formula (Q6-a)

The Convergent Proxy is a single entity replacing both parents:

- **HP** = average(parent_A_HP, parent_B_HP) × **1.2** (survivability bump — retained; the merged body is meant to endure)
- **Damage** = sum(parent_A_dmg, parent_B_dmg) × **1.0** (PARITY; balance-loop tuning range [0.9, 1.1] — magnitude is config, not constant)
- **The tradeoff is STRUCTURAL, not numeric.** One body instead of two means: loss of AoE/positional spread (two emplacements covered two arcs; one body covers one), loss of the second aggro anchor, and a single point of failure — if the Convergent Proxy dies, the kit loses ALL proxy contribution at once, whereas DUAL_PROXY keeps fighting if one proxy falls. That structural fragility-and-concentration IS the cost. No damage penalty is layered on top (Legolas: averaged-stats is already the balance-safe combination method; a further × 0.8 double-taxes it into a trap).
- **The draw is the emergent behavior** (§ 3.2) — each fusion unlocks a tool neither parent has.

### 3.2 Eligibility + output model (Q6-b)

- **Eligibility:** kit has exactly 2 distinct Tier-1 proxy types **from different families** (§ 2 family column). Same-family pairs do NOT converge (no defined behavior; generation will not pair them).
- **Output:** an **emergent named behavior** — a qualitatively new tool, balanced as its own entity, NOT a reduced-efficiency stack of both parents.
- Generation enforces the valid-pair gate (§ 3.3); only listed pairs are generatable convergences.

### 3.3 The valid-pair matrix (33 pairs; ~30–40 budget)

Grouped by family-pair. Each row: the emergent behavior is the "third thing" — what the fusion does that neither parent does alone.

**A Strikers × C Guardians**
| Pair | Emergent name | Behavior (the third thing) |
|---|---|---|
| PF + GO | **Vanguard Construct** | Durable front-liner that auto-attacks AND taunts; gains a retaliation pulse when struck while taunting (neither parent retaliates). |
| PF + BG | **Sentinel-at-Arms** | Attacks the player's target while intercepting lethal hits; each intercepted hit empowers its next attack (stacking on-absorb damage). |
| AC + GO | **War-Idol** | Tanky caster that holds aggro and casts; its taunt radius becomes silence-on-enter for casters (denial behavior unique to the fusion). |

**A Strikers × D Field**
| Pair | Emergent name | Behavior |
|---|---|---|
| PF + TA | **Standard-Bearer** | Fights while projecting a buff/debuff zone centered on itself — the zone MOVES with the unit (parent zones are static). |
| PF + WB | **Champion** | Melee attacker emitting a player buff whose magnitude scales with the Champion's recent damage dealt (a momentum-buff neither parent has). |
| AC + WB | **Cantor** | Caster whose every cast pulses/refreshes the buff aura (cast-linked support; parent buff is presence-only). |

**A Strikers × B Emplacements**
| Pair | Emergent name | Behavior |
|---|---|---|
| PF + TT | **Skirmisher** | Engages in melee but fires ranged volleys when the target is beyond reach — dual-range delivery from one body. |
| PF + VE | **Maelstrom Fighter** | Attacks while emitting AoE pulses centered on a MOVING body (parent emitter is stationary). |
| AC + SQ | **Arc-Caster** | Alternates sustained casting with a charged burst-volley released between casts (two-cadence delivery). |

**A Strikers × F Echo**
| Pair | Emergent name | Behavior |
|---|---|---|
| PF + CT | **Reaver** | Striker that accumulates charge from its OWN hits (parent CT charges from enemy hits) and unleashes a melee burst at threshold. |
| AC + DS | **Phantom-Caster** | Caster whose delayed shadow replays only its highest-cost cast (parent shadow replays last-N generic) — a single big-spell echo. |

**A Strikers × E Economy** *(reviewable — utility-flavored, candidate-cut if matrix trims)*
| Pair | Emergent name | Behavior |
|---|---|---|
| PF + RC | **Tithe-Warrior** | Melee unit generating player resource on each hit (combat-fueled economy; parent conduit is passive/non-combat). |
| AC + RC | **Channeler** | Caster that refunds a fraction of resource on-cast — a self-sustaining cast loop. |

**B Emplacements × C Guardians**
| Pair | Emergent name | Behavior |
|---|---|---|
| TT + GO | **Bastion-Turret** | High-HP turret that draws aggro and fires (parent turret is ignored by AI priority; the fusion is targeted). |
| VE + GO | **Siege-Heart** | Tanky core that taunt-gathers enemies and then pulses them — taunt feeding its own AoE. |
| TM + GO | **Ward-Anchor** | Tank that lays proximity mines around itself as it holds ground — a self-mining bulwark. |

**B Emplacements × D Field**
| Pair | Emergent name | Behavior |
|---|---|---|
| TT + TA | **Bulwark-Tower** | Turret firing within an overlapping zone; shots gain the zone's effect (buffed / ailment-tagged rounds). |
| VE + WB | **Resonance-Pylon** | Pulses that carry the buff to allies they pass through (AoE-delivered buffing; parent buff is presence-aura only). |
| TM + TA | **Glyph-Trap** | A trap embedded in a zone; the zone arms / re-arms the trap faster while enemies stand inside. |

**B Emplacements × E Economy**
| Pair | Emergent name | Behavior |
|---|---|---|
| VE + RC | **Harvest-Bomb** *(canonical — retained from spec)* | Travels to target, explodes for AoE, converts a fraction of enemy HP lost to player resource. |
| TT + RC | **Tribute-Turret** | Turret converting a fraction of its damage to player resource (damage-linked economy). |

**B Emplacements × F Echo**
| Pair | Emergent name | Behavior |
|---|---|---|
| SQ + CT | **Siege-Battery** | Builds a projectile queue AND banks charge, releasing a doubly-amplified burst at threshold (two-axis burst, **capped** per § 4.3 discipline). |
| TT + CT | **Coil-Turret** | Turret that charges per shot and fires a piercing overcharge supershot at threshold. |

**C Guardians × D Field**
| Pair | Emergent name | Behavior |
|---|---|---|
| GO + TA | **Citadel** | Tank anchored to a zone it cannot leave — trades mobility for a larger, stronger zone (an immovable fortress). |
| BG + WB | **Shielded-Augmenter** *(canonical — REFRAMED per Q6-b)* | Intercepts a lethal hit and converts the absorbed damage into a timed party buff-burst. **NOT "70% of each"** — a new absorb-to-buff conversion. |
| GO + WB | **Warlord-Construct** | Tank whose taunt rallies a buff to allies attacking its taunt-target (focus-fire reward). |

**C Guardians × E Economy**
| Pair | Emergent name | Behavior |
|---|---|---|
| GO + RC | **Reactor-Golem** | Durable tank generating resource while it holds aggro — survival-time = resource (tanking fuels economy). |
| BG + FE | **Honor-Guard** | Bodyguard bonded to the fragile reward escort, extending its interception to cover the escort (protect-the-VIP). |

**C Guardians × F Echo**
| Pair | Emergent name | Behavior |
|---|---|---|
| BG + CT | **Retribution-Guard** | Absorbs hits, banking them as charge, then releases a CC-burst at threshold (damage-taken-to-CC; RETRIBUTION-flavored). |
| GO + CT | **Wrath-Anchor** | Taunting tank that charges from the hits it draws and bursts AoE at threshold (taunt-fed burst). |

**D Field × E Economy** *(reviewable — utility-flavored)*
| Pair | Emergent name | Behavior |
|---|---|---|
| TA + RC | **Wellspring-Zone** | A zone granting the player resource while standing in it (positional economy — stand-to-earn). |

**D Field × F Echo** *(reviewable)*
| Pair | Emergent name | Behavior |
|---|---|---|
| WB + CT | **Crescendo-Spirit** | A buff aura that intensifies as the unit banks charge, releasing a brief buff-spike at threshold (building-then-cresting buff). |

**E Economy × F Echo** *(reviewable)*
| Pair | Emergent name | Behavior |
|---|---|---|
| RC + CT | **Capacitor-Font** | Passively generates resource and banks a fraction as charge, dumping a resource-burst at threshold (trickle-then-flood economy). |

**Total: 33 valid convergence pairs.** Of 80 cross-family combinations, the unlisted ~47 have no defined convergence (generation will not pair them). The 5 *reviewable* rows (flagged) are the lowest-confidence — utility-flavored, low combat-impact — and are the first candidates to cut if the matrix needs trimming toward 30.

---

## 4. Q7 — DUAL_PROXY per-primary compatibility pools

### 4.1 Principle applied (Q7-a)

Each pool gives a primary type a set of **role-complementary** secondaries. Rule enforced throughout: **no DAMAGE primary is paired with another co-equal DAMAGE secondary.** Where the primary is a damage type, the pool is tank / defense / zone / support / utility. Where the primary is tank / defense / support / utility, a damage secondary IS offered (tank+damage = the D2 Summonmancer core; support/utility enables a damage unit). The pre-defined pool IS the enforcement — our kits are generated offline, so no live resource-budget is needed (Legolas Finding 6: soft budgets are the genre's live-choice analog of our hard pools).

> **SUPERSEDES Session 1 T4 spec § 3.1 DUAL_PROXY examples.** Those three examples were drafted before Q7-a and each violates role-separation: `PF → {…, Totem/Turret}` (damage+damage), `Volatile Emitter → {Trap/Mine, …, Delayed Shadow}` (damage+damage+damage), and `Golem → {Resource Conduit, Warcry/Buff, Fragile Escort}` (a tank with no damage complement — incomplete). The pools below replace them.

### 4.2 The 14 pools (3–4 secondaries each)

| # | Primary (role) | Compatibility pool (role-complementary secondaries) | Logic |
|---|---|---|---|
| 1 | **Passive Fighter** (DMG melee) | Golem, Terrain Anchor, Warcry/Buff Spirit, Resource Conduit | striker + aggro-anchor / zone / buff / economy |
| 2 | **Autonomous Caster** (DMG ranged) | Golem, Bodyguard, Warcry/Buff Spirit, Resource Conduit | squishy caster wants a front-line + protection + buff/fuel |
| 3 | **Golem/Construct** (TANK) | Passive Fighter, Autonomous Caster, Volatile Emitter, Warcry/Buff Spirit | tank + a DAMAGE proxy (Summonmancer core) + buff |
| 4 | **Totem/Turret** (DMG stationary) | Golem, Terrain Anchor, Bodyguard, Warcry/Buff Spirit | turret + mobile aggro-draw / overlapping zone / protection |
| 5 | **Bodyguard** (DEFENSE) | Passive Fighter, Autonomous Caster, Terrain Anchor, Warcry/Buff Spirit | bodyguard protects player while a DAMAGE proxy works |
| 6 | **Volatile Emitter** (DMG AoE) | Golem, Bodyguard, Terrain Anchor, Resource Conduit | emitter + tank to gather enemies into the pulse / zone / fuel |
| 7 | **Terrain Anchor** (SUPPORT/ZONE) | Passive Fighter, Autonomous Caster, Golem, Charged Threshold | zone enables a DAMAGE / burst unit; tank holds the zone |
| 8 | **Resource Conduit** (UTILITY) | Passive Fighter, Autonomous Caster, Golem, Charged Threshold | economy fuels a DAMAGE / charge-burst unit; tank survives |
| 9 | **Trap/Mine** (CONTROL+DMG) | Passive Fighter, Golem, Warcry/Buff Spirit, Resource Conduit | control sets up a DAMAGE payoff; tank + buff/fuel support |
| 10 | **Warcry/Buff Spirit** (SUPPORT) | Passive Fighter, Autonomous Caster, Golem, Charged Threshold | buff enables a DAMAGE / burst unit; tank carries the aura |
| 11 | **Fragile Escort** (UTILITY reward) | Golem, Bodyguard, Passive Fighter, Warcry/Buff Spirit | the fragile VIP needs protection-heavy complements + 1 damage |
| 12 | **Slot-Queue Emitter** (DMG burst) | Golem, Warcry/Buff Spirit, Terrain Anchor, Resource Conduit | burst unit + tank to survive the wind-up / buff / zone / fuel |
| 13 | **Delayed Position Shadow** (DMG echo) | Golem, Warcry/Buff Spirit, Terrain Anchor, Resource Conduit | echo + tank / buff (amplifies echoed skills) / zone / fuel |
| 14 | **Charged Threshold Proxy** (DMG+CTRL burst) | Golem, Warcry/Buff Spirit, Terrain Anchor, Resource Conduit | charge-burst + tank to survive charge-up / buff / zone / fuel |

Each pool is **role-complementary and dual-damage-free** where the primary is a damage type. Pools 3, 5, 7, 8, 10, 11 (tank / defense / support / utility primaries) deliberately INCLUDE a damage secondary — that is the complement, not a violation.

### 4.3 Bridge-type designation (Q7-b)

**Golem/Construct is the bridge-type.** When a Golem is present alongside ≥1 other allied proxy, it gains a **per-allied-proxy bonus** (damage + HP), modeling the PoE Carrion Golem "stronger-with-the-army" identity. This rewards proxy-primary diversity without bolting complexity onto every dual kit.

- **Scaling-cap discipline (Legolas Finding 10 — PoE 3.8→3.15 cautionary history):** the bonus is **capped** (e.g., +X% per allied proxy, hard cap at +Y% total) and is **one** independent scaling layer, not stacked atop multiple multiplicative proxy-scaling sources. This is the explicit guard against the genre's summoner power-explosion failure mode.
- Note: Golem appears in many DUAL_PROXY pools as the tank complement — its bridge identity makes it the natural anchor of proxy-primary kits, which is thematically correct (the Necromancer's golem is the army's keystone).

---

## 5. Exception rows flagged for Matt review

Per the ruling ("Matt reviews exception rows only"), the items that warrant a look — everything else is mechanical application of the four ratified principles:

1. **Golem-as-bridge-type (§ 4.3)** — the one net-new mechanic in this artifact. Worth confirming: Golem as the diversity-reward anchor, capped. *(Alternative considered: assign the bridge identity to Warcry/Buff Spirit instead — buff-scales-with-army. I chose Golem for the directer Carrion-Golem genre map; flag if you prefer the buff-spirit framing.)*
2. **The 5 reviewable convergence rows** (§ 3.3, flagged): Tithe-Warrior, Channeler, Wellspring-Zone, Crescendo-Spirit, Capacitor-Font — utility-flavored, low combat-impact, first candidates to cut if trimming toward 30.
3. **Shielded-Augmenter reframe** — the canonical spec example moved from "absorbs AND buffs at 70% efficiency of each" to an emergent absorb-to-buff conversion (§ 3.3, C×D). Confirm the reframe reads right.
4. **DUAL_PROXY § 3.1 supersession** (§ 4.1) — the three original spec pool examples are replaced. Flagging because it's a visible change to a ratified spec's illustrative content (the *mechanism* is unchanged; only the example pools change to honor Q7-a).
5. **Merge-formula multiplier** (§ 3.1) — damage parity at × 1.0, balance-loop range [0.9, 1.1]. The principle (parity, not penalty) is ratified; the specific range is my proposal, tunable.

---

## 6. Seam handoff (when this lands)

- **rocket** (generation): the valid-pair gate (§ 3.3 — only listed pairs are generatable PROXY_CONVERGENCE kits); the 14 DUAL_PROXY pools (§ 4.2) as config tables; the Golem bridge-bonus generation flag (§ 4.3). The § 3.1 merge-formula values are config, not constants.
- **gamora** (kernel): the Convergent Proxy entity behaviors (§ 3.3 — each emergent behavior is a ProxyCombatant behavioral spec; ~33 to implement, batchable by family-pair); the revised merge stat-formula (§ 3.1); the Golem bridge per-proxy bonus (capped) in the fight loop.
- These fold into the **proxy-primary generation-prior** work (recognition record § 5.2) — DUAL_PROXY role-separation is literally how a ~0.80-centroid proxy-primary kit composes a coherent summoner (damage-proxy + tank/control-proxy = the Summonmancer pattern).

---

*Sign-off: gandalf, 2026-06-12. The genre never let two minions merge into something weaker — the fusion was always a bargain: give up the many to forge the one. And the genre never let two minions share one job and call it depth — the second pet always held the line the first could not. We have only written down what twenty years of summoners already knew.*
