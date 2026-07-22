# Tier-3 Encounter-Geometry Run — W4 REVIEW BOOK

**STATUS:** W4 REVIEW BOOK — run close-out; disposition fork OPEN (Matt rules).
**Author:** named-`gandalf` (W4 drafting leg), spawned by gandalf `RUN-CONDUCTOR` · 2026-07-22.
**Assembly discipline:** faithful narrative form of the run ledger + frozen prereg sheets + gate reports + QA checks. NO new rulings — every fork here is presented, never resolved (T3-V1 veto-open). Working family labels stay working labels (never canonized). Ch 1–4 report what IS (survey-mode); Ch 5–7 carry the fork + lessons + queue.
**Spine of record:** `agentic_orchestration/gandalf/notes/2026-07-22-tier3-encounter-geometry-run-state.md` (rulings L-1..L-19; Matt-interface PING-1/PING-2). This book is that ledger's chapter form; where they differ, the ledger governs.
**Charter:** `agentic_orchestration/gandalf/notes/2026-07-22-tier3-encounter-geometry-run-charter.md` v1.2 (§4 W4 row: review book + both island-condition chapters + C1–C3 evidence table).

---

## Ch 0 — Verdict summary (one page)

**What the run set out to test.** Tier-3 built an encounter *grammar* — a three-tier language (MACRO map-area decks · MESO formations · MICRO pressure-verbs) for how enemies-as-future-selves arrange in space across four genre eras — and then asked one falsifiable question at a preregistered bar: **does formation geometry move fight outcomes?** Concretely (frozen sheet `5ea56bf3` §6): do high-fit formations show a Cohen-medium effect (d ≥ +0.5) on the outcome-metric triple `mobs_killed` / `total_aoe_hits` / `player_damage_total` over a neutral baseline, do low-fit formations show the inverse (d ≤ −0.5), and does fit predict sign-direction on ≥75% of 32 pairs?

**What happened.** The gate ran twice.

