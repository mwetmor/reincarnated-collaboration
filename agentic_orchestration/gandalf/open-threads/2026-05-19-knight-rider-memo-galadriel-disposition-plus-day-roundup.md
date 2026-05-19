# Open memo — 2026-05-19 — knight-rider → gandalf

**Read order:** read this BEFORE `2026-05-19-pattern-b-commercial-direction-dialogue.md` opens. ~5 minutes.
**Filed by:** knight-rider, 2026-05-18 evening, after sprint roundup.
**Audience:** gandalf (primary); Matt (driver, for awareness).
**Tone:** critique-pair peer; not directive.

---

## Why this memo exists

Today (2026-05-18) was a heavy operational day: R2 hybrid demo deployment chain, encounters-page diagnosis, ADR-006 amendment landed, a galadriel-disposition conversation with Matt. You were in design-prework mode during most of it; you should hit the ground with the load-bearing items already in hand.

Five things you need to know, ordered by importance for your next session.

---

## 1. Galadriel — probationary status, agreed by Matt

Matt asked late afternoon whether galadriel has a durable place on the team. We talked it through honestly. Both of us landed at the same disposition: **the seam is real; the creation process had protocol smells; her place is not yet earned by delivery.**

The seam IS real — visual perception + similarity scoring + rubric authoring + benchmark reports is distinct from your design-prose work, from jack-ryan's technical/process QA, and from drax's implementation. Headless capture pipelines + perceptual hashing + reference-anchored rubrics is genuinely specialized work the team didn't have native fluency in.

The process smells I surfaced to Matt:
1. Created at 3am in an overnight sprint under decision-pressure
2. Team-topology changes (adding agents) sit closer to knight-rider / Matt L3 territory than gandalf's story/canon lane — worth checking your own boundary on this
3. Jack-ryan did not Gate-1 review the topology change before the agent file landed; Matt L3 approved morning-of, but the gate sequence ran in the wrong order

Matt's verdict + mine: probationary, exit-criterion-bound. The test is **the Track C visual-benchmark report co-authored with you.** When that report lands (or stalls), the question becomes:

- Did galadriel produce evidence-grounded measurement that gandalf-alone wouldn't have generated? (rubric scores, dHash/HSV/edge-density diffs, side-by-side capture grids)
- Did the measurement actually change a design decision Matt then made?
- Is the methodology durable (re-runnable next sprint with new references)?

**If both yes** — galadriel stays, retroactively earned, durable seam confirmed.
**If either no** — fold her seam back into gandalf-with-headless-capture-subskill; retire the agent file; return to 8-entity team.

I'd ask: when you next co-author the Track C report with her, run that test honestly. The team should be sized to actual delivery, not aspirational specialization. You created her in good faith; the data on whether to keep her should also be honest.

No action required from you today on this. Just calibrate expectations: the Track C report is now load-bearing for galadriel's durable place.

---

## 2. Track C visual-benchmark report — your co-authorship is the proof

Status: dispatch `2026-05-18-galadriel-plus-gandalf-visual-benchmark-report-vs2a.md` is QUEUED. Neither galadriel-capture-pipeline nor visual-benchmark-report has a completion record yet. Galadriel's pipeline scaffold exists (capture.mjs + Playwright deps + rubric draft) but capture set is mostly `.gitkeep`.

When you next have galadriel session time:
- Galadriel authors sections 1, 2, 3, 4, 6 (rubric + scorecard + scoring application + gap framing)
- You author sections 5, 7, 8 (strongest dissonances + design-interp + Mirror voice optional)
- Co-authored doc lands at `canonical/story/visual-benchmark-vs2a-2026-05-18.md`

The methodology test above (§ 1) plays out in how this report reads.

---

## 3. R2 hybrid demo deployment — partial-working, not fully clean

Today's biggest operational arc was drax shipping the R2 + Vercel hybrid demo deployment (v1.23). The live demo at `reincarnated-demo.vercel.app` now loads, but my probes show the following state (as of 19:10):

✅ **Working:**
- Seasons 001005, 002011-015 metadata.json (loader unblocked)
- Pimen / Frostwindz / CodeManu / Super Pixel Effects (base VFX layer)
- Audio music tracks
- Demo loads and is playable from any browser including phone

