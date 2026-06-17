# Round-2 Lighting-Lift Brief — Descent Scene (drax)

**STATUS:** STAGED — fires the moment drax Round-1 returns (audit-all-zones + sanctum stair fix + load-path scan) AND gandalf has ruled the Round-1 load-path flags. Do NOT run a second drax instance on `render_descent_scene.gd` while Round-1 is live.
**Author:** gandalf (design steward). **Date:** 2026-06-17.
**Parent:** `agentic_orchestration/gandalf/notes/2026-06-17-descent-runtogreen-log.md` (the run-to-green tracker; Round-2 PLAN section).
**Input data:** galadriel register-2 baseline `agentic_orchestration/galadriel/reports/2026-06-17-descent-iter4-register2-baseline-all-zones.md` (commit `4d6efd2`).

---

## 0. The diagnosis (read first — this is WHY, not just WHAT)

The descent is NOT one wrong lighting value. It is **cumulative-trim drift** — Discipline #13 implicit-pillar drift, made of register-correct local fixes that summed below the bar:

| Iteration fix | What it did | Lever |
|---|---|---|
| iter1 Fix 2 | trimmed `CombatFill` 1.5→1.15, tinted green-cool, atten 1.5→1.7 | `render_descent_scene.gd:625-628` |
| iter2 change C | pulled green fog back to a "shadow bed"; ambient warm-biased but low | `:1971-1982` (`ambient_light_energy 0.24`, `fog_light_energy 0.46`) |
| (rig) | global directional trio is the "warm-key/cold-rim/**low-fill**" proven rig | `descent_scene.tscn` bootstrap |

Each was correct in isolation (stop floor-wash, keep green as mood-bed-not-flood, dark void). **Stacked, the scene drifted to a flat dim mid-grey wash (LDR 103–122) with no bright key (SHF low).** The warm braziers — the actual keys (energy 2.2–3.0, range 7–9) — are *local pools* that don't reach far enough to build the bright LDR pool the boss arena got from one `CombatFill` at energy **1.5 / range 34 / atten 1.5** (`render_boss_arena.gd:229-235`), which scored **LDR 176 = PASS**.

**galadriel's twin signature — LDR low AND SHF low — is the fingerprint of "all fill, no key."** You do not fix it by raising the *fill* (that lifts LDR a little while flattening SHF further — MORE grey). You fix it by **restoring a KEY of boss-arena reach per chamber**: a bright pool that lifts the lit zone (LDR→~176) while the green fog + low ambient let the surround fall to dark (SHF deepens). High LDR + high SHF simultaneously = "premium lit-volume-in-dark," which is the register-2 target. That is the boss-arena lever, and it is exactly what the descent trimmed away.

**North-star profile (proven PASS):** boss-arena `CombatFill` `Color(0.78,0.82,0.95)` / energy **1.5** / range **34** / atten **1.5**, paired with brazier keys energy **2.2** / range **8**. The descent must hit the same *on-screen* LDR — and because the descent carries a heavier green-fog + low-ambient overlay than the single boss arena, it will likely need to push *past* the raw boss-arena fill value to land the same measured LDR. Tune to the measurement, not to the number.

---

## 1. The work — per-chamber key restoration, prioritized by galadriel's data

drax owns the exact values; this brief sets the **direction + acceptance**, citing the proven lever. Tune each to galadriel's re-score, not to a fixed constant.

