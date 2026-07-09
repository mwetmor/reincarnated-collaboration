# Dispatch — rocket: Economy-axis (E2) — bc_amplitude → mechanical economy (single-scalar k layer)

**From:** knight-rider → **To:** rocket (generation seam)
**Date:** 2026-07-09
**Pattern:** B (multi-hour build; math-before-code) — **Gate-1 (critique pair: jack-ryan + gandalf) REQUIRED before fire**
**Authority:** Matt-ratified E2 rulings 2026-07-09 (Q-E2-1 mixed portfolio · Q-E2-2 cycle-throughput invariance · Q-E2-3 modulation scope). Design note (BINDING §3): `agentic_orchestration/gandalf/notes/2026-07-09-e2-economy-axis-design-note.md`. Surface-ledger **E2** (OPEN queued → IN-FLIGHT on fire). Second axis of the full-spec main line (E1→**E2**→E4→E3).
**Status:** DRAFT — fires on Gate-1 PASS (both critique-pair members).

---

## 0. Why this axis exists (design note §5)

Post-E1, `bc_amplitude` is **v1-INERT** — a coordinate that never cashes out (a tie-shaper secondary sort only; geometry math note §3). Every kit in a BC cell has identical economy tables regardless of amplitude. E2 gives amplitude **mechanical meaning in the emitted kit's economy**: per-hit size, cooldown cadence, energy-cost texture. Same BC cell address → three recognizably different hands (spiky / flat / variable) **on the same tier spine, without touching certified power**.

## 1. Target seam + the change (design note §0, §1)

- **File:** `generation/per_skill_emitter.py` (yours). No sim-side change expected (E2 emits within existing fields; the sim already consumes per_hit/cooldown/energy_cost).
- **The change:** a **single per-skill amplitude scalar `k`** applied jointly at emission to `(per_hit, cooldown, energy_cost)` — and, for control, to `(cooldown, duration, energy_cost)` with per-hit UNSCALED. `k` is a **separate scalar LAYER on top of the base tables at emission** — NOT an edit to any table.

## 2. THE SPINE IS SACRED (design note §0, §1.2, acceptance §6) — hard constraint

**Zero diffs to** `TIER_COEFFICIENTS` (1.00/1.50/2.17/4.00), `_DAMAGE_MULTIPLIER` per (tier, role), `BASE_SPELL_DAMAGE_L50`, and the base `_ENERGY_COST` / `_COOLDOWN` tables. `k` applies as a scalar layer at emission. If your implementation requires editing any of these tables, STOP — that is a design violation, re-read §1.2.

## 3. MATH-BEFORE-CODE (Discipline #1) — REQUIRED, precedes any code

Author `generation/math/economy-axis-e2-<date>.md` FIRST. It MUST derive `k_spiky` / `k_flat` (stated lean `≈1.6` / `≈0.7`, per-hit ratio ≈2.29) under the design note §2 **four constraints, each shown with the arithmetic**:
1. **Felt-difference floor** — spiky T3 per-hit ≥ 2× flat T3 per-hit at the same (role, tier, delivery).
2. **Cadence sanity ceiling** — `k_spiky` × max modulated cooldown (T3 primary) leaves ≥ 2 casts inside a representative gauntlet fight duration.
3. **Affordability guard** — `k_spiky` × max modulated per-cast cost (T3 = 30 base) is affordable within the sim energy pool; pooling pressure OK, lockout is a defect.
4. **Flat floor** — `k_flat` cooldowns do not collapse below the sim's effective action cadence.

