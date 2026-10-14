# Finding — 2026-10-14 — JOIN-1 J4b ADDENDUM-6 delta: discharge check and readiness of the port-site list for Matt

**Reviewer:** jack-ryan
**Severity:** WARN (verdict **GO-WITH-AMENDMENTS**: the 19-site list may go to Matt **once WARN-2's items are in the ruling text**; WARN-1 and WARN-3 are fixed before the prereg and build, and change no site)
**Target:** engine `c5f66a4e` (ADDENDUM-6), against my binding delta `ae25b2f5f` + `9c1d54cce` and the conductor's KP-432 (PRIMARY r_DMG = mean ÷ mean ×78.58)
**Developer:** gamora · conductor gandalf (drax producing the line inventory in parallel)
**Principles applied:** 1, 3, 5 · Disciplines #10, #12

## Discharge of the binding delta: ALL DISCHARGED

| Item | Disposition in ADDENDUM-6 | Check |
|---|---|---|
| **WARN-1** (statistic asymmetry) | KP-432 makes PRIMARY **mean ÷ mean ×78.58**, statistic-matched to r_HP. The fidelity line states the direction verbatim: WORST-CASE ×97.06 favours her survival (×1.235); USE-WEIGHTED ×46.98 disfavours it (×0.598). All three are printed | ✓. Life 1,004 × 78.5835 = **78,898** recomputes. The fire near-tie is handled honestly: parity 79.70 sits inside her own resist-roll band (74.72–84.68), and no fire ordering is registered |
| **WARN-2 + stage-6 note** (two axes; the quantile spec) | Tier → table; attack kind → law per slot; the type role never keys the map. Pooled per-type max contact AR, n = 64. Both profile halves × board waves; `AttackerTierUnresolved`; mid-rank ties; Hazen interpolation, clamp; `Fraction` → an integer `AR_eq` table emitted once, with the port reading integers only; champion transform `⌊Q·149/100⌋`, mlvl 87; boss/nemesis INTERIM; the landed-weighted print | ✓ (one construction choice in **WARN-1 below**) |
| **WARN-3** (Pierce) | `physical_contact` = weapon swing, or a projectile with Physical or Pierce in its direct rows. Bleeding is not contact (JUDGED, with a sensitivity) | ✓ (a count note in INFO-2) |
| **INFO-1** (block in HITREC; tick → frame) | Block is rollable in HITREC (D2MOO has no mode gate; BLOCK replaces HITREC). `f(k) = (m−1)·400 // AS + 1` is the exact inverse of `ceil(f·AS/400)`, with intake ordered before her action poll | ✓ |
| **INFO-2** (regen) | One C-13 function, `max(1, ⌊max_256/3000⌋)·(100+b)/100 + manarecovery` | ✓. **Byte-identical for her** under the stated conditions: `max_256 ≥ 3000` makes `max(1, ·)` the identity, and `manarecovery = 0` (star-lord to confirm; non-zero would be a named finding) |
| **INFO-3** (registries) | One shared enumerator over both profile halves for rows 25, P-2, P-3 and the tier table | ✓ |
| **INFO-4** (ordering) | Only arms ≥ ×1.2 apart are ordered | ✓ in form. **The threshold itself: see WARN-3** |

## Independent checks
- **H1 grid: SOUND.** I re-ran H1, `clamp(⌊2·alvl·⌊100·AR/(AR+Def)⌋/(alvl+90)⌋, 5, 95)`, with ranged rows at Def + 250, over `d2_hit_chance_r1.json`:
  - **279 / 279 rolled rows reproduce exactly**;
  - **108** caster rows (expected 100);
  - **3** null rows (`suicideminion6` A1, AR 0: the declared refusal);
  - = 390;
  - the per-type max contact-AR table has **n = 64**, as stated.
  
  The perturbed-row negative control is the right partner.
- **The quantile spec is bit-exact-ready.** Every quantity the port uses is an **integer** emitted once by the engine and digested. The port never computes an ECDF or a quantile, so mirror agreement is reduced to integer H1 arithmetic, which the grid tests. The mid-rank, Hazen and round-half-up conventions are explicit in exact rationals.

## WARN-1 — The ECDF's construction population should be the SPAWNABLE set (the step-2b population), not record × every board wave

§ 2.2 builds each tier's ECDF with **equal weight on every (record, wave) row of both profile halves × the board's wave set**: 237 records × the waves, including rows that **never spawn**. That gives totality (no run-time miss), which is good. But the marginal the quantile anchor exists to reproduce is then a marginal over **phantom rows**, and § 2.4's landed print can only reveal the gap after the run.

**The step-2b closure (KP-381/382) already established exactly which (record, wave) pairs the sealed sim can spawn in a cell**: P, 248 pairs. That is roster A + pre-pass B + the pet closure, with no carry-over.

*Action:*
- keep the table **total** over the full product, so no lookup can miss;
- but **weight the ECDF on P only**, so the construction marginal is over bodies that can actually attack her;
- rows outside P take their quantile from the P-weighted ECDF.

This changes `anchor_ar_eq_table`'s values, not S17's code or the site list.

## WARN-2 — The KP-312 ruling text for the 19 sites must carry three further items (the KP-360 precedent)

1. **Booking-census row ADDITIONS.** S04–S06 (Fire Ball, Meteor impact, burning ground) and S10 (potions) introduce new damage and heal bookings (`_offer` / `_cons_add`-class lines). New lines mean **new census rows**, a change to a sealed self-check's content. KP-360 (a) required them **named in the ruling**, with `census_grep` MATCH row for row in the same commit, and T-A FILE-equal as the null-path proof (my site-list review § 1.4).
2. **S16b's emitter dependency.** If the JOIN run report that carries S16b's export is written by the frozen emitter `kc2p_join1_gm_emit.gd`, the export needs an **emitter unfreeze ruling** (the KP-397/402 precedent), in addition to the runtime site. State which file writes it.
3. **The standing KP-312 condition set, stated with the list:**
   - one null-guarded change set (G-B form, as § 5 gives);
   - the predicate-at-defaults column (present);
   - hunk-audit fail-first;
   - per-site fail-first;
   - G3 25/25 and T-A unchanged (present);
   - J-S8 golden master IEEE-754 bit-equal;
   - my delta Gate-2;
   - **Matt's windowed `.app` self-test** before the new digest is cut.

**The count of 19 is right:** S01–S15, S16b, S17–S19. **S16a is engine-side**, a read of `run.non_health_rows` / `run.non_health_by_type` in Python with no port edit, so it needs no ruling. The S08 ⊂ S11 implementation note is fine; separate ids for ruling purposes are correct.

## WARN-3 — The ×1.2 ordering threshold is not safe for SURVIVAL counts. J3a is the counterexample

The one ordering ADDENDUM-6 registers between close arms is **PRIMARY (78.58) ≤ WORST-CASE (97.06)** on survival, ×1.235 apart. But J3a's G-D3 re-emission (collab `4c30b0d64`) gave the Warlord **+15–18 % damage per hit** and moved survival **20/25 → 17/25, adverse (4 vs 1)**: a ~×1.2 lever reversed its intuitive survival direction through trajectory chaos. A survival-count ordering at ×1.235 can fail the same way.

*Action:*
- register **survival** ordering only for **USE-WEIGHTED vs PRIMARY** (×1.67);
- grade PRIMARY vs WORST-CASE on a **continuous paired metric**: Σ survival ticks (death tick or window end) per cell, or intake absorbed before death, with a sign test;
- or declare that pair un-ordered.

The fail criterion is a **strict reversal of the paired total**, stated.

## INFO
- **INFO-1:** the boss/nemesis INTERIM (champion transform pending the D2 unique AR distribution) is labelled. Keep it on the fidelity table's face until legolas supplies the uniques.
- **INFO-2: the `physical_contact` re-count depends on the counting convention.**
  - At (record, surface, slot, tree_index, skill) granularity I get **567** projectile entries (matching) but **262** with Physical and **23** Pierce-only, against ADDENDUM-6's 280 / 21.
  - The difference is probably what counts as a "direct damage row", e.g. whether `weapon_damage_pct > 0` marks physical contact without an explicit Physical row.
  - *Action:* declare whether weapon-damage-carrying projectiles are contact. Have the **bind-time classifier itself** emit the counts and the Pierce-only / Bleeding-only slot lists, digested, as the number of record, rather than hand recounts.
- **INFO-3:** the guard form `rulebook == null or lever == gd → existing lines untouched` is the G-B form. Under ORACLE, PLAY and JOIN-Warlord every site is inert by construction, and the predicted ORACLE byte-identity is the right common proof.

## Action
- [ ] conductor / gamora: add WARN-2's three items to the KP-312 ruling text; **then the 19-site list may go to Matt** (with drax's line inventory).
- [ ] gamora: before the prereg and build, WARN-1 (ECDF weighted on P) and WARN-3 (survival ordering only at ×1.67; continuous metric for the ×1.235 pair). Declare INFO-2's definition.
- [ ] star-lord: `manarecovery = 0` on her rows.
- [ ] legolas: the D2 unique AR distribution; mean ÷ mean R2/R3/R4.
- [ ] Matt: the KP-312 ruling on S01–S15, S16b, S17–S19 (+ the emitter unfreeze if 16b needs it).

## References
- engine `c5f66a4e`; collab `agentic_orchestration/legolas/research/2026-10-14-join1-c13-enemy-anchor/d2_hit_chance_r1.json` (H1 re-run above), `r_dmg.json`; `data/kc2/pm2_tg2_attack_damage.csv` (recount); collab `4c30b0d64` (G-D3 v3 survival counterexample); KC2 KP-360/363/381/382/397/402/432 — all read-only