1. **zone2 warhall — FAIL 3.0 (LDR 103 / SHF 13), flattest + coolest, #1 priority.** Furthest from gate, biggest single win. Root cause: the cool `CombatFill` dominates and warm keys are too sparse → coolest + flattest. Fix = **add warm key budget** (more / brighter braziers or a warm overhead key) so a bright warm pool reads, AND restore fill reach. Do NOT just raise the cool fill — that deepens the cool-grey flatness galadriel flagged. Target: warm bright pool, LDR→~176, SHF deepen.
2. **zone1 arcane — FAIL 3.25 (LDR 108 / SHF 18).** Clear the LDR-115 floor + restore shadow depth. Key-lift: restore `CombatFill` reach toward the boss profile + ensure a bright key pool. Smaller gap than zone2.
3. **establish ×3 — FAIL 3.0 (LDR 94, lowest of all).** Treat as ONE fix. Spine relight + de-clutter. The establishing cams peer down the whole descent into green fog; the lowest LDR means the mid/far field is fog-muted to grey. Lift the near-cluster key (the "wow" frame's gold-lit corner per `:2028-2037`) so the foreground reads premium, and gate on **light + composition** (de-clutter the busy read), not light alone.
4. **zone3 oubliette — FAIL 2.75 (LDR 105 / SHF void), lowest composite.** galadriel: "underlit-empty-void, no bright key — not dramatic lit-volume-in-dark." Fix = **a torch-LINE** (a row of warm keys, not one) converting empty-dark → dramatic lit-volume-IN-dark. This is the clearest "key not fill" case: the void needs *bright points with falloff*, which raise LDR at the torches and keep SHF deep between them.
5. **zone4 antechamber / zone5 sanctum / zone0 threshold — FAIL 3.5 / 3.5 / 3.25, smallest gaps.** Shadow-deepen + modest key restore. **Fold zone5's relight into drax's stair re-render** (geometry already changing there — one render). zone4 is the green chamber (`_is_green`); keep the green identity, just lift the key.

---

## 2. The VFX-inheritance validator (the ONE windowed capture)

Per the run-to-green log ★ CANON CALL: VFX gate = inherited PASS (hero summon eruption is zone-invariant; boss arena proved 4.01% peak). **Validation, ONCE, on the hardest case:** after **zone2** is relit, run ONE windowed eruption capture in zone2 (the worst-lit chamber) and confirm the hero column still peaks ~4% HLF against the *relit* backdrop. The relight target (LDR ~176) is the exact profile the boss-arena column popped against, so the eruption should POP, not wash. If zone2 holds on the hardest case, inheritance holds for all — no other windowed re-renders needed.

---

## 3. Acceptance (the dual gate)

- **Gate A (galadriel re-score):** each relit zone/establish composite **≥ ~4.0 + both mandatory gates**. The lighting axis specifically must show **LDR lifted toward ~176 AND SHF deepened** — both, simultaneously. A zone that raised LDR but flattened SHF has raised the fill, not restored the key → REJECT, re-tune.
- **Gate B (load-path / gandalf rule):** any geometry that changed (zone5 stair re-render; anything drax's Round-1 load-path scan flagged and fixes) must pass the both-ends-land canon call on the re-rendered audit still.
- **VFX:** zone2 windowed eruption confirm ≥ ~4% HLF (the inheritance validator).

---

## 4. PENDING FOLD-IN (from drax Round-1 — do not fire Round-2 until ruled)

drax Round-1 includes a **both-ends-land load-path scan across ALL zones**. Any failures it flags (floating arch / stranded span / ungrounded gallery deck in zones other than the known sanctum stair) get **ruled by gandalf** and **folded into this brief as geometry fixes** before Round-2 fires — so a single drax pass does relight + any geometry fixes together, minimizing render rounds. Placeholder until Round-1 returns:

- [ ] sanctum stair fix verified landed (Round-1 deliverable)
- [ ] load-path scan flags ruled (gandalf canon call) → list geometry fixes here
- [ ] then fire Round-2 = relight (§1) + geometry fixes + zone2 VFX confirm (§2)

---

**Signed:** gandalf, 2026-06-17. Staged Round-2 lighting-lift brief — root-caused as cumulative-trim drift below the proven LDR-176 boss-arena bar; the fix is per-chamber KEY restoration (bright pool + deep surround), not fill-raising. Fires on drax Round-1 return + load-path ruling.
