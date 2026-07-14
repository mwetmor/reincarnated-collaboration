# Session handoff — family-definition → gaps/KPIs/direction → the live decision surface

**Author:** gandalf · **Purpose:** resume-without-a-beat handoff · **Status:** analysis landed & independently verified; **a ruling awaits Matt.**
**Read this first next session, then jump to §8.**

---

## 1. TL;DR (the state in five lines)

1. Two ultra-thinks completed: **family-definition** (`family = fiber of behavior map B`) and its sequel **gaps/KPIs/direction** (Charges A–D, ruling **REFINE + 5 bindings**).
2. I **verified the sequel analysis** against the corpus + engine code — its four surprising claims (all of which corrected *me* or my prompt) **all check out**. Trust is high.
3. The **periodic table as it stands** was rendered: 470 kits → 457 strict cells → 48,550 lattice concepts; **6 confirmed cross-franchise groups** + a 7th seed.
4. **THE OPEN GATE:** Matt has not yet ruled on **REFINE**. I gave it my endorsement **plus two precise pushbacks** (amber-promotion circularity; reference-gauge is under-specified). Everything downstream waits on this ruling.
5. Nothing was pushed to remote (pushes need Matt). All work auto-committed.

---

## 2. What this session produced (the arc)

| step | artifact | commit |
|---|---|---|
| Family-definition ultra-think (member-count-free) | `design-inputs/2026-07-13-family-definition-analysis.md` | `ed9fb60a` |
| Reproducible discovery engine (FCA + lift) | `design-inputs/family-discovery-poc-rerank.py` | `ed9fb60a` |
| Sequel prompt (gaps/KPIs/direction) — draft | `design-inputs/2026-07-13-gaps-kpis-direction-ultrathink-prompt.md` | `b8e2fcfe` |
| Sequel prompt — corrected ("negative kits" = the 38 filtered-out; + Matt's collision signal) | (same file) | `fd22e4d8` |
| **Sequel analysis executed** (Charges A–D) | `design-inputs/2026-07-13-gaps-kpis-direction-analysis.md` | `1bf4c2c9` |
| Engine-tracker sync + **Q28 direction-ruling row queued** | (engine tracker) | `5569d38f` |

**Definition that now anchors everything:** a **kit** is a point in coordinate-space; a **family** is the largest axis-aligned region on which the fight-sim behavior map `B` is invariant to its free coordinates (a *fiber* of B). **Member count = sampling density of the domain, never a property of the map.** Zero members = a fiber not yet sampled = a Mendeleev gap. Lift/support demoted from *definition* to *validation/prioritization* evidence.

**Sequel's sharpening of that definition (the intellectual highlight):** B must be measured at **frozen reference tuning**, not post-balance — because bounded viability (doc 50) is *engineered* to flatten post-balance scalar win-rate, so the balanced scalar carries ≈zero identity information. **The loop owns the scalar; B owns the shape; curation owns the shapes the sim can't see.** This gauge-fixes my original (tuning-unspecified) definition. It is a genuine improvement, not a restatement.

---

## 3. THE DECISION SURFACE — what awaits Matt (begin here)

### The ruling on the table: **REFINE — stay on the bet, with five bindings** (analysis §D.3)

- **(a)** B is *defined* as differential-shape at frozen reference tuning; balanced scalar **excluded as identity signal forever**; B-as-oracle is a *milestone* with a named acceptance test (§B.5); fibers stay **proxy-confirmed** (designer + cross-game recurrence) until it passes. Nothing gates on the oracle.
- **(b)** Cell taxonomy gains **CONTESTED** (cells holding both corpses and survivors, separated by tuning not coordinates); rooted-channel is its first member.
- **(c)** **Amber-promotion law:** graveyard cells with *extrinsic* deaths → *promoted generation targets* (our systems are the specific antidote); the three **intrinsic red laws** stay hard filters: (1) **co-location** (damage at avatar's present position/anchored proxy), (2) **no anti-synergy** (sustain must not eat the build's own substrate), (3) **movement-damage carve-out** (movement-as-damage only at instant-commit + high tempo).
- **(d)** The elrond curation batch (§A.5) fires **before Stage-2 coarsening concludes**, so the coarsening ruling sees the corpses.
- **(e)** Breadth stays the **product-layer pitch, permanently subordinate** to the one-run feel-complete demo gate; **§20d parametric-verb condition is the breadth test, cell-count is not.**

### My verdict + two pushbacks (gandalf, as peer/DRIFT-CRITIC)

**I endorse REFINE.** The bet survives all six steelmen; the evidence strengthens it. Two refinements to weigh *before* it becomes a decision record:

- **Pushback 1 — the amber-promotion law (binding c) grades our own homework on one of its three legs.** Split the amber ledger by *cure mechanism*:
  - *Itemization-orphan* (cured by agnostic loot §3A.1) and *port-context death* (cured by "we are one game") are **architectural facts** → safe to promote **now**.
  - *Tuning-starvation* (cured by the balance loop) is **contingent** — and it's the largest amber bucket. The loop's efficacy *at 470-kit breadth is exactly what isn't proven* (the gauntlet is a ruled-broken instrument per §B.5). **Recommend:** tuning-amber cells are promoted but the promotion is *cashable* only once the loop demonstrates bounded viability at breadth — the same acceptance-test gate B.5 put on the oracle. Player-consequence of getting it wrong: a "museum of cells we *believe* our loop rescues" — steelman #5's failure re-entering the side door.
- **Pushback 2 — "frozen reference tuning" is a load-bearing gauge choice mis-filed as small seam work.** The follow-up table hands "K1 reference-panel freeze spec" to gamora as "small seam work." **It is not small** — the reference gauge *determines which fibers exist* (two kits identical at low reference power can diverge at high power). Choosing the canonical reference = choosing *what counts as same behavior* = the crux of the whole family definition. **Recommend:** reclassify as a **gandalf SPEC-AUTHOR decision** (canonical reference gauge), with gamora implementing accumulators underneath. This is the one genuinely unmade decision the analysis surfaces without resolving.
- *(minor)* the "two-thirds amber" headline is a soft interpretive tally with acknowledged multi-tag overlap — directionally solid; do not quote as a hard statistic.

**What Matt owes:** rule on REFINE, and say whether the two pushbacks fold into bindings (c) + the follow-up ownership *before* this becomes a decision record — or ride as Stage-2 inputs. Q28 (engine tracker) is the queued decision row.

---

## 4. Verified facts (do NOT re-litigate — grounded this session)

| claim | verdict | how verified |
|---|---|---|
| Prompt's "33 genre / 5 pipeline" split | **WRONG (mine)** — all 5 "no rule matched" kits carry real postmortems; that flag is a keying-TODO orthogonal to provenance. Refined: 36 genre-negatives + 1 system-record + 1 unfilled. | corpus query: 37/38 have non-empty `mech_note`; the 5 include `d2-leap-attack`, `gd-reap-spirit`, `hot-blood-catcher` |
| `d2-sacrifice` leaked into the keyed 470 | **TRUE** — present in both `canon_corpus`(neg=1) and `canon_engine_key`(combat-kit), blank-heavy key | corpus query, both tables |
| `engine_version` / `termination_reason` telemetry gaps | **CLOSED schema-side** (my MEMORY note is stale) | `telemetry/migrations.py` (`ADD COLUMN termination_reason`; `engine_version TEXT NOT NULL`) + `recorder.py` |
| Sequel analysis quality overall | **High-trust** — it corrected me four times, every correction factually right; did not merely ratify | above + full read of the analysis |

---

## 5. The periodic table as it stands (snapshot — so next session need not re-query)

```
470 keyed combat-kits → 457 strict cells (13-coord) → 48,550 closed lattice concepts
```
No single canonical grid (lattice-not-partition; groups overlap). Legible only as projections.

**View 1 — landscape (delivery × treatment):** at-target 230 · projectile 107 · self-origin 85 · beam 14 · aura-pulse 12 · orbit 11 … / damage 432 vs control 31 (treatment barely discriminates — the real structure is in the groups).

**View 2 — the confirmed GROUPS (natural kinds; "games" = independent franchises that built it):**

| group | kits (nbhd) | games | lift |
|---|---|---|---|
| WHIRLWIND (spin-to-win) | 15 | **12** | 2120 |
| TOTEM / SENTRY | 26 | **12** | 224 |
| TRAP / MINE | 24 | 8 | 1426 |
| CHANNELED BEAM | 9 | 6 | 233 |
| AURA (damage field) | 8 | 6 | 1231 |
| MINION / PET (taunt-line) | 7 | 5 | 622 |

(neighborhood counts via loose signature-pins; byte-tight fiber cores ~30% smaller. 7th **deferred-detonation** fiber seed pending — 4 Hades isolates = 1 fiber, not 4 gaps.)

**Top ranked gaps (analysis §C.3):** ① mobile beam (UNCLAIMED — "the beam that comes with you") · ② herding spin (UNCLAIMED — whirlwind+control) · ③ retaliation/thorns densification (AMBER-THIN — proven family, we sampled n=1, *cheapest fiber to sim-confirm*, accumulators exist) · ④ control-trap (AMBER-CONTESTED). **Binding honesty rule:** corpus sparsity ≠ genre absence — every UNCLAIMED ruling needs an out-of-corpus genre-check.

---

## 6. Follow-ups + owners (the queue — from analysis §Follow-ups)

| item | owner | gate/note |
|---|---|---|
| **Curation batch A.5** (5 items: mech_note 140-char truncation re-ingest; d2-sacrifice fill/quarantine; **re-key the 37 negatives** = unblocks collision analysis; resolve 5 no-rule-matched; add `death=` provenance tags) | **elrond** | recommend **before Stage-2 close** (binding d) |
| K6 economy accumulators + **K1 reference-panel freeze spec** | gamora (impl) + **gandalf (spec — see Pushback 2)** | unblocks B acceptance test |
| K2 / gauntlet re-base (8-mob saturation wall ruled broken 2026-07-07) | jack-ryan metrology | already queued; unchanged by this analysis |
| Stage-2 dedup review (this analysis feeds it: #4/#3 demote support, #7 economy value-split, CONTESTED annotations, movement-fusion marker) | gandalf + gamora + Matt | already queued |
| Deferred-detonation fiber seed (§C.4 brief 6) — proxy-confirmation pass | gandalf | next design window |
| **Stay/refine/pivot ruling (Q28)** | **Matt** | **§D.3 is the decision surface — §3 above** |

**Open engineering items carried from prior sessions (not this session's work):** economy backfill (~5 unknown-economy kits → elrond); `d4-blood-wave` geometry mislabel → elrond; a production discovery build (gamora runs sim, elrond holds lattice) pending Matt's go.

---

## 7. Artifacts + where everything lives

- **Definition:** `agentic_orchestration/gandalf/design-inputs/2026-07-13-family-definition-analysis.md`
- **Gaps/KPIs/direction analysis (the object of the ruling):** `…/2026-07-13-gaps-kpis-direction-analysis.md`
- **Reproducible discovery engine:** `…/family-discovery-poc-rerank.py` (`python3 <path>` — re-derives the groups)
- **Coordinate register (13 Class-A coords, cell-key):** `canonical/reap-die-rise-engine/coordinate-register-2026-07-13.md`
- **Dedup structure:** `agentic_orchestration/gamora/analyses/2026-07-13-cell-key-dedup-v1/`
- **Corpus (read-only, gitignored):** `agentic_orchestration/research/curated/corpus.db` — tables `canon_engine_key` (470 keyed) + `canon_corpus` (524, `negative` col flags the 38). Always `PRAGMA query_only=ON`.
- **Commits this arc:** `ed9fb60a` · `b8e2fcfe` · `fd22e4d8` · `1bf4c2c9` · `5569d38f` (none pushed).

---

## 8. Where to begin next session (concrete first moves)

1. **Get Matt's ruling on REFINE + the two pushbacks (§3).** This is the gate; do not start downstream spec/curation work until it lands. If Matt accepts with pushbacks folded → **draft the Q28 decision-record delta**: (i) split amber-promotion by cure-mechanism + gate the tuning-leg on loop-proves-bounded-viability-at-breadth; (ii) reclassify the reference-gauge spec as gandalf-authored.
2. **Then author the K1 reference-panel-freeze spec** (gandalf SPEC-AUTHOR — it fixes the gauge that determines which fibers exist) and hand the K6 accumulators to gamora as a design-spec-as-math handoff.
3. **Confirm the elrond curation batch (§A.5) is sequenced before Stage-2 coarsening** (binding d) — the 37-negative re-key is the highest-value item (unblocks corpus-wide negative↔positive collision analysis, which the CONTESTED map needs).
4. **Optional / when a design window opens:** the deferred-detonation fiber-seed proxy-confirmation pass (§C.4 brief 6).

**Do not lose:** the amber-promotion circularity (Pushback 1) and the reference-gauge authorship (Pushback 2) are the two threads most likely to be dropped — they are refinements *to a ruling not yet accepted*, so they live only here and in Q28 until Matt rules.
