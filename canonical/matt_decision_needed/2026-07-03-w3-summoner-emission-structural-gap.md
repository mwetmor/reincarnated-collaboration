# MATT DECISION NEEDED — W3 summoner emission: structural gap (criterion C unsatisfiable as written)

> **Raised:** 2026-07-03, mid-flight in the DEMO-READINESS UNATTENDED RUN (W3 Phase A halt-loud, first §7 invocation of the run).
> **Finding:** `reincarnated-engine/src/reincarnated/generation/notes/w3-ungate-refutation-fired-2026-07-03.md` (rocket, engine `0a1706c`).
> **Adjudication:** critique pair (jack-ryan + gandalf, parallel read-only) — verdicts folded below with attribution.
> **Run disposition while you rule:** W3 fires as **solo full-spectrum BATCH 1** (spec §4 batch mechanism; criterion C PARKED loudly, NOT amended). Nothing below pre-commits your ruling.

## What happened

The run-spec criterion C un-gate ("lift `_DEFERRED_PROXY_BINS` + `ProxySpawn`; emission fires with proxy bins live") is **structurally unsatisfiable** — the generation-side summon-skill composition path does not exist:

1. Phase 4d of `bc_target_composer.py` (`:756-757`) is a no-op stub assuming `proxy_bin=="solo"` — verified verbatim by jack-ryan.
2. The `multi-spawn` geometry maps to `multi_projectile`/`chain`/`fork` (`:380-384`) — projectile multiplicity, no summon taxonomy.
3. `PoolMechanic` carries no summon discriminator; `build_proxies_surface` (`proxy_vocabulary_bridge.py:298-299`) documents "every exported kit gets `[]`."

Lifting the gate composes proxy-heavy targets with **zero summon skills** → hollow kits that would fake criteria B/C. Rocket performed no lift, no tag — halt-loud per §7 (both critics: correct and disciplined). Additionally: `ProxySpawn` at `mechanic_alteration.py:46` is a docstring reference to the register you RETIRED 2026-07-02 — nothing to lift; the spec's "2026-06-24 ratification" reference has no provenance in the engine tree. Spec v1.2 should correct both.

## Process finding riding along (jack-ryan [AMEND])

W0 deliverable #2 ("2-type decl check — PASS (not a gap)") validated the **fixture/classifier layer**, not the composer→kit production path the check was written to guard (Disc #2/#11 finding). The gap existed at W0 and was masked. Bounded — classifier/F-f/singleton-smoke PASSes are self-contained and unaffected; gamora's W2 cert is honest *as a fixture cert*. But no PASS in W0–W2 established emission-viable proxy content.

## The authority conflict your ruling resolves (the load-bearing part)

- **jack-ryan** concurs with rocket's Option 2 (curated certified summoners fill the demo roster's summoner seats, flagged `curated-not-emitted` in the registry), citing One Realm §5.2 "hand-authored acceptable at demo scope" + the III.1b launch-track split already in the tree.
- **gandalf [CONTEST]:** §5.2's hand-authored language is **struck through** — your 2026-07-02 ruling (one-realm-mvp-scope.md line 16, verbatim: *"they need to be balanced and pipeline emitted… we can pick from a seasonal emission… of battle-sim passed kits"*) repurposed the hand-authored decls to calibration fixtures only, zero hand-authored content ships. Option 2 would re-install exactly what you struck. jack-ryan's citation is to the pre-ruling text.
- **Both agree** the distinction is invisible to the player at demo scope (minute-one "raise the dead" promise is satisfiable either way); the emitted-vs-curated question is a *product-integrity* promise — which is precisely why it is yours, not ours.
- **gandalf on G4:** the ~25% is two promises wearing one number — the player experiences *curated-roster share* (2-3 of 8-10, achievable either way); the *emitted share* is an engine-capability goal (currently 0%, structurally).

## Options (rocket's three, critique-pair assessed)

| # | Option | Assessment |
|---|---|---|
| 1 | **Build the missing gen-path** (summon-skill composition + Phase-4d population + PoolMechanic summon discriminator + bridge derivation) as a scoped follow-on — math-first + Gate-1 — then re-fire summoner emission as **registered batch 2** | Both critics: highest integrity; the only path to generation-emitted summoners at the G4 share; the only path consistent with your 2026-07-02 ruling as written. Cannot ride the unattended run (needs a Gate-1 it can't supervise). |
| 2 | Curated certified summoners fill the demo summoner seats now, registry-flagged `curated-not-emitted`; criterion C + G4 formally amended (decisions-log + spec v1.2, not a header edit) | jack-ryan: process-honest with the flag, on-schedule. gandalf: contradicts your struck-through ruling — choose it only knowing you're reversing 2026-07-02. |
| 3 | Minimal Phase-4d stub → undifferentiated summoners emit | **Both critics reject.** False abundance poisoning the §8 shortlist; the D3-vanilla decoration-pet failure; ships the hollow-kit failure mode without Option 2's honesty. |

## What is being asked of you

1. **Rule the summoner path:** Option 1 (batch-2 re-fire after the gen-path build — consistent with 2026-07-02) vs Option 2 (curated seats + formal C/G4 amendment — a knowing reversal). Option 3 is not recommended by anyone.
2. **If Option 1:** authorize the gen-path build dispatch (math-first + Gate-1 critique-pair; new cross-seam `proxies` emission contract → ADR-004 MIGRATION).
3. **If Option 2:** the C/G4 amendment lands as a decisions-log entry + spec v1.2 fold (jack-ryan seam), and jack-ryan asks that the registry schema gain a per-content-type provenance field (`emitted`/`curated`) — G9 fast-pass ratification.
4. **Spec v1.2 hygiene either way:** strike the `ProxySpawn` lift + the 2026-06-24 reference from criterion C.

## What proceeded without you (no pre-commitment)

- **W3 BATCH 1 — solo full-spectrum emission** — fired under spec §4's batch mechanism: pilot beat → thousands of candidates → gauntlet → flavor (survivors-only kits; membership-keyed monster/gear/faction) → assemble + register. Banks curation-from-abundance for the ~7-8 non-summoner roster seats (gandalf Q4: intact). Criterion C recorded as PARKED in the registry/board, not satisfied, not amended.
- **Step-0 registry writer** (#8b, criterion F) — ruling-independent under all options; both critics endorsed the carve-out.
- Empirical criterion that re-engages the summoner leg: **your ruling on this file** (not time-passage).

**References:** finding note (path above) · blockers `bc_target_composer.py:97,318,380-384,756-757` · bridge `proxy_vocabulary_bridge.py:295-311` · W0 smoke `generation/notes/w0_prereqs_smoke_2026_07_03.py:98-131` · struck §5.2 `canonical/reap-die-rise-game/one-realm-mvp-scope.md` lines 16, 50, 67 · run spec v1.1 §1-C, §4, §5, §7 · state board `agentic_orchestration/demo-readiness-run-state-2026-07-03.md`.
