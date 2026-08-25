# Dispatch — drax: **consume the 3A recapture.** Your last session ended before the capture did; the frames exist and nobody has read them.

**Status:** PENDING — **gated on the capture's `COMPLETE` sentinel.** Do not start until `/tmp/s2c_recapture_logs/COMPLETE` exists. If `FAILED` exists instead, read it, report, and stop.
**Authored:** 2026-08-25 (knight-rider)
**Seam:** `reincarnated-godot` (drax)
**Continues:** your 3A recapture session (`713f487..0800f32`). **Nothing in that session is re-opened or second-guessed** — this dispatch exists only because your turn ended and the capture's did not.

---

## 0. Why this dispatch exists at all

Your return closed with *"Post-chain is ready and syntax-checked. **Waiting for the capture to finish.**"* That was an honest report with no number in it — and then your session ended.

**I verified the host rather than assuming either way. The capture survived you:**

```
Godot  98.3% CPU  --out=user://s2c12v3/ --prefix=clip_da_arena     ← 4th pass, in flight
bash /tmp/s2c_recapture_all.sh                                      ← orchestrator alive
```

⚑ **The lesson is on the record and it is not aimed at you:** an agent returning is not a dispatch completing. This session has seen a `completed` status that was a lie (an agent that died) and now a `completed` status that was *true and still meant no result*. **Only the host distinguishes them.**

**So: `s2c_prepost_compare.py` is written, syntax-checked, and unrun. That is the whole job.**

## 1. What to run, and the two-pass structure is YOUR ruling — I am not amending it

You ruled § 3.1 yourself and the reasoning stands:

> The sealed determinism receipt proves the **old** harness was deterministic. **Commit A changed render output by design**, so that property **does not transfer.** Without a post-fix same-code repeat, *"the fix moved the number"* cannot be separated from *"the new code has a flake floor."*

**Therefore, in this order and do not collapse it:**

1. **Flake floor FIRST** — `s2c12v3` vs `s2c12v3b`, and `s2c38v3` vs `s2c38v3b`. Same code, same everything. **Whatever this is, it is the noise floor.**
2. **Before/after delta SECOND** — pre-fix vs post-fix — **interpreted against that floor, never in isolation.**

⚑ **A delta smaller than the floor is not a small effect. It is NO MEASUREMENT**, and per `#80` it is **UNEVALUABLE** — the emptiness guard you were writing when your session ended. **Say so plainly if it happens.** "The fix changed nothing" and "we cannot tell whether the fix changed anything" are different findings and only one of them is honest here.

## ⛔ AMENDED BEFORE PICKUP — 2026-08-25, after jack-ryan's return (`e8b3de6b`). **§§ 1–2 are DISCHARGED. Do not execute them.**

**Read this before anything below it. Roughly half this dispatch is already done and the work is on disk.**

- ⛔ **§ 2 (per-mob breakdown) — ALREADY SATISFIED, and it always was.** `per_body` exists in **both** `harness_logs/s2c_rows12_2026-08-25-v3v3/pair1_reproduction.json` **and** `harness_logs/s2c_rows38_2026-08-25/pair1_reproduction.json`. jack-ryan built the full 16-cell table in one call. ⚑ **I mandated as an output something the harness had been emitting the whole time — my third instance this session of asserting an artifact's state without opening it.** Acceptance criterion 4 is struck.
- ⛔ **§ 1 (flake floor first) — DISCHARGED, and by a stronger instrument than the one I specified.** He derived it from **byte-identity** rather than recomputing SC: `PRE vs POST` = 874 co-named / **0 identical**; `FLAKE FLOOR (twin)` = 874 co-named / **873 identical**. *Identical inputs give identical statistics by construction* — **that is a stronger floor receipt than recomputing the statistic.** The one differing frame is on a scored arm (`clip_da_cathedral_f0050`): 6 px, |Δchannel| = 1 → **ΔSC ≤ 4.3e-5 against a delta of +0.1738, ratio ~4,000:1. Evaluable. `#80` does not fire.** Acceptance criteria 2 and 3 are struck.
- ⛔ **The § 2 pre-registration is spent.** Do not treat it as blinded; it has been scored, **and the prediction's Mob3 limb is `UNEVALUABLE-BELOW-FLOOR` in all four cells, both corpora.** My own "327× confirmation" of it is **RETRACTED** — it compared absolute deltas across arms whose baselines differ 3,000×. See `knight-rider/returns/2026-08-25-the-per-body-numbers-exist-…md`.
- ✅ **STILL LIVE and now the whole point of your session: § 3 (defect-class sweep), § 4 (`census.json` park), § 5 (resource projection), § 6 (image budget), § 7 (forbidden).** ⚑ **§ 3 is the one that matters** — it is the only item here that prevents a future loss rather than describing a past one.
- ✅ **NEW — rows 3–8.** `rows38_v3` is capturing as this is written. jack-ryan **pre-registered five falsifiers on rows 3–8** before it finished (his § 6). **Emit the rows 3–8 numbers before reading them**, same discipline as before, and this time the blinding is real because the run had not landed.

