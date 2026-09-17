# Finding — 2026-09-17 — Run C-6 (the Necromancer) charter v1.1 (Gate-1, pre-GO)

**Reviewer:** jack-ryan (DESIGN-MODE, Gate-1)
**Verdict:** **BLOCK — narrow.** 2 BLOCK · 10 WARN · 6 INFO. Neither BLOCK is a design objection; both are scope-and-record defects with named one-paragraph edits, and neither needs Matt.
**Target:** `agentic_orchestration/gandalf/notes/2026-09-17-necromancer-run-C-6-charter.md` v1.1 (`sha256[:12] cf650a57ecd1`, 77 lines) · ledger `astra_test_01/burst/runs/C-6/ledger.json` (R-C6-0…5, `M-C6-P0-FORKS`) · account `agentic_orchestration/gandalf/notes/2026-09-17-c6-account.md`
**Author under review:** gandalf (ARCHITECT → RUN-CONDUCTOR on GO)
**Principles applied:** 1 (math-before-code) · 2 (smoke-gate) · 3 (cross-seam impact) · 4 (decisions-log as truth) · 5 (severity matters)
**Pattern / disciplines cited:** desirable-run-pattern § 1, § 2 el. 1/2/4/5, § 4 (halt taxonomy), § 6.1 (coverage-before-accuracy), § 6.2 (owner-eye checkpoints), § 6.3 (rubric law) · Disciplines #62(a), #63, #73, #75 cl. 6, #80 · ADR-002, ADR-004, ADR-006 · CLAUDE.md commit-discipline amendments 3 + 4

---

## 0. Verdict in one paragraph

This is a good charter and a markedly better ARCHITECT pass than the lane's precedent: the forks are fully drained, the deviations from C-3 are named in a table rather than left to be discovered, the fallbacks are C-3's verbatim, and the § 4 P4 self-correction on `oracle/staff_tip.py` is exactly the #75 cl. 6 shape — *a remedy inheriting its predecessor's instrument* — caught by the author **before** it fired rather than by me afterwards. I verified that correction and it is accurate to the byte. What the charter has not reckoned with is that it is the first run in this lane to execute **on a substrate its owner is actively rewriting**, and § 1 is written as though that were not true. **BLOCK-A: § 1 is titled "frozen at launch" and the tool tree is not frozen — C-5 re-froze the MANIFEST twelve times in five hours today, the conductor's own pin is already one freeze stale, and `export/godot_import.py` (the exporter C-6's P5 predicate depends on) is among the files that moved.** **BLOCK-B: § 2 predicate 3 and § 4 P4 adopt "the far tip along the facing" as the socket rule ninety minutes after C-5's conductor falsified that rule in three of eight directions and briefed its replacement with the clause "never to the facing rule" — and neither the old rule nor its replacement transfers to a scythe, whose release socket the charter defines as a point on a concave arc, not an endpoint.** Both are fixable in wording plus one conductor decision. The ten WARNs are led by two orderings that matter under F7's no-cap posture: the turnaround that feeds every Grok clip is explicitly *not* a gate, and the Grok balance — which killed C-3 at a 402 — is unverified until 42 images have already been spent.

---

## 1. The six questions, answered

**1. Bounded substrate — is everything frozen and enumerable at launch?** **No, and it is demonstrable rather than theoretical.** See BLOCK-A. The C-5 staged-project clause is a *separate and lesser* question and I judge it **defensible in principle, under-specified as written** (WARN-7): a substrate item consumed once, at the end, with its version recorded, is a legitimate reasoning-boundary — but the charter says "the latest… (v40 at this writing)" where the account says "pin `cliffside_v40`", `cliffside_v41` already exists, and no rule makes a P5 failure attributable between the necro's data and C-5's scene changes. That is fixable in two clauses. The **tool tree** is the leak, not the scene.

