# Proxy-combat architecture — DECISION PACKET (Track 2 HARD-STOP output)

**Status:** KR-assembled decision packet. Track 2 of the combined autonomous run produced a **decision packet, not a subsystem** — no production spatial-combat code, no `_DEFERRED_PROXY_BINS` lift, no proxy kit emitted (all verified by inspection; production `spatial_engine.py` / `proxy_population.py` git-diff = 0 lines). This packet is what Matt needs to make the §2 Matt-halt 3 architecture call: **build Track-2-proper / re-scope / park.** The build, the un-defer, and the 25% emission are NOT in this run and remain Matt's two reserved decisions.

All artifacts LOCAL on `main`, NOT pushed (ADR-006).

---

## 1. The question this packet answers

The genre's primary single-target caster path — proxy/summoner — is reserved at ~25% in the BC cell roster but DEFERRED at composition (`bc_target_composer.py:318-322`, "sim is solo-only; proxy-creation mechanics absent") because the spatial sim measures proxy **contribution-for-classification** only: proxies deal NO spatial damage and take NO position (the COUNT≠CONTRIBUTION cut). This packet brings to the edge of decision: **can a summoner cross that cut and fight — kill the boss — as a real graded build, and what does it cost to build?**

## 2. The three findings (spec → gate → spike)

### T2.1 — Spatial-proxy-combat spec (gamora `6e7f4d5` `gamora/v-spatial-proxy-combat-spec-1`; rocket gen addendum `3069db9` `rocket/v-proxy-gen-interface-addendum-1`)

The cut is crossable as an **EXTENSION**, not a fight-engine rewrite: promote proxies into an **allegiance-filtered realized entity loop**, reusing the existing navigator (`_navigate_entity`), geometry resolver (`_compute_*_hits`), damage path (`_apply_skill_damage` — already target-agnostic, decrements `target.hp`), and the existing survive-and-kill outcome gate. Only two sites hard-wire "mob" (`_navigate_entity:954` player-target; `[player]+mobs` world `:1662`). The ONE new concept is `allegiance ∈ {player, ally, enemy}` as a clean filter.