Also state in the note: the **conservation-law proof** (throughput = per_hit/period and cost_rate = cost/period are invariant under joint `k` by construction — §1.2); the **control cadence-only** treatment (duration scales WITH cooldown so lock-uptime duration/period is invariant; per-hit unscaled — §1.3); and resolve acceptance §8 (**duration-field location** — if control lock duration is not on the emitted skill, locate its real home; uptime-invariance applies wherever it lives — flag, don't fake).

## 4. Modulation scope (design note §1.3) — apply EXACTLY

| Role / tier | Modulation |
|---|---|
| primary_attack, secondary_attack (T1–T3) | **Full** `k` on (per_hit, cooldown, energy_cost) |
| control (T1–T3) | **Cadence-only** `k` on (cooldown, duration, energy_cost); per-hit UNSCALED |
| support | **Exempt** (no `k`) |
| T4 (all roles) | **Exempt entirely** (passive-mode capstones) |

**Per-cell assignment (role-based, not chain-letter-based):**
- **spiky cell** → all modulated chains get `k_spiky` (control cadence at `k_spiky`).
- **flat cell** → all get `k_flat`.
- **variable cell** → **primary_attack chain** gets `k_spiky`; ALL other modulated chains (secondary, control cadence) get `k_flat`. (Mixed portfolio, Q-E2-1 ruling a — burst window + filler cadence in one kit. NOT a mid-point blend, NOT a per-sample coin-flip.)

**E4 boundary held:** no `cast_time` changes under E2.

## 5. Vocabulary pin (design note §1.1, acceptance §4)

Canonical amplitude vocabulary is **spiky / flat / variable** (the catalog coordinate space, `endgame_encounter_catalog.py`). The `per_skill_emitter.py` docstring's stale **"spiky/sustained/flat"** is corrected as part of this change.

## 6. Provenance (design note acceptance §5) — certification honesty

The applied `k` MUST be **recoverable from the emitted skill record** (visible downstream, not folded invisibly into the numbers). Certification must be able to read which `k` shaped a skill.

## 7. Round-trip smoke (design note acceptance §3; E1 #2-FF pattern) — MANDATORY

Emit real kits from **spiky, flat, AND variable** cells; print per-skill `(per_hit, cooldown, cost, duration-where-control)` **before/after**; verify:
- **variable kits show the mixed portfolio** (primary_attack spiky, rest flat);
- **support + T4 byte-identical** pre/post;
- **invariance (exact, float ε):** per-skill cycle-throughput and cost-rate match pre-E2 spine values for all modulated attack skills; control lock-uptime (duration/period) invariant likewise;
- **felt-difference floor** holds on emitted kits (§3 constraint 1);
- the **sim consumes the emitted kits without a contract change**.

## 8. #2-FF fields (MANDATORY)

- **Verdict-rendering instrument named:** the round-trip smoke (§7) + the invariance check (exact) + the provenance read-back.
- **One-command pre-fire verification** that exercises the PATH: e.g. a single command printing the current docstring vocab (`spiky/sustained/flat`, the stale artifact you are correcting) and confirming amplitude is v1-inert pre-change. State the expected post-change first-log line (e.g. "kit <id> variable cell: primary k=1.6, secondary/control k=0.7; throughput Δ=0 within ε").
- **Precondition state cited:** design note (this dispatch's authority); surface-ledger E2; E1 landed (`bfc94eb`).

## 9. Cross-seam discipline (ADR-004)

No sim contract CHANGE expected (emit within existing fields). **If** your math note concludes the sim cannot consume a field you must emit (e.g. control duration lives sim-side and needs a new emitted field), that is a cross-seam change → **MIGRATION.md + Matt before tagging** (gamora owns the sim consumer).

## 10. Acceptance criteria (design note §3 — these BIND)

1. Math note lands FIRST (Disc #1), deriving k_spiky/k_flat under the four §3-constraints with arithmetic shown.
2. `per_skill_emitter.py` applies `k` as a scalar LAYER; **zero diffs** to the sacred tables (§2).
3. Invariance check exact (throughput + cost-rate + control lock-uptime) within float ε.
4. Round-trip smoke passes on spiky/flat/variable cells; variable = mixed portfolio; support/T4 byte-identical; sim consumes without contract change.
5. Vocab pin: docstring corrected to spiky/flat/variable.
6. Provenance: applied `k` recoverable from emitted skill record.
7. #2-FF fields present in the commit/run banner.
8. Tag `rocket/v<X.Y>-economy-axis-2` (seam prefix — intermediate; Matt approves any prefix drop).

## 11. Explicitly OUT OF SCOPE (prevents scope creep)

- **cast-time / wind-up / charge** — E4's axis; no `cast_time` change here.
- **resource-model / regen shapes** — the tempo axis's seam; E2 must not annex it.
- **hybrid dual-scaling** — E3 (own design pass, queued).
- **geometry** — E1, landed; do not touch.
- **band tables / re-fit** — that is gamora's post-E2 re-fit (the conservation-law audit), fires AFTER this lands. Do NOT touch bands.
- **sacred tables** — §2.

## 12. Downstream consequence (for awareness, not action)

When E2 lands, **gamora runs the post-E2 band re-fit** (the C3 ~39-min re-validation rhythm) as the **conservation-law audit**: by construction (§1.2) bands should NOT lurch — spiky/flat deltas come only from real second-order play (overkill waste, burst vs fight-truncation, energy pooling, ailment cadence, B11 interaction). **HALT RULE (relayed to gamora): if the post-E2 re-fit LURCHES, the conservation law leaked — the re-fit HALTS, findings park for Matt, no curve-fit.** That sequencing is KR-orchestrated; your deliverable is the emitter `k`-layer + the invariance/round-trip proof.

---

**Required reading (rocket, at session start):**
1. This dispatch.
2. `agentic_orchestration/gandalf/notes/2026-07-09-e2-economy-axis-design-note.md` — the design note (§3 acceptance BINDS; §1.2 conservation law; §1.3 modulation scope; §2 four constraints).
3. `generation/math/geometry-axis-e1-2026-07-08.md` — the E1 math note (amplitude's post-E1 v1-inert status, §3).
4. `canonical/current-to-end-state/surface-ledger.md` — E2 row + the spine-sacred discipline.

**Sign-off:** knight-rider, 2026-07-09 (DRAFT — Gate-1 pending). Fires on critique-pair Gate-1 PASS.
