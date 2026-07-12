# Re-key prep — DEF slot (design session #4, GREENFIELD)

**Date:** 2026-07-12 · gandalf (mechanical prep; **elicits, does not rule**) · Spec: `corpus-rekey-spec-v1.md` §2 — def RETIRES → raw descriptor; engine target = **NEW defensive-layer vocabulary (a genuine engine design gap)**. Brief instruction: survey engine mitigation surfaces first, then present a *candidate* vocabulary.

## 1. Corpus code frequency (v3 CSV canon positives, n=478)

| code | meaning | count | % |
|---|---|---|---|
| M | mitigation | 164 | 34% |
| D | dodge | 138 | 29% |
| T | tank | 110 | 23% |
| G | glass | 46 | 10% |
| _ | unspec | 20 | 4% |

**4 live codes** (decoded via `code_def`).

## 2. Engine mitigation surfaces (survey — there is NO def *vocabulary* yet, only mechanisms)

From `simulation/combatant.py` + `simulation/math`:
- **Armor mitigation** — `armor/(armor+ARMOR_MITIGATION_K)` curve; `MITIGATION_SYMMETRY` floors elemental resist to the armor-symmetric curve.
- **Elemental resistance** — per-element rolled resist (0.30–0.60 own-element band).
- **Dodge** — `compute_dodge_chance` (avoid-the-hit).
- **Shield absorb** — `get_shield_total` / `absorb_with_shield` (drain shields before HP).
- **Status resist** — `compute_status_resist`.
- **T4 defensive doors** — `DEFENSIVE_CONVERSION`, `DEFENSIVE_TRADEOFF` (`t4_category_schema.py`, Category A character-wide).

The engine has *mechanisms* but no named *layer taxonomy* — this is why the brief calls it greenfield.

## 3. CANDIDATE vocabulary + PROPOSED mapping (corpus → candidate)

Proposed 5-bin defensive-layer vocabulary derived from the mitigation surfaces above:

| candidate bin | engine mechanism | ← corpus | confidence |
|---|---|---|---|
| `tank` | high armor + HP; eat-the-hit | T tank | HIGH |
| `mitigate` | resist / damage-reduction curve | M mitigation | HIGH |
| `evade` | dodge-chance; avoid-the-hit | D dodge | HIGH |
| `absorb` | shield drain-before-HP | *(none)* | — **NEW bin, no corpus code** |
| `glass` | no defensive layer (offense-as-defense) | G glass | HIGH |

**Residue:** `absorb` (shields) is a distinct engine mechanism the corpus folds into `mitigation` — proposing it as its own bin. `status_resist` is orthogonal (a rider on any bin, not its own bin). The corpus 4-code maps cleanly to 4 of the 5 candidate bins — **the cleanest of the six slots.**

## 4. Open forks (UNRESOLVED — Matt rules)

- **Fork D1 — 4-bin or 5-bin? Is `absorb` its own layer?** (a) 4-bin: fold shields into `mitigate` (corpus-parallel, simplest). (b) 5-bin: `absorb` distinct — shields play differently (burst-eating, refresh-gated) from steady mitigation. **Genre precedent:** PoE treats Energy Shield as a wholly separate defensive layer (ES vs Armour vs Evasion vs Block are the four pillars); D3 shields (Ancient Parthan, Squirt's) are distinct from armor/resist; Last Epoch Ward is its own layer. The genre overwhelmingly treats absorb/shield as a **first-class fourth+ pillar**. **Lean (b) 5-bin** — the genre validates absorb as its own axis.
- **Fork D2 — is `block` a sixth bin?** PoE/D2 block (chance to negate) is arguably distinct from evade (dodge) and absorb (shield). Corpus has no block code (folded into dodge/mitigation). Options: (i) block = a flavor of `evade` (both are chance-to-negate); (ii) block earns its own bin. **Lean (i)** — block and dodge are both roll-to-avoid; keep them one bin unless T4 door design needs the split.
- **Fork D3 — greenfield naming.** `tank/mitigate/evade/absorb/glass` is one candidate lexicon; alternatives exist (PoE's `armour/evasion/energy-shield/block`; D4's `barrier/fortify/dodge`). Naming is a senior-design call — Matt picks the register. **Lean:** verb-forward player-facing names (`tank/mitigate/evade/absorb/glass`) over stat-noun names, since RDR surfaces role-feel not stat-sheets.
