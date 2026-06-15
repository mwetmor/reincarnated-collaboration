# Rogue degeneracy — DIAGNOSIS (the envelope dropped the role-composition floor) + WS1 follow-up for KR

**Type:** design diagnosis + WS1 sequencing follow-up (gandalf → knight-rider). Resolves the "rogue-specific open hypothesis" the b6-reshape scoping left HELD.
**Date:** 2026-06-15
**Author:** gandalf (story-and-design steward)
**Authority:** Matt-authorized 2026-06-15 (Pattern-B) — *"solve through strategic design/understanding rather than allowing the archetype label to linger as an open hypothesis … this will turn into massive creep later if left unattended"* + *"I agree to resolve the caster open question."*
**Parent:**
- gamora signature math-note `reincarnated-engine/src/reincarnated/simulation/math/b6-reshape-scoping-per-tier-shape-degeneracy-signature-2026-06-15.md` + `simulation/AGENT_STATE.md` Session 11 (the scoping RESULT this diagnoses).
- `canonical/story/weapon-as-identity-surface-recognition-2026-06-14.md` § 6-quinquies (f) (caster-path-generalization flag) + § 6-sexies (design-fit record).
- `agentic_orchestration/gandalf/notes/2026-06-15-b6-deletion-prerequisites-brief-for-kr.md` (Prereq B = G7 HOLD-SIM — this names what the fix must re-pass).
**Refines (does NOT overturn):** the sub-agent REFRAME-AND-DEFER disposition. It was right to refuse "envelope-specific" off a silent caster leg. This note does one better than defer: it **locates the mechanism in code**, so "hold the hypothesis open" becomes "named composer gap + one empirical confirmation + a substrate-led fix." That is the anti-creep move Matt mandated.

---

## 0. One line

The "rogue degeneracy" is **not about rogue and not an open mystery**: the weapon-as-ENVELOPE composer does not enforce the **role-composition floor** the b6 template guaranteed — it cannot emit a `defensive`-role skill at all (`weapon_envelope_composer.py:243-252`) and emits no `burst_damage` below power-60 (`:248`). A glass single-target cell composed with **zero survival and zero spike** over-shreds swarm (raw ST throughput on low-HP mobs) and craters boss (no survival to outlast it, no burst to drop it) — an unshapeable spread for one global modifier. b6 "rescues" rogue solely because the b6 rogue template **forces** `mobility 2 + defensive 1 + burst_damage 1` + a 25–35% AoE-share floor (`b6_archetype_templates.py:247-250, :242`). **The entire arm-to-arm delta is the role floor.** Fix = a coordinate-derived role-floor in the envelope path. **No "rogue" label returns.**

---

## 1. The mechanism (code-cited)

**Rogue's bc-cell** (`bc_target_source.py`, combo + close + physical): `eng_bin=close-fast` (§2.3.4 override `:147-149`), **`geo_bin=single-target`** (`_RANGE_GEO_BASE["close"]` `:54`), **`def_bin=glass`** (`_ROLE_DEF_BASE["damage"]` `:36`), `tempo_bin=high`. The two load-bearing coordinates: **single-target + glass.**

