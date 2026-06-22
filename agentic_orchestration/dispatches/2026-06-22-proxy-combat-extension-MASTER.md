# Dispatch MASTER — 2026-06-22 — proxy-combat architecture extension (~4-wave)

**From:** knight-rider
**Approved by:** Matt 2026-06-22 — BUILD authorized for the proxy-combat ~4-wave extension per `agentic_orchestration/2026-06-21-proxy-combat-decision-packet.md` §3.
**Coordinates:** rocket (generation prereqs), gamora (sim waves), star-lord (telemetry), gandalf (W3 design ruling), jack-ryan (Gate-1 each sim wave + Gate-2 chain).

> This MASTER is the sequencing + guard authority. Per-wave pickups are extracted as separate dispatch files and fired stage-by-stage by knight-rider (orchestration seam). The build specs ALREADY EXIST (T2.1) — pickups point builders at them; they do not re-derive architecture.

## Design of record (read before any wave)
1. Decision packet (the plan): `agentic_orchestration/2026-06-21-proxy-combat-decision-packet.md` — **§3 scope/sequence, §4 (RESOLVED — see below), §5 build constraint.**
2. T2.1 sim build spec: `~/Games/reincarnated-engine/src/reincarnated/simulation/math/spatial-proxy-combat-spec-2026-06-21.md`
3. T2.1 gen addendum (gen-side build spec): `~/Games/reincarnated-engine/src/reincarnated/simulation/math/spatial-proxy-combat-spec-gen-addendum-2026-06-21.md`
4. T2.2 Gate-1 (the concerns the build must honor): `agentic_orchestration/qa/findings/2026-06-21-t2.2-proxy-combat-gate1-design.md`
5. T2.3 de-risk spike (what's proven / what's still untested): `~/Games/reincarnated-engine/src/reincarnated/simulation/math/proxy-combat-derisk-spike-2026-06-21.md`
6. Encounter-model disposition (the W3 SHAPE, design-pre-cleared): `agentic_orchestration/gandalf/notes/2026-06-21-encounter-model-firm-up-disposition.md`

## DESIGN PRE-CLEAR (Matt 2026-06-22) — §4 is RESOLVED, do NOT route as a fresh open question
The packet's §4 encounter-model question is answered. The typed-resistance wave shipped a real player-death channel for solo; **proxy INHERITS it, not a deferred choice.** gandalf's encounter-model disposition gives the unified shape: a **telegraphed signature slam — build-floor (resist/tank/out-range) + dodge-ceiling — that EVAPORATES THE ARMY AND THREATENS THE CASTER.** Proxy W3 inherits this SHAPE; **gandalf owns the W3 design ruling when W3 calibration evidence is in.** Shape pre-cleared; the specific numbers wait on W3.

## The wave sequence + dependency spine

| Wave | Seam | Depends on | Pickup file |
|---|---|---|---|
| **G1+G2** | rocket (generation) | — (long pole) | `2026-06-22-rocket-proxy-gen-prereqs-G1-G2.md` |
| **W1** | gamora (sim) | — (independent of gen output; generalizes hard-wired mob sites) | `2026-06-22-gamora-proxy-W1-allegiance-spawn.md` |
| **W2** | gamora (sim) | **G1+G2 landed** (sim can't test a fighting proxy until gen emits one) + W1 | *(staged — authored when G1/G2 + W1 land)* |
| **W3** | gamora + gandalf | W2 landed | *(staged — authored when W2 lands; gandalf woken at calibration evidence)* |
| **telemetry** | star-lord | W2 (reads the realized-damage path) | *(staged — alongside W2/W3)* |
| **G3 (Beast-Taming)** | generation | SEPARABLE — NOT a hard prereq for the core | *(deferred; separable per packet §3)* |

**Phase 1 (concurrent, fired now):** rocket G1/G2 (long pole, no Gate-1 per Matt's gate plan — generation, not sim) ∥ gamora W1 (after its Gate-1 ENDORSE). W2/W3/telemetry are STAGED — knight-rider authors each as its dependency lands (W2's exact shape depends on G1/G2's realized stat surfaces; authoring now would go stale).

## GATE PLAN (Matt 2026-06-22 — verbatim)
- **jack-ryan DESIGN-MODE Gate-1 BEFORE each SIM wave** (W1, W2, W3). Generation waves (G1/G2) take the normal Gate-2 chain, no mandated Gate-1.
- **gandalf woken for the W3 design ruling** when W3 calibration evidence is in.
- **Normal Gate-2 chain per wave** (every build, before chaining the next dependent wave).

## NON-NEGOTIABLE GUARDS (carry verbatim into every pickup)
- **G-SOLO — solo byte-identical at `proxy_bin=solo`.** The extension must not perturb the shipped solo instrument. Empty-decl-gated; verify byte-identical at every sim wave (Gate-2 teeth).
- **G-CONSTRAINT (packet §5, Discipline #11) — the realized-damage step must NOT be gated behind the COUNT instrument's non-empty check** (`spatial_engine.py:2066` `if self._track_proxy_population and self._proxies:`), or a summon-in-from-empty army never fights. Load-bearing for W2.
- **G-EXTENSION-NOT-FORK — minimal-change path only.** The ONE new concept is `allegiance ∈ {player, ally, enemy}` as a filter, reusing `_navigate_entity` / `_compute_*_hits` / `_apply_skill_damage` (already target-agnostic) / the existing survive-and-kill gate. No autonomous-AI fork (named §7.3, NOT crossed). No proxy-only ship gate. No fight-engine rewrite.
- **G-COUNT≠CONTRIBUTION — the cancelled selector and the realized fight stay TWO DISTINCT instruments.** Conflating them re-introduces the capstone §6 circularity (T2.2 finding).
- **G-PLAYER-RELEVANT — `0 < s_baseline < 1` stays hard-enforced at emit** (`partition_roller.py:343`); the player must remain relevant, not a spectator to the army.

## NOT unlocked by this BUILD call (stays Matt-gated — do NOT cross)
- **Content emission:** `_DEFERRED_PROXY_BINS` lift + 25% proxy emission — SEPARATE reserved decision even with architecture approved. No kit emitted, no bin un-deferred.
- **Push:** Mac per-cycle Matt-ask. Auto-commit in-scope work-products; do NOT push.

## Scope honesty (T2.2 carry)
The gen→sim proxy seam "was specified at both ends and never soldered in the middle" — G1/G2 are a first-class ~1.5-wave generation prerequisite, NOT folded invisibly into calibration. `grep -rl '"proxies"' exports/` = 0 today; the dict the spec says generation will "emit into" does not exist yet. G1/G2 build it.
