# Finding — 2026-07-29 — WR1-G2-STAR (WR1-LAP0-STAR, HQ-2 provenance leak + `encounters` drift)

**Reviewer:** jack-ryan (DEV-MODE, Gate 2)
**Severity:** INFO (verdict **PASS-with-notes**) — one WARN carried, no BLOCK
**Target:** engine `77b1b86` · note `22bd3747`
**Developer:** star-lord
**Run:** WR1-2026-07-28 Leg 1 Lap-0, cell `WR1-LAP0-STAR` (conductor: gandalf, charter §8 / §8.3)
**Principles applied:** 2 (smoke-gate before commit), 3 (cross-seam impact called out), 5 (severity/escalation), 6 (cross-seam contract round-trip)
**Disciplines cited:** #8 (schema validation at boundaries), #9 (assertions derive from spec sources), #10 (attribution clarity), #11 (empirical inspection over assumption), #12 (semantic-shifting fixes need explicit framing)
**ADRs:** ADR-002 (tiered approval — cleared at my tier), ADR-004 (MIGRATION for cross-seam handoff)

---

## What I found

Five claims were checked by re-measurement rather than by reading the landing's prose. All five hold.

**1 — Write-site fix does not break any legitimate production caller.** `run_w3_emission()` has exactly
two invocation sites in the repo: the driver's own `main()` and `tests/test_w3_emission_driver.py`. No
shell script, no other module, no sibling repo reaches it (demo/loadout are JS). `main()` retains the
ability to write via `--write-band-report` (`store_true`, wired at the call site). The result-dict change
is purely additive (`section8a1_band_report_written`); `section8a1_band_report_path`,
`section8a1_band_summary` and `section8a1_gate_outcome` are unchanged. Nothing downstream loses a key.

**2 — The byte-identity claim is true of the literal.** I hashed the `"encounters": {…}` dict literal out
of both files: `one_realm_bundle_assembler.py:1535-1544` and `w3_emission_driver.py:1206-1217` are
md5-identical (`dc952c77951cba93504e8b4db3dddcb4`), same key order, same `_note` string. The *surrounding
comment* differs — the assembler carries a "Godot loader: treat this as a reserved extension point" line
the driver's block drops in favour of the 2026-07-29 repair rationale. That is a wording difference, not a
payload difference, and the claim the landing needs ("no schema change, drax needs no re-handshake") is
sound. I also checked for *further* drift: all twelve keys `validate_bundle()` requires are present in
the driver's parallel dict (`bundle_version`, `generated_at`, `engine_version`, `season_id`,
`schema_status`, `kits`, `monsters`, `gear_pool`, `floor_manifest`, `proxy_scaling`,
`stage2_run_record`, `encounters`). No second gap hiding behind the first.

**3 — The attribution correction is evidenced, and I reproduced it.** Importing
`reincarnated.simulation.spatial_gauntlet.kitcal_g5_harness` and then filtering `sys.modules` yields zero
`w3_emission` entries — the harness genuinely cannot reach the writer, transitively or otherwise.
`_SECTION8A1_BAND_REPORT_PATH` is defined and written in exactly one source file. Charter §14.36 / HQ-2's
"battery writer path" does not exist as a code object. The correction stands, and the conductor has already
banked it at charter §8 line 282, so no ledger debt remains open.

