# CLAUDE.md — reincarnated-collaboration meta-repo

**You are in the meta-repo.** This directory is the design/coordination hub for the Reincarnated project. The actual codebases are siblings:

- `~/Games/reincarnated-engine/` — Python engine (content gen, simulation, balance, telemetry, LLM)
- `~/Games/reincarnated-demo/` — Pixi.js demo (player-facing demo1)
- `~/Games/reincarnated-loadout/` — React/Vite loadout web app (deployed to Vercel)
- `~/Games/reincarnated-godot/` — Godot 4.x / GDScript 3D-scene presentation prototype (Mac-resident; Synty POLYGON assets, Forward+/Metal renderer, MP4 walkthrough harness; enchanted-forest ravine combat level). Owned by drax (presentation seam) per Matt-approved scope amendment 2026-06-21. (Godot-on-Mac superseded the cancelled Unreal/PC seam, retired 2026-06-30.)

## Synthetic engineering team

  > **Orientation:** Engine first. Game second. Phase third.                                                                                                                                                                                                                                                                                  
  > Engine = architectural integrity (substrate-led discipline; canonical docs).
  > Game = player-facing quality. Phase = operational unit (waves, dispatches).                                                                                                                                                                                                                                                               
  > Conflict resolution: engine > game > phase. 

A **10-agent Mac-resident agentic team** (plus Matt) operates across all repos. **Read `agentic_orchestration/AGENTS.md` first.**

> **The PC-resident team (David-H, Radagast, Sam, Mantis) retired 2026-06-30.** It existed to serve Unreal-Engine work, which was cancelled in favor of Godot-on-Mac (drax owns `reincarnated-godot/`). The agents, their skills, the founding commit doc, and all two-host coordination machinery (SSH/WSL/tmux launch, PC pull/push discipline, PC Remote Control) were removed. Lineage is in git.

Quick launch:

```bash
# === Mac-resident team ===

# Coordinator session (start of day)
cd ~/Games/reincarnated-collaboration && claude --agent knight-rider

# Specialist sessions (task work)
cd ~/Games/reincarnated-engine && claude --agent gamora       # or rocket, star-lord
cd ~/Games/reincarnated-loadout && claude --agent drax        # or reincarnated-demo

# QA session
cd ~/Games/reincarnated-collaboration && claude --agent jack-ryan
```

## Mobile-accessible sessions via Claude Code Remote Control (established 2026-06-08)

Claude Code Remote Control (v2.1.51+) makes local sessions mobile-accessible via the Claude iOS app. **Per-machine policy** (confirmed via hypothesis test 2026-06-08): one Remote Control server per host, with up to 32 concurrent sessions per server. Mac and PC count separately.

```bash
# === Mac Remote Control (gandalf / knight-rider / jack-ryan / specialists) ===
# In a separate Mac terminal window (not your active interactive session):
cd ~/Games/reincarnated-collaboration
claude remote-control --name "Mac RC"
# Spawn mode: 1 (same-dir; default) for shared working tree
# 2 (worktree) for isolated git worktrees per session
```

**Agent role adoption pattern (v2.1.169+ — `--agent` flag removed from `remote-control` subcommand):** Remote Control servers run as generic Claude Code spawn-servers. Agent role is set by **prompt at session engagement**, not at invocation. After connecting from iOS, prompt the session with role-adoption text:

```
Read your operating procedure skill (reincarnated-<agent>-operating-procedure) and execute session-start protocol per OP § 1. Then await my direction.
```

The session reads the OP + role definition + session-start docs and operates as that agent from that point.