**What the envelope does with it** (`weapon_envelope_composer.py`):
1. `geo_bin=single-target` up-weights the pure-ST geometries ×2.2 (`:180-183`) — *correct*; rogue should read single-target.
2. `_role_for_geometry` (`:243-252`) can emit only **{mobility, burst_damage, area_damage, primary_attack}**. There is **no code path that emits `defensive`.** `mobility` fires only when `geometry == "defensive_dash"` (`:245-246`) — one geometry, left at base weight for an ST cell. `burst_damage` fires only at `power_tier >= 60` (`:248`); rogue runs 58 (b6) / 50 (gamora's slice), so it **never** fires.
3. `compose_physical_kit_envelope` (`:277-372`) has **no `required_roles` enforcement and no post-draw role floor** — roles are purely emergent from the weighted geometry draw.

**Net:** a live envelope rogue ≈ a near-pure stack of `primary_attack` single-target skills, **0 defensive, 0 burst, ~0–1 mobility.** Measured behaviour (gamora CELL-4/rogue, envelope arm): swarm WR `1.0` (over-ceiling) → modifier floors to `0.0101` → elite/mini_boss/boss all `0.0`. The b6 arm on the same cell: `converged=0.6133`, elite `0.75` / mini_boss `0.667` / boss `0.967`.

**Swarm-hot is NOT an AoE artifact.** A fast single-target striker deletes low-HP swarm mobs one-by-one faster than they mob you — raw ST throughput over-clears swarm without any AoE. That is *why* a single-target cell, of all things, pins the swarm tier over ceiling.

## 2. Why rogue specifically — the clean canary

| cell | geo lean | b6 carries upper? | reading |
|---|---|---|---|
| **rogue** | single-target, glass | **YES** (b6 converges) | role floor is **necessary AND sufficient** — the canary |
| skirmisher | single-target-ish | b6 build-failed | same family; likely same fix |
| warrior / grappler | AoE-bruiser (0.40–0.50) | **NO** (b6 also craters) | AoE-bruiser spread is swarm-hot/boss-soft *regardless* of the floor — a **separate** problem b6 never solved |
| hunter | ranged | NO (b6 also craters) | separate |

Rogue is the **one** cell where the b6 floor's `burst + mobility + defensive` produces a kit that can *reach and burn* a boss (single-target burst is the boss-killer archetype) **and** stay swarm-in-band. So b6 converges it — isolating the role floor as the single causal variable. For the AoE bruisers the floor is present (b6) yet insufficient: that "co-broken" band is closer to gamora's genuine single-global-modifier architectural question, but it is **not** what b6 was rescuing, so it does **not** gate b6 deletion.

## 3. Caster reconciliation — turns gamora's INCONCLUSIVE into a sharp prediction

Caster PLAYER kits compose through `archetype_composer.py`, which **preserves `required_roles`** (the composed `ArchetypeTemplate` carries the floor). My diagnosis therefore **predicts** casters do NOT exhibit the degeneracy — when the caster-hot follow-up manufactures an over-ceiling-swarm caster cell, the caster should **converge with upper tiers cleared** (math-note §2.3 **branch 4 — ENVELOPE-SPECIFIC**), *because it kept its role floor.*

- **Prediction registered (recognition → validate):** caster-hot run lands on branch 4, not branch 2.
- **Falsifier:** if a caster with its floor intact *also* craters boss while swarm is hot (branch 2 — ARCHITECTURAL), the role floor is **not** the whole story and there is a deeper single-global-modifier limitation. That is the outcome that would re-open the architectural hypothesis — now on *evidence*, not on silence.

Matt greenlit resolving the caster open question. Keep gamora's caster-hot follow-up — but it is no longer an open-ended fish: it is the **confirmation/falsification** of the role-floor diagnosis, with a pre-registered prediction.

## 4. The cheap empirical confirmation (rocket — run FIRST; ~minutes)

Before any fix or any caster run, confirm the diagnosis at near-zero cost:

- **Role-count audit.** Generate one live envelope rogue-cell kit and one b6 rogue kit (same seed). Count skills by `role`. **Diagnosis confirmed iff** the envelope kit has **defensive = 0** and **burst_damage ≈ 0**, while the b6 kit carries `defensive ≥ 1`, `burst_damage ≥ 1`, `mobility ≥ 2`.
- **Guard against a wrong call:** verify nothing downstream (`class_generator`, gear) injects a defensive skill into the envelope kit. If something does, the diagnosis needs revision — surface it, don't paper over it.
- Owner: **rocket** (generation seam owns the composer + the harness). This is the "validate" gate; the fix does not fire until it passes.

## 5. The fix direction (substrate-led — contingent on §4 confirming)

Re-encode the genre truth at the **coordinate** layer, never the label layer. A role-composition floor in `compose_physical_kit_envelope` **derived from the bc-cell's own 8-tuple**:

- **`def_bin=glass` → survival minimum.** Add a `defensive`-role emission path (the composer has none today) and a floor of ≥1 defensive skill for glass cells. *This is the single highest-leverage line item.*
- **`eng_bin=*-fast` → mobility minimum** (≥1–2 mobility for mobile cells).
- **`geo_bin=single-target` → AoE-share floor** so a pure-ST cell doesn't trivially over-shred swarm (mirror the b6 25–35% intent, coordinate-derived).
- **burst:** reconcile the `power_tier >= 60` burst gate (`:248`) with sub-60 single-target cells, or floor burst-role presence by coordinate rather than by a power threshold.

Genre anchors for the floor's *shape*: Diablo III Demon Hunter (Smoke Screen/Vault mandatory), D2 Assassin (Shadow Discipline survival), PoE glass-cannon "defensive layers" doctrine. Every viable ARPG glass striker carries a survival tech; the floor encodes that.

**Owner:** rocket (composer). **Gate-1:** jack-ryan on the floor math-note (it is a composer semantic addition — Discipline #12). **Re-validate:** the fixed envelope rogue must re-pass **Prereq B / G7 HOLD-SIM** (gamora) on the rogue cell — i.e. the envelope arm now clears the upper tiers b6 was carrying.

## 6. Disposition + the b6-deletion coupling (the clean part)

- **The architectural hypothesis is NO LONGER "held open as a rogue mystery."** It is a **named composer gap** (missing role floor) with a confirmation step (§4) and a fix (§5). REFRAME-AND-DEFER's caution is honoured (we did not declare "envelope-specific" off silence); its *defer* is replaced by *diagnose → validate → fix*.
- **b6 STILL stays until the fix lands + re-validates.** Recognition → validate → commit: the diagnosis is the recognition; rocket's role-count (§4) + the G7 re-pass (§5) are the validation; the fix is the commit. No destructive move fires on the diagnosis alone.
- **The role-floor fix IS the real Prerequisite for Decision 2 (b6 deletion).** b6's *only* load-bearing rescue was rogue's upper tiers (§2). Once the fixed envelope carries rogue's upper tiers under G7, b6 has nothing left to rescue → Decision 2's both-pass tally (b6-deletion-prerequisites brief) can finally close. The warrior/grappler/hunter "co-broken" band does **not** gate deletion — b6 wasn't helping them.

## 7. Routing (for KR to sequence)

1. **rocket — §4 role-count audit FIRST** (cheap; confirms or refutes the diagnosis). Gate everything below on its pass.
2. **gamora — caster-hot follow-up** (Matt-greenlit), reframed as the §3 confirmation with a pre-registered branch-4 prediction. Can run in parallel with (1); both are read/measure, neither destructive.
3. **On (1) confirmed:** rocket authors the §5 coordinate-derived role-floor (math-note first, Discipline #1) → jack-ryan Gate-1 → implement → gamora re-runs **Prereq B / G7** on the rogue cell.
4. **On the G7 re-pass:** the b6-deletion both-pass tally closes; Decision 2 fires per the prerequisites brief (gandalf + Matt confirm the destructive deletion; rocket executes; jack-ryan Gate-2).
5. **Matt:** the two reserved WS1 decisions are now *informed by a diagnosis*: (a) the reshape call is **"fix the envelope role-floor"** (not "reshape b6," not "hold open"); (b) the caster side-finding (moderate-modifier upper-tier-kills deficit) remains rocket's separate composition concern — orthogonal to the role-floor fix, NOT gating it. Push of the held commit chain still your call.

---

**Signed:** gandalf, 2026-06-15
**For:** converting the b6-reshape scoping's HELD "rogue-specific open hypothesis" into a located, code-cited diagnosis — the weapon-as-envelope composer dropped the b6 template's role-composition floor (no `defensive`-role emission at all `:243-252`; no `burst` below power-60 `:248`; no `required_roles` enforcement), so a glass single-target cell composes with zero survival/zero spike → over-shreds swarm + craters boss → unshapeable for one global modifier, while b6's forced `mobility 2 + defensive 1 + burst 1` carries it. Fix is a coordinate-derived role-floor (`def_bin=glass` → survival min the highest-leverage line), confirmed cheaply by a rocket role-count, re-validated by a G7 re-pass, and gating the b6 deletion; the Matt-greenlit caster-hot run is reframed as a sharp branch-4 prediction that resolves gamora's INCONCLUSIVE on evidence. The archetype label does not linger and does not return as a template — the floor is substrate-derived.
