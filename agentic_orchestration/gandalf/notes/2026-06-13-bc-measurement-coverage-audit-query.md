# BC Measurement-Coverage Audit — Does the Archive See the Current Kit Surface?

**Type:** query write-up / second audit (gandalf-authored; KR turns into the rocket + gamora dispatch). Sibling to `2026-06-13-bc-orphan-lever-inventory-query.md` — that one asked "are the lock's 8 axes wired?"; this one asks "does the lock's 8-axis surface still cover what generation now builds?"
**Authored:** 2026-06-13
**Author:** gandalf (story-and-design steward)
**Baseline docs:** `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (the lock — but treated as a **2026-05-20 snapshot to re-check against**, NOT as current ground truth for deferrals) + the current generation feature surface in `reincarnated-engine/src/reincarnated/generation/`
**Triggered by:** Matt's framing-audit Q2 — "have we checked orphans against the new items like proxy/etc?" The first audit was structurally blind to post-lock features because it was instructed to trust the lock's deferral registry.
**Routes to:** rocket (generation surface) + gamora (sim-side measurement-to-bin wiring); design ruling on Bucket B by gandalf
**Gates:** the claim "the BC archive measures the current kit." Does NOT gate the Axis-4 defensive bridge (separable; that's confirmed + scoped).

---

## 0. The one-line ask — and why it matters more than a bug hunt

Diff the **current generation feature surface** against the **lock's 8-axis measured surface.** Find every kit feature generation now builds that the BC archive cannot see.

The stakes are not cosmetic. The BC archive is MAP-Elites — it culls behavioral *duplicates* to preserve diversity. **If the archive can't measure a kit dimension, two kits that differ only along that dimension look identical to it, and one gets culled.** A summoner-heavy kit and a solo kit with matching engagement/geometry/tempo collide and one dies — the player never sees the summoner variant. An archive blind to proxy-density / companion / a T4 mechanic *silently homogenizes the build space along that axis* — the exact build diversity Diablo and PoE live on, flattened where the characterization layer has a blind spot. That's the player consequence, and it's why this runs before anyone certifies "the archive measures the current kit."

---

## 1. Why this is a SEPARATE audit (the baseline flips)

The first audit (orphan-lever inventory) used the lock as **ground truth** — including its deferral registry: "the lock says proxy/charge-stack are deferred, so a zero there is expected, not a bug." That instruction was mine, and it was correct for items *still* deferred. But the lock is a **2026-05-20 snapshot**, and the kit surface has grown past it. Confirmed in-engine:

| Lock-deferred item | Lock's 2026-05-20 note | Post-lock build evidence |
|---|---|---|
| Proxy generation (Axis-2A) | §3.3 "player-side proxy generation **absent today**"; sim deferral HIGH | `proxy_combatant.py` + `simulation/math/proxy-kernel-extension-**2026-06-12**.md` |
| Charge-stack (Axis-5) | §3.8 bin **sim-deferred** per §5 | `generation/charge_stack_generation.py` |
| T4 mechanics (no axis) | not in the lock at all | `generation/t4_wireup.py` |

So the first audit would have stamped proxy + charge-stack `DEFERRED-lock / 0 SILENT` off a **stale note**, without checking whether their measurement is now wired. This audit **re-opens** every deferral instead of trusting it, and additionally hunts the features the lock never had an axis for.

---

## 2. The two buckets + classification

### Bucket A — re-opened deferrals (lock-deferred, possibly built-since)

For each item the lock marked deferred, check **current build state**, then **measurement wiring**:

| Class | Meaning | Bug? |
|---|---|---|
| `WIRED` | feature built in generation + sim measures it into its BC bin | no — healthy |
| `ORPHAN-measure` | feature built (generation emits the lever) but **sim computes no bin** for it / no measurement-to-bin path | **YES — SILENT** (the lock told everyone it was deferred, so nobody re-checked) |
| `STILL-DEFERRED` | feature genuinely not built yet; the lock's deferral is still current | no — paper trail holds |

### Bucket B — unaxised features (post-lock, no lock axis at all)

For each generation feature that maps to **no BC axis**:

| Class | Meaning | Next |
|---|---|---|
| `AXISED` | actually captured by an existing axis (incl. the lock's hybrid cross-axis captures — thorns/reflection/charge-stack) | close — document the mapping |
| `UNAXISED — needs ruling` | no axis captures it | **gandalf rules:** belongs-in-BC (→ new axis / extension — my seam) **or** intentionally outside the archive (like the Earth-meta layer; → document + close) |

---

## 3. Bucket A seed (re-check each; do NOT trust the lock's deferral stamp)

| Item | Axis | Lock § | Re-check question |
|---|---|---|---|
| Proxy density | 2A | §3.3 | proxy generation is built (2026-06-12) — is proxy **count** measured and the 2A bin assigned? Or built-but-unmeasured (`ORPHAN-measure`)? |
| Charge-stack | 5 | §3.8 | `charge_stack_generation.py` exists — is charge-stack **detected** and the Axis-5 bin assigned? |
| Damage-taken-converts | 5 | §3.8 | confirm build state; if built, measured→bin? |
| Mobility component | 1 | §3.1 | `movement_displacement_per_cast` "needs adding" at lock-time — added since? If so, measured into the engagement bin's mobility half? |
| Dodger sub-mechanisms (stealth / iframe / reflection) | 4 | §3.7 | likely `STILL-DEFERRED` (sim "NO support") — confirm none silently built |

**Also fold in:** the 2 `GAP-sim` rows the first audit flagged (the sim-seam gaps KR noted don't gate the Axis-4 verdict) — same seam, same question; resolve them here rather than leaving them loose.

## 4. Bucket B seed + method

**Method (rocket):** invert the first audit. The first went axes → levers. This goes **levers → axes**: inventory generation's kit-feature surface and map each feature to a BC axis. The features that map to *nothing* are the Bucket B candidates.

| Feature | Evidence | Prior — confirm |
|---|---|---|
| T4 mechanics (per-mechanic) | `t4_wireup.py`; the Q6/Q7/Q8 cascade | mixed — some `AXISED` (proxy→2A; retaliation/thorns + reflection → lock cross-axis captures), some likely `UNAXISED` |
| Companion binding | Q8 convergence matrix; companion modeled via `proxy_combatant` in sim | likely `UNAXISED → intentionally outside` (companion is a meta-layer bond, not kit-internal identity — but I rule it, not assume it) |
| COMPANION_CONTRACT / MONSTER_PACT | capstone-layer2 (the catalog gap I flagged separately) | needs ruling — is the pact a measured kit dimension or a binding? |

**Per-mechanic, not bulk:** T4 is several distinct mechanics; some are captured by the lock's hybrid cross-axis machinery and some aren't. Map each individually — a bulk "T4 = unmeasured" answer is wrong.

---

## 5. Deliverable shape

Two tables.

**Bucket A:** `item | axis | lock § | built in gen? (Y/N) | sim measures→bin? (Y/N) | class | notes`
**Bucket B:** `feature | gen evidence | maps to axis? (which / none) | class | gandalf-ruling-pending? (Y/N)`

**Roll-up:**
- count of `ORPHAN-measure` (Bucket A live bugs) — built features the archive can't see
- list of `UNAXISED — needs ruling` (Bucket B) handed to gandalf
- the headline: **does the archive measure the current kit surface — Y, or N with this gap list**

## 6. Scope + lanes

- **rocket (generation):** build-state of each Bucket A item; the levers→axes inventory for Bucket B. His seam.
- **gamora (simulation):** for each built Bucket A item, does `bc_measurement.py` compute the bin? The measurement-to-bin wiring is her seam. Also resolves the 2 carried `GAP-sim` rows.
- **gandalf (design):** rules each `UNAXISED — needs ruling` Bucket B feature — belongs-in-BC (→ new axis/extension) or intentionally-outside. The ruling is the flex point KR routes to me; KR does not pre-resolve it.
- **Out of scope:** building anything; authoring new axes; the Axis-4 bridge. Inventory + classify + surface-for-ruling only.

## 7. Why before the "archive measures the current kit" claim

Recognition → validate → commit. We *recognized* (via the keystone) that a built lever can sit silently unwired. We *validated* that on the lock's 8 axes (Axis-4). We have **not** validated it on the surface the lock predates — and that surface is where proxy, companion, and T4 live, the very dimensions that carry late-game build identity. Certifying the archive as kit-complete before this runs would repeat the keystone's mistake one architectural layer up: trusting that what was specced got wired, on features the spec never covered.

---

**Signed:** gandalf, 2026-06-13
**For:** diffing the current generation feature surface against the lock's 8-axis measured surface — re-opening every lock deferral (proxy / charge-stack / mobility, built-since) and hunting the unaxised post-lock features (T4 / companion). Routes to rocket (gen) + gamora (sim) + gandalf (Bucket B ruling). Gates the "archive measures the current kit" claim; does NOT gate the Axis-4 bridge.
