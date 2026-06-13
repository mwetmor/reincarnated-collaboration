# Session 1 Rulings — Q1–Q10 + T4 Catalog Expansion to 25 Strategies

**STATUS:** RATIFIED — Matt, 2026-06-12 (Pattern B session; "I agree with and approve all of what you have listed for Session #1" + "I like them all. approved")
**Author:** gandalf
**Anchors:** Session 1 spec (`2026-06-12-session-1-t4-architecture-spec.md`); Session 3/4/5 specs; qd-engine-bc-axes-lock § 3; five-session-cascade legibility verdict
**Propagation map:** § 7 below

---

## 1. Q1–Q10 rulings

| Q | Ruling (Matt-ratified) |
|---|---|
| **Q1 — DEFENSIVE_TRADEOFF mana shield** | Absorption **50% of incoming damage routes to mana**; coverage **5 elements only** (immunity owns shadow+holy — clean 2/7 immune + 5/7 shielded partition); depletion **spill-to-HP** (graceful degradation, no exposure cliff); activation **always-on passive** while skill slotted; mana-per-damage conversion **1:1 baseline, gear-scalable** (the HIGH-investment hook). Unblocks gamora mana-shield mechanic + rocket mana shield skill. |
| **Q2 — chain count** | **Generation parameter.** Rocket samples chain count from {2, 3} (weighted), fills chains subject to 5–6 skill kit total. T4 node count fixes per Session 1 § 2.1. Rocket retires placeholder. |
| **Q3 — DDA retirement migration** | **Re-evaluate** — Season 001010 corpus reruns the gauntlet without DIRECT_DAMAGE_AMPLIFICATION. No grandfathering; corpus must be reproducible by the current generator. |
| **Q4 — GEOMETRY_COLLAPSE lock** | Collapse: **non-dominant-bin skills convert to the dominant bin's delivery**. Amplification: **1.4× to dominant-bin skills** (provisional-calibration start; Phase-4 DDA lesson — start modest). Multi-geometry kits below the 60% dominance gate: **ineligible, no secondary-collapse mechanic** (complexity cut). |
| **Q5 — RESOURCE_CONVERSION lock** | Overflow applies to **all energy types**; conversion produces **damage** (amplified next skill / burst proc — utility unmeasurable in current sim vocabulary); ratio calibrated so a deliberately-overflowing rotation is **competitive with, not superior to,** a clean rotation. Charge-stack stacks-at-cap conversion composes with Q9. |
| **Q6/Q7/Q8 — matrices process** | **Principles ruled in dialogue; gandalf drafts full matrices offline** (with Legolas Mode A genre-precedent pull: D2 necro army, PoE spectre/zoomancer, Last Epoch minion pairing); **Matt reviews exception rows only.** Budgets: ~30–40 of 196 (Q6), 3–4 secondaries per primary (Q7), ~60–80 valid convergence pairs (Q8). **Sequencing: Q6/Q7 principles fire AFTER the proxy-primary architecture question lands** (matrices serve a pillar, not a facet — see § 5). Q8 pairing is **variant-agnostic** (strategy-level; PROPAGATION/PERSISTENCE pair as single strategies). |
| **Q9 — charge-stack hold-vs-spend** | **Spend-all stays + passive per-stack bonus while held; rocket varies passive-vs-burst magnitudes per kit** so the rotation solver yields hold-optimal kits (measure into locked charge-stack bin) and spend-optimal kits (generator-spender). Zero lock amendment. **Un-holds gamora handoff Item 4 + rocket handoff Item 10.** |
| **Q10 — faction coverage gap** | **Redraw the 8 faction boundaries so all 14 lineages land non-degenerately; if mesoamerican / sub_saharan_african / south_southeast_asian genuinely don't fit, add ONE composite ninth faction** designed as a real home — never absorption-by-default, never token factions. Rocket's nearest-match logging (already dispatched) supplies the routing data for the redraw. |

## 2. T4 catalog expansion — four new strategies (21 → 25)

