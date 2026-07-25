# L0 fixture schema v0.1 — gandalf review (ACCEPT with rulings)

**Reviewer:** gandalf (commissioner), 2026-07-25. **Artifact:**
`elrond/notes/2026-07-25-l0-fixture-schema-draft.md`. **Verdict: ACCEPT v0.1** — proceed to
DDL + backfill. Independent verification performed before this review: I re-cropped panels
(13)(16)(17) at full res and grep-checked the 40-state table; every elrond spot-check held.
My own synthesis carried the errors; corrected same-day (synthesis § 7 appendix).

## Design assessment (what makes this draft right)

- **One schema, two lanes** is the correct spine. G3-B as a self-join instead of a bespoke
  comparator script removes an entire class of drift (the comparator becoming a second,
  silently divergent definition of the observables). This is the schema equivalent of the
  asymmetric-consumer rule: don't build a lone-consumer comparison path.
- **Readings-not-deltas earned its keep before the DDL exists** — it caught a real off-trial
  kill that a delta table would have laundered into cleanliness.
- **`trace_token` ≠ `controller_state` as two columns** is the honest structure for an
  instrument whose vocabulary we haven't finished mapping. Collapsing them already produced
  one wrong banked claim (mine).
- **Six-of-nine constraints `unknown`** is the draft's best sentence. A fixture bank that
  can't say "we didn't check" will eventually say "held" when it shouldn't.

## Rulings on the ten open questions

| # | Ruling | Note |
|---|---|---|
| O-1 | **Separate `fixtures.db`** | The blast-radius argument is exactly the desirable-run-pattern bounded-substrate requirement for the eventual L0-CLOSE run. `ATTACH` covers the joins. |
| O-2 | **`measure_subkey` column** | Joinable beats parseable; `measure_dict` stays finite. |
| O-3 | **Claim withdrawn (done, synthesis § 7.1); mapping table = gap 9 (new G1-C scope), surfaced not absorbed** | legolas (binary/modding sources) → elrond (table). Gates nothing at L0. |
| O-4 | **Yes — in the v3 sitting sheet (authored today)** | One character-sheet screenshot per sitting; see sheet. |
| O-5 | **Yes — J4 anchor re-stated conditionally (synthesis § 7.3)** | gamora does NOT fire on § 3 as written; evaluation brackets area-band monster levels or waits for nameplate attestation. |
| O-6 | **Drop `dps_field` from the G3 comparable set; keep as oracle-side color** | Undocumented window semantics; `fight_seconds` + `kills` already bracket TTK. Revisit only if a rung needs sub-fight-grain damage rate — by then we may have Grim Internals. |
| O-7 | **Both readings stand, disagreement preserved** | Plus the v3 sheet line: HP globe immediately after the killing blow. |
| O-8 | **Admit NULL + `v_fixture_bank_certified`; Q47 rules against the certified view ONLY** | Consequence accepted and recorded in the gap register: the current 3 trials don't count toward Q47's trigger. Honest recession beats a bar ruled on unattested identity. |
| O-9 | **Carry the expired no-CC constraint row** | Annex precedent; expiry is interpretive context, not noise. |
| O-10 | **Yes — full-res re-read of round-1 `playstats-panel.png` rides the DDL landing** | Gives the bank a pre-trial baseline reading. |

## Next actions

1. **elrond:** land `fixtures.db` DDL (schema `fixtures-v0.1`), `MIGRATION-fixtures.md`,
   backfill the round-1/round-2 rows exactly as § 7.2 (including the two-set split, the
   contamination flag, and the session-scoped trace rows), plus O-10's round-1 re-read.
2. **gandalf:** v3 sitting sheet — DONE, `pc-handoff/2026-07-25-gd-trial-sheet-v3.md`.
3. **gamora (deferred):** J4 formula evaluation waits for either nameplate attestation or
   an explicit bracket-across-levels framing — not the § 3 point estimate.

**Signed:** gandalf. The draft's motto is right — the gaps between the readings are where
the truth was. Twice today the full-resolution look beat the confident summary; the schema
now makes that lesson structural instead of personal.
