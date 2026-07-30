# Finding — 2026-07-30 — courtesy verification, WR2 S-6 nova-crossing quantum column

**No GATED predicate is affected.** All four claim-sets CONFIRMED at every printed digit on
independently written instruments. Two INFO-grade label nuances for the conductor; nothing re-opens
Cell BAT's CLEAR and nothing touches the drax baton.

**Reviewer:** jack-ryan (courtesy-read verification, NOT a Gate-2 re-open)
**Severity:** INFO
**Target:** run WR2-ENCGEO-2026-07-29, routed by R-WR2-23
**Source under verification:** `agentic_orchestration/gandalf/notes/2026-07-30-wr2-grading-synthesis-after-baton.md` Part 1 §1.4, Part 2 §2.2
**Principles applied:** #1 (math-before-code), #4 (decisions-log/record as truth), #5 (severity matters); Discipline #12 (empirical inspection over assumption), Discipline #10 (attribution clarity)

## Method

Fresh reader written this session against the banked traces of **both** arms — 900 boss/champion/etc.
traces, 180 boss traces per arm across three legs. I did not reuse the grading lap's code and did not
read its implementation. Nova crossings identified structurally from trace content
(`event: damage`, `target_id == g5_header.kit_id`, `geometry: circle`, `skill_idx: -1`); unit payload
derived as the minimum distinct `delivered` per leg rather than taken from the report; outcomes and
durations from `record_type: footer` (`winner`, `elapsed_s`); boss HP at player death from the last
boss-targeted `target_hp_after` over `opposition_roster` boss `max_hp`. Leg labels bound to the three
directories via the Gate-2 §8.1 unit-payload table and cross-checked against banked win rates.

The BEFORE arm's 450 traces were on disk (my Cell BAT INFO-4 flagged them as untracked); no regeneration
was required.

## 1. The quantum histogram — CONFIRMED, all six legs

| leg | arm | firings | crossings | unit | histogram | mean realized |
|---|---|---|---|---|---|---|
| `pre` | BEFORE | 44 | 44 | 207.4 | `{1×:30, 2×:14}` | 1.3182 |
| `pre` | AFTER | 44 | 44 | 207.4 | `{1×:12, 2×:32}` | 1.7273 |
| `pre_endpoint` | BEFORE | 44 | 44 | 235.4 | `{1×:30, 2×:14}` | 1.3182 |
| `pre_endpoint` | AFTER | 44 | 44 | 235.4 | `{1×:12, 2×:32}` | 1.7273 |
| `post` | BEFORE | 44 | 44 | 207.4 | `{1×:30, 2×:14}` | 1.3182 |
| `post` | AFTER | 44 | 44 | 207.4 | `{1×:12, 2×:32}` | 1.7273 |

Identical on all three legs, both arms, as claimed. 44 firings and 44 crossings per leg on both arms —
one crossing per nova-carrying fight, 44 of 60 boss fights per leg carrying a nova. Mean realized count
per crossing **1.3182 → 1.7273 = +31.03%** (lap: +31.0%). CONFIRMED.

## 2. Derived intake deltas — CONFIRMED

| leg | BEFORE mean nova intake / nova-carrying fight | AFTER | Δ |
|---|---|---|---|
| `pre` | 273.39 | 358.24 | **+84.85 HP** |
| `post` | 273.39 | 358.24 | **+84.85 HP** |
| `pre_endpoint` | 310.30 | 406.60 | **+96.30 HP** |

Reproduced to the last printed digit, and the arithmetic closes independently of the trace scan:
`(30·207.4 + 14·414.8)/44 = 273.39`; `(12·207.4 + 32·414.8)/44 = 358.24`;
`(30·235.4 + 14·470.8)/44 = 310.30`; `(12·235.4 + 32·470.8)/44 = 406.60`. CONFIRMED.

**INFO-1 — the fraction-of-pool gloss is leg-specific, the HP figure is not.** §1.4 writes the two
deltas as "**11.2% and 12.7% of the player's 759 HP pool**". The `pre` and `pre_endpoint` legs do carry
`player_pool_max_hp` **759.0** (verified, all traces), so 84.85/759 = 11.18% and 96.30/759 = 12.69% are
both right for those legs. But `post` (`g5_r3arm_…mitR3`) carries **1607.0 HP**, and §1.4 pairs `post`
with `pre` in the same "+84.85 HP" cell. On `post` that same +84.85 HP is **5.28%** of pool, not 11.2%.
The HP number is correct for all three legs; the percentage is correct for `pre` only. This makes the
Matt-facing severity of the `post` leg slightly overstated — and it happens to reinforce the lap's own
conclusion, since `post` is the leg where nothing flipped. Recommend the gloss be stated per-leg.

## 3. Outcome-conditioned decomposition (§2.2) — CONFIRMED, every cell

| leg / cell | flips WIN→LOSS | reverse flips | stayed LOST | stayed WON |
|---|---|---|---|---|
| `pre` boss/A | 0 | 0 | 30 · 37.18 → 32.04 (**−13.8%**) | — |
| `pre` boss/B | **6** | 0 | 16 · 51.55 → 43.29 (**−16.0%**) | 8 · 65.64 → 67.44 (**+2.7%**) |
| `pre_endpoint` boss/A | 0 | 0 | 30 · 28.57 → 24.02 (**−15.9%**) | — |
| `pre_endpoint` boss/B | **2** | 0 | 28 · 39.84 → 32.68 (**−18.0%**) | — |
| `post` boss/A | 0 | 0 | — | 30 · 57.66 → 58.71 (**+1.8%**) |
| `post` boss/B | 0 | 0 | — | 30 · 57.66 → 58.71 (**+1.8%**) |