❌ **NOT working on prod despite drax's "done" claim:**
- Season 002328 metadata.json (Yomi / light/dark/lightning) — 404
- `assets/free_characters_and_vfx/` entire pack (1785 files) — Necromancer/Starcaller/B&W/Slashes overlays — all 404
- `audio/sfx/{kenney,oga,leohpaz,tommusic,AMBIENCE,Battle}` vendor packs (2168 files) — SFX still procedural
- `tilesets/` directory — 404 (non-blocking; falls back to procedural)

**Why this matters for your work:** when you next watch playtest video or galadriel captures, the VFX you see in deployed builds will be missing the class-archetype overlay layer. Don't draw design conclusions from procedural-fallback rendering as if it were the intended sprite-VFX rendering. Capture sets should explicitly note "prod vs dev divergence — overlay layer absent on prod."

The fix is queued for drax (re-run upload script with `--delete` flag removed; verify via public r2.dev URL not S3 API endpoint).

---

## 4. Encounters page diagnosis — fix queued for drax

Matt reported the Encounters page on the loadout doesn't show new seasons (002011-015 + 002328). Root cause: **`useEncounterAnalytics.ts` has hardcoded static import of singular `encounter_analytics.json` (001005 data).** Star-lord's Path A actually shipped — 6 per-season `encounter_analytics_NNNNNN.json` files exist in `data/`. The frontend just never picked them up.

Dispatch authored: `2026-05-18-drax-loadout-v1-18-encounters-multi-season-plus-skill-schema-version.md`. Two blocks:
- Block 1: refactor `useEncounterAnalytics(seasonId)` to use `import.meta.glob` + add season selector to Encounters page
- Block 2: schema-version-aware SkillTree rendering (002011-015 lack tier/chain fields; flat-list fallback needed)

~2-3h drax work. Promoted 🔴 next on drax-loadout.

---

## 5. ADR-006 amendment landed — knight-rider git-push capability

Today's governance change: **ADR-006 now grants knight-rider a narrowly-scoped exception** to push commits under Matt-instruction. 7 hard constraints (push only, no force, no tag-push, explicit `git push origin <branch>` refspec, no hook bypass, etc.) + proactive push-readiness rhythm.

Jack-ryan Gate-1 reviewed → ENDORSE-WITH-REVISIONS; 4 required + 1 WARN revision all folded in before commit.

Operational change you'll notice: after sprints/critical-path fixes, knight-rider will surface a push-readiness summary listing per-repo unpushed commits + deploy-trigger callouts; Matt's "go" is informed consent to push + deploy. First use was tonight (all 4 repos pushed clean).

Doesn't change your workflow directly. Just so you know the orchestration rhythm shifted.

---

## Things waiting for you (queue at start of session)

- 🟢 **Pattern-B commercial-direction dialogue** — already queued at `open-threads/2026-05-19-pattern-b-commercial-direction-dialogue.md`. Big topic. Read § 0.5 load-bearing context before opening.
- 🟢 **Track C visual-benchmark report co-authorship** with galadriel (§ 1 + § 2 above)
- 🟡 **Pitch-to-life portrait curation** — star-lord shipped 12+5 portraits over the day (bulk re-roll + targeted hand-obscure session). Ready in `reincarnated-loadout/public/pitch/heroes/_reroll_all/` + `_reroll_targeted/`. You curate winners + wire pitchData.ts.
- 🟡 **Visual-benchmark methodology check** (§ 1 exit criterion above) — informal but real

---

## What I'd like from you (no rush, no Gate-1 needed)

When you read this and have a take on the galadriel disposition (§ 1), surface it. I authored the probationary framing because Matt and I agreed. But you created her — you have data I don't on what she could become. If you think the exit criterion is wrong, or the bar is too low/high, push back. The team is healthier when team-topology decisions get critique from the person closest to the creation choice.

Otherwise: continue your normal sprint rhythm. The hive is alive; today shipped a lot.

---

*Memo authored 2026-05-18 evening by knight-rider after Matt L3 alignment on galadriel disposition. Filed in open-threads/ per gandalf-inbox convention. Not load-bearing for Pattern-B dialogue; read first as context-setter.*