**2. Decidable target-state — do the five predicates measure § 0's intent?** All five are checkable in-run: yes. Do they measure the intent sentence: **partly.** § 0 makes three claims — (i) a complete 40-cell matrix in the cliffside scene, (ii) *Matt can walk him through the clearing and cast at the dummies on the Mac*, (iii) *the character lane is proven repeatable*. Predicates 1/2/3/5 serve (i). Predicate 4 is the only one pointed at (ii) and it is **headless import + one cast, in one direction**. **What falls out, named:** *walking* — nothing exercises movement, the input map, the state machine, or the eight directions resolving from an input vector, all of which C-3's own charter carried and this one drops; *repeatability* — no predicate measures it at all; *band coverage* — predicate 2 reads as coverage and covers at most 16 of 40 cells (WARN-4); *the Mac walkthrough* — Matt's eye, correctly, but then the run may not call predicate 4 "playable". This is § 6.3 rubric law: decidability bought by predicate-narrowing, on a run whose intent sentence is **more** ambitious than C-3's while its predicates are **narrower**. WARN-5 carries the edits.

**3. Fork drainage — does any OPEN Matt-gated fork remain?** **On the run's production path, no** — F1–F7 are ruled, the ARCHITECT table is well-formed, and its GATED and reasoning-boundary rows are correctly classed. The claim *"No OPEN Matt-gated fork remains"* is nonetheless **slightly wider than the evidence**: `canonical/matt_decision_needed/README.md` Q78 (b)–(g) is parked with the re-surface trigger *"the character lane resuming on a new character"* — **that trigger has now fired**. Two of its rows touch C-6: **(b)** whose recommendation was *"top up, then 'resume grok' … and set a clip budget that counts cost"* — F2(a) un-shelves Grok, F7 declines the budget, and no record says the top-up happened (WARN-2); and **(f)** the Keeper matrix verdict, still unruled, which § 0's *"proven repeatable"* leans on (INFO-5). Neither blocks P0. Say so precisely rather than "none".

**4. Concurrency law — is § 7 sufficient?** **No — it is sound in its clauses and insufficient in its direction.** § 7 binds C-6 and binds nothing else: it forbids C-6 from changing tools but does not stop the tools changing under C-6 (BLOCK-A); its memory instrument already produced one false positive that the conductor resolved by hand, is blind to a foreground headless Godot, and has no reciprocal obligation on C-5 (WARN-6); `runs/C-3/**` is consumed by C-6 and written by a live C-5 burst with no declared owner (WARN-8); the disk figure is stale with no HALT floor (WARN-9). A concurrency law recorded in one of two concurrent runs is the CLAUDE.md conflict-rule defect one level up — *a posture communicated to one session is not a posture the wave has.* Git discipline (§ 7.4) is the best in the lane and I credit it (INFO-2).

**5. Is "conductor script, not lane code" a clean line?** **Clean on ownership; not clean on instrument discipline — it needs a stated rule.** As an ownership call it is correct and I endorse it: no TOOLING burst, no MANIFEST touch, no C-5 tool edited, § 7.1 respected exactly. But the script in question is a **measurement estimator**, and my C-3 Gate-2 item 4 raised precisely this class (untested, unfrozen, absent from MANIFEST, setting frame selection for 12 of 38 cells) with a next-lap TOOLING action that is **still undischarged** and which § 7.1 forbids C-6 from discharging. C-6's case is one degree worse than C-3's in one respect: C-3's scripts selected *frames*; this one produces coordinates that land in `sockets_v2.json`, a durable artefact the exporter reads and C-5's VFX erupt from. WARN-10 carries the rule text.

**6. Anything else before GO?** BLOCK-B, and the two orderings in WARN-1 and WARN-2.

---

## 2. BLOCK findings

### BLOCK-A — § 1 is titled "frozen at launch"; the tool tree is being re-frozen roughly twice an hour, the pin is already stale, and the exporter P5 depends on is one of the moving files

