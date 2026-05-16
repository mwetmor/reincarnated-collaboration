# CLI Session Prompt — Phase 1 Polish (Three Small Tasks)

## How to use this file

This prompt is intended to be pasted into a fresh Claude Code session opened against `/Users/admin/Games/reincarnated-engine/`. It addresses **three small loose ends** discovered during post-merge SQL forensics on Phase 1's results:

1. A TrialBoss naming regression introduced by Phase 1 (both Phase 1 trials have NULL names in the DB).
2. A `--no-llm` recording behavior that's silently broken (a `--no-llm` season run didn't write to the telemetry DB).
3. A coverage gap in production data (no `rage`-energy class has been written to the DB yet — verified in CP5 but never persisted).

This is **not** Phase 2 work. The scope is tightening up Phase 1's loose ends before Phase 2 (role orientation axis) starts. The three tasks should fit in roughly half a day, with stop-and-review gates between each.

The work should land on a small feature branch (suggested name: `work/priority-12-phase-1-polish`) and merge via PR like Phase 1 did, rather than committing directly to main.

## The prompt

Copy everything between the dashed lines into a new Claude Code session opened at `/Users/admin/Games/reincarnated-engine/`.

---

I'm starting a small Phase 1 polish session — three discrete tasks discovered during post-merge SQL forensics. This is **not** Phase 2 work. The scope is bounded, and the gate pattern from Phase 1 carries over: stop and report at each task boundary; don't expand scope.

**Required reading, briefly:**

1. `CLAUDE.md` (engine repo root, if present).
2. `test-plans/priority-12-dimensional-refactor.md` — Phase 1 sub-section, for status context.
3. `notes/sessions/2026-05-08-phase1-energy-type.md` — Phase 1 session note, especially the "what surprised" and "next" sections.
4. `src/reincarnated/cli.py` — focus on `cmd_generate_season()` and the `--no-llm` argument handling.
5. `src/reincarnated/llm/naming.py` (or wherever `name_monster()` lives) — to understand the current `monster.energy_type` reference and why it crashes for TrialBoss.
6. The TrialBoss schema definition (likely in `src/reincarnated/generation/` or `src/reincarnated/schemas/`) — to find where to add `energy_type` and what the surrounding fields look like.
7. `src/reincarnated/telemetry/recorder.py` and any code paths around `--no-llm` to understand how that flag interacts with telemetry recording.

After reading, **stop and report**:

1. A brief one-paragraph summary confirming you've absorbed the context.
2. Any questions, concerns, or surprises before you start the tasks. Specifically: do the three tasks have any cross-dependencies you're noticing (e.g., does fixing task 1 affect task 3's data collection), or are they independent? Are there any other related loose ends from Phase 1 you found while reading that I should know about?
3. Anything you want to verify before starting (preferred branch name, commit message conventions, whether to PR each task separately or batch them).

**Wait for explicit go-ahead** before starting any of the tasks.

---

**Task 1: Fix TrialBoss energy_type naming bug**

**Context:** Phase 1's CP7 updated `name_monster()` to include `monster.energy_type` in the LLM naming context. This works for regular monsters (which got `energy_type` plumbed through in CP2). But `TrialBoss` is a separate schema that didn't get an `energy_type` field, so `name_monster()` raises `'TrialBoss' object has no attribute 'energy_type'` when called on a trial. Both Phase 1 trials in the DB (season_000042, season_000093) have NULL/empty names as a result.

**Fix (preferred):** add `energy_type: str = "mana"` as a default field on the TrialBoss schema, parallel to where `Monster` has it. Trial bosses are mana-using by design until Phase 5 enables non-mana entities — `mana` is the correct default for now. This is cleaner than guarding `name_monster()` against the missing attribute, because it preserves the assumption that all named entities have the field.

**Acceptance criteria:**
- TrialBoss schema has `energy_type` with `"mana"` default.
- A regression test exists that exercises the trial naming path without crashing. Add it to whichever test file already has trial-related tests.
- Trial naming now succeeds end-to-end. Run a quick verification: generate a small season with LLM (or mock) naming and confirm the trial gets a non-empty name.

**Stop and report after Task 1.** Don't proceed to Task 2 until reviewed.

---

**Task 2: Investigate `--no-llm` recording behavior**

**Context:** A user reported running `python -m reincarnated.cli generate-season --seed 46 --telemetry-db data/telemetry.db --no-llm`, but no `season_000046` appeared in the DB. The seed 93 run (with LLM) did record. Either `--no-llm` is bypassing the recorder (likely an unintended side-effect), or the seed 46 run failed silently.

