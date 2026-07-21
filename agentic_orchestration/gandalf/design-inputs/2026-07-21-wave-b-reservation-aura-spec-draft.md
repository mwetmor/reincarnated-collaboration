# Wave-B Reservation / Aura — DESIGN + FIDELITY EXTENSION (spec draft)

> **DRAFT — pre-build, pre-ratification; refreshes on Wave-A closeout; Matt ratification required before build.**

**Author:** gandalf (SPEC-AUTHOR work unit) · **Date:** 2026-07-21
**Routes to (on ratification):** KR → **rocket** (emission / config / T4-capstone surface) + **gamora** (sim consumers — aura radius/target resolution, exclusivity enforcement, swap-tax timing).
**Authority:** PAUSE-2 RULINGS (Matt, convening 2026-07-12, `agentic_orchestration/gandalf/views/v3-mechanics-leverage-v1.md`) — add-list rows 1–11 all-in; wave order Wave-A summoner → **Wave-B reservation/aura** → Wave-C trigger+mark; GX-20 econ/commitment design ratified; GX-21 + **DL-03 adopted as DESIGN LAW (streams never tax movement)**. Matt directive: draft Wave-B reservation/aura spec NOW in parallel so it is ready when Wave-A closes.

---

## §0 — READ-FIRST: this doc EXTENDS a BUILT spec; it does not duplicate it

A critical governance fact the drafting brief did not carry: **`canonical/reap-die-rise-engine/wave-b-economy-engine-spec.md` ALREADY EXISTS, is BUILT, GATE-2-PASSED (jack-ryan 2026-07-16), and pushed to engine remote `b850800`.** It is REMOTE TRUTH. Do not re-open it.

What the built spec covers (and this draft does NOT re-litigate):

| Built already (REMOTE TRUTH — `wave-b-economy-engine-spec.md`) | Where |
|---|---|
| `reservation` (RS) as a first-class `econ_bin` | built §3; `bc_target_composer._ECON_BIN_COST_TYPE_MAP` += `"reservation": ["mana","focus"]` |
| RS **resource-arithmetic** — the regen-cap tax `regen_cap −= Σ reservation while active` | built §3.2/§3.7; `resource_economy.py:60-63,240-242` (`reservation_percent`/`reservation_flat`/`reservation_resource`) |
| RS %-vs-flat **hybrid** representation (ESCALATION b → hybrid (iii)) | built §3.3; `reservation_percent` (aura, ≤0.75) + `reservation_flat` (summoner-slot, ≤25.0) |
| Per-pool total-reservation **invariants** (Σ% < 0.90; Σflat ≤ 0.75·M; composed floor `eff_cap = max(0.25·M, …)`) | built §3.6 + Gate-2 ERRATA 12/13; sim clamp `spatial_engine.py:283` authoritative |
| `persistent-condition` (PC) as the "always-on" aura/charge/proc-loop **bin** + one-active-at-a-time law (ESCALATION a) | built §2 |
| RS↔Wave-A A3 **shared consumer** — same regen-cap machinery, non-proxy carriers | built §3.7 + Gate-2 ERRATA 14 (`1a0e5e4` is the first regen-cap-tax consumer, serving both A3-flat + hybrid-%) |
| **Q27** (Matt-ruled 2026-07-13, build-true): `regen_cap −= reservation_per_proxy × active_count`, the abandonment-tax inversion | `summon_economy.py:39,59-60,73,120-137`; math note `generation/notes/wave-a-slice2-a3-reservation-math-2026-07-13.md` |

**What the built spec does NOT cover — the gaps this draft fills.** The built RS work is a *resource-economy* spec: it answers "how much of your pool does an aura cost to keep on." It does **not** answer four questions the drafting brief's 8 coverage areas demand, and grep confirms the absences:

1. **Aura RADIUS / TARGET rules under the concrete-positional battle sim** — `grep` for `capstone|aura.*radius|effect_radius` in the built spec = the built spec treats an aura purely as a `tags=["placed"]` self-centered stat-emitter for **DL-03 movement-non-tax** purposes (built §3.9/§5.4). It never says *who* the aura reaches, at *what radius*, with *what target cap*, or *what falloff*. And the sim confirms this is a real hole: **`balance_loop.py:126-127` — `aoe_radius_mod` is a NO-OP in the 1D kernel ("radius is a 2D-spatial concept")**; `MIGRATION.md:8768` — 2D positional motion is DEFERRED (LOUD-FLAG). Auras that grant benefits to *allies/proxies in range* have no positional consumer today.
2. **EXCLUSIVITY as a reservation-economy DESIGN FORK** — the built spec ruled PC one-active-at-a-time (built §2.3, ESCALATION a), but that ruling was scoped to the PC *bin's commitment model*. It did NOT decide the **genre-defining reservation fork**: D2-paladin exclusive-slot (one aura, free) vs PoE stackable-with-reservation-efficiency (many auras, each taxes) vs Grim Dawn exclusive-skill (one-active-max across a whole class of skills). That fork governs the entire feel of aura build-craft and is un-ruled.
3. **T4 / CAPSTONE hooks** — `grep capstone|T4|reservation-effic|aura-transform` in the built spec = **ZERO hits.** The proxy family got a full T4 suite (`proxy-t4-suite-spec-2026-07-02.md`, `proxy-commander-set-6-capstone-spec-2026-06-16.md`); the reservation/aura family has no capstone surface at all.
4. **ABANDONMENT / SWAP tax SEMANTICS generalized from Q27** — Q27's abandonment-tax inversion is specced for *summoner proxies* (re-drop free, standing tax hard). Whether that inversion holds — or inverts again — for *auras* (which cost nothing to re-toggle but may carry a swap-cost or a re-attunement ramp) is un-specced.

**Disposition (per the drafting rule "if partial surfaces exist, draft as extension citing them, do not duplicate"):** this doc is the **Reservation/Aura DESIGN + FIDELITY EXTENSION** — the aura-fidelity + reservation-design layer the built resource-arithmetic spec does not carry. It follows the project's established form exactly: the `wave-c-trigger-mark` and `wave-d-drain-fidelity` specs were authored as follow-on *fidelity ledgers* after the base economy spec built (`wave-d-drain-fidelity-engine-spec.md §5` — "expressibility ships first; positional fidelity is a follow-on"). This is that pattern for reservation/aura.

**Every ruling in the built spec is inherited unchanged. This doc mints NO rulings — it presents [MATT-FORK]s and leans; Matt rules.**

---

## §1 — Section list

