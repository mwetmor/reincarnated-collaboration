# Wave-A Engine Spec — Summon / Proxy mechanics

**Author:** gandalf (SPEC-AUTHOR) · **Date:** 2026-07-13 · **Routes to:** KR → **rocket** (generation / economy + absorption config) + **gamora** (simulation / proxy-AI / calibration).
**Inputs:** `wave-a-summon-proxy-RULINGS-2026-07-13.md` (closed forks) · `wave-a-summon-proxy-evidence-v1.md` (engine inventory + 9 gaps).
**Status:** DRAFT for specialist build. This spec authorizes *what to build*; it does not self-authorize the two engine amendments flagged §8/§9 (those escalate to KR/Matt per Gate-1 fold D).

---

## §0 — Scope & the one-line intent

Wave A makes the summon/proxy family **shippable in the dev-log catalogue** (Matt: ship the full catalogue for veteran gamers). It lifts the summon archetype from "machinery exists but gated" to "4 economies certifiable through the S6 matchup gate."

**The design north star (Fork C):** a summon kit can legitimately occupy **FREE-MOVE × BEAM** — the plane cell the genre barely ships — because the proxy absorbs the commitment the player would otherwise pay. The engine work exists to make that cell *real and balanced*, not exploitative.

---

## §1 — What already EXISTS (do not rebuild)

Per evidence-v1 inventory. Specialists build *around* these, not over them:

| Component | File | State |
|---|---|---|
| Gen→sim proxy bridge | `generation/proxy_vocabulary_bridge.py` | EXISTS + wired; emits `[]` only because the gate is down |
| Proxy decl builder | `proxy_decl_from_summon()`, `build_proxies_surface()` | ready |
| Positioned-ally spawn | `spatial_engine.py:_build_positioned_allies()` | **spawn-at-fight-start only** (no re-spawn loop) |
| Proxy lifetime + fission (count) | `proxy_population.py`, `spawn_fission_subproxy()` | lifetime tracking works; mid-fight combat-spawn unspecified |
| Proxy magnitudes (scaffold) | `proxy_commander.py` (`PROXY_REFERENCE_HP=20_000`, `PROXY_TIER_HP_FACTOR`, `PROXY_TIER_MAX_ACTIVE`) | "gamora calibrates" — numbers not set |
| Player commitment axis | `commitment_state_machine.py` | **PLAYER only** — no proxy channel model |
| Proxy targeting intent | `proxy_vocabulary_bridge.py:PROXY_TYPE_TARGETING`, `PROXY_TYPE_TIER` | targeting intent only, not full behavior branch |
| Navigator (generalized) | `spatial_engine.py:_navigate_entity()` (:1149; `player`→`nav_target` at W1) | 5 behavior branches re-path vs `nav_target` |
| Emission gate | `_DEFERRED_PROXY_BINS = {"proxy-light","proxy-heavy"}` | **DOWN** — `bc_target_cell_sampler.py:466` proxy share yields 0.0 |

---

## §2 — The four summon economies (Fork A = ALL-4)

Each economy is a **drop-rate governor** producing a distinct mobility-vs-uptime tax curve. rocket owns the gen-side config surface; gamora owns the sim-side enforcement.

| # | Economy | Engine representation | New work? |
|---|---|---|---|
| **A1** | cooldown-gated | existing `proxy_spawn_cadence_s` as a re-summon cooldown | re-summon LOOP (see §3) |
| **A2** | spend-to-summon | ties re-summon to `mana`/`focus`/`rage` spend (combat-replenishing economies exist) | cost-on-summon hook in the re-summon loop |
| **A3** | **reservation** | **NEW ENGINE MECHANIC** — a permanent reservation ceiling: each active proxy lowers the player's *regenerating-resource cap*, not a per-cast spend. No engine analog (evidence §9). | **YES — reservation-ceiling resource type** |
| **A4** | harvest/corpse | re-summon gated by a kill counter (corpse/soul token accrues on mob death, spent to summon) | kill-token accumulator + spend hook |

**A3 is the sharpest new build.** Options for rocket+gamora to weigh (rocket leans, gamora validates sim cost):
- (a) model a true `reserved` resource type where `regen_cap -= reservation_per_proxy × active_count`;
- (b) map A3 to a spend-economy approximation (simpler, loses the "army-size wall = permanent tax" fantasy).
- **gandalf lean: (a).** A3's whole identity — and the A3 abandonment-tax inversion (weakest re-drop tax, hardest leash) documented in the rulings — depends on the permanent-ceiling model. Approximating it collapses A3 into A2.

---