**`proxy_max_active` does the boss-grading for free:** max sustained army DPS on a single boss = `proxy_max_active × per_proxy_dps` — a hard ceiling that puts a capped army on the kill-time edge (the mechanism behind the W-C spike's LOW-EDGE @ boss / IN @ open_arena split).

### T2.2 — Gate-1 design review

- **jack-ryan DESIGN-MODE: ENDORSE-WITH-CONCERNS** (`qa/findings/2026-06-21-t2.2-proxy-combat-gate1-design.md`, collab `6b9d879`). Verified first-hand that `_apply_skill_damage` is genuinely allegiance-agnostic and the two hard-wired "mob" sites are the only two — **the extension-not-rewrite claim survives scrutiny in KIND.** The COUNT≠CONTRIBUTION boundary is crossed cleanly (the cancelled selector and the realized fight stay two distinct instruments; conflating them re-introduces the capstone §6 circularity). **The scope-honesty concern:** rocket's "seam never soldered" finding is factually correct (`grep -rl '"proxies"' exports/` = 0; sim reads `class_dict.get("proxies", [])` empty-default at `:2399`) — the dict the spec says generation will "emit into" does not exist. So "2-3 waves" is defensible only when the generation column is counted as a first-class ~1.5-wave prerequisite, not folded invisibly into calibration.
- **gandalf design-fit (KR self-assessed against pre-registered ENDORSE criteria — no PARK trigger fired, gandalf NOT woken): ENDORSE.** All four criteria structurally met: (1) solo byte-identical at `proxy_bin=solo` (empty-decl-gated, verified); (2) proxy boss-kill graded (count wall); (3) player relevant — `0 < s_baseline < 1` hard-enforced at emit (`partition_roller.py:343`); (4) one shared survive-and-kill gate, no special-cased proxy gate. No PARK trigger: no autonomous-AI fork (minimal-change path chosen; fork-line named §7.3 but not crossed), no proxy-only ship gate, and the scope is extension-pattern, not a multi-month rewrite.

### T2.3 — Throwaway de-risk spike (gamora `77215af` `gamora/v-proxy-combat-derisk-spike-1`; THROWAWAY harness, production untouched)

**The load-bearing unknown — does a fighting army kill the boss? — answered: YES, and the extension-not-fork line HELD in practice.** The realized cross wired entirely as a `_step_proxy_population` replacement reusing existing engine state + the existing `boss_killed`/`mini_boss_killed` gate, zero special-casing. **This is a WAVE, not a roadmap item.**

Boss-shell results (`boss_with_adds`, 60k HP): caster-alone WR **0.08** (times out 11/12 seeds) → cap-2 army **0.08** → cap-4 **1.00** → cap-6/8 **1.00**. Clear-time collapses monotonically **225s → 47s → 35s → 26s** across the cap sweep. The army is genuinely load-bearing.

**The valuable twist (prediction 1 falsified as a stable band):** under the CURRENT boss encounter model (95% boss armor + self-heal → the player never dies; every non-win is a timeout), the boss is a **DPS-race against a fixed 240s clock**, so win-rate snaps 0→1 as mean-TTK crosses the timeout — the genuine grading lives on the **TIME axis** (clear-time), not the binary-WR axis. A graded WR window exists only on a ~5%-wide per-proxy-DPS knife-edge. Predictions 3 (count wall binding — HELD strongly on time) and 4 (selector ≠ realized WR — HELD strongly: `contribution_pct` rises smoothly 0.47/0.64/0.73/0.78 while WR steps 0.08/1.0/1.0/1.0) confirmed.

## 3. SCOPE — stated honestly (the load-bearing input for Matt's call)

**Total: an EXTENSION of ~4 waves across 3 seams (asymmetric), behind the Matt-reserved `_DEFERRED_PROXY_BINS` lift (the real T0).**

| Wave | Seam | Work |
|---|---|---|
| **G1 (prereq)** | generation (rocket) | proxy vocabulary-bridge: gen→sim translator (gen speaks `proxy_power_per`/`proxy_geometry`/`proxy_max_active`; sim speaks `damage_multiplier`/`base_hp`/`range_m`; **no translator exists**) |
| **G2 (prereq)** | generation (rocket) | proxy stat-surfaces: emit `base_hp`, fighting-proxy `damage_multiplier`, `proxy_max_active` setting-mechanism, geometry→`range_m` map (all net-new; no `proxies` key in any exported class JSON today) |
| **W1** | sim (gamora) | allegiance + positional spawn; generalize the 2 hard-wired "mob" sites to allegiance-filtered sets. Solo byte-identical. **The genuine untested question** (spike caveat): does `_navigate_entity`'s hard-coded `player` target generalize cleanly to nearest-enemy mob→proxy re-pathing? |
| **W2** | sim (gamora) | realized damage + targetability/death (the cross proper). Depends on G1/G2 (sim can't test a fighting proxy until gen emits one). |
| **W3** | sim + design | calibration against `boss_with_adds`/`mini_boss` + **the encounter-model design question** (see §4). |
| **G3 (separable)** | generation | Beast-Taming mob-capturable tag + tamed-proxy stat inheritance (heaviest single net-new item; separable) |
| telemetry | star-lord | one additive `proxy_realized_damage_dealt` field, likely internal-to-seam + MIGRATION (star-lord's call at build) |

G1/G2 are **coupled prerequisites** to W2 — the gen→sim proxy seam was specified at both ends and never soldered in the middle. Not a multi-month rewrite, not a fork; a bounded ~4-wave extension.

## 4. The open design question Matt + gandalf own (NOT a build blocker — a calibration/encounter-model choice)

The spike moved the question from "can proxies fight?" (yes, cleanly) to **"what makes the boss a STABLE graded outcome rather than a DPS-race step?"** Under the current boss model the player never dies, so the only failure is the clock — making WR a near-deterministic step. Options (gandalf+Matt, a Wave-3 design call, not a fight-engine rewrite):
- grade the proxy boss outcome on **clear-time / efficacy band** (where the grading actually lives) rather than binary WR; OR
- add a **player-death channel** on the boss (boss AoE that can evaporate the army AND threaten the caster), which would restore a WR-graded outcome and make D3-evaporate a real risk.

This is the same texture question the smaller-boss ruling answered for solo — what a "mostly-but-not-always-win" boss should feel like — now for the summoner.

## 5. Production-build constraint surfaced (Discipline #11, for whoever builds W2)

The run-loop gate `if self._track_proxy_population and self._proxies:` (`spatial_engine.py:2066`) requires a non-empty population or the realized-damage step never fires. The realized path must NOT be gated behind the COUNT instrument's non-empty check, or a summon-in-from-empty army never fights.

## 6. What Matt decides from this packet

1. **Architecture call (§2 Matt-halt 3):** build Track-2-proper (the ~4-wave extension above) / re-scope / park. The spike says it is buildable as a bounded wave-series with the fork-line not crossed.
2. **If build:** the `_DEFERRED_PROXY_BINS` lift + 25% emission (§2 Matt-halt 4) remains a SEPARATE reserved decision — the content-emission gate, not unlocked by approving the architecture.
3. **The encounter-model design question (§4)** routes to gandalf for a Wave-3 design ruling if/when build is authorized — not needed to make the architecture call.

**Nothing is half-built. No gate is lifted. No kit is emitted. The proxy question is at the edge of decision with real evidence: the spec, the gate, and the spike that proved the army kills the boss.**

---
**Artifacts (all LOCAL, NOT pushed):**
- `src/reincarnated/simulation/math/spatial-proxy-combat-spec-2026-06-21.md` (T2.1 spec, `6e7f4d5`)
- `src/reincarnated/simulation/math/spatial-proxy-combat-spec-gen-addendum-2026-06-21.md` (T2.1 gen addendum, `3069db9`)
- `agentic_orchestration/qa/findings/2026-06-21-t2.2-proxy-combat-gate1-design.md` (T2.2 Gate-1, `6b9d879`)
- `src/reincarnated/simulation/math/proxy-combat-derisk-spike-2026-06-21.md` (T2.3 spike findings, `77215af`)
- `scripts/gamora_proxy_combat_derisk_spike_2026_06_21_SPIKE_THROWAWAY_.py` (throwaway harness) + `output/proxy-combat-derisk-spike-2026-06-21.json` (raw)
- Prior art: `proxy-contribution-measure-and-set6-calibration-2026-06-17.md` (the COUNT≠CONTRIBUTION cut), `wc-derisk-spike-oracle-first-run-2026-06-13.md` (K5 LOW-EDGE @ boss)