- §0 — Read-first: extends a built spec
- §1 — Section list (this)
- §2 — What already EXISTS (do not rebuild) — the built RS/PC surface + the sim's positional primitives
- §3 — What RESERVES (the carrier taxonomy — unify auras / banners / permanent-minions with Q27)
- §4 — Reservation arithmetic vs the FOUR economies (where reservation sits; what it is NOT)
- §5 — EXCLUSIVITY rules — the genre fork **[MATT-FORK 1]**
- §6 — Aura RADIUS / TARGET rules under the concrete-positional battle sim **[MATT-FORK 2, 3]**
- §7 — T4 / CAPSTONE hooks (reservation-efficiency vs aura-transform) **[MATT-FORK 4, 5]**
- §8 — ABANDONMENT / SWAP tax semantics (generalize Q27 to auras) **[MATT-FORK 6, 7]**
- §9 — Banner / totemic-persistent carrier (the placed-aura sub-case) **[MATT-FORK 8]**
- §10 — Sim consumption points (what gamora's fight engine must resolve)
- §11 — DL-03 conformance (whole extension)
- §12 — Acceptance criteria (decidable predicates)
- §13 — Blocking vs deferrable triage
- §14 — Routing & sequencing (→ KR)
- §15 — [MATT-FORK] register (count + one-liners)
- §16 — Cross-references

---

## §2 — What already EXISTS (do not rebuild)

Two layers exist: the **built RS/PC economy surface** (§0 table — REMOTE TRUTH) and the **sim's positional primitives** this extension's aura-radius work plugs into.

**Sim positional primitives (read-only survey, 2026-07-21 on `simulation/`):**

| Primitive | File:line | State — for aura-radius purposes |
|---|---|---|
| Radius-filtered targeting | `spatial_gauntlet/spatial_engine.py:1098` (`[t for t in targets if attacker.distance_to(t) <= radius]`) | EXISTS — the exact predicate an aura radius needs; used today for attack-range filtering, not aura benefit |
| `distance_to` on combatant | `spatial_engine.py` (used throughout, e.g. :3934) | EXISTS — Euclidean 2D distance; the aura radius check is `caster.distance_to(beneficiary) <= aura_radius_m` |
| Positioned allies (proxy beneficiaries) | `spatial_engine.py:_build_positioned_allies` / `ally.proxy_proximity_radius_m` (:2483) | EXISTS (Wave-A) — allies carry positions; an aura can reach them by the same distance predicate |
| `mobs_in_range` counting | `spatial_engine.py:2620,2706,3662` (`len(alive_mobs) if geo in ("cone","circle","line")` ) | EXISTS — target-count under a geometry; an aura target-cap reuses this pattern |
| Circle-AOE radius field | `MIGRATION.md:846` (`radius_m` — meters, circle AOE) | EXISTS on the telegraph/AOE surface — an aura is a circle centered on the caster with no telegraph (friendly) |
| `aoe_radius_mod` | `balance_loop.py:126-127,140,244-250` | **NO-OP in the 1D kernel** ("radius is a 2D-spatial concept") — this is the LOUD confirmation that aura radius has no consumer today |
| Placed-zone geometry | `wave-c §5.2` placed-lane / `MIGRATION.md:8768` orbit 2D DEFERRED | placed geometry lands as an inert manifest until a fidelity wave wires the collider (Wave-C/D pattern) — banners (§9) inherit this |
| Q27 reservation config | `summon_economy.py:39,59-60,73,120-137` | EXISTS — `economy="reserved"` + `reservation_per_proxy` + `reservation_resource`; the carrier-generalization (§3) extends this, does not replace it |
| RS hybrid fields | `resource_economy.py:60-63,240-242,365-371` | EXISTS (built Wave-B) — `reservation_percent`/`reservation_flat`/`reservation_resource` + LOCKED runaway-guards |

**The one-line reading:** the *arithmetic* of reservation is built. The *positional consequence* of an aura (radius, who it reaches, target cap, falloff) has a ready primitive (`distance_to <= radius`) but **no aura consumer wired to it** — exactly the `aoe_radius_mod` NO-OP. This extension specs that consumer plus the design forks (exclusivity, capstone, swap-tax) the arithmetic spec left open.

---

## §3 — What RESERVES (the carrier taxonomy — unify with Q27)

The built spec ruled two reservation *shapes* (RS %-aura + RS flat-summoner-slot). This extension states the **full carrier taxonomy** — every persistent effect that pays a standing reservation — and unifies it with Q27 so there is ONE reservation mechanism, not a parallel system.

| Carrier class | Reserves via | Positional? | Q27 relationship | Genre exemplars |
|---|---|---|---|---|
| **A. Radius aura** (self-centered) | `reservation_percent` on maintenance pool (built RS %-shape) | **YES — §6 radius/target** | new carrier, same regen-cap machinery | PoE Grace/Determination/Herald-of-X; D2 paladin auras; D4 Auradin |
| **B. Self-only buff / stance** (no radius) | `reservation_percent` OR `reservation_flat` | NO (affects caster only) | new carrier, same machinery | PoE Malevolence (self); D2 Frenzy-charge state (built as PC one-active); Diablo werewolf/werebear form |
| **C. Permanent minion / summon-slot** | `reservation_flat` per slot (built RS flat-shape = **Q27 `reservation_per_proxy`**) | via the minion's own position (Wave-A) | **IS Q27** — the flat-shape RS *is* the summoner slot reservation; `resource_economy.reservation_flat` and `summon_economy.reservation_per_proxy` are the SAME tax on the SAME pool | D2 skeleton-slots; D3 Helltooth Gargantuan; PoE Golementalist |
| **D. Banner / totemic persistent** (placed, not self-centered) | `reservation_flat` OR `reservation_percent` while planted | **YES — §9 placed-radius** (radius centered on the PLANTED point, not the caster) | D2 Warcry/Battle-Orders-adjacent totems; PoE Ancestral banners; Last Epoch totems |
| **E. Toggle-with-tick** (built PC tick-cost sub-shape) | `persistent_tick_cost` (built PC field), NOT regen-cap | maybe (some ticks are radius zones) | orthogonal to Q27 — this is a *drain*, not a *cap tax* | PoE blood-magic-adjacent; consecrate-zone upkeep |

**The unification claim (LOAD-BEARING — this is the "unify with Q27" the brief demands):** carriers A, B, C, D all pay the **same regen-cap reservation tax on the same maintenance pool**, resolved through the **same sim consumer** the built spec already wired (`spatial_engine.py:283` clamp + the Wave-A A3 regen-cap path). Q27's `summon_economy.reservation_per_proxy` (carrier C) and the built Wave-B `resource_economy.reservation_flat`/`reservation_percent` (carriers A/B/D) are **two config surfaces feeding one arithmetic** — the Gate-2 ERRATA 14 finding already confirmed `1a0e5e4` is the single regen-cap consumer serving both. **This extension adds NO new reservation-arithmetic type.** It adds:
- the **positional layer** (radius/target) for carriers A and D (§6, §9);
- the **exclusivity layer** (§5) governing how many carriers of a class may be active;
- the **capstone layer** (§7) that bends reservation-efficiency or transforms auras;
- the **swap-tax layer** (§8) governing the cost of changing which carriers are active.

**[MATT-FORK 8]** (carrier D — banner) is deferred to §9; the rest of the taxonomy is descriptive, not a fork.

---

## §4 — Reservation arithmetic vs the FOUR economies

The brief asks for "reservation arithmetic vs the four economies." The four economies are the four *summon* economies (Wave-A Fork A: A1 cooldown / A2 spend / A3 reservation / A4 harvest). Reservation is **not a fifth peer to the four** — it is the mechanism *underneath* A3, now generalized. The mapping:

| Economy | What it prices | Does it use the reservation tax? |
|---|---|---|
| A1 cooldown-gated summon | the RE-DROP (time) | NO — cadence field |
| A2 spend-to-summon | the RE-DROP (pool draw) | NO — per-cast spend |
| **A3 reservation summon** | the STANDING army (regen-cap tax) | **YES — this IS the reservation tax (Q27)** |
| A4 harvest/corpse summon | the RE-DROP (kill token) | NO — kill accumulator |

**The generalization statement:** the built Wave-B RS bin took A3's mechanism (carrier C, permanent minion) and extended it to non-summoner carriers (A: radius aura, B: self-buff, D: banner). So reservation is the **A3 tax, applied to any persistent carrier.** It is therefore the **fourth distinct economy** in the economy-family sense — not a fourth summon-economy, but the fourth *commitment economy* (per GX-20 econ/commitment ratification): where A1/A2/A4 tax re-establishment and the spend-bins (generator-spender/starved/overflow/steady) tax casting, **reservation taxes STANDING** — the price of keeping something on.

**What reservation is NOT (guard against double-count):**
- **NOT a spend-bin.** A reservation aura does not draw the pool per-cast; it lowers the pool's ceiling while active. A kit that both reserves (aura) and spends (attack) carries `reservation_*` AND a spend `econ_bin` — the built spec's single-bin-per-emission contract (built §5.3) means the *aura's* bin is `reservation` and the *attack's* bin is the spend-bin; they are separate skills on one build, not one dual-bin skill.
- **NOT a PC tick-cost.** Carrier E (toggle-with-tick, built PC) drains per-tick; reservation lowers a ceiling. A kit MAY carry both (built §2.1 D2-Auradin: RS holy-aura + PC frenzy-charge) — the guard is §10's composed-load check.
- **NOT the ailment-layer.** Auras that amp damage compose with sunder/shock at the damage-resolver (built §5.2); the aura's *reservation* is economy, its *amp* is a stat-mod. Separate layers.

---

## §5 — EXCLUSIVITY rules — the genre fork **[MATT-FORK 1]**

This is the single most build-craft-defining fork in the whole extension, and it is **un-ruled** — the built spec's one-active-at-a-time ruling (ESCALATION a) governed the PC *commitment model*, not the reservation *exclusivity economy*. The genre has three canonical answers, and each produces a different game:

### The three genre models (by name, with what each got right/wrong FOR OUR FRAME)

- **D2 paladin auras — EXCLUSIVE-SLOT, FREE.** One aura active from the paladin's list; switching is instant and free; no resource cost at all. *Got right:* aura choice is a crisp, readable, always-live decision ("Concentration for damage OR Salvation for resist"); zero economy friction means the decision is purely tactical. *Got wrong for us:* free means there is NO commitment economy — it bypasses GX-20 entirely. A free exclusive aura is a *toggle*, not a *reservation*. If auras are free-exclusive, the whole reservation arithmetic (§4) does not apply to carrier A.
- **PoE mana reservation — STACKABLE, EACH TAXES.** Many auras active simultaneously; each reserves a chunk of the mana pool; you stack as many as reservation-efficiency lets you fit under the pool. *Got right:* the genre's richest aura build-craft — reservation-efficiency becomes a whole gearing axis; "how many auras can I fit" is a deep optimization; this is the modern validation of reservation-as-core-resource (PoE2 Spirit, cited in the leverage board row 2). *Got wrong for us:* aura-stacking is a known power-creep vector (PoE aurabot / aurastacker archetypes are perennial balance outliers, built §3.2 roster); with our per-pool Σ<0.90 invariant (built §3.6) it is bounded, but the D2-dominance failure mode (a full aura-stack that trivializes content) is real.
- **Grim Dawn exclusive skills — ONE-ACTIVE-MAX ACROSS A CLASS, RESERVED.** A designated *class* of skills (GD "exclusive skills": one aura-line per mastery) permits exactly one active, and it reserves. *Got right:* a middle path — the reservation economy is live (so GX-20 holds) but stacking is forbidden (so no aurabot creep); the one exclusive aura is a *keystone identity choice* with real weight. *Got wrong for us:* "exclusive class" needs a taxonomy of which skills are exclusive vs stackable — extra classification the emission surface must carry.

### The fork

**[MATT-FORK 1] — Aura exclusivity economy. Options:**

- **(1a) EXCLUSIVE-SLOT FREE (D2 model)** — carrier-A auras are free + one-at-a-time; `reservation_percent = 0` for auras; the "cost" is opportunity (you give up the other aura). *Tradeoff:* crisp + readable + zero balance risk; but auras stop being a reservation economy (contradicts §4 generalization and GX-20 — auras become PC toggles, and the built RS %-shape goes unused by carrier A, serving only carriers C/D).
- **(1b) STACKABLE RESERVED (PoE model)** — carrier-A auras stack; each reserves; bounded by the built Σ<0.90 per-pool invariant + reservation-efficiency (§7). *Tradeoff:* deepest build-craft + reservation-efficiency becomes a gearing axis + honors §4/GX-20 fully; but carries the aurastacker power-creep risk (needs the §7 capstone + gamora's D2-dominance calibration to contain).
- **(1c) EXCLUSIVE-CLASS RESERVED (Grim Dawn model)** — a designated exclusive-aura class permits one active + reserves; other buff-auras (heralds-adjacent) may stack cheaply. *Tradeoff:* middle path — reservation economy live, stacking bounded, keystone-choice weight; but needs an `exclusive_aura_class` tag on emission (extra classification).

**gandalf LEAN: (1b) STACKABLE RESERVED, with the §7 reservation-efficiency capstone as the containment lever.** Grounds — three, in order of weight:

1. **It is the only option that honors §4 + GX-20 + the built arithmetic.** (1a) makes the built `reservation_percent` %-shape dead code for carrier A (it would serve only summoner-slots and banners), and turns auras into free PC toggles — which contradicts the pause-2 ruling that routed reservation to econ/commitment design (GX-20). The whole reason Wave-B reservation exists as its own wave is that reservation *is a commitment economy*; (1a) removes the commitment.
2. **The corpus is aura-stacking-shaped.** The built spec's RS roster (built §3.2) is dominated by PoE %-reservation auras (Grace/Determination/Discipline/Herald + the explicit aurastacker/aurabot kits). The census growth-direction ruling (pause-2 item 3, ACCEPTED) tilts the expansion caster/summoner/aura-ward. Shipping the aura family as *free-exclusive* would misrepresent the dominant corpus shape — the same "misrepresents the corpus" argument the built spec used to rule RS hybrid (built §3.3).
3. **The power-creep risk is already bounded and has a designed container.** The Σ<0.90 per-pool invariant (built §3.6, LOCKED) hard-caps total reservation; the composed floor `eff_cap = max(0.25·M, …)` (built ERRATA 12) guarantees the player keeps ≥25% pool regardless. The remaining risk (a stack that trivializes content even under the cap) is exactly what the §7 reservation-efficiency capstone + gamora's D2-dominance band are for. We contain aurastacker, we do not ban it — matching how PoE *healthily* windows it, the same "designed-out failure mode" logic the Wave-A C1a floor used.

**Player consequence of the lean:** an aura build asks "how many auras can I fit under my pool, and how do I raise efficiency to fit one more" — the genre's richest aura decision, and a whole gearing axis (§7). Under (1a) the player would ask only "which one aura this fight" — thinner. Under (1c) "which exclusive keystone + which cheap heralds" — a good middle, and my second choice if Matt judges aurastacker-creep too dangerous for a solo-tuned game.

**Escalation:** [MATT-FORK 1] is ARCHITECTURAL — it decides whether carrier-A auras use the built `reservation_percent` at all, whether the emission surface needs an `exclusive_aura_class` tag (1c only), and whether §7's reservation-efficiency capstone is load-bearing (1b) or cosmetic (1a). Matt rules before rocket touches the composer.

---

## §6 — Aura RADIUS / TARGET rules under the concrete-positional battle sim **[MATT-FORK 2, 3]**

This is the FIDELITY heart of the extension — the `aoe_radius_mod` NO-OP made real. The built spec's `tags=["placed"]` reading answered *only* "does the aura tax caster movement" (no — DL-03). It never answered *who benefits and at what range.* Under the concrete-positional battle sim, an aura is a **circle centered on the caster (or the planted point, §9) whose radius determines which allies/proxies receive the buff and which enemies receive the debuff/amp.**

**Baseline (what lands without this section):** an aura emits a stat-mod that applies globally (or to caster-only) with no positional gate — because `aoe_radius_mod` is a 1D-kernel NO-OP and no aura-radius consumer exists. Low-fidelity outcome: expressibility ✓ (the aura's stat-mod resolves), positional fidelity ✗ (radius is meaningless; a paladin aura "reaches" a proxy 40m away exactly as one 2m away).

**Fidelity gap:** in the solo-tuned RDR sim, most auras have exactly one beneficiary set that *matters positionally* — the player's **proxies/minions** (Wave-A allies carry positions; `ally.proxy_proximity_radius_m` :2483) and **enemies** (for offensive/amp auras like consecrate). A self-only buff (carrier B) has no radius question. So aura-radius fidelity matters specifically for: (a) buff-auras with minions present (does my minion stay in aura range while it fights?), and (b) offensive/amp-auras on enemies (does the enemy have to be near me to be amped?).

### **[MATT-FORK 2] — Aura radius model. Options** (mirrors the `wave-d §5.a/§5.c/§5.d` model-options form):

- **(2a) GLOBAL (no radius) — auras are positionless stat-mods.** The aura buffs all the caster's allies + debuffs all enemies regardless of distance. *Tradeoff:* zero sim cost (reuses nothing positional; the current NO-OP behavior formalized); honest for a solo game where the player is usually near their own minions anyway. *Failure:* a "consecrated ground" aura that amps enemies-in-a-ring loses its entire identity — position stops mattering, which fights the concrete-positional sim's whole point.
- **(2b) RADIUS-GATED, HARD EDGE (D2/PoE model) — beneficiary must be within `aura_radius_m`.** Per-tick: `caster.distance_to(beneficiary) <= aura_radius_m` (the exact primitive at `spatial_engine.py:1098`). Inside = full effect; outside = none. *Tradeoff:* uses the ready primitive; matches D2 aura pulses + PoE aura AoE verbatim; makes minion-positioning and enemy-luring matter (a real tactical layer). *Cost:* per-tick distance check per beneficiary (cheap — reuses the attack-range filter pattern).
- **(2c) RADIUS-GATED WITH FALLOFF (few-games model) — effect scales with distance inside radius.** Full at center, linear/quadratic decay to edge. *Tradeoff:* smoothest; but no major ARPG models aura falloff (auras are binary in D2/PoE/D4/GD/LE) — this over-engineers against every genre precedent and adds a decay-curve field for no attested kit.

**gandalf LEAN: (2b) RADIUS-GATED, HARD EDGE.** Grounds: (1) it is the universal genre shape — D2 auras, PoE aura AoE, D4 aura-adjacent, GD auras, LE totems are ALL binary in/out (2c has zero corpus support and the built spec's whole method is "match the attested shape"); (2) it uses the primitive that already ships (`distance_to <= radius`, `spatial_engine.py:1098`) — the smallest sim lift; (3) it makes position *mean something* for auras, which is the concrete-positional sim's reason to exist and the reason `aoe_radius_mod` being a NO-OP is a defect worth fixing, not a design choice worth keeping. (2a) is the "do nothing" option and I flag it only because for a SOLO game where the player hugs their own minions, the radius rarely bites for *buff* auras — but it bites hard for *offensive/amp* auras (consecrate-ground), and those are in the corpus, so (2b) earns its keep.

**Player consequence:** under (2b), an Auradin's minions must fight *near* the paladin to keep the buff — positioning is a live decision; a consecrate-ground offensive aura means the player lures enemies onto the ring. Under (2a) neither matters. The concrete-positional sim exists to make position matter; (2b) lets auras participate in that.

### **[MATT-FORK 3] — Aura target CAP. Options:**

Under (2b), does a radius aura cap how many beneficiaries it affects, or reach everyone in range?

- **(3a) NO CAP — every ally/enemy in radius is affected.** *Tradeoff:* matches D2/PoE (auras have no target cap — a paladin buffs the whole party in range); simplest; correct for buff-auras. *Risk:* an offensive amp-aura in a large pack could amp 30+ enemies (relevant only to the aura *caster's* incoming damage, so bounded in a solo frame).
- **(3b) CAPPED for offensive auras, UNCAPPED for buff auras.** Buff-auras (help my minions) reach all; amp/debuff-auras (hurt enemies) cap at N targets (`mobs_in_range` pattern, `spatial_engine.py:2620`). *Tradeoff:* contains offensive-aura outliers; but needs a per-aura `aura_target_cap` field + a buff/debuff polarity tag.

**gandalf LEAN: (3a) NO CAP.** Grounds: no major ARPG caps aura targets (auras are the *uncapped* counterpart to capped nova/AoE skills — that contrast is part of the aura identity); in a solo frame the offensive-aura-hitting-many-enemies case affects only how much *the player* is amped-against, which the existing per-fight balance already bounds; adding a cap field + polarity tag is complexity for a risk the solo frame already contains. If gamora's S6 calibration surfaces an offensive-aura outlier, (3b) is the escalation — but ship (3a) and let cert prove the need, matching the built spec's "calibration band, not spec" discipline.

**Radius fields (rocket seam, IF [MATT-FORK 2]=(2b)):** `aura_radius_m` (float, meters, LOCKED band e.g. `[2.0, 12.0]` — gamora tunes; D2 aura radii ~2.6–8yd, PoE ~2.2m base scaling); `aura_polarity ∈ {buff, debuff, amp}` (needed only if [MATT-FORK 3]=(3b)). These are NEW emission fields on the aura carrier — additive, Discipline #12. **Sim consumer (gamora):** at the per-tick loop, gate each aura's stat-mod application by `caster.distance_to(beneficiary) <= aura_radius_m` (new helper `_aura_beneficiaries_in_radius`, deterministic, reuses `spatial_engine.py:1098`). Zero new RNG.

---

## §7 — T4 / CAPSTONE hooks **[MATT-FORK 4, 5]**

Grep of the built spec = **zero capstone/T4 surface for reservation/aura.** The proxy family has a full T4 suite; the aura family has none. This section specs the hooks. Reservation/aura is a rich capstone space — the genre's two archetypal aura-capstones are **reservation-efficiency** (fit more) and **aura-transform** (change what an aura does). Both should exist as T4/capstone targets; the fork is *which is the primary identity capstone.*

**Precedent by name:** PoE reservation-efficiency (the "Enlighten" gem + reservation-efficiency mastery — the whole aurastacker archetype is *built on* efficiency capstones); PoE aura-transform (auras that gain secondary effects at capstone — "aura effect" scaling, Guardian's aura-sharing); D2 paladin synergies (aura levels boosting other auras — a transform-adjacent capstone); the built proxy-commander-set-6 capstone pattern (`proxy-commander-set-6-capstone-spec-2026-06-16.md`) is the structural template for how a 6-set capstone reads.

### **[MATT-FORK 4] — The primary reservation/aura capstone identity. Options:**

- **(4a) RESERVATION-EFFICIENCY capstone** — the capstone lowers total reservation cost (multiplies `reservation_percent` down, or raises the effective per-pool cap toward but never past the Σ<0.90 LOCK). "Fit one more aura." *Tradeoff:* it is THE aurastacker fantasy (PoE-canonical); it is the containment lever [MATT-FORK 1](1b) needs (efficiency gates how far stacking goes, so the capstone *is* the balance dial); load-bearing under a stackable model. *Risk:* it is only meaningful if [MATT-FORK 1]=(1b) stackable — under (1a) exclusive-free there is nothing to be efficient *about*.
- **(4b) AURA-TRANSFORM capstone** — the capstone changes what the active aura DOES (a damage-aura also chills; a defense-aura also reflects; radius doubles). "Your aura becomes more." *Tradeoff:* works under ANY exclusivity model (even (1a) free-exclusive — a single powerful transformed aura); more visually/mechanically dramatic (drax presentation-friendly); a keystone-choice payoff. *Risk:* transform effects are per-aura bespoke content (each aura needs its transform authored) — heavier content lift than a single efficiency multiplier.
- **(4c) BOTH — efficiency AND transform as two capstone lines** (the full genre offering). *Tradeoff:* richest; matches "ship the full catalogue for veterans" (the Wave-A Fork-A logic); but two capstone lines to author + balance.

**gandalf LEAN: depends on [MATT-FORK 1], and I state the conditional explicitly** — this is the one place two forks couple:
- **IF [MATT-FORK 1]=(1b) stackable (my §5 lean): (4c) BOTH, efficiency-primary.** Efficiency is the load-bearing balance dial for stacking (mandatory), and transform is the flavor payoff on top. This is the full PoE aura offering and matches the veteran-catalogue mandate.
- **IF [MATT-FORK 1]=(1a) exclusive-free or (1c) exclusive-class: (4b) TRANSFORM only.** With no stacking there is nothing to be efficient about; the single/keystone aura earns a transform capstone instead. Efficiency would be dead content.

I flag the coupling loudly because ratifying [MATT-FORK 1] silently decides [MATT-FORK 4]'s viable set. Rule §5 first.

### **[MATT-FORK 5] — Capstone delivery vehicle. Options:**

- **(5a) 6-set capstone** (the proxy-commander-set-6 pattern) — a gear 6-set that unlocks the reservation/aura capstone. *Tradeoff:* structurally proven (proxy family uses it, `proxy-commander-set-6-capstone-spec`); consistent with engine convention.
- **(5b) T4-suite entry** (the proxy-t4-suite pattern) — a T4 gear slot. *Tradeoff:* also proven (`proxy-t4-suite-spec-2026-07-02.md`); finer-grained.

**gandalf LEAN: (5a) 6-set for the identity capstone (efficiency/transform), with T4-suite entries (5b) for the incremental efficiency steps.** Grounds: the proxy family already established this split (6-set = the archetype-defining capstone; T4-suite = the graduated stat entries); reservation/aura should mirror it for engine-convention consistency, not invent a third vehicle. This is a low-stakes fork (both vehicles ship elsewhere already) — I present it so the emission surface knows which table to write to, not because either is risky.

**Capstone fields (rocket seam, deferred until §5+§7 ruled):** the capstone modifies existing built fields — `reservation_percent` (efficiency multiplies it down) or a new `aura_transform_id` (transform selects a secondary effect). No new *arithmetic*; capstones ride the built reservation surface + the §6 radius surface (an "aura radius doubles" capstone multiplies `aura_radius_m`).

---

## §8 — ABANDONMENT / SWAP tax semantics **[MATT-FORK 6, 7]**

Q27 specced the abandonment-tax inversion for *summoner proxies* (carrier C): re-drop FREE, standing tax HARD (`generation/notes/wave-a-slice2-a3-reservation-math §3`). The brief asks how that inversion behaves for *auras* (carriers A/B/D). Auras differ from proxies in one decisive way: **a proxy that dies must be physically re-summoned (and can be out-run — the Wave-A leash); an aura that is toggled off can be toggled back on instantly, from anywhere, with no travel.** So the Q27 inversion needs re-examination for auras.

**The Q27 inversion (proxies, carrier C):**

| | re-drop / re-toggle tax | standing tax |
|---|---|---|
| A1/A2/A4 proxies | present (cooldown/spend/token) | none |
| A3 proxies (carrier C) | weakest (free re-drop) | hardest (permanent cap tax) |

**For auras (carriers A/B/D), the question:** an aura's re-toggle is trivially free and instant (no travel, no cooldown by default). Its standing tax is the reservation (held while on). So an aura is *even more* Q27-shaped than an A3 proxy — free to flick, taxed to hold. But that raises a design risk the proxy case did not have:

**The flicker exploit.** If re-toggle is free AND instant AND the reservation only bites *while held*, a player could toggle a costly aura ON just before a big hit (reservation drops their pool momentarily, but the aura's defensive value lands) then OFF immediately to restore regen — micro-managing reservation frame-by-frame to get aura value without paying the standing cost. PoE prevents this because reservation is *paid on activation and held* (you cannot flicker — the mana is reserved the instant it is on, and turning it off does not refund mid-fight fast enough to matter). D2 aura-swap is free but D2 auras cost nothing, so there is no flicker incentive.

### **[MATT-FORK 6] — Aura swap-tax model. Options:**

- **(6a) FREE INSTANT SWAP (D2 model)** — toggling auras is free + instant; reservation applies while held; no swap cost. *Tradeoff:* crisp + matches D2; but under a *reserved* aura (not D2's free auras) it opens the flicker exploit above — the whole reservation economy can be micro'd away by frame-perfect toggling.
- **(6b) SWAP RE-ATTUNEMENT RAMP (the flicker-proof model)** — toggling an aura ON starts a short re-attunement ramp (the aura's benefit ramps in over ~0.5–1.5s) AND the reservation is paid the instant it is on (held immediately). You cannot get the benefit faster than the ramp, so flickering ON-for-one-hit-then-OFF yields nothing (the ramp never completes). *Tradeoff:* flicker-proof; mirrors the Wave-A C1a ramp-floor logic (the ramp *is* the commitment floor made mechanical — the exact device Wave-A used for absorption proxies); a small, familiar sim addition. *Cost:* a per-aura ramp field + ramp-state on the ActiveEffect.
- **(6c) SWAP COOLDOWN (blunt model)** — a cooldown gates how often you may swap auras. *Tradeoff:* simplest flicker-prevention; but blunt (punishes legitimate tactical swaps as hard as exploitative flickers) and feels bad — no major ARPG uses aura-swap cooldowns.

**gandalf LEAN: (6b) SWAP RE-ATTUNEMENT RAMP.** Grounds — three: (1) it is the *only* option that keeps swap free-and-instant-feeling (no cooldown wall, (6c)'s fail) while closing the flicker exploit that a *reserved* aura opens (which (6a) leaves wide open); (2) it reuses the Wave-A C1a ramp device verbatim — the project already ruled "ramp = commitment floor made mechanical" for absorption proxies (`wave-a-engine-spec §6`), so this is a known, sanctioned pattern, not a new invention; (3) it makes the abandonment inversion *hold* for auras: you can flick the aura in and out freely (Q27's cheap re-establish), but you cannot get its value without paying the ramp (the standing-commitment floor), so the "free re-toggle, taxed to hold" identity survives contact with frame-perfect play. **Player consequence:** aura swaps feel free and responsive in normal play (the ramp is short), but you cannot cheese reservation by flickering — the ramp guarantees that holding an aura for its value means paying its reservation for the whole window. This is the Q27 inversion, flicker-proofed.

### **[MATT-FORK 7] — Reservation refund timing on abandonment. Options:**

When an aura is toggled OFF (or a minion dies / a banner expires), when does the reserved pool-ceiling come back?

- **(7a) INSTANT REFUND — ceiling restores the tick the carrier ends.** *Tradeoff:* matches PoE (unreserve is instant); clean; but is the *other half* of the flicker exploit — instant refund + instant re-toggle = flicker. Paired with (6b)'s ramp, the flicker is already dead (the ramp gates the *benefit*, so instant refund is safe), so under (6b) this is fine.
- **(7b) DECAY REFUND — ceiling restores over a short decay window.** *Tradeoff:* belt-and-suspenders flicker-prevention (even without (6b)); but adds a decay-state the sim must carry and feels arbitrary (why does turning off an aura slowly give mana back?).

**gandalf LEAN: (7a) INSTANT REFUND, because (6b) already kills the flicker.** Grounds: with the re-attunement ramp gating the *benefit* (6b), the *refund* side can be instant without exploit — you get your ceiling back immediately when you drop the aura, but you cannot re-acquire the aura's value faster than the ramp, so there is no flicker profit. Instant refund matches PoE (the universally-understood model, the built spec's "veterans understand it" argument, built §3.3) and avoids an arbitrary decay-state. (7b) is only needed if Matt rules (6a) free-instant-swap over my (6b) lean — in that case (7b) becomes the flicker-prevention and I would switch to leaning (7b). The forks couple: (6b)→(7a); (6a)→(7b).

---

## §9 — Banner / totemic-persistent carrier (the placed-aura sub-case) **[MATT-FORK 8]**

Carrier D (banner/totem) is a radius aura whose center is a **planted point**, not the caster. It reserves while planted (§3), and it projects a §6 radius from the plant point. It inherits every §5–§8 ruling *except* the center-of-radius question. Genre by name: PoE Ancestral banners (planted, buff-radius, no reservation in PoE but reserve-able in our frame), D2 Battle-Orders-adjacent totems, Last Epoch totems (LE reserved-mana idols are the *reservation-idol* precedent the leverage board cited).

**The placed-geometry dependency (LOUD):** placed geometry in the sim lands as an inert manifest until a fidelity wave wires the collider — this is the exact `wave-c §5.2` / `wave-d §5.d` pattern (placed-lane persistent collider was REGISTERED RESIDUE, wired in a fidelity slice, not the base wave). A banner's *radius-from-plant-point* has the same shape: the plant-point is a fixed position, and beneficiaries are gated by `plant_point.distance_to(beneficiary) <= aura_radius_m` — the same §6 primitive, different center.

### **[MATT-FORK 8] — Banner in Wave-B, or Wave-B-fidelity-follow-on. Options:**

- **(8a) SHIP banners in Wave-B** — carrier D lands with the aura family; the plant-point radius reuses the §6 consumer with a positional anchor. *Tradeoff:* completes the aura catalogue (banners are attested — LE reserved idols, PoE banners); the anchor-radius is a small delta on §6. *Cost:* needs a plant-point spawn + anchor tracking (adjacent to Wave-A's positioned-ally spawn `_build_positioned_allies`, so machinery exists).
- **(8b) DEFER banners to a Wave-B-fidelity follow-on** — ship self-centered auras (carriers A/B) + summoner-slot (C) in Wave-B; banners (D) ride a fidelity slice like the Wave-C/D placed-geometry items. *Tradeoff:* matches the established "placed geometry is a fidelity follow-on" precedent exactly; lets the base aura family ship without the plant-point spawn dependency. *Cost:* banner-carrier kits stay expressible-but-low-fidelity (or blocked) until the follow-on.

**gandalf LEAN: (8a) SHIP banners in Wave-B — IF the plant-point spawn is genuinely a small delta on Wave-A's `_build_positioned_allies`; ELSE (8b) defer.** Grounds: banners are a small, attested, high-value carrier and the radius machinery is the same §6 consumer with a positional anchor — *if* the plant-point spawn reuses Wave-A's positioned-ally spawn cheaply, there is no reason to defer. BUT the placed-geometry-is-a-fidelity-follow-on precedent (Wave-C/D) is strong and exists precisely because positional-persistent objects are where fidelity gaps hide. So this fork is **conditioned on gamora's read of the plant-point spawn cost** — I lean ship, but I defer the final call to gamora's cost assessment at Gate-1, which is the honest engineering-reality gate. Player consequence either way: banners let a build "plant a reservation" — commit pool to a fixed zone the player fights around — a distinct spatial-commitment feel from a follow-me aura.

---

## §10 — Sim consumption points (what gamora's fight engine must resolve)

Consolidated list of every sim-side resolution this extension adds (all deterministic, zero new RNG; all reuse existing primitives per §2):

| # | Consumption point | Sim site | What resolves | Depends on fork |
|---|---|---|---|---|
| C1 | **Aura beneficiary radius gate** | per-tick loop; new `_aura_beneficiaries_in_radius`; reuses `spatial_engine.py:1098` (`distance_to <= radius`) | for each active radius-aura, the set of allies/enemies within `aura_radius_m` receives the stat-mod; outside get nothing | [MATT-FORK 2]=(2b) |
| C2 | **Aura target-cap** (if capped) | `mobs_in_range` pattern `spatial_engine.py:2620` | if offensive auras cap, apply to first-N-in-radius | [MATT-FORK 3]=(3b) only |
| C3 | **Reservation-while-held** (carriers A/B/D) | pool-regen tick `spatial_engine.py:283` (the BUILT clamp) — **NO NEW ALGORITHM, extends the built consumer to non-proxy carriers** | subtract Σ active-carrier reservations from `max_pool` before regen; the built RS consumer already does this for the arithmetic — this extension only widens the carrier set to include radius-auras/banners | inherited (built §3.7) |
| C4 | **Swap re-attunement ramp** | per-tick; ramp-state on `ActiveEffect.params` | on aura toggle-ON, ramp benefit 0→full over `aura_reattune_ramp_s`; reservation paid instant | [MATT-FORK 6]=(6b) |
| C5 | **Reservation refund on abandonment** | pool-regen tick | on carrier-END, restore ceiling (instant under 7a / decay under 7b) | [MATT-FORK 7] |
| C6 | **Banner plant-point anchor + radius** | plant-spawn adjacent to `_build_positioned_allies`; radius from anchor | banner projects §6 radius from a fixed point; reserves while planted | [MATT-FORK 8]=(8a) |
| C7 | **Capstone application** | composition step (efficiency multiplies `reservation_percent`; transform selects secondary effect; radius-capstone multiplies `aura_radius_m`) | apply capstone modifiers pre-clamp | [MATT-FORK 4/5] |
| C8 | **Composed-load guard (RS + PC on one pool)** | pool-regen tick + `effect_resolver.tick_effects` | a kit with BOTH a reservation aura AND a PC tick-cost on the same pool must not drive regen below the built `eff_cap = max(0.25·M, …)` floor | inherited (built ERRATA 12) + this extension's radius-auras |

**The load-bearing sim statement:** C3 (the reservation arithmetic) is BUILT — this extension does not touch it, it only widens the carrier set feeding it. The NEW sim work is **C1 (aura radius gate)** and **C4 (swap ramp)** — both small, both reusing shipped primitives (`distance_to`, the Wave-A ramp device). C6 (banner anchor) is fork-gated (§9). Everything else is composition/capstone application on the built surface.

---

## §11 — DL-03 conformance (whole extension)

**DL-03 DESIGN LAW (Matt 2026-07-12, pause-2): streams never tax movement.** Binding check for every carrier + mechanism this extension adds:

- **Carrier A (radius aura):** the aura is a self-centered `tags=["placed"]` zone (built §3.9) — it does NOT tax caster movement; the player walks freely while the aura ticks. The §6 radius gate checks *beneficiary* distance, never *caster* movement-lock. **PASS.**
- **Carrier B (self-buff):** no zone, no movement interaction. **PASS.**
- **Carrier C (summoner-slot):** Q27 — reservation is a stat-tax on regen-cap, no stream, no movement interaction (built §3.9). **PASS.**
- **Carrier D (banner):** planted zone; the caster is free to leave the banner and move (the banner stays planted, the player roams). The banner does not root the caster. **PASS.**
- **§6 aura radius:** a *stat gate*, not a channel — the player does not stand still to "maintain" the aura; the radius simply determines who benefits at each tick as the player moves. **PASS.**
- **§8 swap ramp:** the re-attunement ramp gates the aura's *benefit* over time; it does NOT lock the player in place (the player moves freely during the ramp). It is a temporal ramp, not a positional root. **PASS.**

**CRITICAL guard against a DL-03 violation this extension could accidentally introduce:** an aura upkeep design that required the caster to *stand still* to hold the aura (a "channel to maintain" aura) would violate DL-03. **This extension explicitly forbids that** — every carrier holds via *reservation* (a resource-ceiling tax) or *tick-cost* (built PC), NEVER via a movement-taxing channel. Reservation is the flicker-proof upkeep (§8) precisely so we never need a movement-taxing "maintain" channel. **DL-03 satisfied for the whole extension by construction.**

---

## §12 — Acceptance criteria (decidable predicates)

Written as decidable predicates where possible (per drafting rule). Fork-gated criteria state their fork.

**Reservation arithmetic (inherited — already GATE-2-passed; re-assert for the widened carrier set):**
- **AC-1** (decidable): for any build with active carriers, `regen_cap_effective ≥ max(0.25·M, M·(1−min(Σ reservation_percent, 0.90)) − Σ reservation_flat)` at every tick — the built composed floor (ERRATA 12) holds when radius-auras/banners are added to the carrier set. Sim assertion at `spatial_engine.py:283`.
- **AC-2** (decidable): a carrier-A aura and a carrier-C summoner-slot reserving the same pool sum correctly (no double-count, no double-refund) — the Gate-2 ERRATA 14 single-consumer invariant holds for mixed carriers.

**Aura radius (fork-gated on [MATT-FORK 2]=(2b)):**
- **AC-3** (decidable): a beneficiary at `distance > aura_radius_m` from the aura center receives ZERO aura stat-mod at that tick; a beneficiary at `distance <= aura_radius_m` receives the FULL stat-mod. Assertion: smoke fixture with a minion walked across the radius boundary — buff toggles at the boundary tick.
- **AC-4** (decidable): a self-buff (carrier B, no radius) applies to the caster regardless of position (no radius gate on carrier B).

**Swap tax (fork-gated on [MATT-FORK 6]=(6b), [MATT-FORK 7]=(7a)):**
- **AC-5** (decidable, the flicker-proof predicate): toggling an aura ON at tick `t` and OFF at tick `t+1` yields strictly LESS than the aura's full benefit (the ramp did not complete) — flicker yields no full-value. Assertion: a fixture that toggles an aura on/off within one ramp-window measures benefit < full.
- **AC-6** (decidable): reservation is applied at the tick the aura turns ON (not after the ramp) — the pool ceiling drops immediately on activation. And restores at the tick the aura turns OFF (7a instant).

**Exclusivity (fork-gated on [MATT-FORK 1]):**
- **AC-7** (decidable, under (1b) stackable): the number of simultaneously-active auras is bounded only by the Σ reservation_percent < 0.90 pool invariant (no hard count cap) — activating an aura that would breach Σ<0.90 is blocked (built §3.6 activation-block semantics).
- **AC-7-alt** (decidable, under (1a) exclusive or (1c) exclusive-class): at most ONE aura (1a) / one exclusive-class aura (1c) is active at any tick; activating a second ends the first.

**Capstone (fork-gated, judgment where not fully decidable):**
- **AC-8** (decidable, under (4a) efficiency): a build with the efficiency capstone can hold strictly MORE total reservation-percent of auras than the same build without it, up to but never exceeding the Σ<0.90 LOCK (the capstone raises effective fit, never breaks the invariant).
- **AC-9** (judgment): the reservation/aura capstone is felt as an archetype-defining choice at S6 — a build with the capstone plays recognizably differently (more auras fit, or a transformed aura), not marginally. gamora S6 cert judges this against the D2-dominance / evaporate bands (per built RS calibration §3.10).

**DL-03 (decidable):**
- **AC-10** (decidable): NO carrier or mechanism in this extension emits a caster movement-lock — grep the emitted skill data for any aura-carrier with a `commitment_bin=channel` maintenance requirement returns EMPTY. Auras hold via reservation/tick-cost only.

---

## §13 — Blocking vs deferrable triage

| Item | Wave-B-extension status | Reason |
|---|---|---|
| §5 exclusivity [MATT-FORK 1] | **BLOCKING** — architectural; decides whether carrier-A uses the built `reservation_percent` at all + whether §7 efficiency is load-bearing | rules before rocket touches composer |
| §6 aura radius [MATT-FORK 2] | **BLOCKING for radius-auras** — decides if the aura family has positional fidelity or is positionless (2a) | the FIDELITY heart; the `aoe_radius_mod` NO-OP fix |
| §6 target-cap [MATT-FORK 3] | **DEFERRABLE via S6 cert** — (3a) no-cap ships; (3b) is the escalation IF cert surfaces an offensive-aura outlier | calibration band, not spec (built discipline) |
| §7 capstone identity [MATT-FORK 4] | **DEFERRABLE past base aura family** — auras ship without capstone; capstone is the endgame payoff layer (proxy family shipped base-then-capstone) | but COUPLED to [MATT-FORK 1] — rule together |
| §7 capstone vehicle [MATT-FORK 5] | **DEFERRABLE** — low-stakes; both vehicles ship elsewhere | emission-table selection, not risk |
| §8 swap ramp [MATT-FORK 6] | **BLOCKING under (1b) stackable** — the flicker exploit is live once reserved auras stack; DEFERRABLE only under (1a) free-exclusive (D2 auras cost nothing, no flicker incentive) | flicker-proofing is load-bearing for reserved auras |
| §8 refund timing [MATT-FORK 7] | **couples to §8 (6b)** — (6b)→(7a) instant; (6a)→(7b) decay | rule with [MATT-FORK 6] |
| §9 banner [MATT-FORK 8] | **DEFERRABLE (fidelity-follow-on precedent)** — self-centered auras (A/B) + slots (C) ship; banners (D) may ride a fidelity slice | placed-geometry-is-fidelity-follow-on (Wave-C/D pattern); gamora costs the plant-spawn |
| C3 reservation arithmetic | **NOT NEW — inherited built** | widen carrier set only |

**The Wave-B-extension MVP (what must land for the aura family to be real):** [MATT-FORK 1] ruled + §6 radius (C1) + §8 swap-ramp (C4, if stackable). Capstone (§7) and banner (§9) are the endgame + fidelity-follow-on layers, deferrable behind the MVP — exactly how the proxy family shipped (base economies first, T4/capstone after).

---

## §14 — Routing & sequencing (→ KR)

**rocket (generation / config / emission):**
- §6 aura-radius fields — `aura_radius_m` (+ `aura_polarity` only if [MATT-FORK 3]=(3b)) on the aura carrier; additive (Discipline #12).
- §5 exclusivity tag — `exclusive_aura_class` ONLY if [MATT-FORK 1]=(1c); (1a)/(1b) need no new tag (1b uses the built Σ-invariant; 1a is a one-active flag on the built PC surface).
- §8 swap field — `aura_reattune_ramp_s` on the aura carrier if [MATT-FORK 6]=(6b).
- §7 capstone surface — the 6-set / T4-suite entries (per [MATT-FORK 5]) modifying `reservation_percent` (efficiency) / a new `aura_transform_id` (transform) / `aura_radius_m` (radius-capstone). Rides the built reservation surface + §6 radius surface; NO new arithmetic.
- §9 banner — carrier-D emission (plant-point + reservation-while-planted) if [MATT-FORK 8]=(8a).
- **Does NOT re-touch** the built `bc_target_composer._ECON_BIN_COST_TYPE_MAP` reservation entry or `resource_economy.py` reservation fields — those are REMOTE TRUTH.

**gamora (sim / resolution / calibration):**
- C1 aura-radius consumer — `_aura_beneficiaries_in_radius` at the per-tick loop, reusing `spatial_engine.py:1098`. **The primary new sim work.**
- C4 swap re-attunement ramp — ramp-state on `ActiveEffect.params` (if 6b).
- C3 widen the BUILT reservation consumer (`spatial_engine.py:283`) to include radius-aura/banner carriers — NO new algorithm, wider input set (mirrors the built RS §3.7 "widen to non-proxy carriers" that Gate-2 ERRATA 14 already realized once).
- C6 banner plant-point anchor (if 8a) — adjacent to Wave-A `_build_positioned_allies`; gamora costs this and rules [MATT-FORK 8] at Gate-1.
- C7 capstone application + C8 composed-load guard — composition-step modifiers on the built floor.
- Calibration — S6 gauntlet cert of the aura family at the D2-dominance / evaporate bands (per built RS §3.10); AC-9 aura-capstone-is-felt judgment.

**Sequencing (LEAN — KR sequences):**
1. Rule the forks — **[MATT-FORK 1] first** (it gates §7 and part of §8), then 2/3/6/7 as a batch, then 4/5/8 (deferrable-layer forks).
2. **MVP slice** — §6 radius (C1) + §8 swap-ramp (C4) + carrier-set widen (C3). This makes self-centered auras (A/B) + summoner-slots (C) positionally real.
3. **Capstone slice** — §7 (after MVP certs), mirroring the proxy base-then-capstone sequence.
4. **Banner slice** — §9 (8a) as an MVP add if gamora costs it cheap, else a fidelity-follow-on (8b).
5. **S6 cert** at each slice; the aura family certifies at the D2-dominance / evaporate bands.

**Gate discipline:** this DRAFT refreshes on Wave-A closeout (Wave-A's positioned-ally spawn + the regen-cap consumer are the primitives §6/§9/C3 build on — confirm their final shape at Wave-A close before this goes to Gate-1). Then DRIFT-CRITIC (gandalf-prime) + Gate-1 (jack-ryan) per the built Wave-B/C/D chain, then build.

---

## §15 — [MATT-FORK] register

**Count: 8.**

1. **[MATT-FORK 1] Aura exclusivity economy** — (1a) exclusive-free D2 / (1b) stackable-reserved PoE / (1c) exclusive-class-reserved Grim Dawn. **Lean (1b) stackable** — only option honoring §4+GX-20+the built arithmetic; corpus is aura-stacking-shaped; creep is bounded by Σ<0.90 + contained by §7 efficiency capstone.
2. **[MATT-FORK 2] Aura radius model** — (2a) global-positionless / (2b) radius-gated-hard-edge / (2c) radius-with-falloff. **Lean (2b)** — universal genre shape, reuses the shipped `distance_to<=radius` primitive, makes position matter (the `aoe_radius_mod` NO-OP fix).
3. **[MATT-FORK 3] Aura target-cap** — (3a) no-cap / (3b) capped-offensive-uncapped-buff. **Lean (3a) no-cap** — no ARPG caps aura targets; solo frame bounds the risk; (3b) is the S6-cert escalation if needed.
4. **[MATT-FORK 4] Primary capstone identity** — (4a) reservation-efficiency / (4b) aura-transform / (4c) both. **Lean: COUPLED to Fork 1** — (1b)→(4c) efficiency-primary; (1a)/(1c)→(4b) transform-only.
5. **[MATT-FORK 5] Capstone vehicle** — (5a) 6-set / (5b) T4-suite. **Lean (5a) 6-set for identity capstone + (5b) T4 for incremental efficiency** — mirrors the proxy family's split.
6. **[MATT-FORK 6] Aura swap-tax** — (6a) free-instant / (6b) re-attunement-ramp / (6c) swap-cooldown. **Lean (6b) ramp** — flicker-proof without a cooldown wall; reuses the Wave-A C1a ramp device; keeps Q27's inversion holding for auras.
7. **[MATT-FORK 7] Reservation refund timing** — (7a) instant / (7b) decay. **Lean (7a) instant** (couples to 6b) — the ramp already kills flicker, so refund can be instant + PoE-familiar; (7b) only if Matt rules (6a).
8. **[MATT-FORK 8] Banner carrier timing** — (8a) ship-in-Wave-B / (8b) fidelity-follow-on. **Lean (8a) IF gamora costs the plant-spawn cheap on Wave-A's positioned-ally spawn; ELSE (8b)** — conditioned on the engineering-reality gate; placed-geometry-is-fidelity-follow-on precedent is strong.

---

## §16 — Cross-references

- `canonical/reap-die-rise-engine/wave-b-economy-engine-spec.md` — **the BUILT spec this extends** (RS/PC arithmetic = REMOTE TRUTH; §0 table maps what is inherited). Do not re-open.
- `agentic_orchestration/gandalf/design-inputs/wave-a-engine-spec-2026-07-13.md` — Wave-A form model; §2 A3 reservation = carrier C; §6 C1a ramp device = §8 swap-ramp precedent; §5 positioned-ally spawn = §9 banner + §6 radius primitive.
- `agentic_orchestration/gandalf/design-inputs/wave-a-summon-proxy-RULINGS-2026-07-13.md` — Q27's Fork-A/C rulings.
- `~/Games/reincarnated-engine/src/reincarnated/generation/notes/wave-a-slice2-a3-reservation-math-2026-07-13.md` — **Q27 build-true math note** (the abandonment-tax inversion §3 that §8 generalizes to auras).
- `~/Games/reincarnated-engine/src/reincarnated/generation/summon_economy.py:39,59-60,73,120-137` — Q27 config surface (`economy="reserved"`, `reservation_per_proxy`, `reservation_resource`).
- `~/Games/reincarnated-engine/src/reincarnated/generation/resource_economy.py:60-63,240-242,365-371` — BUILT Wave-B RS fields + LOCKED runaway-guards.
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py:1098` — the `distance_to <= radius` primitive §6 reuses; `:283` = the BUILT reservation clamp C3 widens; `:2483` = `proxy_proximity_radius_m`; `_build_positioned_allies` = §9 plant-spawn base.
- `~/Games/reincarnated-engine/src/reincarnated/simulation/balance_loop.py:126-127` — the `aoe_radius_mod` NO-OP (the LOUD confirmation aura radius has no consumer today; §6 fixes it).
- `canonical/reap-die-rise-engine/proxy-t4-suite-spec-2026-07-02.md` + `proxy-commander-set-6-capstone-spec-2026-06-16.md` — the T4/6-set capstone vehicle precedents (§7 [MATT-FORK 5]).
- `canonical/reap-die-rise-engine/wave-c-trigger-mark-engine-spec.md §5` + `wave-d-drain-fidelity-engine-spec.md §5` — the **fidelity-ledger form** this extension mirrors (expressibility-first, positional-fidelity-follow-on; placed-geometry-as-residue).
- `agentic_orchestration/gandalf/views/v3-mechanics-leverage-v1.md` PAUSE-2 RULINGS — the governing add-list + wave order + GX-20 + DL-03-as-law authority.

---

**Signed:** gandalf (SPEC-AUTHOR), 2026-07-21. **DRAFT — pre-build, pre-ratification; refreshes on Wave-A closeout; Matt ratification required before build.** This extension mints no rulings; it presents 8 forks with leans. The built reservation arithmetic is REMOTE TRUTH and untouched — this doc adds the aura-positional-fidelity + exclusivity + capstone + swap-tax layers the arithmetic spec left open, mirroring the project's established base-then-fidelity form. The conductor reviews and commits.