- **W3 (T3-F4)** — FAIL, and the instrument was **invalid**. Zero-discretion execution of the frozen sheet was faithful, but the sheet itself carried two defects owned by its author (the conductor): a selection×construction seam (RF-A) and — the load-bearing one — an HP-budget confound (RF-B) that made 2 of 3 gate metrics measure destructible-HP, not geometry. The FAIL was registered as W3's verdict; its *interpretation* was "the ruler is broken," not "the hypothesis is false." (`b2a77763`, gate report `…/2026-07-22-tier3-w3-gate-report.md`; L-15.)
- **W3′ (T3-F4′)** — Matt authorized one re-instrument (`"W3′ go!"`, L-16 — a commitment-boundary ruling, never the conductor's to self-grant). The amendment sheet (`904f317c`) re-pinned exactly the two defects — composition-matched per-pair baselines (RF-B) + hole-cell eligibility exclusion (RF-A) — and carried every threshold verbatim. The re-run was clean: **zero red-flags, instrument VALID** — and still **FAIL** on all three legs. (`719d9e4a`, gate report `…/2026-07-22-tier3-w3prime-gate-report.md`; L-19.)

**What it means.** Two FAILs with two different meanings — and the distinction is the whole point of the honorable-fallback machinery. **W3's FAIL was the ruler's failure; W3′'s FAIL is the hypothesis's honest miss.** With RF-B dissolved (matched-baseline `mobs_killed` mean 15.2 ≈ the neutral pool's 15.28), outcome-level metrics do **not** detect formation-geometry effects at d=0.5, and fit does not predict direction (10/32, at/below chance). **The geometry hypothesis is unsupported at the preregistered bar on outcome metrics.**

**What survives.** The encounter *grammar itself* was never gated on W3 — it is the run's durable design substrate (Ch 1). The gate tested whether the grammar's geometry moves an *outcome sim*; the answer is no. Whether that means "geometry doesn't matter" or "outcome sims are the wrong venue for geometry" is the live fork of this book (Ch 5). RD-1 (the conditional emission fixture) is DISCHARGED-UNFIRED; the `encounters` bundle key stays reserved-empty by design; Lane-1 was never blocked on it.

---

## Ch 1 — The design products that STAND regardless of the gate

These were authored in W0–W2 and were **never conditioned on the T3-F4 verdict.** A FAIL at the gate retires none of them. They are the run's durable substrate — buildable-against artifacts on frozen, provenance-honest data.

**What W3/W3′ actually gated — and what it did not.** The gate tested exactly one proposition: *does the geometry these artifacts describe move an outcome sim at d=0.5?* It did NOT test whether the census is accurate (Gate-2 verified that), whether the era-decks are coherent (DRIFT-CRITIC PASS at W1), whether the fit-layer is total (0-error over 1068 rows at W2), or whether the grammar reads as drama (that is Ch 5's fork). The design products below stand on their own gates or on no gate at all; the outcome-sim gate sits *downstream* of all of them and its failure propagates to none.

**§1.1 — The encounter-grammar census (W0, frozen `f7224485`).** 80 monster-side rows across four eras (I:20 D2 · II:20 PoE1 · III:18 GD · IV:22 — 13 PoE2 / 9 LE), quota PASS ×4, md5-stamped, with an era×family coverage matrix and a two-value provenance axis (80 GENRE-ATTESTED / 0 RDR-NATIVE-DERIVED reserved). Its discipline is the thing worth keeping: **genre holes are load-bearing findings, not coverage failures.** The famous PoE1 melee deficit (MELEE-STRIKE 0/36 in Age II), SHAPESHIFT's absence as a monster-template in Ages I+III, AURA's Age-III hole — each is *published as truth*, never fabricated over. Gate-2 PASS-WITH-CONCERNS (`7f158953`, L-9). Artifact: `agentic_orchestration/elrond/notes/2026-07-22-tier3-w0-census-substrate-freeze.md`.

**§1.2 — The four era-decks + the act structure (W1, `074d0135`).** Each era carries a self-contained, order-agnostic MACRO deck of ≥4 map-area archetypes plus one exempt traveling-kin slot. The eras have *personalities because the families genuinely lived and died by era* — this is the design's spine, not decoration:
- **Age I — Diablo II's physical-brawl world.** BRAWL-form headlines (Travincal, Chaos Sanctuary courtyards). Signature family MELEE-STRIKE.
- **Age II — PoE1's attrition-and-emplacement world.** OUTPOST/EMPLACEMENT headlines (totem nests, trap fields, DoT clouds). Signature DOT-AILMENT — and its melee hole is honored, not patched.
- **Age III — Grim Dawn's sustained-fight world.** Aetherial channel-beams down city streets. Signature CHANNELED-BEAM.
- **Age IV — the hybrid frontier (PoE2 + Last Epoch).** All ten families present, none dominant; widest deck (58% unclaimed residual).

The kin-slot mechanism (Matt-ruled R-b3, "traveling kin is right") is the story's spatial form: beat a family → become it → ≥1 faction of that family travels as guaranteed kin into the next act, exempt from era-nativity (the whirlwind caravan in the trap-age — *the anachronism IS the story*). Spec: `…/2026-07-22-tier3-w1-encounter-grammar-spec.md` (§2).

**§1.3 — The element-courts structure.** Q38 inherited and instantiated: **element-courts k=5 · eras = shelves · biome-morph rider.** The encounter side speaks the kit side's coordinate vocabulary so `fit(kit, encounter | era)` computes on one address space. Every W3/W3′ era draft cleared the ≥3-courts floor with 4–5 courts represented — the courts structure held under selection pressure across both gate generations.

**§1.4 — The MESO formation catalogue + the COMMON-4 sim-expressible subset.** The MESO tier is the run's formation vocabulary: each working-label family carries ≥2 era-tagged, provenance-flagged formations, geometry-described and harvest-anchored. The eleven families' headline formations (working labels; `formation_id` · geometry · what pressure it creates):

| Family | Headline formation | Geometry / pressure |
|---|---|---|
| WHIRLWIND | `ww_converge_spin` | rotating encirclement body pins-and-closes on the player point |
| CHANNELED-BEAM | `cb_lane_hold` | caster channels a directed beam down a lane; screen holds player in the zone |
| AURA | `aura_carrier_pack` | hidden carrier buffs the pack; identify-and-kill-the-carrier first |
| TOTEM-SENTRY | `ts_anchor_screen` | stationary emplacement sustains threat; mobile screen guards it; prioritize the anchor |
| TRAP-MINE | `tm_preseed_corridor` | hazards pre-seed a corridor into a sequential detonation field |
| MELEE-STRIKE | `ms_swarm_surround` | massed low-threat runners close-and-surround; lethal by density |
| DOT-AILMENT | `da_field_retreat` | casters stack DoT ground-fields from range, chaff drives player INTO them |
| MPV | `mpv_fan_from_position` | ranged units fan volleys from a fixed/elevated position, screen holds the cone |
| CHAIN-BOUNCE | `cbn_corridor_arc` | arc-bolts bounce player↔adds↔walls; corridor amplifies to multi-hit |
| SHAPESHIFT | `ss_phase_transform` | mid-fight form-transition brings NEW attack verbs (strain-4 — CANNOT yet) |
| DASH-STRIKER | `ds_flank_burst` | mobile gap-close from a flank into burst pressure |

Of these, four formation *classes* are fully expressible in the live `spatial_gauntlet/` harness today and became the gate's construction vocabulary — the **COMMON-4: swarm · volley-fan · lane · emplacement.** These are the run's proven-buildable formation grammar (all four held 40-mob parity across both gate generations). The full catalogue stands as design substrate; COMMON-4 is the subset the sim can currently *render as combat* (strain-4 — the four hardest — remain queued as Lane-2 requirements, §1.6).

**§1.5 — The fit-layer v2 (W2, rode `f1752755`).** The instrument that scores `fit(kit, formation | era)` = `0.50·verb + 0.30·topology + 0.20·shelf`, computed total over 267 kits × 4 era-decks = **1068 rows / 0 errors / 0 kits dropped** — every kit either resolves a family or degrades cleanly to era-level (no fabrication). After the prereg-beat re-join it resolves 131/267 spine kits at full family basis (up from 46), with per-row `membership_tier` and `scoring_basis` tags so any downstream stratifier can see the resolution mix. This is a reusable scored-catalogue artifact independent of the gate result. Report: `…/2026-07-22-tier3-w2-fit-layer-report.md`.

**§1.6 — The strain-4 requirements (W2 → Lane-2).** The four deliberately-harder STRAIN formations that the harness CANNOT yet fully express were probed and routed as requirements (L-12), not faked: `ss_phase_transform` (CANNOT — mid-fight entity-mutation hook, net-new) + `cbn_corridor_arc` / `cb_crossfire` / `ts_environmental_nest` (PARTIAL — projectile wall-reflection, native paired-emitter tracking, killable-spawner-entity). One-way coupling held: gamora reported, conductor routed, nobody wrote into Lane-2's spec. These are honest capability-gaps published as a queue.

---

## Ch 2 — Island conditions C2/C3 (from the W1/W2 evidence)

Matt's island ruling (2026-07-22): *"build out new islands after Tier 3 completes if the data points will be fully populated and if you have ultra thought about how we can develop these families at that point"* → island conditions C1 (Tier-3 complete), C2 (per-family data-population census), C3 (family-development ultra-think). The build-out + scoring is **PRE-RATIFIED** (Matt third grant, L-6: *"You have my ratification to build it out and score it"*); it fires on C1–C3 evidence at conductor timing, survives the fallback path (depends on data population, not the T3-F4 verdict). **Island NAMES remain Matt's** (Q32 naming one-sitting).

**§2.1 — C2: per-family data-population census (what the W2 evidence shows).** The three-tier family membership is materialized on the spine at **131/267 kits** (L-13(b), sidecar `6dd43161`): RATIFIED 86 + PROPAGATED 44 + DOCKET 145 tiers joined, precedence RATIFIED > PROPAGATED > DOCKET, every kit exactly one active row. Four signature families were recovered from zero-spine to populated (MELEE-STRIKE 0→15 · DOT-AILMENT 0→20 · MPV 0→14 · SHAPESHIFT 0→5). Honest remaining holes: **MINION-PET + IDENTITY-GAUGE** (guest families, catalogue-only this run per charter §1 — no native act presence, L-4) and **CHAIN-BOUNCE + DASH-STRIKER** (fresh-draft tier, excluded from serving per T3-V2). The population is real but skewed: the resolved spine leans TOTEM/TRAP-heavy (58 of 131) — a sampling fact any island re-cut must handle, exactly as the W3 sample rule did via family round-robin.

**§2.2 — C3: family-development ultra-think (what the run learned about developing families).** The W1 grammar is the family-development instrument: it demonstrates that each working-label family carries a coherent MESO formation vocabulary (≥2 per present cell) and a MICRO pressure-verb inherited from the family kit-leader's mechanism (R-b2). The era-honesty finding is the development lesson: **families should not be developed uniformly across eras — they should be developed where the genre lived them.** The census's per-era signature-vs-hole pattern is the map for that:

| Family (working label) | Where it is SIGNATURE / rich | Where it is a load-bearing HOLE |
|---|---|---|
| MELEE-STRIKE | Age I (D2 brawl, 8 rows) · Age III (7) | **Age II** (the famous PoE1 melee deficit, 0/36) |
| DOT-AILMENT | Age II (PoE1 attrition, signature; 15 kit-mass) | — (present all eras, thin outside II) |
| CHANNELED-BEAM | Age III (its home shelf, 6 rows) | **Age I** (D2 Inferno-career hole) |
| AURA | Age I (3) · Age IV (3) | **Age III** (true genre hole; GD "Supporter" unratified) |
| TOTEM-SENTRY | Age IV (the Age-IV signature, 5 rows) | — |
| MPV | Age I (4) · Age IV (4) | **Age III** (GD ranged is single-shot, not fan-volley) |
| WHIRLWIND | Age IV (2) · Age I boss (1) | **Age II** (served only via RDR-native derivation — no PoE1 spin-mob) |

An island layer re-cut on this substrate should **inherit that per-era weighting rather than flatten it** — a MELEE island in the trap-age would be genre-false, an AURA island in Age III fabricates over a load-bearing hole. The cross-era resurrection-leader verb (U-2/U-6 candidate spanning Ages I+III) is a flagged development-input — CANDIDATE / NOT-A-FAMILY / docket-input, do NOT canonize.

**§2.3 — L-6 pre-ratification standing.** The island build-out + scoring is authorized to fire on this C2/C3 evidence at conductor timing; the beat gets its own mini-charter (input set pinned there; ARCHITECT completeness pass at that boundary). This chapter satisfies the C2 + C3 *evidence* obligation; the build-out itself is a downstream beat, and **island NAMES stay Matt's Q32 gate** — nothing here canonizes a name.

**C1–C3 evidence table:**

| Condition | State | Evidence |
|---|---|---|
| **C1** Tier-3 run COMPLETE | ☑ (this book closes it) | W0–W3′ executed; W4 book delivered |
| **C2** per-family data-population census | ☑ (§2.1) | 131/267 spine resolved; 4 signature families recovered; 4 honest holes; TOTEM/TRAP skew noted |
| **C3** family-development ultra-think | ☑ (§2.2) | per-era-weighted development lesson; MESO/MICRO vocabulary demonstrated; resurrection-leader docket-input flagged |

---

## Ch 3 — Instrument generation 1 (W3): the ruler's failure

W3 executed the frozen sheet `5ea56bf3` with zero discretion — census clean (courts 5/era ×4, 0 swaps), 40-mob parity held by all four COMMON-4 builders, fighter byte-identical to baseline, HEAD `a3671d4` unmoved (subtrees byte-identical, no HALT), corpus md5 stable, zero engine/telemetry writes. The executor was **faithful.** The FAIL came from two defects in the sheet, both owned by its author (the conductor).

**§3.1 — RF-A: the selection×construction seam.** Sheet §5.1's candidate pool admitted hole cells (`family_present=hole`, fit 0.15, `meso=[]`) that §5.4's construction rule cannot build — a hole cell means the era's deck deals that family NO formation, so there is no geometry to construct. Four low-side argmin picks landed on genre holes (I/CHANNELED-BEAM, II/MELEE-STRIKE, III/AURA, III/MPV). The executor **stopped those 4 pairs and recorded them** — it did not improvise a formation (that would fabricate substrate). Consequence: the low side scored 12/16, a complete 32-sample was impossible, and per §6's no-partial-pass a PASS could not be certified regardless.

**§3.2 — RF-B: the HP-budget confound (the load-bearing defect).** Sheet §2 pinned mob-COUNT parity ("40 total") believing count pinned budget. It did not. The baseline `open_arena` was **3-elite + 37-swarm at 1.5× MOB_HP_DIFFICULTY ≈ 19,575 destructible HP**; the COMMON-4 formations were homogeneous, unscaled, ~6,000 HP. The mechanism:
- `mobs_killed` **saturated at the 40 ceiling** — the fighter cleared the weaker homogeneous formation to 40/40 on nearly every seed, while the elite-heavy baseline sat lower, so low-fit pairs registered *large positive* d (kill more, weaker mobs).
- `player_damage_total` **pinned to formation total-HP** (~6,000 for a full swarm clear), regardless of fit.

So **2 of 3 gate metrics measured HP budget, not geometry**, and `total_aoe_hits` was ceiling-coupled to `mobs_killed`. This mechanically explains the signature failure — **LEG-2 stress inverted to +0.507** (needs ≤ −0.5): low-fit pairs did *better* than the elite-heavy neutral because they faced a cheaper HP pool. The confound was inherent to the frozen instrument; matching per-mob HP alone would not have dissolved it, because the elite/swarm split was unpinned by "40 total."

The three legs and the confound made visible in the per-metric medians (W3, `b2a77763`):

| Leg | Value | Threshold | Pass |
|---|---|---|---|
| LEG-1 showcase (16 high) | 0.0 | ≥ +0.5 | ✗ |
| LEG-2 stress (16 low) | **+0.507** | ≤ −0.5 | ✗ (sign-inverted) |
| LEG-3 direction | 7/28 | ≥ 24/32 | ✗ (incomplete 32 per RF-A) |

| Metric | high median d | low median d | reads as |
|---|---|---|---|
| mobs_killed | 0.0 (ceiling-pinned) | +0.507 | HP budget |
| total_aoe_hits | 0.0 (ceiling-coupled) | +0.585 | HP budget |
| player_damage_total | −0.727 | −0.065 | formation-HP-pinned |

**§3.3 — The "surviving emplacement signal" (and its later re-attribution).** W3's report noted that even HP-confounded, emplacement high-picks showed genuine-looking positive fit response (d2-frenzy-barb +1.05 · le-explosive-trap-falconer +1.19 · poe1-armageddon-brand +0.70), and named `player_damage_total` as the metric to free. **W3′ later re-attributed this signal to the RF-B artifact** (Ch 4.5) — under a clean instrument it did not survive. Recorded here as the honest lifecycle of a signal: it looked real at generation 1 and dissolved at generation 2. LEG-1 showcase median was 0.0 and LEG-3 was 7/28 — a FAIL robust to any HP choice the sheet left open.

The verdict registered as W3's, its interpretation as **"instrument invalid for the geometry hypothesis," not "hypothesis false"** — the exact distinction the honorable fallback exists to carry (L-15).

---

## Ch 4 — Instrument generation 2 (W3′): the honest miss

Matt authorized one re-instrument (L-16). T3-F4′ was a **NEW gate** — the W3 FAIL stands unrevised, the RULER changes, the BAR does not. jack-ryan verified this framing as honest on three axes (`f1c45e9f` (f)): W3 FAIL stands verbatim, the bar is byte-identical (X=0.5, Y=75%, three-leg conjunction, no-partial-pass), only the measurement instrument changed. This is the textbook-legitimate reason to re-run a preregistered experiment.

**§4.1 — The fix: composition-matched per-pair baselines.** Each pair's baseline is now the open arena holding that pair's **exact encounter mob multiset** (count + tier + per-mob HP + scalars), placed without formation structure. `Δ_m(seed) = m(encounter) − m(matched baseline)`. Now **both** the fighter (carried from base §2) AND the HP budget cancel in Δ — the manipulated variable is placement geometry alone, the isolation the base sheet claimed and did not deliver. A COMPOSITION-PARITY HARD INVARIANT (equal multisets both arms, else per-pair red-flag) enforced it; the executor verified parity TRUE ×4 classes with the 1.5× multiplier correctly inert on both arms (per-mob HP byte-identical, 150 both sides — resolutions M1–M3, `…/2026-07-22-tier3-w3prime-gate-math.md`).

**§4.2 — The §8 freeze-beat pins (jack-ryan's three WARNs folded, L-18).** The re-instrument's second-order consequences were pinned before freeze so no discretion survived:
- **C1 — standardizer DECLARED conservative.** `sd_pool′` keeps composition-scale spread in the denominator BY DESIGN; d is conservative on both magnitude legs (larger denominator, harder to clear ±0.5), neutral on sign. The within-composition alternative was **REJECTED** — it would silently weaken what X=0.5 means while claiming "bar unchanged." (Recomputed pre-gate: mobs_killed 13.011 · aoe 13.011 · damage 1951.69.)
- **C2 — SEALED pre-gate artifact.** The runner wrote `…-w3prime-pregate-seal.json` after the 128 baseline fights and BEFORE any encounter fight — 32 compositions + parity verification, per-cell means, `sd_pool′`, degeneracy flags, informative-count + sign rule; the gate output embeds its md5 (`3c2bf374…`); mutation ⇒ HALT. This makes "stamped pre-gate" a hash-checkable invariant, not an assertion.
- **C3 — degeneracy-rule edges.** ≥90%-at-bound over the 32 baseline cells' 4-seed MEANS only (integer ≥29/32); informative-metric count frozen at the seal, immutable post-encounter (a metric informative on baselines but saturating on encounters stays IN). This is the anti-gaming shape: **every metric-drop tightens toward HALT, never toward an easier pass.**

**§4.3 — The clean execution.** Eligibility redraw clean (full 32, 0 swaps, courts ≥4/era, the 4 W3 hole picks redrawn to next-best buildable); seal written pre-encounter and immutable; degeneracy baseline-only (NO metric degenerate — 4/32 at-bound < 29; α nominal 0.0035 discharged, C5 reporting obligation met exactly); 256 distinct fights, no memoization (C6 discharged); HEAD byte-identical; corpus md5 stable; ZERO writes; **ZERO red-flags.** The W3 red-flag machinery was retained unchanged and had nothing to catch. The latent `SHAPESHIFT/IV` unbuildable-present edge sat mid-pack (fit 0.5–0.6), never drafted as argmax/argmin, did not fire.

**§4.4 — The three legs (the honest miss).**

| Leg | Metric | Value | Threshold | Pass |
|---|---|---|---|---|
| LEG-1 showcase | median composite d, 16 high-fit pairs | **0.0** | ≥ +0.5 | ✗ |
| LEG-2 stress | median composite d, 16 low-fit pairs | **+0.192** | ≤ −0.5 | ✗ (wrong sign, uniform across all 4 eras) |
| LEG-3 direction | pairs sign-correct (≥2-of-3 informative) | **10/32** | ≥ 24/32 | ✗ (at/below chance — high 7/16, low 3/16) |

Per-era decomposition (descriptive, not gated) — the LEG-2 sign failure is **uniform, not an era outlier**: every era's low-fit median is POSITIVE, and only Era II shows even a mild high-side tilt:

| Era | high median d | low median d | sign-correct |
|---|---|---|---|
| I | −0.231 | +0.442 | 2/8 |
| II | +0.240 | +0.346 | 4/8 |
| III | 0.0 | 0.0 | 2/8 |
| IV | +0.346 | +0.346 | 2/8 |

**§4.5 — RF-B dissolution evidence (the whole point of W3′).** Under the matched baseline, `mobs_killed` now spreads 0–40 with **mean 15.2 ≈ the neutral pool's 15.28** — the ceiling saturation that drove W3's inversion is gone; only 4/32 baseline cell-means sit at the ceiling (< the 29 threshold). The instrument now isolates geometry, and the honest geometry-only result is FAIL. **W3's "surviving emplacement signal" is thereby re-attributed to the RF-B artifact.**

**§4.6 — Metric collinearity 28/32.** In homogeneous-mob clears, kills, AOE hits, and damage move together — **28 of 32 pairs have identical d across all three metrics**, so the composite ≈ a single shared d and the ≥2-of-3 rule provides no independence here. This is not an execution defect; it is a property the base sheet acknowledged ("correlation within the triple is acknowledged; ≥2-of-3 is a robustness device, not an independence claim") and W3′ confirms empirically. It sharpens the negative result: at the outcome-metric layer for homogeneous clears, there is effectively **one** metric, and geometry does not move it.

**§4.7 — The positive per-family minority (swamped).** A minority of families showed positive mean composite d — **TRAP-MINE +0.793 · MPV +0.705 · AURA +0.589** · TOTEM +0.208 — while WHIRLWIND 0.0 · CHANNELED-BEAM −0.077 · MELEE-STRIKE −0.103 · DOT-AILMENT −0.231 sat at or below zero. The emplacement/pre-seed families (things that hold a position the player must approach) tilt positive; the swarm/melee families do not. But the d=0.0 bulk swamps the minority: the showcase *median* is 0.0. This is a texture-level hint the outcome-median cannot register — a thread Ch 5(a) picks up.

**§4.8 — jack-ryan's INFO carries (routed here per §8.4).**
- **C4 (fit-instrument note for future laps):** hole cells score fit=0.15 while the worst *buildable* cells score fit=0.10 — "no geometry dealt" scored *higher* than "geometry present but terrible fit." The hole penalty is mis-ordered relative to real low fits. Immaterial to W3′ (holes excluded entirely), but **any future lap reusing the v2 scorer should floor holes below any buildable candidate.**
- **C5 (α-basis note):** did NOT fire — no metric went degenerate, so `alpha_realized` = 0.0035 exactly (identical to nominal). Had §4 fired and pairs renormalized to 2-of-2 or 1-metric, Y's binomial null would have shifted off p=0.5 and required recomputation; it did not.
- **C6 (no-memoization):** discharged — 128 baseline + 128 encounter = 256 distinct fight records, every per-pair baseline genuinely re-run even where two pairs shared a multiset.

---

## Ch 5 — THE DISPOSITION FORK (the book's live decision; veto-open, Matt rules)

W3′ established, cleanly, that **outcome-level metrics do not detect formation-geometry effects at d=0.5.** That is a fact about *the measurement venue*, and it forks two ways. **The two are not mutually exclusive** — (b) can proceed while (a) waits for appetite. Neither is ruled here.

**§5(a) — Texture-metrics lap.** *Hypothesis:* geometry lives at the fight's TEXTURE level — the moment-to-moment shape of the encounter — and is invisible to terminal outcome metrics that only ask "how many died / how much damage." A future instrument would gate on **time-series texture**: time-to-Nth-kill curve shape (does a lane produce a staggered kill-cadence vs a swarm's front-loaded burst?), damage-intake timing (does an emplacement force a spike as you close on the anchor?), positional churn (how much does the player have to *move*?). The W3′ per-family minority (§4.7 — emplacement/pre-seed families tilting positive while the median reads 0.0) is exactly the signature a texture instrument might resolve where an outcome-median cannot.
- *Costs:* new metric engineering in the sim seam (time-series capture the harness does not currently emit), a new prereg sheet, a new charter.
- *Risk:* texture metrics are a **math hotspot** (curve-shape comparison, timing-distribution distance) — they would likely need Discipline #18 methodology consultation before a bar is set, or they risk the same instrument-defect lifecycle W3 just paid for.
- *Player-consequence framing:* if this lands, what the player *feels* is that a totem-nest and a swarm-charge play *differently second-to-second* even when both end in a cleared room — the pacing, the pressure-rhythm, the "when do I have to reposition" — and the engine can measure that difference. If it does NOT land, geometry's effect is genuinely below the sim's resolution and belongs to presentation alone (→ (b)).
- *Genre precedent for the venue-shift itself:* Path of Exile's own design discourse treats pack *density and layout* as a pacing lever measured by clear-*speed feel* and screen-reading load, not by whether a map completes — GGG tunes "juice" (Beyond portals, Breach density, Delirium fog) against the texture of a clear, and the community build-crafting culture optimizes *clear rhythm* (how the screen empties) as a first-class quantity distinct from whether it empties. A texture instrument is the sim analogue of that lever. The W3′ per-family split (§4.7) is the seed data: emplacement/pre-seed families already register a mean-d tilt the outcome-median erases — precisely the "there is a texture signal under the null outcome" that a time-series instrument exists to resolve.

**§5(b) — Presentation-layer routing (CONDUCTOR LEAN — presented as a lean, not a ruling).** *The reframe:* the encounter grammar is **SCENE grammar** — it is what the player *reads* when they enter a space: a gauntlet lane, a totem nest, an ambush ring, a channel-arena kill-zone. Its natural validation venue is the **Godot presentation seam** (drax; SCENEWRIGHT review; optionally galadriel CV rubrics), judged by **look / read / feel**, not by outcome sims.
- *Genre precedent (why the lean points here):* in **Diablo II**, pack shape transforms moment-to-moment play while rarely changing whether you clear. A doorway boss-pack (Pindleskin, the Countess's tower landings) reads and plays completely differently from the same monster count strewn across an open field — the funnel, the "do I peek or commit," the corpse-explosion daisy-chain in a corridor — yet *whether you clear* is nearly identical. **Outcome metrics were never where formation lived.** Formation is legible drama — the player reading the room and choosing an approach — not a stat modifier on a kill-count. W3′ is the empirical confirmation of exactly that: 28/32 metric collinearity and a 0.0 showcase median say the outcome layer is blind to formation *because formation was never an outcome quantity.*
- *Player-consequence framing:* the value the grammar delivers is the *reading* — the half-second where the player sees a totem ring and knows to break the anchor, sees a lane and knows to funnel, sees an ambush arc and knows they walked into it. That is validated by whether the Godot scene *communicates the shape* (does the camera frame it? does the player recognize the archetype?), which is a SCENEWRIGHT/look-read-feel judgment, not a `mobs_killed` delta.
- *Non-exclusivity:* (b) routes the grammar to the venue where it can be validated *now*, on the E4 camera per Path A; (a) remains available later if there is appetite to prove a *mechanical* texture-effect on top of the read. A PASS in (b) does not require (a); (a) failing would not retire (b).

**Why a lean and not a ruling.** Routing the grammar to a new validation venue (presentation) versus commissioning a new sim instrument (texture) is a **direction-of-development** call with resource and sequencing weight — it belongs to Matt. The conductor's lean is (b)-primary / (a)-optional-later; the fork rides open.

---

## Ch 6 — Run-methodology lessons (desirable-run-pattern feedback)

*This chapter is FINDINGS for `operating-procedures/desirable-run-pattern.md` lore — NOT an OP edit. Any OP amendment is a separate proposal beat.*

**§6.1 — The two-generation instrument story IS the honorable-fallback pattern working.** The pattern's whole claim is that a preregistered gate that FAILS is not a wasted run — the FAIL is decidable substrate that routes forward. Tier-3 is the founding worked example: W3 failed *and its instrument was invalid*, and the machinery held anyway — the FAIL registered as the run's verdict while its interpretation ("ruler broken") stayed distinct from "hypothesis false," the commitment-boundary to re-run went to Matt (never self-granted), and the re-run produced a *clean* answer. **Two FAILs, two meanings, zero goalpost-moves** — that is the pattern surviving the hardest case (an instrument that measured the wrong variable). It belongs in the lore as: *a preregistered FAIL whose red-flags indict the instrument earns exactly one Matt-authorized re-instrument at the same bar; the second result is the run's real answer.*

**§6.2 — count-parity ≠ budget-parity (a prereg-authoring lesson).** RF-B's root cause: the base sheet pinned "40 mobs total" believing count pinned the difficulty budget. It did not — an elite-heavy 40 and a homogeneous 40 carry wildly different destructible HP, and the metrics measured the HP. **The prereg-authoring lesson: when a gate isolates a variable, pin the parity at the level of the thing that actually enters the metric** (here: composition + effective HP), not a proxy for it (count). A count-parity claim is not a budget-parity claim; state which one the metric consumes.

**§6.3 — the SEALED pre-gate artifact as a reusable device.** W3′'s C2 pin (write the baseline fights + standardizer + degeneracy determination to a hash-embedded seal BEFORE any encounter fight) converted a *sequence assertion* ("computed pre-gate") into a *verifiable invariant* (hash-checkable ordering). This is a reusable device for **any run where the standardizer or an admissibility rule is computed from data**: seal the pre-gate determination, embed its md5 in the final output, make mutation a HALT. It closes the "analyst computes the denominator after seeing outcomes" degree of freedom structurally rather than on trust.

**§6.4 — slate-freshness as a conductor-brief discipline.** The #9 stale-ledger catch (L-17): a fire-word inherited a ~2-week-stale ledger row (#9 phases had all landed 2026-07-03→08; no build wave existed to fire). The paste-able's mandatory STATE-RECONSTRUCT-FIRST clause caught it — the fire-word became an audit, Discipline #3 respected. **Lesson for conductor briefs: a run's slate is a snapshot with a decay half-life; a launch brief must reconstruct current state before firing, never trust an inherited ledger row's freshness.** This is the OP 4.10.3 slate-freshness guardrail class, now with a Tier-3 instance.

---

## Ch 7 — Queued follow-ons (registry, no new authorizations)

*Registry only. Nothing here is an authorization — each item names its owner + trigger + what it feeds. Fire-words stay with their owners.*

| # | Item | Trigger / status | Owner | Feeds |
|---|---|---|---|---|
| 1 | **III.1 temperature consult** (Discipline #18 methodology) | post-W3 trigger now MET | gandalf ELICITOR → rocket | any future sim-instrument at the extension hotspot (incl. Ch-5(a) texture metrics) |
| 2 | **combined R-1 SHAPESHIFT + E4 ECHO design consult** | offered post-Tier-3 (L-17); both are identity-adjacent net-new sim verbs, design-consult-first class | gandalf (consult) → Lane-2 follow-on queue | Lane-2's R-1 Pattern-B build + any future ECHO dispatch |
| 3 | **island build-out + scoring** | PRE-RATIFIED (L-6); fires on C1–C3 evidence (Ch 2, now complete) at conductor timing; own mini-charter | gandalf RUN-CONDUCTOR | island layer re-cut on the enriched substrate (Path A, E4 camera) |
| 4 | **island NAMES** | Matt's Q32 naming one-sitting — NOT pre-ratified | Matt | island layer naming (gated behind #3's build-out) |
| 5 | **story design session** | queued on Matt's sequencing; PING resolved | gandalf STORYWRIGHT + Matt | traveling-kin caravan NPC ensemble (L-4 / §2.3 deferral), act-order fork, family-name canonization |
| 6 | **C4 fit-instrument note** | recorded (Ch 4.8) | any future lap reusing v2 scorer | floor holes below buildable candidates before re-selecting |
| 7 | **disposition fork resolution** (Ch 5) | OPEN — Matt rules | Matt | texture-lap charter (a) and/or presentation-routing to drax/SCENEWRIGHT (b) |

---

## Close

The Tier-3 Encounter-Geometry Run asked whether formation geometry moves fight outcomes, and — after paying once for a broken ruler and rebuilding it clean — answered honestly: **not at the outcome layer, not at d=0.5.** The grammar it built to ask the question outlived the question. A totem nest, a channel-arena, a gauntlet lane, a traveling-kin caravan camped in the wrong age — these are real, buildable, provenance-honest, and waiting. The open question is not whether they matter but *where they are validated:* in a finer sim that can see texture, or on the camera where the player reads the room. That fork is Matt's.

RD-1 discharged-unfired. The `encounters` key waits, reserved and empty, for the venue this book's fork will name.

**Signed:** named-`gandalf` (W4 drafting leg), for gandalf `RUN-CONDUCTOR`, 2026-07-22 — veto-open (T3-V1).
