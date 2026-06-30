# Doc-lifecycle governance — 14-scenario stress-test (+ S15 first-run refinement) (lineage record)

> **STATUS:** CURRENT (verdict-class lineage — § 6.1). Cited by `agentic_orchestration/operating-procedures/canonical-doc-format.md § 6` (= the installed skill) as the reasoning behind the doc-lifecycle governance system. Because a canonical skill cites it as source, this note is **evidentiary** per § 6.1 → never auto-pruned.

**Authored:** 2026-06-30
**Author:** gandalf (Pattern-B dialogue with Matt)
**Authority:** Matt 2026-06-30 — *"before I rule on this, please ultra think through a variety of scenarios and agents past or potential future workflows to pre-stress-test the system… Then we can dive into the rulings"* → after the stress-test, *"agreed with all four."*
**Companion:** `canonical-doc-format.md § 6` (the system this validated); `00-ground-state.md` (the three canon homes); `2026-06-30-canonical-reorg-fold-map.md` (the reorg this rides on)

---

## 0. Why this note exists

Matt asked for two new systems — (A) propagation of canonical-doc changes into the current-to-end-state trackers, and (B) auto-pruning of superseded/irrelevant docs and notes — and then required a **stress-test before ruling.** That discipline was correct: the stress-test *changed the design twice* before it was safe to ratify. This note captures the 14 scenarios (each grounded in a **real** artifact already in the tree, not an imagined workflow), what each tested, and the four rulings that survived.

The system's one job: **nothing depends on someone remembering to clean up or to update the trackers.** Propagation and pruning fire on *events*, verified before they fire.

---

## 1. The four ratified rulings (the output)

| # | Ruling | Lives at |
|---|---|---|
| **(a)** | **Total vs partial supersession split.** Total supersession → `git rm` (git is the archive). Partial supersession (the dominant pattern) → banner + fold in place; **never amputate.** | § 6.4 |
| **(b)** | **Auto-prune ceiling.** Auto = event-triggered + reference-verified, never a blind timer. The 4-predicate prune-safe rule; ambiguity → surface-for-ratification; "became irrelevant" *always* surfaces (no detectable event). | § 6.3 |
| **(c)** | **Three note sub-classes.** Evidentiary (cited → never auto-prune) / verdict-recognition (prune on total-supersede + zero citations) / working-memory (the only auto-prunable class). | § 6.1 |
| **(d)** | **Markdown-design-artifact scope only.** Data / code / binary (`.json`, `.csv`, `.py`, `.png`, `.mp4`, `.html`) live under seam-owner lifecycle, out of § 6. | § 6.3 pred. 1 |

Two of these (a, c) are **corrections forced by the stress-test** — see scenarios S1 and S2. Had I ruled before testing, the system would have amputated load-bearing content and dangled a ratified decision.

---

## 2. The 14 scenarios

### Design-changing scenarios (forced a ruling revision)

**S1 — Partial supersession (the correction that produced ruling a).**
Real artifact: `canonical/story/2026-06-13-companion-as-hall-of-heroes-ally-commitment.md`. Under the v2 lexicon, its *isekai / spirit-guide labels* die — but its commitment + mechanics survive and are being folded into the engine spec. My **original** draft rule ("supersession = remove, not banner") would have `git rm`'d it and destroyed live structure. **Revision:** total-vs-partial split. Partial → `STATUS: CURRENT` + `⚠ FRAME PARTIALLY SUPERSEDED` banner, fold in place, leave the tree only when the worklist marks it fully absorbed. *Reconcile, do not amputate.*

**S2 — Evidentiary note cited by decisions-log (the correction that produced ruling c).**
Real artifact: a Phase-2 spot-check note cited in `reincarnated-engine/design/decisions/decisions-log.md` as "load-bearing empirical evidence." My **original** draft rule ("notes are ephemeral; prune on workstream-close") would have deleted the *source* of a ratified decision, dangling the permanent record. **Revision:** three note sub-classes; classify at prune-time by the cross-repo reference check; evidentiary notes are never auto-pruned.

### Validating scenarios (confirmed the system as-designed)

**S3 — Binary / data artifact.** Real: the cycle-14 telemetry `.json` files and the Godot MP4 walkthroughs. A naïve "prune superseded artifacts" sweep could target a stale telemetry dump. **Validated:** predicate 1 (markdown-design-only) excludes them; data/code/binary are seam-owner lifecycle. Out of scope by construction.

