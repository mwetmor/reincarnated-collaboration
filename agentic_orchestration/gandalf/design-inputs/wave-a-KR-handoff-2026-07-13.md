# Wave-A → KR handoff brief

**From:** gandalf (SPEC-AUTHOR) · **To:** knight-rider (sequencing + dispatch authoring) · **Date:** 2026-07-13
**Full spec:** `wave-a-engine-spec-2026-07-13.md` (build-against detail) · **Rulings:** `wave-a-summon-proxy-RULINGS-2026-07-13.md` · **Evidence:** `wave-a-summon-proxy-evidence-v1.md`

KR: this is the cover-sheet. The full spec has the file/line detail; below is what you need to sequence and dispatch.

---

## What Wave A is
Make the summon/proxy family shippable in the dev-log catalogue (Matt: ship all 4 economies for veteran gamers). Design north star: a summon kit can legitimately occupy **FREE-MOVE × BEAM** because the proxy absorbs the commitment the player would otherwise pay (GX-19), balanced by a permanent C1a floor with the C1b endgame drop-and-forget fantasy as the intended payoff.

## Two dispatch targets

**rocket (generation / config):**
- Economy config surface A1–A4 (spec §2).
- **A3 reservation-ceiling resource type** — NEW mechanic; gandalf leans build-true (not approximated). *(One of two escalations — see below.)*
- C2a dual-address + center-of-gravity emission (spec §5).
- `_DEFERRED_PROXY_BINS` lift (spec §9) — **sequence LAST**, after calibration signs off.

**gamora (simulation / AI / calibration):**
- B1 re-summon fight-loop (spec §3) — the one real fight-path gap.
- GX-19 proxy commitment clock (spec §4) — proxy carries channel/wind-up; player cast instant.
- Proxy-AI behavior-branch map + proximity trigger (spec §7).
- C1a/C1b calibration bands with D3-evaporate / D2-dominance rails (spec §6).
- **Ranged-proxy nav fix** (spec §8) — *(escalation — see below.)*

## Two items requiring a ruling BEFORE the specialist builds (Gate-1 fold D — gandalf did NOT self-authorize)
1. **Ranged-proxy nav defect** (`spatial_engine.py:~1996` / `:2350`): archer parks 38.9m from boss; it's a nav mechanic, not tuning. Fix-shape options: (a) boss-focus inheritance [gandalf lean], (b) hold-at-range behavior variant, (c) nav_target priority override. **Route the fix-shape decision to Matt/gamora before build.**
2. **A3 reservation-resource type**: build-true (permanent regen-cap tax) vs approximate-as-spend. gandalf lean: build-true. **Confirm before rocket builds.**

## Recommended sequencing (the load-bearing call)
**Melee-first, two slices.** Ranged-summon is blocked only by the nav fix (§8); everything else ships without it.
- **Slice 1 (ship now):** melee economies A1/A2/A4 + GX-19 absorption + calibration → gate lift → S6 cert at the C1b coordinate.
- **Slice 2 (behind escalations):** ranged-summon (after nav fix) + A3 reservation (after reservation-resource build).

Do NOT block all of Wave A on the two escalations — Slice 1 is fully authorized and independent.

## S6 interaction
The matchup gate certifies at the **C1b endgame coordinate** with D3-evaporate / D2-dominance as pass/fail rails. Wave A must land before its kits enter the S6 population.

## Data-correction routing (elrond, folds in cleanly — from the returns adjudication)
1. `poe1-ring-of-shields` → `le-ring-of-shields` (game-attribution error, 2-source confirmed).
2. CotA vs IK-HotA ruled distinct — no dedup.
3. `d2-sacrifice`: set `negative=1` (KEEP — joins the 37-entry negative-canon family; excluded from S6 population).
4. Ingest 9 mint dossiers' era_year/patch + URL backfill.
