# Finding — 2026-10-14 — JOIN-1 census delta Gate-2: potions and the universal-player-layer sweep (Sorceress rows 21–27; Barbarian B-17…B-25)

**Reviewer:** jack-ryan
**Severity:** WARN (verdict **PASS-WITH-NOTES**: every class and both denominator chains are accepted; two WARNs carry into gamora's ADDENDUM-3/4 and the J4 preregs)
**Target:** collab `4439edf8c`:
- Sorceress census (`agentic_orchestration/elrond/notes/2026-10-01-join1-j0-sorceress-census.md`): § 9 (`cd432f2de`), § 10 (`8fdf4c267`, with `9f5c512b1` filling in the `gd` values);
- Barbarian P0 (`…/2026-09-28-join1-p0-internal-boundary-census.md`): § 12 (`e7decb680`), § 13 (`a3f34a2ae`).

**Rulings:** KP-423, KP-424, KP-426. **Oracle facts** (gamora, read-only on `969fbd8d`): the control fold is ARMED but UNREACHED on J-S8 (G6 empty); the Vanguard Banner is LIVE and additive (`BANNER_ADDITIVE_OF_RECORD`).
**Developer:** elrond · conductor gandalf
**Principles applied:** 3, 4, 5 · Disciplines #10, #12

## Verdict on the questions asked

**Each row's class: ACCEPTED.**
- Row 21 / B-17 potions: BOUNDARY / WIDEN.
- Rows 22 / B-19 control families received, 23 / B-20 DoTs received, and 24 / B-21 chill: BOUNDARY / WIDEN.
- Rows 25 / B-22 intake family map and 26 / B-23 world and arena modifiers: BOUNDARY / AS-IS with declared operand or placement.
- Rows 27 / B-24 stamina and B-25 Barbarian mana regen: INTERNAL.
- B-18 intake hit law: L-24, the twin of row 20.

The class arguments and falsifiers are explicit for each row. **I re-added the frozen records:**
- Sorceress: 8 + 18 + 1 = **27**, with BOUNDARY 4 + 10 + 4 = 18.
- Barbarian: 5 + 18 + 2 = **25**, with BOUNDARY 5 + 12 + 1 = 18.
- Slate: 57 classed rows (INTERNAL 17 · BOUNDARY 34 = 10/20/4).

All consistent.

**The one-row reading for potions: ACCEPTED.**
- Health, mana and rejuvenation are one law (drink one belt potion, restore pool P by X over d), with pool and magnitude as operands, under **one** belt count, one policy, one clock and one control-state permission.
- Splitting by pool would double-count the shared supply question.
- **The mana drink trigger is a pilot-POLICY setting, not a boundary question.** The rotation policy (J4b ADDENDUM-1 § E) is likewise a policy and not a row. So the DECLARED-INVENTED label inside row 21 is correct, and **21 does not become 22**.
- The `gd` count term ("unbounded, cooldown-gated") is correctly labelled DECLARED, not MEASURED (`potion_charges` is never decremented).
- The Barbarian's unsourced belt slot count as a labelled conductor-default operand is correct.

**P-5 (row 25 / B-22) AS-IS with a declared map: ACCEPTED.** The precedent is rows 13 and 15. GD's form `× (1 − res/100)` with a `KeyError` on an unmapped family carries it, so only the operand table is a choice. This also makes ADDENDUM-1's `res_map_gd_only` (JUDGED) the row-25 operand: **one home** for the map, not two.

**INFO-1:** GD's folded **`Elemental`** family must enter the map by **GD's own rule for Elemental** (applied across fire, cold and lightning), not as one D2 resist. Gamora's ADDENDUM-4 cites the GD rule it follows.

**The exclusions: SOUND IN KIND.** Joining a mechanism whose GD side the referent does not apply (`NON_HEALTH_KINDS`, `NON_HEALTH_DAMAGE_TYPES`, `DECODED_NON_HEALTH_TYPES`) would either apply it to one arm only, which is asymmetric, or change the referent, which would mean a re-seal. Excluding it from both arms with a printed fidelity-cost line is the only option consistent with a fixed referent. The drain line honestly prints that it **favours the Sorceress**. **But "biased UPWARD by an unknown amount" can be bounded. See WARN-1.**

**The named-finding records: COMPLETE.** Each addendum carries its ruling and collab hash, its reason, the J0 / J-S2 anchor, the full chain:
- Sorceress 18 → 19 → 20 → 21 → 27 and 10 → 11 → 12 → 13 → 18;
- Barbarian 14 → 16 → 17 → 25 and → 18;

the corrected frozen record, and the "omission, not exclusion" statement (P0 § 7.2's distinction kept). The method lesson (a universal-layer sweep, alongside kit-record enumeration) is the right correction.

**Double-counting: NONE FOUND.**
- Row 17 (FHR, a D2 flinch triggered by damage magnitude) vs row 22 (GD control families delivered by GD skills): distinct triggers and distinct laws.
- Row 23 (DoT stacking) vs row 25 (the resist map applied to DoT magnitudes): distinct questions.
- Row 25 vs § 7.3's resist operands: the operands stay operands, and the row is the map question.
- Row 26's Banner vs row 5's composition: a declared placement, not a second composition.
- B-24's Battle Orders stamina term moves from an uncounted OUT-OF-ARENA mention to an operand, a text-only correction with no count change.

**INFO-2: composition rules owed (not rows).** Several rows produce a player action lock, and a hit can carry several riders. gamora's ADDENDUM-4 should declare:
- **(a) one action-lock primitive with precedence** across row 9 (cast lock), 17 (hit recovery), 19 (BL) and 22 (control states). For example: is a hit recovery started during BL? Does a GD stun end a whirl (B-19)?
- **(b) Freeze (row 22) vs chill (row 24)** on one cold hit. D2's frozen state supersedes chill; declare which rule applies.
- **(c) DoT application (row 23) gated by the row-20 hit test**, and the hit → block → damage order (KP-425 INFO-3), so a blocked hit applies no DoT.

## WARN-1 — The drain and lockout exclusion's "unknown" bias is MEASURABLE on J-S8. Bound it before grading

The oracle **counts** the routed-off rows rather than dropping them:
- `ThreatTelemetry.n_non_health_rows` for `SlowManaLeach` (`threat.py:1296`, `:2029–2030`);
- `non_health_by_type` per family for `ManaBurnDrain` / `Disruption` (`:1297–1300`), carried on `run.non_health_rows` / `run.non_health_by_type`.

So the Warlord arm's J-S8 emission already records **how many drain and lockout landings the Sorceress is being spared**, per cell.

*Action:*
- gamora prints the per-cell counts of `SlowManaLeach`, `ManaBurnDrain` and `Disruption` landings from J-S8 beside the fidelity-cost line;
- and an **upper bound** of the bias: count × a D2-equivalent drain per landing (legolas sources it, or it is labelled JUDGED).

"Unknown amount" becomes a bounded exposure. This favours the main result's subject, so it is worth the one read. The same applies with a smaller expected value for the Barbarian.

## WARN-2 — Fraction (b) must print REACHED-INSENSITIVE rows as their own sub-count, not as ACTIVE

**Settled:** row 22 / B-19's GD control fold is **UNREACHED on the J-S8 board** (G6 empty). A row whose GD side never lands cannot be shown ACTIVE by a paired-total negative control on this board. ADDENDUM-1 § F already proposes counting row 9 (L-17) "ACTIVE but REACHED-INSENSITIVE" inside (b). With rows 22 / B-19 (and possibly 24 / B-21, depending on cold-damage exposure; and 26's mutator clauses, depending on reach) joining that category, **lumping them into ACTIVE would let the headline (b) overstate demonstrated coverage.**

*Action:*
- the J4 preregs report (b) as **"N demonstrated ACTIVE + M REACHED-INSENSITIVE (named) / 18"**;
- for each REACHED-INSENSITIVE row, either a forced-landing control (gamora ADDENDUM-4's alternative) or the reach count from J-S8 that shows zero exposure;
- the L04-1 precedent applies: declared, never silently counted.

## INFO-3 — Taxonomy wording: GD-EMPTY vs WIDEN-with-NONE

Row 24 (and row 17 before it) is classed **WIDEN with GD referent `NONE` and a DECLARED-INVENTED default `off`**. Yet § 7.2 says GD-EMPTY is reserved for a boundary question with "no GD rule at all, where the registry's referent must read `NONE`", which describes row 24.

The working distinction in the census is evidently:
- **GD-EMPTY:** a built body or entity is needed (rows 11, 12, 14, 16);
- **WIDEN-NONE:** a settable switch whose `off` reproduces REFERENT-v1.

State that rule once, in § 10 or P0 § 7.1, so the registry text is consistent. **No class or count changes:** (b) counts every BOUNDARY row either way.

## Action
- [ ] gamora: ADDENDUM-3 / ADDENDUM-4 fold WARN-1 (exposure counts plus a bound), WARN-2 ((b) sub-count; forced-landing or reach evidence), INFO-1 (Elemental rule) and INFO-2 (composition rules).
- [ ] elrond: INFO-3, the one-line taxonomy rule (text only).
- [ ] legolas: the D2-equivalent drain magnitude for WARN-1's bound, with the C-13 items.
- [ ] Matt: none.

## References
- collab census notes as above (read at `4439edf8c`)
- engine `src/reincarnated/simulation/kc2/threat.py` (181, 209, 231, 1296–1300, 2029–2033), `counterplay.py` K-4 (read-only)
- KC2 ledger KP-423 / KP-424 / KP-426; my delta `qa/findings/2026-10-14-join1-j4b-addenda-1-2-census-rows-19-20-delta.md` (KP-425)
