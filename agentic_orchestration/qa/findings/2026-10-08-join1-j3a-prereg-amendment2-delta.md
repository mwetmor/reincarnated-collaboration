# Finding — 2026-10-08 — JOIN-1 J3a prereg AMENDMENT-2 delta (Gate-1, DESIGN-MODE)

**Reviewer:** jack-ryan
**Severity:** WARN (verdict **GO-WITH-AMENDMENTS**)
**Target:** engine `1200ee19`, `src/reincarnated/simulation/math/join1-j3a-crit-model-prereg-2026-10-08-AMENDMENT-2.md`
**Developer:** gamora · conductor gandalf (KP-371)
**Principles applied:** 1 (math before code), 3 (cross-seam impact), 5 (severity matters) · Discipline #10
**Companion:** `qa/findings/2026-10-08-join1-dl5-decode-gate1.md` (WARN-1…4, routed KP-371)

## Verdict

**GO-WITH-AMENDMENTS.**
- The **build may start** on the structure: the `gd-decoded` rename, the `pth-coupled` model, `bracket_sealed_d100`, `independent-proc` kept as the D2 alternate, and G-D1, G-D2 and G-D4.
- Two WARNs must be folded into the prereg (one doc commit, alone) **before pack v2's `crit_damage_pct_*` rows are committed**. Nothing that depends on a value lands before then.
- One of those WARNs is new. It came from re-reading Lap L, and it changes the default crit-damage value for the Eye of Reckoning stream.

## Checks against the three routed WARNs, plus the equivalence

**Equivalence (`ROLL = PTH·u` with refusal below 100): HOLDS. INFO-1.**
- On PTH ≥ 100, `max(100, PTH) = PTH` identically.
- The binary's miss gate is `comiss PTH, [+0x27c]; jae` (skip when PTH ≥ 100.0), so the refusal boundary `PTH < 100` matches the binary at the equality case as well.
- The sub-70 path and the 55 floor are unreachable on that domain. Tier selection by the strict `>` cascade over i ≥ 2 matches `0x10d98e–0x10da0b`.
- *Hygiene:* in the § 2 formula, `pth_roll_span_floor` is load-bearing only as the refusal boundary. Write step 3 as `ROLL = max(span_floor, PTH)·u`, or state that the row's sole role is the refusal boundary. Otherwise a pack row exists that the arithmetic never reads.

**WARN-1 (lower-side label): NOT ADDRESSED. Becomes WARN-A2-2 below.**

**WARN-3 (no `p2m_*` source): SATISFIED IN SUBSTANCE. INFO-2.**
- § 2 sources PTH from `PLAYER_OA` and the pack v1 `offense_da` row through `probability_to_hit`.
- G-D1's DA operands (2011.53 / 2770.09) are the board's DA column, not its crit columns. No path reads `p2m_p_crit_any_pct`, `p2m_p_tier*` or `p2m_expected_mult_*`.
- *Ask (one line):* make it an assertion, not an absence. The build's law scan or a test should fail if `gd-decoded` code or its pack rows reference any `p2m_*` crit, tier or expected-multiplier column.

**WARN-4 (crit-damage total per modelled ability): NOT SATISFIED. Becomes WARN-A2-1 below.**

## Findings

**WARN-A2-1 — the Eye of Reckoning stream (row 32) defaults to the wrong crit-damage family. The corpus already records why.**

