# Gate-2 request — gamora: proxy-T4 sim-eval EXTENSION — both §7 gates cleared (A2 HOLD + A3 unconditional PASS on landed `focus`); F-f HELD eval-side

**Filed by:** gamora, 2026-07-07 (proxy-T4 sim-eval EXTENSION — §7 gate-blockers cleared).
**Critique pair:** jack-ryan (DEV-MODE Gate-2, BLOCK authority) + gandalf (design — the A3-energy read consumes gandalf's DoF-A `focus` determination).
**Tag under review:** `gamora/v-proxy-t4-rebase-eval-extension-1` @ engine `8a29009`.
**Math note (before-code + §9 completion record):** `reincarnated-engine/src/reincarnated/simulation/math/proxy-t4-suite-rebase-eval-extension-2026-07-07.md`.
**Governing spec:** `canonical/reap-die-rise-engine/proxy-t4-suite-spec-2026-07-02.md` **v3** (§2/§6.1/§8).
**Extends:** my Phase-2 (`gamora/v-proxy-t4-rebase-eval-1`, MIGRATION v1.83).

## Why Gate-2 (cert-path)

This is a DEV-MODE post-output cert: the proxy-T4 eval + the energy-designation READ is the certification path for the ratified four-family PROXY suite at the demo roster + LOCKED anchor. Both §7 gate-blockers named in my SESSION-53 extension note are now cleared and the cert ran against the landed source in ONE pass (A2 + A3 together; no split re-fire).

## What cleared the gates (Disc #11 — inspected the landed source, not assumed)

- **rocket Phase-1 anchor** `rocket/v-proxy-t4-rebase-phase1-v3-confirmed-1` @ `0e9fc91` — ratified `PROXY_T4_FAMILY` (`mechanic_alteration.py:1466`) + `_PROXY_SCAFFOLD_MAGNITUDES` (`:938`) bands UNCHANGED from my §1.2 pre-registration → no PUSH trigger fired.
- **DoF-A field** `rocket/v-batch2-dof-a-focus-field-1` @ `1af6889` — `energy_type="focus"` on `DemoSummonerSpec` + accessors `demo_summoner_energy_type(kit_id)` / `all_demo_summoner_energy_types()` (`generation/demo_summoner_kits.py`).

## The three cert results

### A2 — magnitude sweeps (HOLD; no band re-opened)

N=24/cell, both certified melee fixtures (bone / crypt) × 2 shells × 3 active members = 12 cells, all **OK**: axis-directional (e.g. FISSION crypt 60.1s→9.7s, army_dps 500→3300; SOVEREIGNTY 500→1000; ASCENSION +adjacency 500→550/575), **proxy-borne** (`proxy_dmg>0` / `player_dmg==0` every row → R1 by construction), WR held ≥ baseline, D3-certified baseline byte-unchanged under every apply (G-SCAFFOLD). Caster-alone controls stay WR 0 (no member makes solo viable). Peak RSS 59.8 MB (0.7%/8GB). Default disposition HOLD stands (§1.2). Artifact: `simulation/math/proxy-t4-rebase-eval-extension-full.json`.

### A3 — energy re-confirm (UNCONDITIONAL PASS; retired the hard-code)

RETIRED the eval-side hard-code (`A3_FIXTURE_ENERGY` in harness; `_A3_ENERGY` in tests, both `"charge_stack"`) — the eval now READS rocket's landed `energy_type` via `demo_summoner_energy_type(kit_id)`. This removes the hidden eval-side coupling gandalf/rocket flagged (rocket noted `charge_stack` was not even a valid `energy_type` token). Landed designation = `focus` (non-mana) on both certified fixtures → ratified SOVEREIGNTY `energy≠mana` gate (`mechanic_alteration.py:1069`) OPENS → **bone→FISSION** (sep 0.0610), **crypt→SOVEREIGNTY** (sep 0.0890) → DIFFERENT tops → the v1.83 conditional becomes **unconditional PASS**. F-d pair (ASCENSION-vs-SOVEREIGNTY) separated on both. `focus` grounded on mechanism (gandalf DoF-A determination): kernel `focus` economy passively DECAYS + refills-by-acting (`combatant.py:418`) — the upkeep-army death-economy; RATIFIED, not assumed. MANA-collapse counterfactual retained as a documented refutation pin.

### F-f (DoF-B) — HELD at eval-side invariant (Disc #12; NOT promoted)

rocket determined the leg-2 summoner primary_t4 route does NOT make the GEOMETRY co-draw reachable (the live collision call-site is B4-scoped — the consumer `enforce_family_max_one` EXISTS at `t4_catalog_v2.py:159-215` but is UNWIRED). My AST live-consumer probe over the landed generation package returns **False** (no executable reference to `FAMILY_MAX_ONE`). Per **Disc #12** I did NOT wire an inert guard on the frozen surface: the eval-side INVARIANT (`_geometry_max_one_filter` reduces a ZONE_CONTROL + GEOMETRY_COLLAPSE co-draw to ≤1) is the catch; `enforce_family_max_one` live-wiring stays B4-scoped and is **re-surfaced to KR**. NOT promoted to a live-consumer assertion (my §3 sub-case-2 branch).

## A4 / A5 / A6 — all PASS

F-e ZONE_CONTROL positional-denial (boss forced off optimal line by the ChokeZone primitive; a puddle has no clamp). A5: R1 (DDA keys disjoint from proxy intent keys), R2 (calibrated constants not in exec code + baseline byte-unchanged by construction), F-f invariant holds. A6: retirement executed (v1 S1-S6 + revival classes not importable), INVERSION excluded (not in family, not reachable under mana OR focus), solo zero-effect, coverage held. **20/20 test pins pass (0.12s); smoke + full-pass GREEN.**

## Cross-seam (MIGRATION)

Consumer-read note appended to `simulation/MIGRATION.md`: gamora now CONSUMES rocket's `energy_type` field (cross-ref rocket's MIGRATION line for the DoF-A producer contract). NO producer/schema change on gamora's side — star-lord owes nothing. No `SpatialFightResult` field change, no SQLite schema change.

## Guards honored (batch-2 standing, Matt-restated)

Kit-side chassis constants FROZEN (2.3384× fossil — no chassis touch, T4 intent layer only); bars/bands FIXED (READ only; no PUSH re-opened them); kits vote BARE; `pilot_policy` N/A (no new bands produced — HOLD). Seeds fresh disjoint (BASE_SEED 54M); single-stream sequential. Auto-committed in-scope; NOT pushed (Matt-gated).

## Files under review

- `reincarnated-engine/scripts/gamora_proxy_t4_suite_eval_2026_07_02.py` (harness — energy read + F-f HOLD framing + rebase-tag provenance)
- `reincarnated-engine/tests/test_proxy_t4_suite_eval.py` (20 pins — energy read; landed-non-mana pin added)
- `reincarnated-engine/src/reincarnated/simulation/math/proxy-t4-suite-rebase-eval-extension-2026-07-07.md` (§9 completion record)
- `reincarnated-engine/src/reincarnated/simulation/math/proxy-t4-rebase-eval-extension-full.json` (N=24 full-pass artifact)
- `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` (consumer-read note)