**Investigation:**
1. Read `cmd_generate_season()` in `cli.py` to understand the code path under `--no-llm`.
2. Verify whether the recorder is wired up when `--no-llm` is set. The expected behavior is: `--no-llm` skips LLM naming (replaces with NullClient or equivalent) but **still records** to the telemetry DB. The recorder shouldn't depend on the LLM client at all.
3. If the recorder is being skipped under `--no-llm`, fix it so the recorder is always wired up when `--telemetry-db` is provided, regardless of LLM presence.
4. If the recorder *is* wired up but writes silently fail under `--no-llm`, find the failure path — possibly the recorder requires a name field that's missing under no-LLM, and the insert fails.

**Acceptance criteria:**
- `--no-llm` runs that pass `--telemetry-db` write to the DB.
- A test verifies the no-LLM + telemetry-db combination produces a recorded season with the expected number of classes.
- A quick smoke test: run `python -m reincarnated.cli generate-season --seed 46 --telemetry-db data/telemetry.db --no-llm` and confirm `season_000046` appears in the DB with energy_type populated and 10–11 classes.

**Stop and report after Task 2.**

---

**Task 3: Generate seasons until rage coverage exists in the DB**

**Context:** Of the 5 energy types Phase 1 introduced (mana, rage, combo, focus, stamina-as-resource), all 5 work mechanically per CP5 verification. But the only seasons recorded in the DB so far (42 and 93) happened to roll only `mana`, `combo`, `focus`, and `stamina-as-resource` for their physical class slots — no `rage` class has been persisted. The forensics SQL would benefit from at least one rage class in the DB so all 5 types are represented.

**Approach:**
1. With Task 2's fix landed, `--no-llm` runs are now cheap data-collection tools (free, fast). Use them.
2. Run several `--no-llm` seasons with different seeds: e.g., 1, 7, 13, 99, 137, 200, 314, 500, 700, 1000. Stop after the **first** seed that produces a rage class.
3. Verify in the DB that the rage class is present.

```bash
# After each season run:
sqlite3 data/telemetry.db \
  "SELECT season_id, COUNT(*) FROM classes WHERE energy_type='rage' GROUP BY season_id;"
```

**Acceptance criteria:**
- At least one season in the DB contains at least one class with `energy_type = 'rage'`.
- Quick visualization: run `python -m reincarnated.cli generate-season ... --no-llm` for whatever seeds were needed, and document the seeds in the session note. (One rage class is sufficient — don't go for completeness across all seeds.)

**Stop and report after Task 3** with a final summary covering all three tasks.

---

**Constraints — do not violate these:**

- **Polish only.** Do not implement Phase 2 (role orientation axis), Phase 3 (geometry palette expansion), or Phase 4 (diversity constraint) work. The architectural decision is captured; this session is closing loose ends only.
- **No architectural decisions.** If Task 2's investigation surfaces something that *appears* architectural (e.g., recorder/orchestrator coupling needs rework), pause and surface it — don't decide unilaterally. Route back to the discussion folder if needed.
- **Don't touch the spirit-swap mechanics layer** — duration model, earth-self vulnerability, etc. (open questions in `06-trial-room-and-class-scoping.md`).
- **Don't expand into name-collision fixes.** The CP7 finding about "Smoke-Spire Cantor" colliding across 4 mana classes is a real bug, but it's prompt-tuning territory and not in this polish session's scope. Phase 2 or a separate naming-quality pass owns it.
- **One commit per task** is preferred. Each task should produce a reviewable commit on the polish branch.

**Stopping condition:**

The polish session is complete when:
- TrialBoss naming works end-to-end (Task 1 done).
- `--no-llm` runs record to the DB when `--telemetry-db` is set (Task 2 done).
- At least one rage class is present in the DB (Task 3 done).
- All three commits are on a feature branch (`work/priority-12-phase-1-polish` or similar) ready for PR review.
- A short session note is written at `notes/sessions/2026-05-XX-phase1-polish.md` (using `docs/notes-protocols.md` format) summarizing what was fixed, what surprised, and what's next.

After the session:
- Open a PR (or report the branch is PR-ready) and merge to main.
- Phase 2 prompt drafting becomes the next task in the discussion folder.

---

## Notes for the project owner

- The three tasks are independent enough that they could be split across two or even three short sessions if you want each to land on a separate PR. The prompt assumes a single session for efficiency, but the stop-and-report gates make it easy to pause between tasks.
- Task 2 is the one most likely to surface unexpected complexity. If `--no-llm` and recorder coupling has a structural reason for being broken (rather than a one-line fix), that's worth knowing rather than papering over.
- After this polish lands, you'll have all 5 energy types in production DB data, working end-to-end naming for trials, and a `--no-llm` path that's reliable for cheap forensics runs going forward. Phase 2 starts from a clean baseline.