## §3 — B1 re-summon cadence (manual, native per-economy)

**Fork B = B1:** no auto-refresh. **Gap (evidence §3):** `_build_positioned_allies()` spawns only at fight start; there is no re-spawn loop during the fight. The population tracker handles *lifetime*, but the positioned-ally fight path has no *re-establish* mechanism.

**Build:** a fight-runtime re-summon path that, on the economy's native trigger (A1 cooldown elapsed / A2 resource available / A3 slot freed by a dead proxy / A4 kill-token spent), re-invokes the positioned-ally spawn for the freed slot. Manual = player-initiated action-slot, not a background tick.

**gamora note:** this is where the abandonment tax becomes real in sim — a proxy that dies or expires while the player has kited out of drop-range leaves a gap the player must return (or stop) to refill. The re-summon path must respect the player's position at trigger time (drop-at-player, not drop-at-dead-proxy).

---

## §4 — C3 absorption modes: channel + wind-up (the GX-19 seam)

**Fork C3 (leaned):** Wave A ships **channel-absorption + wind-up-absorption**. Life/mana **cost**-absorption rides the economy layer (§2), so no separate build.

**Gap (evidence §2):** the existing proxy seam puts *damage* on the proxy. GX-19 absorption is different — the **player's action-budget must see an "instant" cast** while the **proxy entity models the channel/wind-up duration internally**. `commitment_state_machine.py` covers only the PLAYER's commitment axis. The interaction between the proxy's absorbed-channel clock and the player's cadence clock is **undefined**.

**Build (gamora, sim seam):** a proxy-local commitment clock. When a kit has an absorption mode:
- the player's action resolves at instant cadence (no channel lock on the player entity);
- the proxy entity carries the channel/wind-up duration and ramps its output over that window;
- the absorbed commitment is **not refundable to the player as free DPS** — the ramp *is* the C1a floor made mechanical (§6).

**Canonical exhibit to match:** PoE Pizza Sticks — totem carries the Flameblast channel; player cast is instant + mobile.

---

## §5 — C2a dual / bridge plane address (data representation)

**Fork C2 = C2a:** an absorption kit occupies BOTH the player-movement cell AND the proxy-delivery cell, rendered as a tethered pair.

**Data contract (rocket emits; feeds the atlas render + S6):** an absorption kit emits **two plane addresses** plus a **center-of-gravity weight** (0.0 = fully at proxy-delivery cell / ROOTED×BEAM; 1.0 = fully at player-movement cell / FREE-MOVE×BEAM). The CoG is a **function of the kit's tuned config** (ramp floor, leash, economy, count) and **slides with progression** — low-investment CoG near proxy cell, endgame CoG near (never onto) the player cell.

**Note the S7 dependency (elrond S1 finding):** roster movement is S7-emitted, so the *player-cell* half of the dual address for the curated 45-kit roster is UNMAPPED until S7. Corpus kits (478 engine_key rows with `mob_policy_while_casting`) carry it now. This spec does not resolve that; it flags it as the render/mouseover Phase-2 gate.

---

## §6 — C1a floor + C1b endgame coordinate (balance target for S6)

The Wave-A balance target the **S6 matchup gate certifies against**:

- **C1a floor (permanent):** ramp-time + fragility, **protected from buy-out**. Ramp shortens with investment but never reaches literal-instant (illustrative floor **~0.5–0.8 s** — gamora calibrates the actual number). Proxies stay killable/expirable; count-stacking trades uptime for exposure.
- **C1b endgame coordinate (the target):** the FREE-MOVE × BEAM drop-and-forget fantasy is the **intended endgame payoff** — S6 certifies the archetype *at* this coordinate, not against a flattened-away version of it.
- **Composed:** abandonment tension asymptotes toward FREE-MOVE × BEAM; the C1a floor is the permanent asymptote gap.

**Calibration bands (gamora — the two documented failure modes, evidence §4):**
- **D3-evaporate:** proxy HP too low → killed before dealing damage. Floor the proxy survivability.
- **D2-dominance:** proxy DPS too high → player has nothing to do. Cap the drop-and-forget ceiling so the C1a floor stays felt even at endgame.
- Certify `proxy-light` and `proxy-heavy` BC cells pass the gauntlet at the correct band.

---

## §7 — Proxy-AI variant taxonomy (evidence §7 — the 12+-kit gap)

`rdr-kit-atlas-v3.csv` flags "turret/pet AI variants + summon economy needed" for 12+ kits. The engine has one nav behavior per entity; different proxy types need different AI:

