# jack-ryan's four dispositions — captured by record, because he wrote no files, and **one of them is a pre-registered prediction against a run that was still executing when he filed it**

**Filed:** 2026-08-25 (knight-rider), immediately on return.
**Why this file exists:** jack-ryan returned **as text, writing nothing** — invocation constraint. Four dispositions, three corpus amendments escalated to Matt, and one forward-pointer stamp he names as **owed by him and not performed**. Left in a transcript, all of it evaporates at session end. **This is the capture; it is not a ruling of mine, and every disposition below is his.**

---

## ⚑ 0. THE TIME-CRITICAL PART — read this first

jack-ryan **pre-registered a falsifier for his own ruling**, against drax's 3A recapture, **while that recapture was still running.** I verified it was still mid-analysis when the return landed (drax was writing his `#80` emptiness guard, not yet at results), so the pre-registration is **genuine and not post-hoc.** Recording it here timestamps it ahead of the numbers.

> **Prediction:** deltas confined to caster-silhouette overlap → **large on Mob0/1/2, near-zero on Mob3.** `step_concentration` gaps move **« 0.2069.** Verdict direction unchanged in both stages.
>
> **Falsifier, his words:** *"If Mob3 moves materially, my trace is wrong and the seal reverts to PROVISIONAL."*

**drax does not know this prediction exists.** That is *ideal for blinding* — he cannot steer toward it — but it creates one live hazard:

⚑ **If drax's output does not break deltas out PER MOB, the prediction is untestable against what he returns.** I could not tell him to include it: **`SendMessage` is unavailable — ninth confirmation this session, second one TESTED rather than inferred** (`ToolSearch select:SendMessage` → *"No matching deferred tools found"*). The compensating control is unchanged: **file, don't relay.**

**So the standing instruction to whoever reads drax's return:** check for a per-mob breakdown first. If it is absent, **the prediction is not lost and must not be quietly dropped** — his frames are preserved, and the breakdown is a re-analysis over existing captures, not a re-capture. Dropping it silently would be exactly the mooted-escalation failure this project already ruled on once.

**Also note what the recapture is NOW FOR.** Its role changed under this ruling: it is **the known-negative run for jack-ryan's own trace**, not a re-derivation of the verdict. His stated reason is that #75 cl. 2 binds him — *a derivation is not a sensitivity proof.* **drax remains forbidden from ruling; that condition is jack-ryan's and it is now on the record.**

---

## 1. The sealed verdict — **HOLDS.** And he threw out my reasoning while reaching my conclusion.

**L-29(6) and R-1.3 stand, un-re-derived.** Not by seal-inertia — and ⚑ **explicitly NOT by the common-mode argument I offered him.** I had reasoned that the differential survives because the yaw defect appears in both arms and cancels. He did not adopt that. He derived something stronger:

> **The yaw defect is not on the causal path from the artifact to the measured quantity. It is a pure sink — written, rendered, never read.**

His four-link trace, from shipping code:

| # | Link | Reads caster transform? |
|---|---|---|
| 1 | **Region** — `body_disc()` scores **Mob0–Mob3 only**; the caster is emitted separately as `caster{}` and **is not a scored disc** | **No** — a disc carries no orientation term; yaw-invariant by construction |
| 2 | **Signal** — `mean(max(0, Y_on − Y_off))`, `off` = same run, layers hidden, **motion unchanged** | **No** — caster mesh renders identically in both arms, cancels exactly |
| 3 | **Payload placement** — `aim_vector()` from exported `aim_deg`; contacts by world distance | **No** — world-framed end to end |
| 4 | **The yaw itself** — `S2Facing.face_toward(...)` | **Write-only.** Nothing reads it back |

**This matters for how I should have argued.** My framing — *"complete coverage of the wrong subject"* — he calls the right general worry that **does not obtain here**, because the mechanism I invoked (body-anchored effects emitting along body-forward) **requires the payload to be parented to or computed from the body basis**, and on these rows it is computed from `aim_deg`. **The body was 180° wrong and nothing downstream asked it anything.** I reached a correct disposition through an argument he had to replace. **That is a near-miss, not a win** — a common-mode argument would have held only as long as the two arms stayed symmetric, and nothing guaranteed that.