---

## 2. ~~REQUIRED OUTPUT SHAPE: per-mob breakdown~~ ⛔ STRUCK — see the amendment above. Retained only for lineage.

**Emit deltas broken out PER BODY — Mob0, Mob1, Mob2, Mob3 separately — not pooled.**

**Why, stated so you can refuse it if it is wrong:** jack-ryan's ruling derives that the caster travels world −Z **through Mob0 (0,0,−2.6), Mob1 (0,0,−4.4), Mob2 (0,0,−6.2)**, while **Mob3 sits off that path at x = +2.9**. That geometry makes **Mob3 a control** and the other three the exposed set. Pooled numbers destroy exactly that contrast. Your `s2c_prepost_compare.py` was authored before his ruling existed, so there is no reason it would already do this — **it is a re-analysis over frames you have already captured, not a re-capture.**

⚑ **There IS a pre-registered prediction about these numbers, recorded and timestamped BEFORE the capture finished**, at `knight-rider/returns/2026-08-25-jack-ryan-four-dispositions-and-a-prediction-filed-against-a-run-still-executing.md` § 0. **Emit your numbers before you read it.** The analysis is a deterministic script rather than a judgement call, so the risk is low — but the ordering costs you nothing and the pre-registration is only worth what its blinding is worth.

## 3. ⚑ Sweep the defect class — this is the #72 discharge for your own finding

You found that `run_s2c_rows12.sh` **wipes `s2c12` on every invocation with any argument** (hardcoded `USERDIR`, `--out=user://s2c12/` baked into 24 arm invocations, `SUFFIX` reaching only `$OUT`, unconditional `rm -f`). **`s2c12` is the pre-fix capture the sealed L-29(6) adjudication rests on.** The fresh-suffix instruction *I* wrote would, in that script, have been the command that destroyed the evidence it was meant to protect.

**Your own diagnosis is the reason this section exists:** *"I fixed the runner that had bitten me and did not sweep its sibling."*

**So: enumerate every `run_*.sh` (and any script performing `rm -f` against a resolved output directory) in `reincarnated-godot/scripts/`. For each, state whether the output path is suffix-parameterised end-to-end or hardcoded anywhere. Hit table INCLUDING ZERO.** Two known instances of one shape is a class; **a class fixed only where it drew blood is not fixed.**

**Fix what the sweep finds, or state explicitly why an instance is safe.** Do not leave a third sibling waiting.

## 4. `census.json` — jack-ryan RULED. You are ratified, and the action is now authorized.

You encountered `tmp/br2watch/measure/census.json` (dirty 23 days, `energy_label_seen` 117 → 0) and **deliberately left it alone.** jack-ryan's words: **drax ratified explicitly for refusing to dispose of a stranger's work.** Your prior instruction to not touch it was right for the state of knowledge then; the ruling has since arrived.

**Disposition — PARK. Not commit, not discard:**

- **Do NOT commit it.** Writing `energy_label_seen: 0` onto the canonical path is **`#63` verbatim** — an *unmeasured* zero promoted to a *measured* zero on the authority surface.
- **Do NOT discard it.** It may be the evidence *of* the regression rather than a product of it.
- **DO** preserve the worktree version at a **distinct quarantine path** with an **`UNEXPLAINED-REGRESSION`** marker, leave the committed version canonical, and file the 117 → 0 as an open investigation. **The tree then stops being one `git checkout` from data loss.**

