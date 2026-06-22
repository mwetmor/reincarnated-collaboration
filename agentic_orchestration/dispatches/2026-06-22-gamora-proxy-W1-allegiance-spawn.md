# Dispatch — 2026-06-22 — gamora — proxy W1 (allegiance + positional spawn)

**From:** knight-rider
**To:** gamora
**Approved by:** Matt 2026-06-22 — proxy-combat BUILD authorized.
**Gate-1 REQUIRED before build** (jack-ryan DESIGN-MODE — this is a sim wave). Pickup fires only on Gate-1 ENDORSE.
**Gate-1 status: ENDORSE-WITH-CONCERNS** (`agentic_orchestration/qa/findings/2026-06-22-proxy-W1-gate1-design.md`). Three carry-items folded into §Scope below — READ THE FINDING.
**Estimated effort:** ~1 wave. **Independent of rocket G1/G2** — W1 generalizes the hard-wired mob sites; it does NOT consume gen output. Runs concurrent with rocket's generation prereqs.

> **Parent MASTER:** `agentic_orchestration/dispatches/2026-06-22-proxy-combat-extension-MASTER.md`. Read it for the full guard set + gate plan.

## Acceptance
The two sites that hard-wire "mob" are generalized to allegiance-filtered sets, and proxies take a real position via positional spawn — WITHOUT perturbing the solo instrument. The ONE new concept is `allegiance ∈ {player, ally, enemy}` as a clean filter. **Solo BYTE-IDENTICAL at `proxy_bin=solo`.**

## Required reading before starting
1. Sim-side build spec (THIS IS YOUR SPEC): `~/Games/reincarnated-engine/src/reincarnated/simulation/math/spatial-proxy-combat-spec-2026-06-21.md`
2. T2.3 de-risk spike (what's proven vs the W1 untested question): `~/Games/reincarnated-engine/src/reincarnated/simulation/math/proxy-combat-derisk-spike-2026-06-21.md`
3. T2.2 Gate-1 (the two hard-wired sites verified; extension-not-rewrite holds in KIND): `agentic_orchestration/qa/findings/2026-06-21-t2.2-proxy-combat-gate1-design.md`
4. Parent MASTER (guards + not-unlocked fences): `agentic_orchestration/dispatches/2026-06-22-proxy-combat-extension-MASTER.md`

## Scope
- [ ] **Allegiance filter — generalize the NAVIGATION-target hard-wiring PARAMETRICALLY.** Introduce `allegiance ∈ {player, ally, enemy}` and generalize the navigation-target sites. **Gate-1 carry-item #1:** the mob's nav-target is hard-coded to `player` at **MULTIPLE `_navigate_entity` branches (`:947, :954, :972, :986, :989` + reposition math), not just `:954`.** The correct fix is **PARAMETRIC** — pass an allegiance-filtered target into `_navigate_entity` so ALL branches re-path. Patching `:954` alone leaves four behaviors walking mobs at the player; a per-branch allegiance conditional is the fork-smell the extension-not-fork guard forbids. Also generalize the **world entity-set** (`all_entities = [self.player] + self.mobs`, at **`:1668`** — note the `:1662` citation drifted through the spec/T2.2/this dispatch; find it by content) to allegiance-filtered sets so an ally-proxy can exist alongside player + enemy mobs.
- [ ] **Positional spawn.** Proxies take a real position (generalize the spawn that today exists only for mobs).
- [ ] **THE GENUINE UNTESTED QUESTION (spike caveat — answer it):** does `_navigate_entity`'s hard-coded `player` target generalize cleanly to nearest-enemy re-pathing for a mob→proxy? Verify the navigator re-paths an ally-proxy to nearest enemy without special-casing.
- [ ] **Gate-1 carry-item #2 — LEAVE THE MOB ATTACK-TARGET UNTOUCHED (it is W2's).** The mob's ATTACK target is independently hard-wired to `[self.player]` at **`:1943`/`:1952`** — this is the realized-damage/aggro cross, which W2 owns. Do NOT generalize it in W1. Consciously DECOUPLE navigation (W1) from attack-targeting (W2) and DECLARE the decoupling in your math note, so "finishing the player-assumption generalization" does not pull the attack-target cut into W1.
- [ ] **G-SOLO guard — solo byte-identical at `proxy_bin=solo`.** Empty-decl-gated (empty `proxy_decls` → `_build_player_proxies()` returns `[]`, allegiance degenerates to player-vs-mobs). Prove it (a solo run produces byte-identical output to pre-W1 HEAD). **Gate-1 carry-item #3:** the byte-identical fixture MUST exercise MULTIPLE mob behaviors — a single-behavior solo run can pass byte-identical while masking an incomplete (1-site) generalization. The multi-behavior fixture is where carry-items #1 and #3 interact.
- [ ] AGENT_STATE.md updated at session end.
- [ ] Tag: `gamora/v-proxy-W1-allegiance-spawn-N`

## Cross-seam contract change (Principle 6)
W1 is sim-internal (allegiance/spawn generalization) — likely no cross-seam contract change. If W1 surfaces a consumer-visible change, MIGRATION.md required. The realized-damage cross + the gen-consumed surface are W2's scope, not W1's.

## NON-NEGOTIABLE GUARDS (from MASTER)
- **G-SOLO** — solo byte-identical at `proxy_bin=solo` (the shipped solo instrument must not move). This is the load-bearing W1 guard.
- **G-EXTENSION-NOT-FORK** — minimal-change; reuse `_navigate_entity` / existing spawn; `allegiance` is a filter, not a new navigation engine. No autonomous-AI fork.
- **G-CONSTRAINT (carry forward, primarily W2)** — note for continuity: the realized-damage step must NOT be gated behind the COUNT instrument's non-empty check (`spatial_engine.py:2066`). W1 doesn't wire realized damage, but do NOT entrench that gate in a way W2 then has to unwind.
- **No content emission** — `_DEFERRED_PROXY_BINS` stays deferred; no proxy kit emitted.
- **Push HELD** — auto-commit; do NOT push.

## Out of scope (explicit non-goals — these are W2/W3)
- **Realized damage / targetability / death** (the cross proper) — W2, depends on rocket G1/G2.
- **Calibration vs boss_with_adds / mini_boss** — W3.
- **The encounter-model shape** — design-pre-cleared, gandalf owns the W3 ruling; not W1's concern.
- Anything that consumes rocket's `proxies` surface — W2.

## Disciplines
#1 math-before-code, #3 seed hygiene (**fresh disjoint base — prior bases used through 49M; use 50M+ and record it**), #11 empirical inspection (prove the navigator re-paths; prove solo byte-identical), #12 semantic-shift (declare if allegiance shifts any outcome semantics).

## Report back to knight-rider
Confirmation the two hard-wired sites are generalized + the navigator re-paths ally-proxy → nearest-enemy cleanly (the untested question, answered with evidence), solo-byte-identical proof at `proxy_bin=solo`, the seed base used, the tag, and any finding that changes what W2 can assume. Flag anything needing Matt or gandalf.