**The one residual he refuses to paper over, and it IS on-path:** the caster travels world −Z through Mob0/1/2, and where its mesh overlaps a disc it **occludes payload pixels** — a humanoid rotated 180° has a different silhouette, which **does not cancel**. Bounded at tens of pixels (caster ≈ 43 px tall against a ≈ 1,520 px disc), same mechanism on both arms, against a class gap of **+0.2069**. Hence the pre-registration in § 0 — Mob3 sits off the travel path at `x = +2.9`, so it is the control.

⚑ **His own self-correction, which he volunteered and which nearly went the other way.** He formed a hypothesis that the `_novfx` control does not control the caster's *motion* — that would have been a **BLOCK on drax's control arm**. He read the code and it is **false**: `novfx` hides layers, `static` disables motion, **independent axes**, caster travels the identical path in both arms. *"drax's control is sound; my hypothesis died on the read."* **Fourth instance this session of `the check running is not the check passing` — this one caught before it left the building.**

### The exposure boundary (his Q2 answer) — and it **corrects his own F-9 narrowing**

Not "every pre-fix capture," not "body-anchored claims." **Per-CLAIM, two entry points and only two.** A claim is exposed iff **(i)** its measurement region is caster-anchored, **or (ii)** its signal's world placement reads the caster transform. Everything else is off-path — **including rows where the caster is plainly visible in frame**, because a visible-but-unread body is a sink.

> ⚑ *"Authoring frame is a property of the ROW. Exposure is a property of the CLAIM."*

F-9 narrowed PENDING-RECAPTURE to *world-framed rows only*. He now rules that axis **correct for deciding which rows the FIX changes and wrong for deciding which CLAIMS are exposed** — Pair 1 is world-framed *and* off-path, so his own narrowing leaves exposed a claim that needs nothing. **A third axis neither of F-9's names, and he calls it his error to correct.** Discharge is mechanical per **#72**: enumerate every sealed verdict over pre-fix captures, name its region anchor and signal placement source, **hit table including zero.**

### Flank 3 gets a name: **`#75` clause 7 — deliberately NOT a new number**

Per his own #58-DECLINED / §75.5 precedent. **cl. 6 and cl. 7 are exact duals**, and splitting them would let a landing satisfy one while violating the other *and believe itself compliant*:

- **cl. 6** — the **instrument** moved under a fixed subject → re-derive the **instrument**
- **cl. 7** — the **subject** moved under a fixed instrument → re-derive the **verdict**

Proposed text, three dispositions: **OFF-PATH** (holds, trace on record) · **ON-PATH-INVARIANT** (holds conditionally — *"the same-mechanism condition is the one that fails"*) · **ON-PATH-UNPROVEN** (→ **PROVISIONAL**, not revoked: keeps authority for planning, loses it for sealing). And the load-bearing sentence:

> **Sealing is not a disposition.** It records that examination ceased and creates **no presumption in the seal's favour**; the burden is on the party asserting the seal holds. **The default for an untraced verdict is PROVISIONAL.**

with drax's founding sentence carried into the corpus: ***"Reproducibility is not validity"*** — a byte-exact reproduction certifies the procedure repeated itself, **and a procedure repeating itself is not evidence the subject was right.**

**The three flanks are now closed:** instrument (`#75`) · gate (`#80`) · **subject (`#75` cl. 7)**.

⚑ **He flags himself:** three rulings into `#75` in two days. *"If a fourth arrives, the right move is to ask whether #75 has become a container rather than a rule."* **Recording it so someone asks.**

---

## 2. The 23-day orphaned regression — **WARN.** Park it; the inventory question gets a clause.

**(a) `census.json` — PARK. Do not commit, do not discard.** Committing writes `energy_label_seen: 0` onto the canonical path, which is **`#63` verbatim** — an *unmeasured* zero promoted to a *measured* zero, on the authority surface. Discarding destroys possible evidence *of* the regression. **Disposition: preserve the worktree version at a distinct quarantine path with an `UNEXPLAINED-REGRESSION` marker; leave the committed version canonical; file 117 → 0 as an open investigation with a named owner.** Nothing lost, nothing bad promoted, and **the tree stops being one `git checkout` from data loss.**

⚑ **drax is ratified explicitly for refusing to dispose of a stranger's work** — *"that was correct and it is recorded here, not left silent."* Owner routing is mine; jack-ryan does not own godot files.

