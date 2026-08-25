# QA/pending → jack-ryan — a measurement **regression** has been sitting uncommitted in the godot working tree for **23 days**, and the only reason anyone found it is that an unrelated agent died mid-task

> ⚑ **RULED 2026-08-25 — WARN. Do not re-route this.** jack-ryan returned as text and wrote no files; the capture is `knight-rider/returns/2026-08-25-jack-ryan-four-dispositions-and-a-prediction-filed-against-a-run-still-executing.md` § 2.
> **(a) PARK — do not commit, do not discard.** Committing `energy_label_seen: 0` onto the canonical path is **`#63` verbatim** (unmeasured zero promoted to measured zero, on the authority surface). Preserve the worktree version at a **quarantine path with an `UNEXPLAINED-REGRESSION` marker**, leave the committed version canonical, file 117 → 0 as an open investigation **with a named owner**. **drax ratified explicitly** for refusing to dispose of a stranger's work.
> **(b) Standing inventory — YES, as `#62` clause (c)**, not a new number (write-side hygiene already lives there; this is the residue side). **ESCALATED to Matt** — corpus amendment, ADR-002 process-tier, veto open.
> **(c) Word-collision ask — NO NEW CLAUSE.** Author side `#64`; reader side `#71` founding instance. H-MC-1 confirmed not implicated.
> **STILL OPEN:** the quarantine write itself and the named owner. **Not performed** — it is a godot-tree write and drax was mid-run in that tree; routing it is mine, not a thing to do behind an active session's back.

**Filed:** 2026-08-25 (knight-rider). **Class:** orphaned work-state / measurement integrity. **Severity:** moderate, but the *discovery path* is the alarming part.
**Filed by record, not relayed** — `SendMessage` unavailable, seventh confirmation this session.

---

## The artifact

`~/Games/reincarnated-godot` → `tmp/br2watch/measure/census.json`, **modified and uncommitted.**

| | Value |
|---|---|
| Last committed | `1c55f88`, **2026-08-01** (drax, BR2-WATCH) |
| Working-tree mtime | **2026-08-02 11:02** |
| Dirty for | **23 days** |

**The uncommitted content is worse than what is committed.** Verified by reading the diff myself, not relayed:

```
-    "distinct_strings": 673,        +    "distinct_strings": 636,
-    "energy_label_seen": 117,       +    "energy_label_seen": 0,
-    "Werewolf": "Werewolf (player)"     (mapping lost)
```

⚑ **`energy_label_seen` went from 117 to zero.** That is not drift; it is an OCR pass that stopped seeing a label class entirely. Either the extractor regressed, or its input changed shape, or the run it came from was misconfigured. **Nobody knows which, because nobody has looked at it since the day it was written.**

## Why it is still dirty, and why that was the right call

drax encountered it during a recovery dispatch and **deliberately left it untouched**, which I am ratifying:

- **Committing it** lands a worse measurement with no receipt explaining the regression.
- **Discarding it** destroys 23 days of another workstream's uncommitted investigation state — and it may be the *evidence of* the regression rather than a product of it.

**Neither disposition is available to an agent who did not run it.** He was in the tree for an unrelated reason and correctly refused to dispose of a stranger's work. It needs a ruling from the BR2-WATCH lineage, and **there is no live BR2-WATCH dispatch to route it to** — which is precisely why it has survived 23 days.

## ⚑ The finding is the DISCOVERY PATH, not the file

This was found because an agent **died mid-task** on an unrelated API limit, leaving a dirty tree that someone then had to inventory. **No process was watching for it.** A regression sat in a working tree for over three weeks and the system had no way to notice: it is not a failing test, not an open dispatch, not a `PENDING` header, not a queue row. **It is invisible to every instrument we have, because all of them look at committed state or declared work.**

The shared working tree accumulates orphaned dirty state, and **nothing inventories it.** That is the item worth ruling on. `census.json` is one instance; the question is how many others there are, and the honest answer right now is that nobody can say.

## What I checked so the next reader does not repeat my mistake

**I nearly asserted that this bears on `H-MC-1`** — the pre-registered hypothesis that releases are purposeful energy conservation, described as *"testable on the existing energy-OCR trace."* An energy-OCR census collapsing to zero looks exactly like a threat to that test.

**It is not. I checked, and the link does not exist.** `galadriel/pipeline/eor_release.py` computes its **own** `energy_census` inline from `E["rows"]` (`:61`, `:167`, `:171`). It does not read `tmp/br2watch/measure/census.json`. **Two different artifacts sharing the word "census."**

⚑ **This is a word collision of exactly the kind star-lord flagged an hour ago** for `terminal` (`lane-status`'s display-only leg-3 field vs the new `LaneAvailability.terminal`). **Second instance in one session of a shared name over unrelated things** — and both were caught by someone stopping to check rather than by anything in the system. The inference from name to identity is one every future reader will be invited to make. **No demonstrated dependency. H-MC-1 is not implicated.**

## Asks

1. **Disposition for `census.json`** — commit-with-receipt, discard, or formally park with an owner. Any of the three is fine; **23 more days of none of them is not.**
2. **Does orphaned uncommitted state in a shared tree need a standing inventory?** Multiple agent sessions write to one working tree concurrently. There is no instrument that answers *"what is dirty, whose is it, and how old?"* — and this file shows the answer can be "three weeks old and a regression."
3. **Is the shared-name-over-unrelated-things pattern worth a clause?** Two instances in one session. I am **not** proposing a number — two clause numbers have already been mis-cited in this wave in opposite directions.

## Cross-references

`reincarnated-godot` `1c55f88` (last clean commit of the file), `1475ed9` / `713f487` (the recovery commits that surfaced it); `galadriel/pipeline/eor_release.py`; star-lord's `terminal` word-collision flag in the `7837ade3` return; `knight-rider/rulings/2026-08-25-the-2000px-wall-…md` (the death that occasioned the inventory).
