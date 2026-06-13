# BC Orphan-Lever Inventory — Generation-Side Audit Against the Lock Spec

**Type:** query write-up / framing-audit instrument (gandalf-authored; KR turns into the rocket dispatch)
**Authored:** 2026-06-13
**Author:** gandalf (story-and-design steward)
**Baseline doc:** `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — the 8-axis lock; authoritative **required-inputs registry** AND **deferral registry** (it does both jobs; see §1)
**Triggered by:** the BC-measurement keystone (Cycle-4) Axis-4 collapse/inversion finding — defensive levers composed-but-never-allocated
**Routes to:** rocket (generation-side primary); gamora flagged for sim-side rows
**Gates:** the eventual defensive-bridge design-spec-as-math (gandalf) is gated on this audit's result — one-off vs class decides contained-fix vs general allocator-wiring pass

---

## 0. The one-line ask

For every measurement-formula **input** the lock spec requires across all 8 BC axes, trace the generation pipeline (`bc_target` → composition lever → allocation consumer → sim telemetry) and classify each input. **Goal: determine whether Axis-4's composed-but-unallocated "silent orphan" is a one-off or a class.** This sizes the fix *before* any bridge gets specced.

This is inventory only. Fixing nothing here.

---

## 1. Why the lock doc is the baseline — and does double duty

Matt's question was exact: *will this find all orphans as compared with the lock specs?* Yes — and the lock (`qd-engine-bc-axes-lock-2026-05-20.md` §3.1–3.8) is authoritative for **two** things this audit needs:

1. **The required-inputs registry.** Each axis's *Measurement* block names exactly what its bin-assignment formula consumes. Axis-4 §3.7: `HP`, `shield_pool`, `regen_per_sec`, `mitigation_fraction`, then `evasion_misses` / `iframe_coverage` / `stealth_no_hit` / `reflection_redirected`. Every named input is one audit row. No input the lock names is exempt.

2. **The deferral registry.** Each axis's *Substrate flags* + *Sim deferral risk* subsections already **declare** which inputs are known-absent or sim-deferred — Axis-2A proxy generation "absent today"; Axis-4 dodger stealth/iframe/reflection "NO support" (§3.7 rows 356-365); Axis-1 `movement_displacement_per_cast` "needs adding to generation metadata"; Axis-5 charge-stack / damage-taken-converts bins sim-deferred per §5. **Those zeros are EXPECTED. They are not bugs.**

So the audit's real product is a subtraction:

> **(inputs that read zero) − (the lock's own declared deferrals) = the SILENT orphans.**

The SILENT orphans are inputs the lock *assumed wired*, that have no generation-side allocator, that nobody flagged. **Axis-4's eHP levers are the seed case:** §3.7 lists no deferral for `shield_pool` / `regen_per_sec` / `mitigation_fraction` / vitality-driven `HP` — they were supposed to be wired. They weren't. Silent. That is precisely why the axis collapsed without anyone noticing for three weeks.

---

## 2. Classification scheme

Per (axis × formula-input) row, classify into one of:

| Class | Meaning | Bug? |
|---|---|---|
| `WIRED` | composition lever + allocation consumer + sim telemetry all present | no — healthy |
| `ORPHAN-gen` | lever composed (written to `substrate_trace`) but **no allocator consumes it** into a kit stat | **YES — the Axis-4 class** |
| `MISSING-gen` | formula needs the input; generation creates **no lever at all** | **YES** (unless lock-deferred) |
| `GAP-sim` | kit gets the stat but sim emits **no telemetry** for it → formula reads zero | **YES — gamora seam** |
| `DEFERRED-lock` | named in the lock's own *Substrate-flags* / *Sim-deferral* subsection | no — known gap, paper trail |

Plus a boolean **`SILENT` flag:** true when the class is a bug-class (`ORPHAN-gen` / `MISSING-gen` / `GAP-sim`) **AND** the input is NOT in the lock's deferral registry.

**The `SILENT=true` rows are the punch list.** The roll-up count of SILENT rows, by axis, answers the one-off-vs-class question and sizes the fix.

---

## 3. Per-axis input seed (lock-sourced; rocket reconciles against the authoritative blocks)

Seeded from the lock's *Measurement* subsections, with a gandalf prior per row for rocket to confirm or refute. **Rocket: treat the lock §3.x per-axis *Measurement* + *Substrate-flags* + *Sim-deferral* blocks as authoritative; complete or correct any input I missed.**

| Axis | Formula input(s) | Lock § | Lock's own deferral note | gandalf prior (confirm/refute) |
|---|---|---|---|---|
| 1 Engagement | mean weighted skill range | §3.1 | "range well-tagged today" | `WIRED` |
| 1 Engagement | `movement_displacement_per_cast` | §3.1 | "needs adding to generation metadata" | `DEFERRED-lock` (loud) — unless added since 2026-05-20 → `WIRED` |
| 2 Geometry | `aoe_radius` / `is_chain` / `is_multi_spawn` | §3.2 | sim LOW; "chain/multi-spawn distinction requires metadata confirmation" | `WIRED` — confirm chain & multi-spawn tags |
| 2 Geometry | per-event source-tag (cast/reactive/proxy/environmental) | §3.2 | substrate flag, no defer | `WIRED` — confirm |
| 2A Proxy | mean active proxy count | §3.3 | "player-side proxy generation absent today"; sim HIGH; Profile A excludes | `DEFERRED-lock` (loud) |
| 2B Control | CC-weight / total-weight | §3.4 | sim LOW | `WIRED` |
| 3A Tempo | per-second damage-event count | §3.5 | sim LOW | `WIRED` |
| 3B Variance | CV of per-event magnitude | §3.6 | sim LOW (PARTIAL channeled) | **`WIRED` — positive control** (this axis measured CLEAN in the keystone) |
| 4 Defensive (eHP) | `HP` ← `defensive_vitality_scale` (1.8 tank → 0.55 glass) | §3.7 | **no deferral named** | **`ORPHAN-gen` SILENT — seed** (HP currently driven by element/energy priors, not the vitality scale) |
| 4 Defensive (eHP) | `shield_pool` | §3.7 | **no deferral named** | **`ORPHAN-gen` SILENT — seed** |
| 4 Defensive (eHP) | `regen_per_sec` | §3.7 | **no deferral named** | **`ORPHAN-gen` SILENT — seed** |
| 4 Defensive (eHP) | `mitigation_fraction` | §3.7 | **no deferral named** | **`ORPHAN-gen` SILENT — seed** |
| 4 Defensive (avoid) | `evasion_misses` | §3.7 | "evasion-stack builds populate dodger bin today" (assumed wired) | **SILENT CANDIDATE — confirm** (keystone avoidance_rate collapsed to ~0; if generation never allocates evasion-chance, this is a second silent orphan) |
| 4 Defensive (avoid) | `iframe_coverage` / `stealth_no_hit` / `reflection_redirected` | §3.7 (rows 356-365) | "NO support" (sim-deferred by design) | `DEFERRED-lock` (loud — not a bug) |
| 5 Resource | skill cost types (structural), resource mean/var (statistical) | §3.8 | mostly sim-side statistical reads | `WIRED` or `GAP-sim` — confirm (orphan risk here is sim-side, not gen-side) |
| 5 Resource | conversion mechanics (damage-taken-converts), charge mechanics (charge-stack) | §3.8 | bins sim-deferred per §5 | `DEFERRED-lock` (some) |

---

## 4. Deliverable shape

A table, one row per (axis, formula-input):

```
axis | formula input | lock § | composition lever? (Y/N) | allocation consumer? (Y/N) | sim telemetry? (Y/N) | class | SILENT? | notes
```

Plus a **roll-up**:
- count of `SILENT=true` rows, **by axis**
- the verdict line: **one-off (Axis-4 only) → contained defensive-bridge spec** vs **class (SILENT on N>1 axes) → general allocator-wiring pass (fresh cycle)**

---

## 5. The Axis-4 seed rows are the self-check

The Axis-4 eHP rows are the diagnostic seed — the audit should **reproduce** the keystone finding (`ORPHAN-gen`, SILENT). If any Axis-4 eHP lever comes back `WIRED`, that **refutes** the keystone diagnosis, and it is the single most important thing this audit could surface (it would mean the collapse has a different cause and the whole fix line is mis-aimed). Trust-but-verify built into the instrument.

Second Axis-4 suspect to resolve explicitly: §3.7 assumes `evasion_misses` is live ("evasion-stack builds populate dodger bin today"), yet the keystone's `avoidance_rate` collapsed to ~0 and the dodger bin never fired. Confirm whether generation allocates evasion-chance onto kits — if not, dodger is unreachable for a *second* silent reason, independent of the eHP levers.

---

## 6. Scope + lanes

- **Primary: rocket, generation-side.** The demonstrated bug class (`ORPHAN-gen`) lives in generation — composition writes the lever, allocation ignores it and draws the stat from the wrong prior. Rocket traces `bc_target` → composition → allocation per input.
- **Sim-side rows: flag for gamora, don't block.** `GAP-sim` (allocated-but-not-measured) is gamora's seam. Rocket fills the `sim telemetry?` column from the `substrate_trace` / telemetry schema where visible; flags uncertain rows for gamora confirm rather than stalling the inventory.
- **Out of scope:** fixing anything; authoring the allocator; the bridge spec. Those are gated downstream on this result.

---

## 7. Why this fires before the bridge spec (framing-audit Q2)

This is a framing-audit Q2 instrument (gandalf OP §4.1): *what evidence in current scope could refute "Axis-4 is a one-off?"* The `SILENT`-row count is that evidence, and it is cheap to get. If the defensive bridge gets specced in isolation and the orphan is actually a class, the project will have authored one patch where the architecture needed a general allocator-wiring pass — four one-offs instead of one move. Cheap audit first; spec second. Recognition → validate → commit.

---

**Signed:** gandalf, 2026-06-13
**For:** sizing the BC generation-side orphan class before the defensive-bridge fix is specced. Lock-sourced against `qd-engine-bc-axes-lock-2026-05-20.md` §3.1–3.8. Routes to rocket (gen-side) + gamora (sim-side flags); gated upstream of the design-spec-as-math.