**You do not own the BR2-WATCH lineage and are not being asked to explain the regression.** Preserve it and name it. Owner routing is mine.

## 5. Resource projection — MANDATORY (#1.1), and re-measure

**This tranche has halted twice on host resources** (free space **2.7 GB** at HALT #2). The recapture you just fired **consumed disk**. Before writing anything: `df`, state the margin, **and if the projection fails, DO NOT FIRE — report it.**

## 6. Image handling — a hard limit killed one of your sessions

`400 invalid_request` at ~128 accumulated image blocks: **image dimensions >2000px on many-image requests.** ⚑ **CROP at native resolution. NEVER downscale.** The features under investigation are **1–3 px**; downscaling averages them out of the reference *and* ours **at the same rate**, manufacturing a false "no difference." Ruling: `knight-rider/rulings/2026-08-25-the-2000px-wall-killed-drax-and-the-obvious-fix-destroys-the-detail-matt-asked-for.md`. **Budget images explicitly, well under 100 blocks.** If the analysis needs more looking than one context holds, **that is two dispatches, not one degraded one** — say so and stop.

## 7. ⚑ FORBIDDEN

**Do not rule on the sealed verdict.** `L-29(6)` / `R-1.3` disposition is **jack-ryan's**, and he has explicitly retained it. He has staked his own trace on your numbers and named the condition under which **he** is wrong. **Produce the measurement; do not adjudicate it.** Surfacing an observation is welcome; ruling is not.

## Quality criterion

**Game-quality goal:** the S2C class gaps drive VFX archetype minting. If those gaps were measured through a defective capture path, the archetypes inherit the defect silently. This dispatch converts a jurisprudential argument about whether a seal survives into **numbers that can refute it** — including refuting the person who ruled it holds.

**Refutation conditions — surface before executing if any apply:**
- The `FAILED` sentinel exists → report the contents and stop; do not re-fire the capture on your own initiative.
- Frame counts in any `v3` directory do not match their pre-fix counterparts → the matched-pair premise you tested in § 8 has broken; stop and report.
- Any pre-fix directory (`chmod a-w`) is missing or short → **stop immediately**, this is the loss scenario.
- The flake floor swallows the delta → report **UNEVALUABLE** per `#80`; do not report a small effect.
- Per-mob breakdown is not derivable from the captured frames → say why; do not substitute pooled numbers silently.

## Acceptance criteria

1. `COMPLETE` sentinel verified present before starting; `FAILED` handled by reporting and stopping.
2. **Flake floor computed first**, from same-code pairs, and **stated as a number.**
3. Before/after delta computed and **explicitly interpreted against that floor.**
4. **Per-mob breakdown emitted** — Mob0/1/2/3 separately, not pooled.
5. Numbers emitted **before** reading the pre-registration in § 2.
6. **Defect-class sweep** of `scripts/run_*.sh` with a **hit table including zero**; each instance fixed or justified.
7. All five pre-fix directories **verified intact** (count + `chmod a-w` still set) after the run.
8. `census.json` parked per § 4 — quarantine path + `UNEXPLAINED-REGRESSION` marker; canonical path untouched.
9. Resource projection **stated with margin.**
10. `AGENT_STATE.md` updated; **this dispatch's header moved off `PENDING`.** *(A completion record filed while the header still reads PENDING is the stale-header defect this wave has four instances of.)*
11. `git commit --only <paths>`; **before** = `git diff HEAD --name-status -- <paths>`, **after** = `git show --stat HEAD`. **Never `git diff HEAD~1` alone** — on this shared tree it reports other live sessions' dirty files as though they rode along. `git -C ~/Games/reincarnated-godot` on **every** git call; `pwd` first if any git result surprises you.
12. **No verdict on the sealed adjudication.**

## Out of scope

- The WW-AB render — **that dispatch is BLOCKED**; its comparison arm does not exist in any repo. Do not pick it up.
- Explaining the `census.json` regression (BR2-WATCH lineage, not yours).
- Any change to VFX authoring. This measures; it does not improve.
- Re-firing the capture.

## Push

Matt authorized push across repos **this session only**; it expires at the session boundary. **Do not stage untracked files** — the tree carries other sessions' capture directories and **other agent sessions are live.** Name every path explicitly.