Facts:
- AMENDMENT-2 § 2 sets `crit_damage_pct_player_stream = 57.0` and labels it **MEASURED** (the sheet's "+57 % Critical Damage"). It applies 57 % to Soulfire too, and leaves the +0.69 family open.
- Lap L `method.md` § 3.2 records the **Warborn Visor's +12 % crit damage as an EoR-scoped skill modifier** (`modifiedSkillName` → Eye of Reckoning, `head_d028_eyeofreckoning.dbr`), not a global stat. The character sheet's +57 % is the global figure. A skill-scoped modifier is not part of it.
- Lap N attributes the 0.12 gap between its two crit families to that same Visor. The +0.69 family (B) carries the **larger** damage numbers (median 46,889 vs 15,111).
- Row 32 is the EoR physical per-tick stream, which is the Warlord's main attack (Lap L: %WD = 43 skill + 14 Gutsmasher).

So the corpus's own records point to **EoR packets taking 57 + 12 = 69 %** (JUDGED, sourced from Lap L § 3.2 and Lap N family B). The 57 % figure is the measured global stat. Applying it to the EoR stream drops a datamined, EoR-scoped term. That is a value judgement wearing a MEASURED label.

Size: E[mult | hit] goes from **1.0876 / 1.2070 to 1.1040 / 1.2408** (DA 2770 / 2011).

Soulfire (`eyeofreckoning2.dbr`, a separate orbiting-projectile skill) is genuinely undetermined. Nothing here shows whether an item modifier on EoR reaches the modifier skill's projectile.

*Action (gamora, prereg):*
- Row 32 takes `crit_damage_pct_player_stream = 69.0`, labelled **JUDGED (sheet global 57, MEASURED, + Visor 12, EoR-scoped, DATAMINED; additive composition MEDIUM-HIGH)**. The 57 % alternative is printed beside it.
- Soulfire takes its own row, `crit_damage_pct_soulfire`, with **both** 57 and 69 printed. Pick one as the declared default with a one-line reason.
- Add the 69 % column to the § 4 bracket table, and use it to re-score V2-PLAYER-CRIT in § 5 (×1.104 … ×1.241).

If gamora has evidence that the Visor's modifier is already included in the sheet figure, or does not reach EoR packets, cite it and keep 57. Either way the choice gets a citation, not a default.

**WARN-A2-2 — the "lower-side" framing is absent.**
- § 4 prints the decoded expectation 1.0876 … 1.2070 with no statement of where it sits relative to the referent footage.
- The Lap N tier shape (12 hits at ×1.3 or ×1.4 against about 2.1 expected; ×1.4 needs PTH > 130, above the board's maximum of 124.89) implies realised in-run PTH above the board. The footage fit gives a 22–27 % crit share, against 20.8–21.9 % for the board-fed profile.

*Action:* add a `basis` column to the § 4 bracket table that marks `gd-decoded` (board-fed PTH) as **lower-side relative to the referent footage**. Then do one of two things:
- carry a footage-implied PTH-lift sensitivity row, or
- declare the in-run PTH lift as a named input gap (DA shred, temporary OA, source mix).

G-D3's direction prediction is unaffected; it only gets more certain.

**INFO-3 — placement of J3-INTAKE-ROLL: a later J3 step (kit-join), not J3a. Register it in J3a only.**
- Every J3a emission (`gd-decoded @ 196`, `@ X`) is Warlord-only. The intake lane reads `m2p_pth_effective` keyed to the **Warlord's** DA 2591 (max 99.98), so the d100 cap cannot bind in J3a.
- The defect appears only when a joined kit with lower DA faces the board. At that point the measured `m2p` row is **itself wrong for that kit**, because it is keyed to the Warlord's DA. So the fix is broader than the roll: per-kit intake PTH from monster OA against kit DA, *then* the decoded roll at PTH ≥ 100. That belongs with whichever J3 step first gives a non-Warlord kit its own DA.

*Ask for J3a:* one line in the open items naming J3-INTAKE-ROLL and its predicate ("intake PTH ≥ 100, or defender ≠ Warlord DA"). Optionally add a tripwire counter on the intake lane that is predicted to read 0 on J-S8. No other build.

**INFO-4 — carry the sign in § 1.** The `pth-tiered` row says "≤ 1 pp". Add: *one-signed, mean −0.58 % per swing (−1.08 % … +0.10 %) intake expectation against the binary; flatters the Warlord* (decode Gate-1 WARN-2). Without the sign, a V2 reader cannot tell which way the referent errs.

**INFO-5 — G-D1, G-D2 and G-D4 are sound.**
- The G-D1 table matches `worked_example.py` (crit 13.5368/103.5368 = 0.130744; E[tier|crit] 40.854/34.888 = 1.171015). Bit-equality is well posed as stated: same order, differences printed and never tuned.
- "Miss share 0 on 196/196" is consistent with KP-368 (min PTH 102.55 at DA + E_L).
- G-D3's per-body Poisson-binomial bounds are the right family.
- **With WARN-A2-1 applied, the G-D3 mean-multiplier expectation must be computed with the per-row crit-damage value**, not a global 57.

## Action
- [ ] gamora: one prereg doc commit, alone, folding WARN-A2-1 and WARN-A2-2, plus INFO-1, INFO-2 (assertion), INFO-3 (open-item line) and INFO-4. Then the pack v2 `crit_damage_pct_*` rows (star-lord) follow that commit.
- [ ] conductor: record J3-INTAKE-ROLL against the kit-join J3 step (INFO-3).
- [ ] Matt: none.

## References
- engine `1200ee19`: AMENDMENT-2 § 0–§ 5; prereg `6e412839` (row 32 / row 34 population, NC-J3-L06-4)
- `agentic_orchestration/legolas/notes/2026-08-14-kc2-pm4-lap-l-player-offense/method.md` § 3.2 (Warborn Visor, EoR-scoped +12 % crit damage), line ≈310 (Soulfire)
- `agentic_orchestration/legolas/notes/2026-08-14-kc2-pm4-lap-n-crit-and-collision/pm4n_findings.md` § A.3–A.4
- `Game.dll` build 24825149, `0x10d878–0x10d891`, `0x10d98e–0x10da0b` (read-only)
- `qa/findings/2026-10-08-join1-dl5-decode-gate1.md`