**4 — Test honesty under the `encounters` confound: correctly handled.** I confirmed the ordering the
landing rests on: the §8-A1 write sits at `w3_emission_driver.py:689`, `validate_bundle()` at `:1250`, and
that validation call is *not* smoke-gated. So pre-fix every smoke run wrote the artifact and then halted —
meaning the Group G pin, run against a fully reverted driver, fails on the HALT-LOUD before it ever
evaluates its own assertions. star-lord names this explicitly and refuses to bank "4 red pre-fix, green
post-fix," resting the discrimination on the artifact md5 movement (`852558404c…` → `e49dd652c2…`) instead.
That is the right instrument for the question (Discipline #11), and declining the confounded-but-flattering
claim is the honest move. Going forward the pin is non-vacuous in the ordinary sense: with `encounters`
in place, reverting only the write-gate makes it fail on the provenance assertion.

**5 — The NOT-MINE flag is honest.** I reproduced the flagged failure at HEAD:
`test_no_canonical_four_in_llm_prompts.py::TestMonsterNamingNoCanonicaFour::test_all_elements_monsters`
fails with `ValueError: Unknown element: 'water'` raised at
`src/reincarnated/generation/ability_grammar.py:457` — rocket's seam, no contact with this diff.
Note for the record: the "389 passed" figure appears in the conductor's §8 bank entry but in none of
star-lord's own filed artifacts, which document only the 36/36 on the single file. The attribution is
sound either way; the suite-width number is the conductor's claim, not the developer's.

**Discipline #12 assessment — no violation.** Two semantic shifts occurred and both are framed loudly,
in four places each (docstring, inline comment, MIGRATION.md, AGENT_STATE): (a) the driver stops
persisting by default, framed with an explicit operator-action line and an additive truth-telling result
key; (b) the driver's bundle gains a required key, which converts a 7-day guaranteed HALT into a pass.
(b) cannot regress any consumer, because no bundle has successfully left this driver since 2026-07-22 —
the old shape was never emitted, so there is no prior contract to break, and the new shape is exactly the
one drax already signed. The landing reasons to that conclusion rather than asserting it.

**Independent re-run of the acceptance arm.** I re-ran Group G myself at `77b1b86`:
`4 passed, 32 deselected in 288.72s`. Before, during and after, the artifact held at
`852558404c91b2fe4d8e76b58f685ab7` with `git status` clean for that path. Notably this ran while a
*second*, unrelated `pytest tests/test_w3_emission_driver.py` process was live in the same worktree
(not mine) — so the guard was verified under exactly the concurrent-battery load HQ-2 was about, which
is stronger corroboration than the landing itself claims.

## Rationale

The landing satisfies Principle 2 (the acceptance proof is a real executed measurement, not an argument),
Principle 3 (cross-seam impact is stated and correctly scoped to operators rather than drax), and
Principle 6 (the `encounters` repair is a conformance move to an already-round-tripped contract, so no
re-handshake is owed). Discipline #10 (change one thing) is technically strained by shipping two defects
in one commit; it is defensible here because the `encounters` halt *blocked* the acceptance proof — the
fixes were not separable in practice — and both are named distinctly in the message, MIGRATION and
AGENT_STATE, so archaeology is preserved. Recorded, not charged.

The carried WARN is not about what was fixed; it is about the residual edge the gate does not cover.

## Action

- [ ] **star-lord (WARN-1, seam-owned, next touch of this file):** `--smoke --write-band-report` is an
  unguarded clobber path. The gate keys on the flag alone, and the report payload's `pilot_context` block
  (`generation_seed` / `n_candidates` / `gauntlet_wall_clock_s`, `w3_emission_driver.py:267-271`) carries
  no smoke marker. An operator passing both writes a 5-kit smoke report over the 18-candidate measurement
  of record, and the substitution is only *inferable* post-hoc from seed and candidate count — which is
  precisely the forensic reconstruction HQ-2 required in the first place. Close it one of two ways:
  refuse the write when `smoke=True` (skip with WARNING, or HALT), or stamp `smoke: bool` into
  `pilot_context` so the artifact keeps self-identifying. Cite Discipline #8.
- [ ] **star-lord (INFO-1, follow-up item, post-baton):** the driver still maintains a *parallel* bundle
  dict rather than delegating to `assemble_one_realm_bundle()`. That duplication is the root cause of the
  7-day silent halt and will drift again on the next required-key addition. Cheapest durable guard is a
  test asserting the driver's bundle key set covers `validate_bundle()`'s required list *derived from the
  assembler's own tuple*, not hard-coded — Discipline #9. Structural fix (delegate to the assembler) is a
  larger call and not asked for here.
- [ ] **No action — recorded for the next reader (INFO-2):** the Group G pin is deliberately non-hermetic
  (asserts on the real repo path including `st_mtime_ns`). That is the correct choice and star-lord
  defends it well — a `tmp_path` redirect would have passed pre-fix. The consequence to record is that it
  is concurrency-fragile: any other process touching that path mid-run produces a false red. Charter §8.3
  and §8.8 document exactly that two-sessions-one-worktree condition. This is a known-flake class, not a
  defect; the next person to see it red should check for a co-resident run before debugging cold.
- [ ] **No action — recorded (INFO-3):** no test covers the WARNING branch (non-smoke, flag absent).
  Exercising it costs a ~1500 s gauntlet, so this is a gap of record, not an ask.
- [ ] **Matt:** nothing. No escalation. Cleared at my tier per ADR-002 — the bundle-shape change is
  conformance to an already-published, already-signed schema (2026-07-22 MIGRATION entry), and the
  behavioural change is operator-facing within star-lord's own seam.

## Verdict

**PASS-with-notes.** Both defects are real, both fixes are correct, the acceptance evidence is the right
instrument for the question, and the attribution correction is measured rather than argued. WARN-1 is a
residual edge for star-lord's next touch and does not gate the landing. `77b1b86` stands.

## References

- `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/w3_emission_driver.py` (gate `:688`; WARNING branch `:710-711`; `encounters` block `:1210-1219`; `validate_bundle()` call `:1250`; `main()` flag `:1466`; report payload `:263-278`)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/one_realm_bundle_assembler.py` (`:1266` required-key tuple; `:1535-1544` reference `encounters` block)
- `/Users/admin/Games/reincarnated-engine/tests/test_w3_emission_driver.py` (Group G, `:593-694`)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` (`[2026-07-29]` entry)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/AGENT_STATE.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/star-lord/notes/2026-07-28-wr1-hq2.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-07-28-wr1-wave-relay-run-charter.md` (§8, §8.3, §14.36 correction banked at §8 line 282)

*— jack-ryan, Gate 2, 2026-07-29*
