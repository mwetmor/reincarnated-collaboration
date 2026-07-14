# Cell-key materialization — gandalf independent verification (gate CLEARED)

**Role:** gandalf (ARCHITECT) — run-authorization gate between elrond materialization and gamora dedup.
**Date:** 2026-07-13 · **Method:** read-only queries on `agentic_orchestration/research/curated/corpus.db` (`PRAGMA query_only=ON`), after confirming the writer had settled (mtime + size stable across a 20s window).
**Context:** elrond ran as a **subagent** (KR-fired). The subagent built the columns correctly but did **not** append its dispatch completion record or commit a migration script / curation log. This note is the durable gate-clearance until elrond closes that record. **corpus.db is untracked — without elrond's committed artifacts, the migration logic is unreproducible.**

## Verdict: PASS — well-formed, non-degenerate cell_key. gamora is cleared.

### Structural gate
| Check | Result | Pass? |
|---|---|---|
| Coverage (combat-kit non-null `cell_key`) | 470 / 470, 0 null | ✓ |
| Arity (fields per `cell_key`, expect 14) | 470 rows all = 14 | ✓ |
| system-record excluded | 0 carry `cell_key` | ✓ |
| unknown/blank footprint | 49 cells (~10%) — meaningful, not degenerate | ✓ |
| Distinct cells vs 470 | **457** | ✓ (see collapse note) |

### Classifier degeneracy checks (the reason to verify a subagent build)
- **economy_model** — spend 182 / cooldown 61 / free 48 / reserve 47 / unknown 43 / generator-spender 37 / finite 35 / self-cost 15 / **spend+finite 1 / spend+cooldown 1**. Tracks the corpus predictions near-exactly (spend 182≈183, self-cost 15 exact, cooldown 61 exact). **Hybrids preserved as literal compounds — guardrail honored.**
- **activation_val** — active 376 / **triggered 87** / unknown 7. Discriminator fired (not the degenerate all-active).
- **dependency_val** — one-shot 359 / apply→detonate 60 / build→spend 44 / unknown 7. All values present.
- **ctrl_function** — none 311 / hard-stop 44 / hex 28 / stun 27 / knockback 20 / expose 12 / taunt 11 / blind 7 / fear 3 / unknown 7 (silence absent — no kit classified there; acceptable).
- **resource_verbatim** — 463/470 (98.5%), 172 distinct. 1:1 lineage preserved, out of key.
- The 7 `unknown`s co-occur across columns = the same ~7 under-documented kits falling to conservative-literal. Clean.

## The design headline: strict-13 is near-maximally split
Isotope-depth histogram: **445 singletons · 11 depth-2 · 1 depth-3** → 457 cells, only **13 kits collapsed.** This is exactly what strict-first predicts (split-late beats merge-wrong) and it means **the periodic table's real grain is decided at Stage-2, not here.** 457 cells is "every kit its own element" — not yet a usable table. The near-twin adjacency aggregate is now THE object that turns 457 → a few dozen archetypes.

### The 12 multi-member cells validate the whole thesis
Every collapse is a legitimate "same mechanical element, different game/element/skin" isotope — including cross-franchise:
- **poe1-cyclone = d3-ww-wastes** (Cyclone ≡ Whirlwind — the canonical spin-to-win melee element)
- **d3-dashing-strike-monk = le-shift-bladedancer** (dash-strike across Diablo 3 / Last Epoch)
- **d3-invoker-thorns = gd-retaliation-warlord** (reflect/retaliation across Diablo 3 / Grim Dawn)
- **d3-inarius-bonestorm = d4-bouldercane** (cross-Diablo-generation)
- **di-draw-quarter-crusader = tq-shield-charge-conqueror** (shield-charge across Diablo Immortal / Titan Quest)
- **d2-wl-fire = d2-wl-abyss** (same werewolf skeleton, fire vs abyss — **element-as-overlay confirmed**)
- + 6 more (poe trap-triple, archmage/ball-lightning, tornado-shot/wander, rolands/callidors, hot splinters/archer, torchlight bots)

Mechanical identity transcends franchise, and element is a Class-B overlay — both proven by the data, not asserted.

## Residual (owed, non-blocking for gamora)
1. **elrond durable record** — completion record + committed migration script/curation log. The subagent's data is correct but its *recording discipline* was skipped (the concrete cost of subagenting a migration). Close before building further on the key.
2. Spot `cell_key`s read sensibly (e.g. `d2-trapsin → walk|at-target|spiky|totem|damage|none|evade|spend|heavy|dual|low|instant|triggered|apply→detonate`). Note: delivery/geometry tokens are the *existing* column vocabularies (`at-target`, `totem`, `single_target`…), not the register's 7-value delivery enum — a future normalization question, NOT a gate failure.