**S4 — historical/dead subfolders are gone.** Real: the reorg retired `canonical/historical/` + `canonical/dead/`. A pre-reorg "demote to subfolder" prune model would now write to non-existent dirs. **Validated:** git-is-archive — total supersession removes from the live tree, no subfolder hop. (Reconciled § 1 + § 3.)

**S5 — Tracker row reopened.** Real: B3 season-two-companion, reopened by Matt 2026-06-30 after being "resolved." A delete-on-resolve tracker would have lost it. **Validated:** tracker rows are *resolved, not deleted* — CLOSED appendix in-tree; reopening is cheap (§ 6.5).

**S6 — Sub-agent cannot write shared docs.** Real: sub-agents fire `run_in_background` (Discipline #19) and cannot reliably write `canonical/`. If propagation required the author to write the tracker, sub-agent writes would silently never propagate. **Validated:** author *emits* a `Tracker-delta:` footer in returned text; KR *captures* it at wave-close. Emit ≠ write (§ 6.2).

**S7 — Move vs prune.** Real: the reorg's 11 `git mv` R100 renames. A "path changed → it's superseded" heuristic would false-positive on every relocation. **Validated:** move ≠ prune; only content *replacement* triggers (§ 6.3).

**S8 — "Became irrelevant" with no event.** A doc that's simply gone stale has no detectable supersession event. **Validated:** irrelevance *never* auto-fires — always surface-for-ratification. Auto-prune requires a *positive* event (supersession-at-authoring or workstream-close), never absence-of-relevance.

**S9 — Cross-repo citation.** Real: `decisions-log.md` lives in `reincarnated-engine/` and cites notes in the collab meta-repo. A single-repo reference check would miss the citation and wrongly clear an evidentiary note. **Validated:** predicate 4 greps **both** repos.

**S10 — New canonical write → tracker propagation.** The base case for System A. **Validated:** every spec/state-moving canonical write carries a `Tracker-delta:` footer; gandalf consolidates design-session writes immediately, KR consolidates orchestrated writes at wave-close; `none` is a valid footer.

**S11 — Never-prune ledgers.** decisions-log, CHANGELOG, the trackers, the router, AGENTS/GOVERNANCE/REVIEW_PROCESS, all OPs + skills, the spec-folder `00-index.md`. A supersession-looking edit to any of these must not trigger a prune. **Validated:** explicit never-prune class (§ 6.3).

**S12 — Recognition record later cited by decisions-log.** A verdict-class note starts auto-prunable-on-total-supersede, but if decisions-log later cites it as the source of a ratified commitment it must promote to evidentiary. **Validated:** classification is at *prune-time* by reference check, not at authoring-time — so promotion is automatic (§ 5, § 6.1).

**S13 — Transition-lineage fold-source.** A partially-superseded doc actively being folded must be audit-exempt while the fold is in flight, without a per-doc flag to maintain. **Validated:** a doc is transition-lineage iff it's an explicit fold-source in an active worklist — self-documenting via the worklist (§ 6.4).

**S14 — Scheduled audit catches residue.** The first two triggers (supersession-at-authoring, workstream-close-self-prune) are distributed and *will* miss things. **Validated:** the standing hygiene Routine (§ 6.6) is the centralized backstop — runs the reference check, auto-prunes the safe tier, surfaces the judgment tier, flags missing Tracker-delta footers, collapses aged tracker rows. *Distribute routine, centralize judgment.*

---

## 3. The load-bearing principle the stress-test proved

**Fully-blind auto-delete is unsafe; event-triggered + reference-verified auto-prune is safe.** The two corrections (S1, S2) both came from the same failure mode: a rule that fired on *appearance* (looks superseded / is a note) rather than on a *verified event + reference check*. Every safe trigger in the final system fires on a positive event and verifies references across both repos before acting. The ceiling — surface-for-ratification on any ambiguity — means the worst case is a human reads a prune-list, never a silent deletion of live content.

This is the same discipline as substrate-led design (the substrate votes; you don't pre-impose the taxonomy) applied to the doc tree: **the reference graph votes on prunability; you don't pre-declare a doc dead.**

---

## 4. S15 — the first-run refinement (POST-ratification; Matt-agreed 2026-06-30)

S1–S14 were *pre*-ratification stress scenarios. **S15 emerged from running the system** — the first real verify-then-prune pass (14 cancelled-prototype notes; ravine ×9 + crypt-vault ×5). The run exposed a gap that the imagined scenarios missed, and Matt agreed the reframing before it was canonized (*"Regarding (3) I agree"*). It is a refinement of **ruling (c)**, not a reversal.

**S15 — author-role modulates note-class; the real discriminator is substance-homing.**

The first run revealed that a **filename-class heuristic mis-fires for a steward/coordinator.** Ruling (c) sub-classes notes (evidentiary / verdict-recognition / working-memory) and treats verdict/recognition filenames (`*-verdict`, `*-recognition`, `*-capture`, `*-brief`) as auto-prunable-on-supersede. That heuristic is correct for a *builder* whose notes are scratch (gamora's sim-debug capture is genuinely ephemeral). It is **wrong for a steward**, because:

- **A steward's PRIMARY WORK-PRODUCT IS design transmission.** gandalf's notes *are* the design record — the lineage by which a recognition reaches canon. A `*-recognition` note from gandalf is not scratch; it is often the only home of a load-bearing observation until it's folded. Pruning it by filename-class would delete the design lineage. The same filename means *scratch* from a builder and *design-transmission* from a steward. **Author-role modulates the class.**

But author-role alone is a trap. If you simply exempt steward notes, you get a **perpetually growing queue** — steward notes never prune, accumulation is monotonic. The fix is the pairing:

- **The exemption must ride the PROMOTE-THEN-PRUNE lever.** A steward note becomes prunable *when its substance is promoted to a durable home* (canonical doc or current-to-end-state tracker) and the note collapses to a redundant pointer. The cancelled-prototype run is the clean proof: ravine + crypt learnings → extracted into one self-contained carry-forward note → the 14 raw notes became redundant → prunable. Promote-then-prune makes the steward-exemption **self-liquidating** instead of monotonically growing: it is not a permanent shield, it is a *promotion incentive.*

Combining the two, the actual prune predicate is neither filename-class nor author. It is:

> **Is the substance already homed elsewhere?**
> - **Homed** (substance lives in a durable canonical / tracker home) → **prunable**, regardless of author or filename.
> - **Not-homed** (substance lives *only* in this note) → **judgment-tier** (surface for ratification), regardless of filename class.

This subsumes ruling (c)'s reference-check (a cited note is "homed" in the citing doc's dependency graph) and **adds** the promote-then-prune axis (a note whose content was folded into a tracker is "homed" even if nothing cites the note by path). The substance-homing check is the operational form of promote-then-prune, and it is self-liquidating by construction: the queue shrinks exactly as fast as substance gets homed. *The real cleanup lever was never a better classifier or a bigger broom — it is promotion.*

**Conflict-of-interest flag (the honest part).** S15 is a rule about note-prunability authored by **the agent whose own note-class the rule most affects.** gandalf is the meta-repo's largest note-producer; a rule that makes steward notes harder to prune favors gandalf's own output. That is the developer↔judge conflict transposed to governance: rule-maker = rule-subject. The rule's **content** (substance-homing discriminator) stands on its own merits and Matt has agreed it. The rule's **ratification-authority** — *who owns doc-lifecycle discipline*, by symmetry with jack-ryan owning engineering-disciplines — is an **open question pending Matt's role-separation ruling** (the cluster-III governance seam; see the role-separation verdict of 2026-06-30). Until that rules, S15's content is Matt-agreed but its ownership is explicitly *not* gandalf-self-ratified. This flag is the governance-proposer→ratifier switch-moment, named in place.

**Refinement to § 6.6 hygiene operation:** the standing audit's classification step gains a third question after the reference check — *"is this note's substance folded into a tracker/canonical home?"* If yes, it moves to the safe tier even without a path-citation. This is why the first run's safe-auto tier was empty: nothing had yet been *promoted*, so nothing was yet *homed-and-redundant*. The 14 prunes only became safe **after** the carry-forward fold — promotion preceded prunability, exactly as the predicate requires.

---

**Tracker-delta:** none (governance/process artifact; no engine build-vs-spec or story-settledness delta).

**Signed:** gandalf, 2026-06-30