**What I found.** The account pins `MANIFEST.sha256` at start = `c8745186…2fb64d`. That value is the MANIFEST as of commit `f3edcbda` (2026-09-16 21:05). The working tree now reads `560e6205…` — commit `d4a701f0` (21:33), C-5's FL-5 freeze, **28 minutes later and before this Gate-1 completes.** The twelve most recent commits touching the MANIFEST:

| commit | time | MANIFEST sha12 |
|---|---|---|
| `d4a701f0` | 21:33 | `560e62056be1` ← now |
| `f3edcbda` | 21:05 | `c87451863398` ← C-6's pin |
| `4e1e01f7` | 20:23 | `f41a750d28b5` |
| `44809931` | 19:55 | `245b8b78660a` |
| `a58a3b72` | 19:31 | `40200567d379` |
| `9ef2a5fb` | 19:12 | `fb7e62fb1e06` |
| `80cea956` | 18:40 | `75d9c034cfdd` |
| `51170963` | 18:17 | `ed8acae2ea1a` |
| `7de058bc` | 17:34 | `a21b15884ee4` |
| `df45cda8` | 17:09 | `62aee65ea0fe` |
| `79b61ec4` | 16:42 | `ac13eeed7a7d` |
| `8961a6d8` | 16:27 | `5d539fadc3bf` |

**Twelve freezes in five hours and six minutes.** Which paths moved, pin → now: `export/effect_kit.py`, **`export/godot_import.py`**, `tests/test_effect_kit.py`, `tests/test_godot_import.py`, `tests/test_vfx_picker.py`, three `fixtures/fl1b/*`. Across the whole day the same set plus `SPEC.md`. `export/godot_import.py` is the T3f exporter — the instrument of **predicate 4**, the one that runs `--cells runs/C-6/cells --sockets runs/C-6/sockets_v2.json`. FL-5b, briefed at `e40aa076` and not yet landed, reads it again and realigns `tests/test_godot_import.py`.

**Why BLOCK.** § 1's heading makes a claim the substrate does not support, and pattern § 1's test is explicit: *"you can count it, list it, and diff it"* — you cannot diff at launch a tree that will be rewritten forty times before P6. C-3's method was *"instrument before candidate"* with a freeze and a re-freeze after T3f; C-6 correctly declines to re-freeze (§ 7.1 is right) and replaces the freeze with nothing. The consequence is an **attribution hole**, not a crash: a cast cell cut in wave 1 and one cut in wave 6 may come from different tools, and a P5 export failure is unattributable between the necro's data, the conductor's blade-tip script, and C-5's exporter edits. That is the § 0 question itself — *is the character lane repeatable* — measured with a ruler that changes length during the measurement. I am also not asking C-5 to stop; the fix is recording and scoping, entirely inside C-6.

**The charter edit that clears it** — replace § 1's "Lane tools (frozen)" row and add one clause to § 7:

1. **Rename the § 1 row** from *frozen* to **"Lane tools — C-5-owned, live; pinned by sha at every wave, not at launch"**, and **enumerate the consumed subset** rather than the whole tree: the T3a–T3f cut / matte / bands / encode set, `oracle/staff_tip.py`, and `export/godot_import.py`. C-6 consumes ~8 paths, not 24,995 bytes of manifest.
2. **Every wave's ledger entry records the MANIFEST sha in force at that wave** (one line in `cl.py`; R-C6-6 records the launch sha as already planned).
3. **State the disposition rule:** a mid-run change to a **consumed** path is a ledgered event with a named disposition — either the cells produced under the prior sha are re-cut, or the sha boundary is recorded as an attribution boundary and surfaced in `matrix.html` per cell. Silence is not a disposition.
4. **P5 runs once, against one recorded sha**, and predicate 4 names it. If `export/godot_import.py` moves after P5, that is a C-7 finding, not a re-run.

---

### BLOCK-B — § 2 predicate 3 and § 4 P4 adopt a socket rule that its owner falsified ninety minutes earlier, and neither that rule nor its replacement fits a scythe