**(b) Standing inventory — YES, and it lands at `#62` clause (c), not a new number.** #62 already governs *parallel same-tree agent hygiene* on the **write** side (what a commit contains); this is the **residue** side (what the tree accumulates) — same discipline, same premise, unaddressed. Proposed: *at session-start and session-close, each agent emits `git status --porcelain` plus mtime for every repo it touched; any path dirty beyond one session boundary is named with an owner or handed back.* **One tool call.** He adopts my framing verbatim as the argument: **every instrument we have watches committed state or declared work, and this was neither.**

## 3. Word collisions — **NO NEW CLAUSE. Both halves already bind.**

- **Author side → `#64`** (referent-binding declaration): *a field whose name does not determine its referent must declare it at the site.* **`terminal` and `census` are both exactly that, and both sites are violations today.**
- **Reader side → `#71`** (join validation before contradiction). Its stated object is a value *difference*; mine was a *dependency* — but the mechanism is identical: **identity inferred from label coincidence rather than independently established.** He reads that as extension, not stretch, and gives it **a founding instance at #71** rather than a number. He calls the H-MC-1 near-miss the cleaner instance *"because you stopped and opened `eor_release.py:61/167/171` instead of asserting."*

**H-MC-1 confirmed NOT implicated, independently.** No read of `tmp/br2watch/measure/census.json` anywhere in `eor_release.py`.

## 4. Unconstructible receipts — **two failures wearing one description. He splits them, and the worse half is his.**

- **(B) Asserting a receipt's VALUE without running it** — *my* `git diff --stat` claim; gandalf's `LINEAGE CLEAN` at a stale ref. **Already covered: `#79` cl. 1** (a number is DERIVED at the moment of writing) **+ `#11`.** No mint. gandalf's is aggravated — a stale-ref verdict is #73-shaped record/state divergence on top.
- **(A) Mandating a receipt that CANNOT BE CONSTRUCTED** — **his**, five sites, four impossible. **This has no home**, and he identifies it as **`#75` cl. 2 one step earlier in time**: cl. 2 binds the author of a *reading*; **nothing binds the author of a *mandate*.** Proposed as an extension of cl. 2, not a number: *a receipt is ordered only after the command that produces it has been run once, on this repo, at this ref, and shown to emit.* **One tool call, and it would have caught all three.**

> *"Mint nothing for item 4. Cite #79 cl. 1 for yours and gandalf's; the cl. 2 extension is mine to land and it convicts me, not you."*

**This closes the thread I opened with the miscount.** gandalf refuted my count (my instance was downstream of his defect, not a fourth peer); jack-ryan now refutes the *category* — the two halves are different failures and my one-line framing collapsed them. **Both critics corrected the same brief from opposite directions and neither needed me to arbitrate.**

---

## 5. What is UNLANDED — tracked here so it does not become #73 in a week

He wrote **no files**. These are owed and outstanding:

| Owed | Owner | Status |
|---|---|---|
| Forward-pointer stamp at head of `qa/findings/2026-08-25-godot-forward-axis-convention.md` (Q2 narrowing **corrected, not superseded**; no back-editing) | jack-ryan | **NOT WRITTEN** — text drafted in his return, captured § 1 above |
| `#75` cl. 7 into `engineering-disciplines.md` | jack-ryan | **ESCALATED to Matt** (ADR-002 process-tier, veto open) |
| `#75` cl. 2 mandate-limb | jack-ryan | **ESCALATED to Matt** |
| `#62` cl. (c) standing dirty-tree inventory | jack-ryan | **ESCALATED to Matt** |
| `census.json` quarantine + named owner | knight-rider routing | **OPEN** — no live BR2-WATCH dispatch to route to; that absence is why it survived 23 days |

**The three escalations are corpus amendments and correctly Matt's.** The dispositions themselves — seal holds, exposure boundary, census park, the #64/#71/#79 citations — **are process-tier and land now under his own authority.**

## Paths he cites

`s2c_onset.py` (`body_disc` :71-76, `added_luma_series` :88-125, `step_concentration` :128-139) · `s2a_stage.gd` :1011-1014, :1042-1045 (the construction that refuted his own hypothesis) · `s2c_dash_attack.gd` (`aim_vector` :273, mover :342, facing-write :354, contacts :404-434) · `harness_logs/s2c_rows12_2026-08-25/render.txt` · `engineering-disciplines.md` (#62 :3002, #63 :3101, #64 :3138, #71 :3457, #72 :3496, #75 :3648, #79 :3897, #80 :3962)

**He loaded no images, staged nothing, pushed nothing.**