| Proxy type | Behavior branch (existing in `_navigate_entity`) | Notes |
|---|---|---|
| `totem_turret` | `stationary_caster` | stays put, casts at range — the classic GX-19 host |
| `passive_fighter` (melee pet) | `melee_aggressive` | closes to `range_m`, attacks — **works today** |
| `volatile_emitter` | proximity-triggered | **NEW** — no proximity-trigger branch exists |
| `ranged_proxy` (archer) | `ranged_kite` / `cast_at_range` | **BLOCKED by §8 nav defect** |

**Build (gamora):** extend `PROXY_TYPE_TARGETING` from targeting-intent-only to a **full behavior-branch assignment** (`PROXY_TYPE_BEHAVIOR`), mapping each proxy type to its `preferred_behavior`. Add the proximity-trigger branch for `volatile_emitter`.

---

## §8 — Ranged-proxy nav defect (BLOCKING ranged-summon; escalated)

**Defect (evidence §6):** a ranged proxy parks **38.9 m** from a boss it hits at 10 m — ally-nav chases nearest-enemy adds instead of holding boss-focus at range (`spatial_engine.py:~1996` nearest-enemy nav; `:2350` attack-phase boss-focus parity). No magnitude lever moves `proxy_realized_damage_dealt`; this is a **nav mechanic**, not tuning.

**Fix candidates (gamora scopes; DO NOT self-authorize per Gate-1 fold D — KR routes):**
- (a) boss-focus **inheritance** — ranged ally adopts the player's boss-focus target;
- (b) a **hold-at-range** behavior variant — proxy maintains engagement distance vs its target;
- (c) a nav_target priority override.
- **gandalf lean: (a) or (b).** (a) is cleaner for the drop-and-forget C1b fantasy (proxy tracks what the player is fighting); (b) is more general.

**Wave-A scope consequence:** melee-summon is nav-complete and ships now. **Ranged-summon cert is BLOCKED on this fix.** Wave A can ship melee economies first and gate ranged behind the nav amendment — recommend KR sequence it that way rather than block all of Wave A.

---

## §9 — `_DEFERRED_PROXY_BINS` lift (the gate)

Lifting `_DEFERRED_PROXY_BINS = {"proxy-light","proxy-heavy"}` (evidence §(b), `bc_target_cell_sampler.py:466`) is the **switch that turns Wave A on**. Downstream machinery (bridge, decl builder, `_build_positioned_allies`) is ready. **Sequence the lift AFTER** §3 re-summon loop + §6 calibration land, else the gate opens onto uncalibrated proxy cells (D3-evaporate / D2-dominance risk in live cert). rocket owns the lift; gamora signs off on calibration readiness first.

---

## §10 — Blocking vs deferrable triage

| Gap | Wave-A status |
|---|---|
| §3 re-summon loop | **BLOCKING** (B1 requires it) |
| §2 A3 reservation mechanic | **BLOCKING** (Matt ruled all-4) |
| §4 GX-19 absorption clock | **BLOCKING** (Fork C is the north star) |
| §6 calibration bands | **BLOCKING** (S6 cert needs the target) |
| §7 proxy-AI behavior branch | **BLOCKING for typed proxies**; melee-only ships without proximity branch |
| §8 ranged-proxy nav | **BLOCKING ranged-summon only** — melee ships first (KR sequences) |
| §2 fission mid-fight combat-spawn (evidence §8) | **DEFERRABLE** — lifetime fission works; combat-spawn is post-Wave-A |
| B11 master-hides / zero-aggro taunt (evidence §5) | **DEFERRABLE** — whitespace kit; taunt-0.6 approximates, full model later |
| `poe2-archmage-totems` econ re-harvest (evidence §6) | **DEFERRABLE** — legolas re-harvest, not a build blocker |

---

## §11 — Routing & sequencing (→ KR)

1. **rocket:** economy config surface (A1–A4), A3 reservation-ceiling resource type (§2 lean (a)), C2a dual-address + CoG emission (§5), `_DEFERRED_PROXY_BINS` lift (§9, last).
2. **gamora:** re-summon fight-loop (§3), GX-19 proxy commitment clock (§4), proxy-AI behavior-branch map + proximity trigger (§7), C1a/C1b calibration bands (§6), ranged-proxy nav fix (§8 — **escalate fix-shape to KR/Matt before building**).
3. **Sequence:** melee economies (A1/A2/A4) + absorption + calibration → gate lift → S6 cert; **ranged-summon + A3 reservation** as a second slice behind the nav amendment + reservation-resource build.
4. **S6 gate certifies at the C1b endgame coordinate** with the D3-evaporate / D2-dominance bands as pass/fail rails.