Eight WIN→LOSS flips total, 6 on `pre` boss/B and 2 on `pre_endpoint` boss/B — CONFIRMED. Zero reverse
flips anywhere, which the lap does not claim but which is the stronger form of its point 1. Stayed-lost
band **−13.8 … −18.0%** — CONFIRMED at both endpoints. Every surviving win longer, +2.7% (`pre` boss/B)
and +1.8% (`post`), no exceptions — CONFIRMED. Pooled leg means and win rates all reproduce exactly
(0.0000/0.0000 · 0.4667/0.2667 · 1.0000/1.0000 · 0.0000/0.0000 · 0.0667/0.0000).

**INFO-2 — the `post` row's n is 30 per cell, not 30 pooled.** §2.2 labels the row `post` boss/A+B with
`30 · 57.66 → 58.71 s`. A+B pooled is **60** fights. The mean is unaffected because A and B are
duration-identical on `post` **per seed** — I checked all 30 seed-pairs and `elapsed_s` matches to
1e-9 on both arms — so 30 and 60 give the same figure. The identity is mechanically explained, not an
anomaly: the A/B cell distinction on this leg is the lifesteal door (0.05 vs 0.08, the only content
difference across 643 differing lines in the pair I diffed field-by-field), and on `post` the player
wins every fight, so duration is set by time-to-kill, which the lifesteal door does not move. Recommend
the row read `n=30 per cell (A ≡ B on duration)` so a future reader does not read a pooled 60 as a typo
or the identity as a copy error.

## 4. Flip bifurcation table — CONFIRMED, all eight rows

| flip | BEFORE | AFTER | boss HP left at player death | quantum |
|---|---|---|---|---|
| `pre` 74000803 | player 65.3 s | monster 34.3 s | 53.5% | 1× → 2× |
| `pre` 74000806 | player 63.5 s | monster 39.0 s | 43.3% | 1× → 2× |
| `pre` 74000811 | player 63.5 s | monster 34.3 s | 52.6% | 1× → 2× |
| `pre` 74000826 | player 67.1 s | monster 34.1 s | 56.2% | 1× → 2× |
| `pre` 74000829 | player 65.3 s | monster 34.3 s | 52.6% | 1× → 2× |
| `pre` 74000815 | player 63.5 s | monster 59.6 s | **9.2%** | 1× → 1× (unchanged) |
| `pre_endpoint` 74000800 | player 63.5 s | monster 61.6 s | **9.0%** | no nova either arm |
| `pre_endpoint` 74000814 | player 62.6 s | monster 58.4 s | **10.0%** | no nova either arm |

Five 1×→2× catastrophic flips with the boss at **43.3–56.2%** HP (lap: "43–56%"), three knife-edge flips
at 9.0–10.0%, and the bifurcation line is exactly the nova quantum. The flip set is also *complete* —
my enumeration over all six leg×cell groups found these eight and no others. CONFIRMED.

## 5. The lap's instrument-validation claim — CONFIRMED

Its reader's stated validations hold on mine too: the six banked boss-tier leg means
(37.18/32.04 · 57.94/48.92 · 28.57/24.02 · 41.39/34.50 · 57.66/58.71), the four banked win rates, and
the WR1 `{1×:30, 2×:14}` histogram on the BEFORE arm on all three legs. The BEFORE-arm-as-WR1-stand-in
argument is sound on the nova line specifically: the histogram, the crossing count, and the unit payload
all agree with the WR1 baton, which is the claim §1.4 needs it to carry.

## Standing of the miss

I confirm the lap's own characterisation and add nothing to it. S-6's fourth pre-registered column was
never computed by any cell and never demanded by any gate, including mine — my Cell BAT §4.4 reproduced
firings, crossings, delivery rate, `distinct_wind_up_s`, `distinct_onset_tick` and `d_onset` exactly as
reported, and did not ask for the 1×/2× distribution the pre-registration named. That is a Gate-2 miss
of the "verified what was reported, did not audit the register against the report" family, and it is
mine to own alongside the cell's. It changes **no gated predicate**: S-6 is reported-not-gated by
charter design, worst single hit genuinely did not move on either grain (2× was already the maximum),
and the outcome/duration figures were banked and graded before this lap. Cell BAT's CLEAR stands.

## Action

- [ ] Conductor: apply INFO-1 (state the fraction-of-pool gloss per leg; `post` is a 1607 HP pool, so
      +84.85 HP is 5.28% there, not 11.2%) before any of these numbers reach Matt.
- [ ] Conductor: apply INFO-2 (`post` row `n=30 per cell`, note A ≡ B on duration and why).
- [ ] Conductor: the two-instrument standard is now met on all four claim-sets — they may go to Matt.
- [ ] jack-ryan (own it): future Gate-2 obligation lists should audit the **pre-registration** against
      the report, not only the report against the substrate. Candidate discipline refinement; not filed
      as a discipline change in this courtesy read.
- No developer action. No BLOCK. Nothing here gates the drax baton.

## References

- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-07-30-wr2-grading-synthesis-after-baton.md` (§1.4, §2.2 — claims under verification)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-07-29-gate2-gamora-wr2-cell-bat.md` (§4.4, §8.1 — prior Gate-2, leg/unit binding)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5/wr2_battery_after/` (3 legs × 150 traces)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5/wr2_battery_before/` (3 legs × 150 traces; still untracked per Cell BAT INFO-4)
- My instruments (independent, scratch, regenerable): `/tmp/jr_quantum.py` (histogram + intake),
  `/tmp/jr_outcome.py` (outcome-conditioned decomposition + flip enumeration + boss-HP-at-death)