**What I found.** § 2 predicate 3: *"the **scythe-blade release socket** (the blade's inner curve), derived by the **FL-1a/FL-5 rule (the far tip along the facing)**."* § 4 P4: *"one-shot landmarks for cast = the **blade tip** … (topmost alpha extent / far-tip rule)."*

`runs/C-5/ledger.json`, **F-C5-41**, ts `2026-09-16T21:34:45`:

> *"The far-tip-along-facing rule picks the WRONG END of the staff in three directions: S lands on the belt/hands … SW lands on the butt end behind the caster … W lands on the lower end. N/NE/NW/E/SE look right."*

And `briefs/C-5/FL-5b.task.json`, the replacement, states the retirement in terms: *"where both ends are cold (no ferrule visible) fall back to the end FARTHEST FROM THE HANDS' centroid … **never to the facing rule**."* FL-5b is **briefed, not landed.**

**Three separate defects sit on top of each other.**

- **(a) The cited rule is falsified, 3/8.** The charter names FL-5 by name, as a predicate, after its owner recorded the defect. Preregistration (pattern § 5 safety 1) pinning a known-broken instrument is worse than pinning none.
- **(b) The replacement does not transfer.** FL-5b's discriminator is a **brass ferrule** — a warm-bright pixel cluster within 14 px of the staff's tip end. A scythe has a blade at one end and a butt-spike at the other; it has no ferrule, and its *warm-bright* cluster, if any, is the blade's edge highlight running the whole arc rather than a 14-px cap. FL-5b's cold-fallback (farthest from the hands' centroid) is also wrong here: the charter says *"the haft crosses the torso"* with **both hands on it**, so the centroid sits mid-haft and the butt-spike may be farther than the blade in several facings.
- **(c) The charter's own two methods are not the same method, and neither yields the defined socket.** § 4 P4 ORs *"topmost alpha extent"* with *"far-tip rule"* on a slash. For a scythe held **blade up-left across the torso**, these disagree in most of the eight directions — and the socket the charter actually defines, *"the blade's **inner curve**"*, is a point on a **concave arc**, which is not an extremum of anything. No endpoint rule, facing or ferrule or topmost, returns it.

**Why BLOCK and not WARN.** It is one of five predicates; it feeds `sockets_v2.json`, a durable artefact read by `export/godot_import.py` and used as the eruption origin by C-5's VFX — so a wrong socket is cross-seam, not conductor-internal (Principle 3). And it is the exact defect C-5 is mid-repair on, about to be re-minted on a second character. Matt's own words on the staff case (R-C5-122) were *"Projectile must emanate from the TIP OF THE STAFF"* — the equivalent miss on the necro is three directions of fire erupting from his hip.

**The charter edit that clears it.** § 2.3, § 1's "Cast socket" row and § 4 P4 name **one** C-6 rule, and it should be neither staff rule:

> **The release socket is the blade's inner curve, fixed per direction on the audited marked sheet (conductor eye), from a script-proposed candidate.** The conductor script's role is to *propose* — the topmost alpha extent of the blade mass, with the haft axis excluded — and to render the marked sheet; **the sheet is the authority and the eight coordinates are conductor-authored data**, exactly as § 1's "Cast socket" row already says. No FL-5 or FL-5b citation survives in C-6's derivation; FL-5b is cited only as the reason the staff rules were not reused.

Add one clause: **C-6's `sockets_v2.json` is written against the schema `export/godot_import.py` holds at P5, re-read at P5** — FL-5b adds `release_socket_rule` and rewrites `runs/C-3/sockets_v2.json`; today's schema is `{version, canvas, cells.cast_<dir>.{sockets[8], measurements[]}, notes}` and it is about to gain a field.

---

## 3. WARN findings — each with the edit that clears it

**WARN-1 — the turnaround that seeds every Grok clip is explicitly *not* a gate, on a run whose binding budget is Grok.** § 6: *"the P2 turnaround contact sheet (**report, not gate** — fallback proceeds flagged)"*. So 40 clips — the scarce, uncapped, externally-metered resource — are generated from eight rest frames Matt has never looked at. C-3 had the same shape **and a 45-clip budget**; F7 removes the cap, which makes a bad turnaround able to consume the whole weekly allowance before anyone sees a frame. Pattern § 6.2 was written from exactly this: *"when the run's output is a watched surface, the owner's eye is … an instrument of record"*, and both KIT-FIDELITY catches were Matt's, mid-stream, after the run's own gates said green.
**Edit:** § 4 P2 and § 6 — *"Matt's eye on the P2 contact sheet is a **GATE**: P3 does not fire until he has looked, or 24 h pass with no red flag (conductor proceeds, ledgered)."* One packet and one pause.

**WARN-2 — the Grok balance is unverified, C-3 died on it, and the queue's own remedy has no record of being performed.** C-3 halted at `API error (status 402): Grok Build usage balance exhausted`. Q78 (b) recommends *"top up, then 'resume grok'"*; nothing records a top-up; `grok_calls` is `[]`; F7 makes an allowance of **unknown size** the sole constraint. P3 is the first call, and it comes after P2 has spent ≤ 42 images and ~21 bursts.
**Edit:** § 4 P0 gains *"a one-call Grok liveness probe (cheapest clip, discarded) before P1 — a 402 here is the F7 external-state HALT with nothing stranded; record any printed allowance figure (`costUsdTicks` was captured at C-3) in `grok_calls[0]`."* Cost: one clip. Also route the top-up question to Matt (§ 5 below).

**WARN-3 — F7's HALT instrument is a C-3 script that does not halt, and both candidates are hard-wired to C-3.** § 1 lists `clips_seq*.sh`. `clips_seq.sh` counts to **three** consecutive failures before breaking — my C-3 INFO and its action. `clips_seq2.sh` **was** fixed under R-C3-24 (stops on first failure, greps `402|balance|Error`) — so the remedy exists, unnamed. But **both** hard-code C-3's session scratchpad UUID `423f7949-3b86-43e3-82bd-845c71630541` and `~/astra-burst/grok/C-3/`, and **neither writes a HALT packet** — they break the loop and print `SEQ DONE`, which reads identical to success. Discipline #75 cl. 6: *a remedy does not inherit its predecessor's instrument.*
**Edit:** § 1 and § 4 P3 name **`clips_seq2.sh` only**, re-pointed to C-6's scratchpad and `~/astra-burst/grok/C-6/`, and add *"a certain-cause failure (402 / out-of-budget) writes the HALT packet and stops the phase; a loop break is not a HALT."*

**WARN-4 — predicate 2 reads as coverage and covers at most 16 of 40 cells; 12 in practice.** `oracle/bands_proposed.json` holds exactly five rows: `idle_relaxed_video`, `walk_E_video`, `walk_W_video`, `walk_N_proposal`, `walk_S_proposal`. **There are no run, jump or cast rows**, and F3(a) forbids minting any in-run. So 24 cells have no band to report against, and walk NE/NW/SE/SW have no facing row — leaving ~12 banded cells of 40. This is my own C-3 Gate-2 WARN-5(a) (*"22 of 38 complete cells have no proposed band"*) carried forward un-named, which is the § 6.3 failure: a predicate that looks like coverage and is a sliver. #63.
**Edit:** § 2 predicate 2 states the covered set — *"idle ×8 and walk E/W/N/S against the five Keeper rows; the remaining ~28 cells carry numbers with **no** proposed band, and say so on the row"* — and § 3's deviation table gains a "band coverage" line.

**WARN-5 — § 2 does not measure two of § 0's three intent clauses.** Per Q2 above.
**Edit, three clauses:** (i) extend predicate 4 — *"and a headless movement probe asserts each of the eight directions plays its walk cell from the input vector, and the jump input plays the jump cell"* (`probe_move.gd` / `probe_cliff.gd` already exist in `runs/C-3/conductor_scripts/`); (ii) **add predicate 6** — *"`runs/C-6/repeatability.json` records images / bursts / Grok clips / wall-clock / fallback-count / conductor-intervention-count against C-3's, since that is what § 0's 'proven repeatable' means"*; (iii) add the fell-out sentence to § 2 — *"the Mac walkthrough is Matt's eye, not a predicate; the run does not claim 'playable' on predicate 4 alone."*

**WARN-6 — § 7 binds one of two concurrent runs, and its memory instrument has a known false positive.** § 7.2 scrapes `c5_*.log` for `WAVE START` without `WAVE DONE`; the account records that this **already misfired** (`c5_bl1a.log` open, closed by `c5_bl1a_r1.log` — *"stale record, not live"*). It is also blind to a headless Godot launched in the foreground outside the wave scripts, and C-5 carries no reciprocal duty toward C-6.
**Edit:** replace the log-scrape with a shared advisory lock — `astra_test_01/burst/.heavy.lock` (`flock`, holding pid + run + ts; a dead pid is stale by definition) — taken by **either** conductor before headless Godot or the test suite; and **file § 7 with C-5's conductor so it is recorded in C-5's ledger too.** A two-sided law recorded on one side is the CLAUDE.md conflict-rule defect.

**WARN-7 — the P5 scene: charter and account disagree, and the named version is already stale.** Charter § 1: *"the latest `runs/C-5/cliffside_v<N>` staged by C-5 (v40 at this writing)"*. Account: *"pin `cliffside_v40` at GO; if C-5 stages later, use the latest staged and record the version."* `runs/C-5/cliffside_v41` **exists on disk now.** (Same shape as my C-5 BLOCK-A, far milder: charter and record disagreeing about how bound a decision is.)
**Edit:** § 1's "Playable scene" row reads what the account reads — **pinned at GO, recorded in R-C6-6** — plus: *"predicate 4 is evaluated against the pinned version; if a later staged project is used at P5, the same probe is re-run against the pinned one as a control, so a failure is attributable."*

**WARN-8 — `runs/C-3/**` has no declared owner while both runs touch it.** C-6 § 1 consumes `runs/C-3/cells_v7/*` (41 dirs, verified), `oracle/bands_from_exemplar.py` outputs and `runs/C-3/conductor_scripts/`; C-5's FL-5b brief authorizes an Astra burst to **write `runs/C-3/sockets_v2.json`**.
**Edit:** one line in § 7 — *"`runs/C-3/**` is read-only for C-6; the consumed paths (`cells_v7/`, the four conductor scripts copied, `bands_proposed.json`) are recorded by sha256 in R-C6-6."*

**WARN-9 — the disk figure is stale and there is no HALT floor.** § 7.5 says *"~45 GB free at handover"*; the account measured 39 GB; `df -h /` now reads **37 GB**, with `astra_test_01/burst` at 21 GB (`runs/C-5` 13 GB and growing, `runs/C-3` 6.9 GB for the Keeper's 40 cells, **39 `cliffside_v*` trees** and nobody pruning). C-6 should be expected to add C-3-scale footprint. Free space falling ~2 GB/h under two runs is external-state danger in pattern § 4's sense with no declared floor.
**Edit:** § 7.5 — *"HALT if free space < 10 GB; purge each wave's Grok frame dumps at the close of that wave, not 'after cutting'; `df -h /` recorded in each wave's ledger line."*

**WARN-10 — the conductor-script line needs the rule stated, and it inherits an undischarged debt.** Per Q5 above. My C-3 Gate-2 item 4 action — *"reproduce the tip, settle and cast-key rules under test and freeze; re-cut the 12 cells and diff them against the conductor indices"* — is open, and § 7.1 forbids C-6 from being the lap that discharges it. That is a legitimate scoping call; it is not legitimate to inherit it silently.
**Edit:** § 8 gains the rule — *"a conductor script may **propose or select**; any number it produces that lands in a durable artefact consumed outside the conductor's own reasoning is marked `conductor_derived: true`, the script's sha256 is recorded in the ledger, and the audited sheet is the authority"* — and § 3's deviation table or § 8 records that the C-3 Gate-2 item-4 TOOLING debt remains open and is **not** discharged by C-6.

---

## 4. INFO findings

- **INFO-1 — the § 4 P4 self-correction is right, and I verified it.** `oracle/staff_tip.py` exists, is in the MANIFEST (`1324d5db…`) with `tests/test_staff_tip.py`, and exposes exactly one entry point, `tip(rgba)` — no landmark parameter, no argparse. v1.0's *"re-pointed by parameter"* was wrong and v1.1 is right. **Credit:** this is #75 cl. 6 caught by the author before it fired, which is the first time in this lane a charter has done that to itself.
- **INFO-2 — § 7.4 names the *correct* pre-commit instrument.** *"pre-commit check `git status --porcelain -- <paths>`"* is CLAUDE.md's **fourth amendment** form — the one that can see a new file, which `git diff HEAD` cannot. First charter in the lane to carry it. **One addition:** the post-commit form is missing — add *"after committing, `git show --stat HEAD`"* (third amendment; `git diff HEAD~1` alone reports a concurrent session's dirty files as though they rode along, and there are two live sessions on this tree). #62(a).
- **INFO-3 — the register citation is half-supported.** § 1 cites `CS-parallax-in-v10/walkable.json` for *"151-px figure = 14 %"*. The file gives `"figure_height_px": 151` on a 5376×4096 canvas; 151/4096 = 3.7 %. The **14 %** is against the 1080 viewport — correct, and the account explains it, but the charter cites one source for two facts and only one is in it. Cite both. Relatedly, `M-C6-N3-CAM` records **146 px (13.5 %)** for the CS-props-v23 prop placement; name **151** as the cell contract so the two numbers do not get confused downstream.
- **INFO-4 — predicate 1 is stricter than C-3's and may be unreachable.** *"exists for all 40 cells"*, with fallbacks listed separately. C-3 said it explicitly: *"any cell that cannot complete carries its reason and its fallback taken — that is a complete cell"*, and C-3 exited **38/40**. Restate C-3's sentence in § 2, or 40/40 is a predicate the run can fail while doing everything right.
- **INFO-5 — Q78 (f), the Keeper matrix verdict, is unruled and its trigger has fired.** Not on C-6's production path; it is what § 0's *"the character lane is proven repeatable"* leans on. Worth one line in § 0 or § 6 saying repeatability is a **C-7** claim, not a C-6 exit.
- **INFO-6 — § 7.6 is vestigial under F7.** *"image caps reserve against C-6's own cap only"* — there is no cap; `images_cap` is the 999999 sentinel. Harmless; say "counted and reported" to match § 1.

---

## 5. Action summary

**gandalf (charter edits, all pre-GO, none needing Matt):**
- [ ] **BLOCK-A** — § 1 lane-tools row: live-not-frozen, consumed subset enumerated, per-wave sha recording, mid-run-change disposition rule, P5 against one recorded sha.
- [ ] **BLOCK-B** — § 1 / § 2.3 / § 4 P4: one C-6 socket rule (blade inner curve, sheet-authoritative, script proposes); drop the FL-5 citation; re-read the exporter's socket schema at P5.
- [ ] WARN-1 P2 contact sheet becomes a gate · WARN-2 P0 Grok liveness probe · WARN-3 `clips_seq2.sh` only, re-pointed, HALT packet on certain-cause · WARN-4 state band coverage · WARN-5 movement probe + predicate 6 + fell-out sentence · WARN-6 shared `.heavy.lock`, § 7 filed with C-5 · WARN-7 pin v40 + control re-run · WARN-8 `runs/C-3/**` read-only, shas in R-C6-6 · WARN-9 disk floor 10 GB · WARN-10 conductor-script rule + C-3 debt named.
- [ ] INFO-2 add `git show --stat HEAD` · INFO-3 cite both sources, name 151 · INFO-4 restate C-3's complete-cell sentence · INFO-5 repeatability is a C-7 claim · INFO-6 drop the cap clause.

**Matt (2 items, neither blocking P0–P2):**
- [ ] **Grok top-up / allowance.** Q78 (b)'s *"top up, then resume grok"* has no record of being performed; F7 makes the allowance the only constraint and its size is unknown. Only you can answer whether the balance is live. *(WARN-2 — the P0 probe makes this cheap either way.)*
- [ ] **Your eye at P2.** WARN-1 asks to move one of your checkpoints earlier — the turnaround contact sheet before the first Grok clip. That is a change to your declared interface (§ 6), so it is yours to accept.

**ADR-002 approval authority.** Every gandalf item above is charter wording, record correction or within-lane conductor tooling — **mine to approve directly**, and I approve them on execution. Nothing here is a cross-seam schema change (C-6 *consumes* the sockets schema; it does not alter it) and nothing needs a new ADR.

**Gate-1 verdict: BLOCK — narrow.** Both BLOCKs are scope-and-record defects with named edits; neither changes the design, neither needs Matt, and the run can be GO within one editing pass. On BLOCK-A's four clauses and BLOCK-B's one rule, **this charter is GO.** The fork drainage is complete, the deviation table is the clearest this lane has produced, and the P4 self-correction is the kind of catch that makes a Gate-1 cheaper rather than more expensive.

---

## 6. References

**Under review**
- `agentic_orchestration/gandalf/notes/2026-09-17-necromancer-run-C-6-charter.md` (v1.1, `cf650a57ecd1`)
- `astra_test_01/burst/runs/C-6/ledger.json` · `agentic_orchestration/gandalf/notes/2026-09-17-c6-account.md`

**Evidence inspected**
- `astra_test_01/burst/MANIFEST.sha256` (working tree `560e6205…`; twelve freeze commits `8961a6d8`…`d4a701f0`)
- `astra_test_01/burst/runs/C-5/ledger.json` (R-C5-121…126; **F-C5-41**) · `astra_test_01/burst/briefs/C-5/FL-5b.task.json` · commit `e40aa076`
- `astra_test_01/burst/oracle/staff_tip.py` · `astra_test_01/burst/oracle/bands_proposed.json` (five rows) · `astra_test_01/burst/runs/C-3/sockets_v2.json`
- `astra_test_01/burst/runs/C-3/conductor_scripts/{clips_seq.sh, clips_seq2.sh, grok_clip.sh}` · `runs/C-3/cells_v7/` (41) · `runs/C-5/cliffside_v40`, `cliffside_v41`, `probe_events.gd`
- `astra_test_01/burst/runs/C-5/artifacts/CS-parallax-in-v10/walkable.json` · `df -h /` (37 GB) · `du -sh` (`burst` 21 G; `runs/C-5` 13 G; `runs/C-3` 6.9 G; 39 `cliffside_v*` trees)

**Law and lineage**
- `agentic_orchestration/operating-procedures/desirable-run-pattern.md` §§ 1–6
- `agentic_orchestration/gandalf/notes/2026-09-13-astra-burst-lane-run-C-3-charter.md`
- `agentic_orchestration/qa/findings/2026-09-13-run-C-3-gate2.md` (items 4, 5; the undischarged TOOLING action)
- `agentic_orchestration/qa/findings/2026-09-15-run-C-5-charter-gate1.md` (format precedent; BLOCK-A shape)
- `canonical/matt_decision_needed/README.md` (Q78 (b)–(g), parked on the character-lane trigger)
- `CLAUDE.md` commit-discipline amendments 3 and 4 · `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` #62(a), #63, #73, #75, #80

— jack-ryan, Gate-1 (DESIGN-MODE), 2026-09-17
