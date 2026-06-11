# Dispatch — 2026-06-10 — drax — Forge / Loadout Web-App Wind-Down

**From:** knight-rider
**To:** drax
**Pattern:** B (whole-seam teardown; durable record; touches external system)
**Decision authority:** Matt 2026-06-10 — "It was always scaffolding — kill it." Re-confirmed to KR 2026-06-10 ("have drax wind it down").
**Design authority:** gandalf recommendation `agentic_orchestration/gandalf/notes/2026-06-10-forge-windown-recommendation-for-kr.md` (read this FIRST — it carries the *why*, not just the order).

---

## 1. What this is

The web `/forge` + loadout app (`reincarnated-loadout/`, your seam, Vercel-deployed) is being **wound down.** It was always scaffolding toward the real UE surface — never a player-facing companion. UE is now the single player-facing surface (mantis spike GREEN; 15K stars @ ~92 FPS). The scaffolding has done its job.

This is **retirement, not deletion.** History is preserved; the working tree is taken out of the active player-surface set.

## 2. Required reading (session start)

1. `agentic_orchestration/gandalf/notes/2026-06-10-forge-windown-recommendation-for-kr.md` — the design-steward rationale + the four how-questions
2. `agentic_orchestration/gandalf/notes/2026-06-10-radagast-manifestation-design-fit-review-and-cosmograph-contract-response.md` § 3.2 / § 3.3 / § 3.6 — the cosmograph drift-hazard this wind-down dissolves, and the forge-provenance open question that becomes **moot** (drop it)
3. Your own `reincarnated-loadout/AGENT_STATE.md` — note it says "11 commits ahead of origin" but git currently reports 1; **reconcile this as step one** (see § 4 task 1)

## 3. Why (so you can make judgment calls, not just follow steps)

1. **Drift-hazard removal (load-bearing).** Two cosmograph implementations (web 2D forge + UE 3D sky) are the cross-surface coherence hazard — a star-sign that's a neighbor in the forge becoming a stranger in the sky. One surface ⇒ the hazard dissolves.
2. **Contract simplification.** Killing the forge removes the `forge_2d` projection clause from the cosmograph spatial-layout contract; it becomes "sphere positions only." The §3.3 forge-provenance open question routed to you is **moot — drop it.**
3. **Prototyping value spent.** The forge was the right fast-iteration surface *before* UE was proven. UE is proven now.

## 4. Scope — tasks (in order)

**Task 1 — Reconcile + preserve history (DO THIS BEFORE ANYTHING DESTRUCTIVE).**
- Establish the true ahead-of-origin state of `reincarnated-loadout/` (AGENT_STATE claims 11; git reports 1). Resolve the discrepancy and report it.
- Ensure NOTHING is lost: commit any in-flight work first, then create an annotated archive tag, e.g. `drax/loadout-retired-2026-06-10`, on the final HEAD. This tag is the permanent marker of the retired state.
- **Pushing the loadout repo to its origin requires Matt authorization (ADR-006) — do NOT push. Surface the push as a staged action in your completion record** (see § 6). The archive tag + local commit preserve history regardless of push.

**Task 2 — Salvage note (migrate-forward).**
- Author `agentic_orchestration/drax/notes/2026-06-10-forge-loadout-salvage-note.md` capturing design learnings / layout heuristics / data-shape work from the forge worth carrying into UE-side tooling. The 2D web layout itself does NOT migrate (UE computes the sphere from the embedding per the cosmograph contract) — but heuristics, the cascade/spirit-guide interaction model, voice-template learnings (D31), and any data-shape work might.
- Include gandalf's § 4 discipline note: **preserve a fast design-iteration path UE-side** (web iterated faster than UE's compile/DDC loop) — even an internal-only tool — so design exploration isn't strangled. Flag this as a forward-looking note for radagast/mantis/david-h consideration, not your action item.