**Operational notes:**
- Remote Control servers must keep their interactive process alive (Mac terminal window OR PC SSH session). Closing kills the server.
- Mac Mini configured for no-sleep supports this naturally
- Session conversation history persists across iOS app flips — switching from gandalf session to KR session in iOS doesn't kill either
- GitHub OAuth re-auth (Issue #44805 workaround): claude.ai → Settings → Account → GitHub
- Cross-cycle credential durability: switch git remote to SSH-key auth at project init for any host running Remote Control; HTTPS credential helpers (osxkeychain / wincredman) fail in non-interactive contexts

## Where to find things

| Need | Path |
|---|---|
| **Canon router — FIRST READ, every session** | `canonical/00-ground-state.md` (thin router to the three canon homes) |
| **STORY spec (end-state)** — *Reap. Die. Rise.* death-faith frame, keystone, gameplay loop, style register | `canonical/reap-die-rise-story/` (read `00-index.md` first) |
| **ENGINE spec (end-state)** — generation, simulation, balance, gear/stat/T4, progression, build/perf stack | `canonical/reap-die-rise-engine/` (read `00-index.md` first) |
| **GAME spec (end-state)** — playable-product scope: One Realm MVP demo (THE DENOMINATOR), demo-critical vs launch-scope, wishlist gates | `canonical/reap-die-rise-game/` (read `00-index.md` first) |
| **Build-vs-spec deltas + forward sequencing** — what's owed, open queues (replaces the retired roadmap) | `canonical/current-to-end-state/` (`…-engine.md` / `…-story.md` / `…-game.md` / `…-serial-content-emission.md`) |
| **Matt decision queue** — human-in-the-loop items; check at session start/end | `canonical/matt_decision_needed/` |
| **Matt to-do queue** — actions only Matt can perform (host/credential-level), parked with what they unblock | `canonical/matt_to_do/` |
| Team topology + scope map | `agentic_orchestration/AGENTS.md` |
| Founding ADRs | `agentic_orchestration/GOVERNANCE.md` |
| Review process + 5 principles | `agentic_orchestration/REVIEW_PROCESS.md` |
| Latest handoff context | `agentic_orchestration/skill_handoff_<date>.md` |
| Team event log | `agentic_orchestration/CHANGELOG.md` |
| Engineering disciplines | `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` |
| Decisions log | `~/Games/reincarnated-engine/design/decisions/decisions-log.md` |
| Anything older (superseded designs, wave records, the old numbered `canonical/NN` root docs) | **git history** — searchable, not pre-load |

## Key conventions

- **Working branch (engine):** `main`
- **Tag prefix (intermediate):** `<seam>/v<X.Y>-<feature>-<n>` (e.g., `gamora/v1.3-b14-2`)
- **Tag prefix (milestone, Matt-approved):** `v<X.Y>-<feature>` (e.g., `v1.3-b14-5-secondary-loop`)
- **Cross-seam handoff:** `MIGRATION.md` per ADR-004
- **Per-seam checkpoint:** `AGENT_STATE.md` per agent

## Senior Architect

Matt (mhwetmore@gmail.com) — final approval, design direction, resolves jack-ryan BLOCKs.

---

## Team commit + push discipline (multi-agent refinement of system-default)

> **Authored 2026-05-25** per Matt directive to resolve recurring knight-rider over-asking behavioral bug.

The Claude Code system-default commit rule ("NEVER commit changes unless the user explicitly asks") was designed for single-user single-agent scenarios. The reincarnated-collaboration meta-repo runs a **10-agent Mac-resident synthetic engineering team** where routine in-scope work-products SHOULD auto-commit without per-commit re-asking.

This addendum refines the system-default rule for team-level operation:

### Commits — AUTO-FIRE without per-commit Matt re-asking

Seam-owning agents AUTO-COMMIT routine work-products from authorized in-scope work. Examples:

**Mac-resident team (canonical authority for cross-cutting):**

| Agent | Auto-commit pattern (when authorized cycle work produces) |
|---|---|
| Knight-rider | Cycle orchestration dispatches; Gate-1 critique-pair coordination artifacts; state-file updates; wave-closeout summaries |
| Gandalf | Canonical doc updates from design sessions; recognition records; request artifacts; notes from Pattern-A/B dialogue |
| Elrond | Substrate-curation artifacts from dispatch execution; schema-extension MIGRATION docs; per-source extraction logs |
| Rocket | Generation-code amendments from authorized engine work; algorithm spec updates |
| Gamora | Simulation-code amendments from authorized engine work; balance-loop artifacts |
| Star-lord | Export-pipeline + telemetry amendments from authorized engine work; LLM-call infrastructure updates |
| Galadriel | CV-pipeline + visual benchmark artifacts from authorized vision work |
| Drax | Loadout / demo amendments from authorized player-surface work |
| Legolas | Research + crawl artifacts from authorized Mode A / Mode B work |
| Jack-ryan | Gate-1 / Gate-2 findings; engineering-discipline canonical writes; decisions-log entries |

**Authorization for auto-commit:** the work-producing TASK was Matt-authorized (e.g., "fire dispatch authoring" → dispatch authoring AND its commit are both authorized). Do not re-ask per-commit.

**Authorization scope:** auto-commit applies to work-products of the AUTHORIZED CYCLE / WORKSTREAM. Cross-cycle commits OR scope-amendment commits require fresh Matt-authorization.

### Pushes — REQUIRE Matt-explicit-authorization

Push to remote remains Matt-explicit-authorization per ADR-006 read-only-by-default external-systems rule. EXCEPTION: per-workstream push-pattern can be established by Matt authorization (e.g., "push pattern established for this cycle; push after each wave completes" = auto-push for that cycle).

#### ⚑ ACTIVE PUSH PATTERN — Step-2 VFX-archetype build wave (Matt authorization, 2026-08-24: *"push as you go"*)

**Status: LIVE.** For the remainder of the **Step-2 build wave** (T-A archetype minting: tranche 2 and the T2/T3 tranches that follow), **push is authorized as work lands** — no per-push ask. KR pushes as each gate closes; specialists' committed in-scope work is carried out with it.

**Recorded here, and not only in the session that received it, because that is what my own conflict rule below requires.** A push posture communicated to one session is not a posture the wave has — the same defect the ruling below was written to close, one turn after writing it. If this pattern is later narrowed or revoked, **the revocation is recorded here too**, not merely spoken.

**Scope boundaries that survive this authorization:**
- It covers **`reincarnated-collaboration` and `reincarnated-engine`** — the two repos this wave writes to. It does not silently extend to `reincarnated-godot`, `reincarnated-demo` or `reincarnated-loadout`; a push there is a fresh ask unless a dispatch says otherwise.
- **The per-dispatch push clause still governs over it** per the conflict rule immediately below. A standing pattern is the wave's *default*, not an override of a narrower instruction.
- It authorizes pushing **already-committed** work. It does not authorize staging untracked files (`git add -A`, capture directories, `.lock` files) into a push — **#62(a)** still binds: verify ~~`git diff --cached --name-status`~~ **`git diff HEAD --name-status -- <the paths you named>`** against what you named.
  ⚑ **INSTRUMENT AMENDED 2026-08-25** per `#62(a)`'s third amendment + **`#75` cl. 6** (jack-ryan, engine `3c2009de` / `a62fd836`). `#62(a)` now mandates `git commit --only <paths>` as the primary staging clause — and **`--only` ships the WORKTREE, not the index.** So `--cached` can report a staged v2 while the commit lands the worktree's v3, and **a tracked path never staged at all is committed anyway, exit 0** (verified by hand, git 2.39.5, scratch repo). The two commands answer **different questions**; only the `HEAD` form answers *"what will this commit contain."* Run both if you like — the `HEAD` form is the one that binds. This line is the standing-law instance of `#75` cl. 6: *a remedy does not inherit its predecessor's instrument.* `#62(a)` changed the mechanism of committing; this check was left pointing at the old one.

  ⚑ **THIRD AMENDMENT, 2026-08-25, ONE HOUR AFTER THE SECOND — the amendment above fixed the PRE-commit check and left the POST-commit check broken. It produced a false alarm within the hour.**

  **`git diff HEAD~1 --name-status` DOES NOT ANSWER *"what did that commit contain."*** With only one commit named, `git diff` compares that commit to the **WORKING TREE** — so it reports every *other* agent's uncommitted edits as though they had ridden along in your commit. On a shared working tree with concurrent agent sessions, that is not an edge case; **it is the normal state.**

  **Verified, scratch repo, git 2.39.5** — `other.txt` dirty and never staged, then `git commit --only mine.txt`:

  | Instrument | Output | Correct? |
  |---|---|---|
  | `git diff HEAD~1 --name-status` | `M mine.txt` · **`M other.txt`** | ❌ names a file the commit does not contain |
  | `git diff HEAD~1 HEAD --name-status` | `M mine.txt` | ✅ |
  | `git show --stat HEAD` | `mine.txt \| 2 +-` · `1 file changed` | ✅ |

  **`git commit --only` is sound and did nothing wrong. The instrument was the defect.**

  **Standing rule — two questions, two commands, neither substitutes for the other:**
  - **BEFORE committing** — *"what WILL this commit contain?"* → ~~`git diff HEAD --name-status -- <the paths you named>`~~ ⚑ **`git status --porcelain -- <the paths you named>`** *(amended below — the `diff` form cannot see a new file)*
  - **AFTER committing** — *"what DID this commit contain?"* → **`git show --stat HEAD`** (or `git diff HEAD~1 HEAD --name-status`, with **both** commits named)

  ⚑ **FOURTH AMENDMENT, 2026-08-25, same session as the second and third — the PRE-commit instrument is BLIND TO NEW FILES. It reported nothing for a file that was about to be committed.**

  **`git diff HEAD` compares the working tree to `HEAD` across TRACKED paths only.** An untracked file is in neither `HEAD` nor the index, so it is not in the diff — **and the command exits 0 with silence.** Verified live, this repo: four paths named, three tracked and one brand-new; the mandated check printed exactly **three rows**. The fourth file was created, real, on disk, and about to ship.

  | Instrument | On a NEW file about to be committed | Correct? |
  |---|---|---|
  | `git diff HEAD --name-status -- <paths>` | **(no output)** | ❌ **omits it entirely, silently, exit 0** |
  | `git status --porcelain -- <paths>` | `?? <path>` | ✅ reports it, and distinguishes `M` from `??` |

  **Both failure directions are live and the second is the dangerous one.** *Under-report*: you conclude a file "isn't really changed" and drop it — recoverable, the work is still on disk. ⚑ *Over-trust*: you read a silent check as *"the commit contains only what I see,"* when it is **the check that cannot see, not the commit that is clean.** **A new file is precisely what you most want a pre-commit check to catch** — it is the one path with no prior review history.

  ⚑ **Fourth instance of ONE shape in a single session** — *an instrument returning cleanly after it stopped answering the question* (the `factory/permissions.py` non-defect · the crop that could not see the aim difference · `git diff HEAD~1` naming a concurrent session's file · this). **And the reflexive sting compounds: this is the third consecutive amendment to this same block, and each fixed the half of the instrument that had just embarrassed it while leaving the other half un-derived.** The second amendment fixed the pre-commit check's **ref**. The third fixed the post-commit check's **ref**. ⚑ **Neither asked what either command's DOMAIN was** — and `git diff`'s domain has always been *tracked paths*: documented, unchanged, unread.

  **`git status --porcelain -- <paths>` answers the pre-commit question for both classes at once**, and it is what the *"never `git add -A`"* rule above was already implicitly relying on without naming. **Operational note:** `git commit --only` on an untracked path errors rather than silently skipping, so the failure here is a *blind check*, not a lost file — **but the check is the thing that was supposed to make the error unnecessary.**

  **Occasioned by:** KR ran the post-commit form, saw a third file — a live drax session's uncommitted note — and read it as evidence he had swept a concurrent session's work into a push **for the second time in one session**. He had not. `git show --stat HEAD` showed exactly the two files named; the note was still unstaged and untouched. **The near-miss is the finding**: an incident report was minutes from being filed against a correct commit and against a builder who had done nothing.

  **Third instance in one session of one shape** — a mis-matched instrument answering a question it does not address, **returning cleanly, and returning the wrong answer** (cf. the `factory/permissions.py` non-defect; the crop that could not see the aim difference). **The check running is not the check passing.** And the reflexive sting: the defect was in the instrument mandated by *this very line*, one amendment earlier. `#75` cl. 6 says a remedy does not inherit its predecessor's instrument — and the remedy that established cl. 6 then shipped with half of its own instrument un-derived.

- ⚑ **REVOKED BY MATT, 2026-08-25 (recorded per this section's own revocation mandate).** A "third-boundary" rule authored unilaterally by knight-rider on 2026-08-25 (staged into `a7bcd4ee`, refined at `aa973115`; never Matt-ratified) stood here: it forbade any push that would carry another workstream's commits, converting Matt's standing push authorization into a per-workstream veto — in practice letting any autonomous run's unpushed commits hold the shared `main` hostage (jack-ryan's #78/#80 mints sat un-releasable under 17 KC2-run commits for a day). **Matt's ruling (verbatim intent): pushes are NOT to be de-authorized per autonomous run; the rule is deleted completely.** The posture now in force: **a Matt push authorization (standing pattern or explicit word) covers the BRANCH state being pushed — sealed, committed work from any seam rides along as ancestors; autonomous runs do not acquire a push veto over `main` by committing to it.** A conductor who genuinely needs commits withheld from `origin` must use a branch, not an embargo on the shared trunk. (Full deleted text in git history at `aa973115` if lineage is ever needed.)

⚠ **Operational note, recorded because it nearly bit:** `Bash` working directory **persists between calls**. A `cd ~/Games/reincarnated-engine` in one call silently retargets a later bare `git push origin main`. **Use `git -C <path>` for every cross-repo git operation** rather than relying on inherited cwd. Caught 2026-08-24 by verifying the push output against the repo I believed I was in; the push was authorized either way, but the label was wrong, and a wrong label on a correct action is how the next one becomes a wrong action.

⚑ **SECOND FACE, 2026-08-25 — and the note above does not prepare you for it.** The same drift fired again in the opposite direction: after a `cd ~/Games/reincarnated-engine`, later bare `git` calls ran against the engine repo, and their **entirely correct** output — no `agentic_orchestration/knight-rider/rulings/` directory, no commit `20dfcc64` — read as **a ruling and a commit having vanished.** Effort went into a disappearance that had not happened. **So the hazard is not only "a wrong label on a correct action"; it is equally "a correct reading of the wrong repo, presenting as a FALSE ALARM."** The first face corrupts an ACTION; the second corrupts a DIAGNOSIS — **and the second is harder to catch, because the evidence looks like a genuine problem and invites you to start repairing it.** The fix is identical and costs one call: **`git -C <path>` on every cross-repo git operation, and `pwd` as the FIRST move whenever a git result surprises you** — before forming any hypothesis about what it means.

#### Conflict rule — a standing push-pattern vs a per-dispatch push clause (knight-rider ruling, 2026-08-24)

**Occasioned by:** jack-ryan Gate-2 ESCALATE, `agentic_orchestration/qa/findings/2026-08-24-step2-first-landings.md` § ESCALATE. **Two drax sessions eight hours apart received opposite push instructions on the same repo in the same wave.** The first flagged the conflict, resolved conservatively (pushed nothing), and routed the escalation. The second received the opposite instruction and pushed, carrying the first session's commit out to `origin` as an ancestor. **No unrecorded actor, no unilateral push — but the escalation was never answered. It was mooted.** An escalation that dies by supersession rather than by ruling is Discipline #73 one level up: the state changed and the record did not follow.

**The ruling, in two clauses:**

1. **The per-dispatch push clause GOVERNS over a standing workstream push-pattern.** Narrower and more recent wins. **drax reasoned exactly this way and he was right** — the ruling ratifies his call rather than correcting it. A dispatch is the instrument by which a wave's general posture is specialized for one piece of work; if the standing pattern silently overrode it, the per-dispatch clause could never mean anything.

2. **The defect was NOT the conflict — it was that knight-rider changed the instruction mid-wave without recording the change against the wave.** So: **when KR alters a wave's push posture after dispatches are already in flight, KR records the change in the wave's run-state or charter, not only in the session that receives it.** A posture communicated to one session is not a posture the wave has. Same failure family as a completion record filed in `AGENT_STATE.md` while the dispatch header still reads PENDING — **the work is right and the record does not carry it.**

**Corollary on mooted escalations:** an escalation overtaken by events still requires a disposition. *"Resolved by supersession"* is a legitimate disposition and takes one line; **silence is not.** The agent who raised it does not learn whether their judgment was correct, which is the part that compounds — drax's conservative call was the right one and nothing in the record said so until a QA gate reconstructed it eight hours later.

### What anti-patterns this addendum retires

The following patterns are EXPLICITLY ANTI-PATTERNS per this addendum (originally surfaced as knight-rider over-asking behavioral bug):
- "Awaiting your direction on (1)+(2)+(3) before firing" for items where (1) and (2) are clearly in-scope orchestration / seam decisions
- "Awaiting your 'commit + push' go" for routine work-products of authorized cycle work (commit auto-fires; push asks)
- "Confirm sequence to proceed" for items that are seam-owner's scope per hive-mind decision-routing directive (Matt 2026-05-23)
- **Per-task confirmation requests during session-start protocol execution** — session-start protocol items (read ground-state, read role-def, read in-flight dispatches, read own notes) are NEVER permission-gated; they fire as part of the agent's normal session-start discipline. Asking "should I read X?" is anti-pattern.

### Composition with hive-mind decision-routing (Matt 2026-05-23 verbatim)

This addendum composes with hive-mind decision-routing: seam-owners decide in-scope work AND auto-commit its work-products. Matt is LAST-resort escalation for (a) decisions exceeding seam authority per ADR-002 tiered approval, (b) push-to-remote (default), (c) scope-amendment.

### Authority

This addendum is authoritative per Matt 2026-05-25 directive to resolve recurring knight-rider over-asking behavioral bug. Supersedes strict-interpretation of Claude Code system-default commit rule WITHIN this project's multi-agent context. Does NOT affect single-agent Claude Code sessions outside this project.