All four enter the Session 1 § 3 catalog. Magnitude numbers are PROVISIONAL pending implementation calibration (same posture as COLLAPSE's 1.4×).

### 2.1 GEOMETRY_PROPAGATION (GEOMETRY family) — two Layer 2 variants

**Design intent:** the perpendicular to COLLAPSE. Collapse modifies static geometry (breadth→depth); PROPAGATION modifies dynamic geometry — events beget events (depth→breadth). Value is **density-conditioned** (the genre's self-balancing: Corpse Explosion is worthless vs a lone boss). Genre: D2 Corpse Explosion, PoE Herald of Ice / Profane Bloom / Inpulsa's, D3 Area Damage, Torchlight 2 overkill transfer.

| Variant | Mechanic | Eligibility |
|---|---|---|
| `geometry_propagation_cascade` | Kills during AOE skills spawn a secondary burst at the corpse (radius ~2 tiles; damage ~50% of killing skill); bursts can re-chain on their own kills, **recursion cap 3 generations** (FISSION-style bound). Price: base AOE magnitude reduced ~15% (funds the cascade). | Predicted Axis 2 ∈ {small-AOE, large-AOE} |
| `geometry_propagation_overkill` | A fraction (~50%) of overkill damage on a killing hit splashes concentrically to nearest enemies within ~4 tiles; additionally hits above a per-kit magnitude threshold splash ~20%. | Predicted Axis 2 = single-target dominant |

**Pass/fail (gamora):** secondary events appear in `damage_event_log` with T4 attribution; recursion cap enforced; **lone-boss sanity check — propagation contribution ≈ 0 in Push single-boss config** (the price is real); zero regression on non-propagation kits.

**What it solves:** chain/multi-spawn-adjacent Axis 2 cell coverage (Test 3); single-target kits gain a priced clear story without changing bin philosophy.

### 2.2 RETRIBUTION_ENGINE (DEFENSE family)

**Mechanic:** ~40% of post-mitigation damage taken accumulates in a vengeance pool (capped); the next damage skill discharges the pool as bonus damage. When `energy_type = rage`: hits taken additionally generate rage. **Not flat thorns** — pure reflect scales with enemy damage, not player build; stored-conversion keeps the player's skills as the delivery vehicle.

**Eligibility:** predicted Axis 4 ∈ {tank, mitigator}.
**Kernel cost:** cheap — shares SACRIFICE_ASCENDANCY's on-damage-taken hook.
**Pass/fail (gamora):** pool accumulation ±5% of formula; discharge attributed to T4; kits exhibit the **damage-taken-converts Axis 5 signature** (resource/output gains correlated with damage-taken events).
**What it solves:** the structurally-dead `damage-taken-converts` Axis 5 bin (Gap 1); tanks gain offensive identity (D3 Thorns Invoker set, Grim Dawn retaliation, rage-on-hit Barbarian).

### 2.3 PERSISTENCE_ENGINE (COMBAT family) — two Layer 2 variants

**Design intent:** the sustained/even archetype's champion — the catalog's first mechanically interesting T4 that pushes AWAY from spike. Genre: PoE Righteous Fire / poison stacking, D2 poison Necromancer, Last Epoch DoT builds.

| Variant | Mechanic |
|---|---|
| `persistence_uptime` | Damage dealt in every consecutive 1.0s window for ~4s grants a ramping multiplier (~+5%/s, capped ~+40%); a missed window resets it. Uptime IS the build. Serves beam/periodic/channel kits. |
| `persistence_saturation` | While ≥~6 DoT stacks are active across enemies: ~+25% damage AND any hit refreshes existing stack durations. Stack-maintenance mastery. |

**Eligibility:** ≥2 skills with periodic trigger OR stacking DoT (Layer 2 structural).
**Pass/fail (gamora + telemetry):** uptime multiplier tracks window continuity; saturation refresh fires; PERSISTENCE kits measure even `front_load_profile` + flat/variable Axis 3B at rates above catalog mean.
**What it solves:** Gap 2 — Test 2's even-population criterion + Test 3's Axis 3B flat ≥5% gain a deliberate driver; the flat/even quadrant's capstone shelf is no longer only the ELEMENT_CONVERSION multipliers.

### 2.4 PHASE_MOMENTUM (DEFENSE family)

**Mechanic:** each ~1s window without taking a hit builds 1 Phase stack; at ~5 stacks the player enters Phase state (~+20% movement, ~+25% damage, ~6s); the next hit taken during Phase consumes ALL stacks and negates that hit; stacks reset. Avoidance-streak converts to offense — PoE Raider's onslaught/phasing identity.

**Eligibility:** predicted Axis 4 = dodger.
**Pass/fail (gamora):** stack accrual on no-hit windows; Phase trigger at threshold; hit-consumption negation fires once per Phase; dodger telemetry divergence visible.
**What it solves:** Gap 3 — the dodger bin's empty capstone shelf (Phantom/Windrunner labels gain a mechanical voice).

### 2.5 Layer 2 capstone assignments (Session 3 § 1.5 table additions)

| T4 strategy | Capstone Layer 2 assignment |
|---|---|
| GEOMETRY_PROPAGATION (cascade) | `trigger=on_kill`, `stackability=non_stacking`, `magnitude_pattern=flat`, `scaling_pattern=player_level` |
| GEOMETRY_PROPAGATION (overkill) | `trigger=on_hit`, `stackability=non_stacking`, `magnitude_pattern=scaling`, `scaling_pattern=player_level` |
| RETRIBUTION_ENGINE | `trigger=on_take_damage`, `stackability=non_stacking` (pool, not stacks), `magnitude_pattern=flat`, `scaling_pattern=gear_tier` |
| PERSISTENCE_ENGINE | `trigger=periodic`, `stackability=non_stacking`, `magnitude_pattern=escalating`, `scaling_pattern=elapsed_time` |
| PHASE_MOMENTUM | `trigger=threshold_stack` (Phase stacks), `stackability=stacking_capped_5`, `magnitude_pattern=threshold_burst`, `scaling_pattern=player_level` |

### 2.6 Family table update (Session 1 § 2.2)

| Family | Strategies (post-expansion) |
|---|---|
| ELEMENT | ELEMENT_CONVERSION_MONO / _HYBRID / _PHYSICAL, ELEMENTAL_ECHO |
| DEFENSE | DEFENSIVE_TRADEOFF, SACRIFICE_ASCENDANCY, **RETRIBUTION_ENGINE**, **PHASE_MOMENTUM** (max-1 rule preserved — all four are damage↔defense conversions) |
| GEOMETRY | GEOMETRY_COLLAPSE, GEOMETRY_INVERSION, **GEOMETRY_PROPAGATION** |
| RESOURCE | RESOURCE_CONVERSION, TEMPORAL_CHARGE, MOMENTUM_CASCADE |
| PROXY | PROXY_ASCENSION, PROXY_SOVEREIGNTY, PROXY_FISSION, PROXY_INVERSION, PROXY_CONVERGENCE, DUAL_PROXY |
| COMPANION | COMPANION_CONTRACT, MONSTER_PACT |
| COMBAT | NETWORK_AMPLIFIER, RESONANCE_LOOP, ELEMENTAL_ECHO, **PERSISTENCE_ENGINE** |

**Count: 25 strategies.** Q8 convergence matrix runs at strategy level (variant-agnostic), now 25×25 ≈ select ~60–80 valid.

## 3. Validation amendments (Session 5)

1. **Test 3 dodger divergence criterion (NEW):** Axis 4 dodger-bin kits show divergent damage-avoided telemetry (avoidance events per fight) vs mitigator/tank/glass. Non-circular — the bin is stat-defined; the metric is behavioral. The dodger bin was previously invisible to validation.
2. **Test 5 three-way comparison (AMENDED):** HIGH-cognitive-load-with-RESONANCE_LOOP vs HIGH-without-RESONANCE_LOOP vs LOW. De-confounds complexity penalty from single-strategy tuning.
3. **Flag 4 generation prior (NEW, rocket):** cognitive-load HIGH bin ≥ ~8% of in-band corpus with ≤50% of the HIGH bin carrying RESONANCE_LOOP — forces the 4-chain stacked-state route (e.g., TEMPORAL_CHARGE + NETWORK_AMPLIFIER + SACRIFICE_ASCENDANCY = 19.5 HIGH, no Resonance).

**Root-cause record (the finding behind §§ 2–3):** the 21-strategy catalog answered "what makes a build exciting" twenty-one ways and "what makes a build enduring" zero ways — burst-biased across magnitude_patterns (threshold_burst ×3, burst_spike ×2, escalating). Gaps 1–3 + Flag 4 are the systematic correction. Matt independently held one-two of these before the audit; full cross-matrix at the Session 1 dialogue transcript.

## 4. Proxies-of-proxies ruling

**Proxy entities do NOT summon their own proxies.** Genre precedent exists (PoE minions-of-minions: summoning spectres, Herald secondary minions) and is uniformly cautionary — the genre's most notorious jank source (AI pathing, attribution chaos, performance cliffs). **PROXY_FISSION is the one sanctioned exception:** death-triggered, recursion-capped, 4-entity max. GEOMETRY_PROPAGATION's cascade recursion cap (3 generations) follows the same bounding discipline for damage events.

## 5. Proxy-primary architecture — CHARTERED (recognition record)

Companion recognition record: `2026-06-12-proxy-primary-architecture-recognition.md`. Summary: the canonical ARPG trichotomy is physical / caster / **summoner** (Legolas finding, 20-year corpus); our architecture types (Session 4 § 1.1) encode only damage-scaling architectures; the measurement layer already reserves the summoner's seat (Axis 2A, multi-spawn bin, Invoker label, proxy-gear investment row). **Commitment deferred per recognition → validate → commit:** empirical gate = post-gamora-Items-1-2 smoke population testing whether `proxy_contribution_pct` can reach ~0.5 under current modifier math. Q6/Q7 principles sequence AFTER this lands.

## 6. What remains open after these rulings

| Item | Gate |
|---|---|
| Q6/Q7 principles dialogue | Proxy-primary empirical gate (§ 5) |
| Q8 matrix drafting | Q6/Q7 principles + Legolas pull |
| Proxy-primary architecture commit | Smoke-population `proxy_contribution_pct` data |
| New-strategy magnitude locks | Implementation calibration (provisional numbers in § 2 are starting bids, COLLAPSE-1.4× posture) |
| Session 3 Q3 (front_load window), Q4 (chain sequence_depth), Q6 (displacement CC); Session 4 Q1–Q7 | Future dialogue / generation testing |

## 7. Propagation map

| Consumer | What changes |
|---|---|
| **Session 1 spec** | § 1.2 strategies 5–6 lock (Q4/Q5); § 2.2 family table (§ 2.6 above); § 3 + four strategies; § 5 mana shield ruled; § 8 questions resolved |
| **Session 3 spec** | § 2.3 Q9 RESOLVED; § 1.5 capstone table + 5 rows (§ 2.5 above) |
| **Session 4 spec** | § 1.1 proxy-primary architecture type PENDING empirical gate; § 4.6/§ 6 Q10 redraw direction |
| **Session 5 spec** | Test 3 dodger criterion; Test 5 three-way; Test 3 Axis 5 coverage note (damage-taken-converts now reachable) |
| **Gamora dispatch** | Item 4 UN-HELD (Q9 ruled); five new-mechanic implementation contracts queue behind Items 1–5 |
| **Rocket dispatch** | Item 10 UN-HELD (Q9 ruled); Q2 chain-count parameter ruling; Flag 4 prior added to scope |
| **Jack-ryan** | Decisions-log entry proposal: Q1–Q10 rulings + catalog expansion (KR routes) |

---

**Sign-off:** gandalf, 2026-06-12. Matt verbatim ratifications: "Also, I agree with and approve all of what you have listed for Session #1 above including Both as Layer 2 variants under these names: geometry_propagation_cascade, geometry_propagation_overkill" + "I like them all. approved" + proxies-of-proxies agreement.