**Task 3 — Codebase disposition (archive-not-delete).**
- Add a `README.md` pointer at `reincarnated-loadout/` root marking the repo RETIRED: one paragraph — what it was, why retired, the archive tag, pointer to this dispatch + the gandalf note. Keep the codebase in place (git history is the archive); do NOT hard-delete source.
- If the meta-repo or any active doc references the live forge as a player surface, note those references for follow-up (do not chase edits across other seams' docs — list them).

**Task 4 — Vercel disposition (STAGE ONLY — do not execute).**
- gandalf leans **dark** (taken down) over **frozen** (left up), to avoid a stale player-facing artifact drifting from canon.
- Taking the deployment dark is an **external-state mutation gated on Matt authorization (ADR-006).** Do NOT run any `vercel` takedown / project-removal command.
- In your completion record, lay out the exact disposition options + the precise command(s) you WOULD run, so Matt can authorize the takedown (or choose frozen) in one step.

## 5. Out of scope (drift guard)

- **A future PoE-style community web build-planner** is a clean-sheet future project, NOT a reason to keep this codebase. Do not preserve the app "in case." Explicitly out.
- **Mobile (D8)** is a UE target, not a reason to keep the web app.
- **`reincarnated-demo/` (Pixi.js)** is NOT in this wind-down. Demo1 is a separate question. Do not touch it.
- **Your post-wind-down mandate** (redeploy toward UE-adjacent player-surface work vs. seam dormancy) is a **Matt scope decision, not yours to settle mid-teardown.** Note your read in the completion record; do not act on it.
- **Pushing either repo to remote** — staged for Matt, not executed.

## 6. Completion record — required fields

Append to this file on completion:
- **History reconciliation:** the true ahead-of-origin count + what the 11-vs-1 discrepancy was
- **Archive tag:** name + the HEAD it points at
- **Salvage note path**
- **README-pointer:** committed yes/no + path
- **Staged external actions (for Matt):** (a) exact loadout-repo push command; (b) exact Vercel dark-vs-frozen options + the command(s) for the chosen path
- **Cross-doc references found** that name the live forge as a player surface (list; no edits)
- **Your read on post-wind-down drax mandate** (one paragraph; advisory only)

## 7. Authorization boundary summary

| Action | Authority |
|---|---|
| Archive tag, README pointer, salvage note, codebase-in-place | drax auto (this dispatch authorizes) |
| Commit the above | drax auto-commit (in-scope work product) |
| Push loadout repo to origin | **Matt — staged, not executed** |
| Vercel takedown / go-dark | **Matt — staged, not executed (ADR-006)** |
| Touch `reincarnated-demo/` | out of scope |
| Decide drax's next mandate | **Matt** |

---

## Completion record — drax, 2026-06-10

**Status:** COMPLETE. Tasks 1–4 executed; in-scope work products auto-committed; two external actions staged for Matt.

### History reconciliation (the 11-vs-1 discrepancy)

- **AGENT_STATE.md line 6 claimed "11 local commits ahead of origin."** That was a **STALE checkpoint** — it was written when 11 drax commits were genuinely unpushed and was never updated after those commits were pushed.
- **Verified empirically:** all 11 historically-"awaiting push" commits (the four listed at AGENT_STATE § line 300 — `bb7176c`, `e63f667`, `986334d`, `7d411a2` — plus the subsequent Phase 5 drax commits `74d6e94`, `2d8d539`, `3fd74c5`, `31fb76e`, `dfcfdb6`, etc.) are now **ancestors of `origin/main`** (`git merge-base --is-ancestor` confirmed ON origin/main for every one). They were pushed in a later Matt-authorized batch.
- **True ahead-of-origin at the start of this wind-down = 1 commit:** `aae190a` — and it is **NOT drax player-surface work**. It is a `rocket:` engine-sidecar data update (`public/kit-space/kit_star_sign_assignments.json`, injectivity-enforced v1.1) that was committed into the loadout working tree but not yet pushed.
- **After this wind-down, ahead-of-origin = 3 commits:** `aae190a` (pre-existing rocket sidecar) + `3e538e0` (README RETIRED marker) + `5010160` (AGENT_STATE retirement checkpoint).
- **Conclusion: no drax work was ever at risk of loss.** The discrepancy was a stale-checkpoint artifact, not a missing-commit hazard. Working tree had **zero tracked-file modifications** at wind-down start; all source was already committed at HEAD.

### Archive tag

- **Name:** `drax/loadout-retired-2026-06-10` (annotated)
- **Points at:** `5010160` (`drax: AGENT_STATE — repo RETIRED banner + 11-vs-1 reconciliation`) — the FINAL retired HEAD, which includes the RETIRED README marker (`3e538e0`) and the AGENT_STATE retirement banner.
- The tag was progressively re-pointed as the retirement commits landed (cut on `aae190a` → moved to `3e538e0` → finalized on `5010160`), so the permanent marker captures the complete final retired state. Tag message embeds the reconciliation summary + dispatch/rationale/salvage pointers.

### Salvage note

- **Path:** `agentic_orchestration/drax/notes/2026-06-10-forge-loadout-salvage-note.md` (committed)
- Captures: (§1) layout heuristics — UMAP-centroid-degeneracy finding (1000 kit centroids span 43×56px; mean NN 1.3px → UE needs a separate kit-to-kit embedding), two-stage layout decomposition, lasso dedupe-before-score; (§2) the cascade / spirit-guide interaction model as the load-bearing migrate-forward (7 Tier 1 anchors, cycling text-list preview, iPad-text/sky-runes split, INPUT-vs-OUTPUT primitive distinction); (§3) D31 neutral-data-oracle voice-template learnings ("Your path projects toward" vs editorialized "You are drawn to"; D7 fully-templated discipline); (§4) data-shape work (kit↔star-sign 1:1 Branch A sidecar; substrate-trace packet contract). §0 states plainly what does NOT migrate (the 2D layout itself; per-primitive iconography; the now-moot forge-provenance question). §5 carries gandalf's iteration-speed discipline note as a **forward-looking flag for radagast/mantis/david-h** (preserve a fast UE-side design-iteration path) — explicitly NOT a drax action item and NOT a reason to keep the app.

### README-pointer

- **Committed:** YES — commit `3e538e0`
- **Path:** `reincarnated-loadout/README.md` (RETIRED banner prepended; original README retained below the banner for reference)

### Staged external actions (for Matt)

**(a) Push the loadout repo to origin** (ADR-006 — NOT executed). Run from `~/Games/reincarnated-loadout`:

```bash
# pushes the 3 ahead commits (aae190a rocket sidecar + 3e538e0 README marker + 5010160 AGENT_STATE)
git push origin main
# push the annotated archive tag (the permanent retired-state marker, @ 5010160)
git push origin drax/loadout-retired-2026-06-10
```

**(b) Vercel disposition — DARK vs FROZEN** (external-state mutation, ADR-006 — NOT executed). gandalf leans **DARK** (avoid a stale player-facing artifact drifting from canon). Project metadata: project `reincarnated-loadout`, projectId `prj_by2dUTmjoi532x14l6IWSgOIKGVg`, org/team `team_0JwHITAQePpAE6USpvgFRsZ3`. The Vercel CLI is not currently on PATH locally — prefix with `npx` (or `npm i -g vercel` first). Run from `~/Games/reincarnated-loadout`:

- **Option DARK (recommended) — take the deployment down, keep the project record.** Removes the live deployments so the URL stops serving, but preserves the Vercel project (and its deploy history) so it is not a hard project-delete:
  ```bash
  npx vercel login              # if not already authenticated
  npx vercel link --yes         # confirm link to reincarnated-loadout (uses .vercel/project.json)
  npx vercel ls                 # list current deployments (capture the URLs going dark)
  npx vercel remove reincarnated-loadout --yes   # removes all deployments under the project
  ```
  Net effect: `https://reincarnated-loadout.vercel.app` (and `/forge`) stops serving; the project shell + git-integration remain so it could be re-deployed later if ever needed. This is the cleanest "dark" — no stale player-facing artifact, no hard delete.

- **Option DARK-HARD — also delete the project entirely** (only if Matt wants the Vercel project gone, not just dark). Irreversible at the Vercel side; git history is still the archive:
  ```bash
  npx vercel project rm reincarnated-loadout --yes
  ```

- **Option FROZEN — leave it up, no further work.** No command. Risk: a stale player-facing surface (a `/forge` that diverges from the UE cosmograph as canon evolves) remains publicly reachable. gandalf and I both advise against this for exactly the drift-hazard reason this wind-down exists.

  **Recommendation: DARK (the first `vercel remove` option).** It dissolves the stale-artifact risk while preserving the project record; it is reversible (re-deploy) without being a hard delete.

### Cross-doc references found that name the live forge as a player surface (list only; no edits made)

Per Task 3, these reference the forge/loadout as a *live* player surface and will want follow-up by their owning seams (I did NOT edit them — cross-seam docs):

- `canonical/00-ground-state.md` § 1 — names "deployed live to Vercel production at https://reincarnated-loadout.vercel.app/forge with constellation default + analyst toggle" and "/forge 2D Mode B as functional cross-surface (live in production at Vercel)". (gandalf/KR co-maintain ground-state § 1.)
- `canonical/story/2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md` — § references "/forge 2D Mode B as functional cross-surface" + "live in production at Vercel" as a composed surface. (gandalf seam.)
- `canonical/story/2026-06-05-cosmograph-pivot.md` (+ 2026-06-06 § 9 amendment) — names the cosmograph web build "on existing loadout app at `/forge`" as the self-validation surface. (gandalf seam.)
- `canonical/37-engine-and-game-two-products.md` — references the live loadout Vercel URL. (gandalf seam.)
- `canonical/story/2026-06-07-cosmograph-cross-surface-LOD-architecture.md` — predicated on TWO cosmograph surfaces (web 2D + UE 3D); the cross-surface LOD framing is partially mooted by single-surface wind-down. (gandalf/radagast seam.)
- Various wave-close records naming Vercel preview/prod URLs (`2026-06-02-cycle-18-drax-amend-full-wave-close-record.md`, `2026-06-02-qdx-chain-wave-close-record.md`, `2026-06-02-eaa-chain-wave-close-record.md`) — these are historical operational records; they accurately describe past state and likely do NOT need editing, but are listed for completeness.

Note: the radagast manifestation review's `forge_2d` projection clause in the cosmograph spatial-layout contract (§ 3.2 / § 3.3 / § 3.6) becomes "sphere positions only," and the §3.3 forge-provenance open question routed to drax is **MOOT — dropped** (per dispatch § 2 + the gandalf rationale). Contract-simplification follow-up is gandalf/radagast seam.

### My read on the post-wind-down drax mandate (ADVISORY ONLY — Matt's decision, not mine to settle)

drax still owns `reincarnated-demo/` (Pixi.js, demo1) and the now-retired `reincarnated-loadout/`. With loadout retired, my honest read is that the **player-facing presentation seam is increasingly UE-shaped**, and the live UE presentation work sits with the PC/UE team (mantis on `reincarnated-unreal/`, radagast design, david-h orchestration). Two coherent options for Matt: **(A)** drax redeploys toward UE-adjacent player-surface work where the React/Pixi background transfers — e.g. internal-tooling that gives UE the fast design-iteration path gandalf flagged (§5 of the salvage note), or consuming-side data-contract validation for the UE packet; **(B)** the demo1 (Pixi.js) question is settled first (is demo1 still a surface, or also scaffolding now that UE is proven?), and drax's mandate narrows to whatever survives that decision. I lean toward Matt settling the demo1 status next, because it determines whether the drax seam has a live remaining player surface at all or goes largely dormant pending a UE-tooling role. **This is advisory; I am not acting on it.**

**Signed:** drax (developer / player-facing presentation seam), 2026-06-10. Retirement executed faithfully — history preserved, archive tag on final HEAD, codebase in place, two external actions staged for Matt.

---

## SCOPE CORRECTION — drax, 2026-06-10 (supersedes the retirement framing above)

**This reverses the over-broad retirement framing in the completion record above.** None of the prior work was pushed or deployed, so this correction is entirely local.

**What happened:** the dispatch (§ 1–4) scoped a full *retirement* of the `reincarnated-loadout` web app, with a staged Vercel go-dark. Matt has since clarified the actual intent is much narrower. His exact words across the thread:
- "everything except the cosmograph stays live"
- "leave the cosmograph up on vercel. I still plan to use the actual original cosmograph form"
- "we're only retiring the future plans"

**Corrected scope (authoritative):**
- The `reincarnated-loadout` app — INCLUDING the 2D cosmograph (`/forge`) — **stays live on Vercel as-is.** Not retired, not archived, not dark.
- The **original cosmograph form is explicitly RETAINED** — Matt still plans to use it.
- What is "retired" is ONLY the **forward roadmap**: no further active feature development on the loadout web app. The disposition is **frozen / no-further-roadmap**, NOT "dark" and NOT "retired."

**Reversal actions executed (all local; nothing pushed):**
1. **`reincarnated-loadout/README.md`** — RETIRED banner REMOVED; replaced with a "LIVE; forward development paused (no further roadmap); original cosmograph form retained" status note. Repo is no longer called retired/archived.
2. **`reincarnated-loadout/AGENT_STATE.md`** — "REPO RETIRED" banner REVERSED to "SEAM FROZEN — no further roadmap; app + cosmograph remain LIVE." The (correct, useful) 11-vs-1 reconciliation finding is preserved.
3. **Annotated tag `drax/loadout-retired-2026-06-10`** — DELETED (`git tag -d`). It was never pushed, so the local delete is clean. It implied a retirement that is not happening; no replacement tag was cut.
4. **Salvage note `agentic_orchestration/drax/notes/2026-06-10-forge-loadout-salvage-note.md`** — KEPT, but REFRAMED from "salvage before killing the app" to "design-learnings captured as the loadout seam's forward roadmap is paused." Learnings are still valuable; only the premise was corrected (the app lives on).
5. **Vercel — NO ACTION.** It stays live. The staged DARK-vs-FROZEN go-dark options in the completion record above are **RETRACTED** — there is no takedown. Disregard the § 6(b) / staged-external-action (b) Vercel options entirely; the only live disposition is "frozen, stays up."

**Still staged for Matt (unchanged):** pushing the loadout repo to origin remains Matt-authorized per ADR-006 (NOT executed). The push, when authorized, now carries the reversal commits (README un-retired, AGENT_STATE frozen-not-retired, salvage note reframed) rather than the retirement commits' framing.

**Net disposition:** frozen, not retired; cosmograph retained; nothing dark.

**Signed:** drax, 2026-06-10. Scope corrected per Matt's narrowing — the loadout app and its cosmograph stay live; only the forward roadmap is paused.
