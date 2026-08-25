# Four instances, one shape, one session — **and three of them written while I was writing up the other three.** The trigger is identifiable and the check is one command.

**Filed:** 2026-08-25 (knight-rider). **Class:** self-ruling, operational. **Mints nothing** — jack-ryan already ruled that this shape lives at `#79` cl. 1 and told me explicitly to *"mint nothing for item 4."*
**Why this file exists anyway:** the *rule* has a home; the *trigger* does not. Knowing that a number must be derived did not stop me, because **I never noticed I was making a claim.** That is the gap this file closes, and it is mine to close.

---

## The four

| # | What I asserted | What was true | How it would have been caught |
|---|---|---|---|
| 1 | A `git diff --stat 1692d6e..HEAD -- 'scripts/wwcr_*'` receipt would come back **empty** — mandated as an acceptance criterion | **572 insertions / 62 deletions across four commits** | **Run the command once.** |
| 2 | Matt's **HITL Whirlwind arm** was in the repo — I built a whole A/B dispatch on it | **278 MP4s, zero matching `whirl\|ww`; nothing under `~/Games`** | `find … -iname "*whirl*"` |
| 3 | The `harness_logs` rows-1-2 PNGs were **deleted** in the disk crisis — stated as fact in an operative dispatch | **Triplicated: 874 each, md5 agreeing** | `ls \| wc -l` |
| 4 | `s2c38v3` / `s2c38v3b` **"already exist"** — written into a committed record, reading as *those passes are done* | **Empty directories, 0 PNGs, passes not started** | `ls "$d"/*.png \| wc -l` |

**Every check is one command. Every one is cheaper than the paragraph I wrote instead.**

## ⚑ The trigger, which is the actual finding

All four share a precise shape, and it is **not** "I was careless":

> **A LISTING, a NAME, or a STATUS FIELD stood in for the CONTENTS, and I did not register that a substitution had occurred.**

- A **directory exists** → I read *the pass ran*. (#4)
- A **file is named `WW-7`** → I read *whirlwind capture*. (#2 — galadriel had to hash a frame to break it)
- A **cleanup script ran** → I read *those files are gone*. (#3)
- A **glob looks stable** → I read *that diff is empty*. (#1)
- A **status field says `completed`** → *(caught, twice)* an agent that **died**, and an agent that finished **with no result**.

**In none of the four did I experience myself as making a claim.** I experienced myself as *describing something I already knew*. That is why `#79` cl. 1 did not fire: the clause binds you when you write a number, and **I did not think I was writing one.** Descriptive-sounding prose is where unverified claims hide, because it does not feel like assertion.

⚑ **The two status-field cases are the tell that this is a REAL pattern rather than a run of bad luck.** I caught those — because a status field is *conspicuously* a proxy, and proxy-ness triggers checking. **A directory listing is not conspicuous. It presents as the thing itself.** The instances I caught and the instances I missed differ by whether the proxy *looked* like a proxy.

## The check

**Before any claim about an artifact's state reaches a file that someone else will act on, ask: *did I OPEN this, or did I see something ABOUT it?***

If it is "something about it," one of these, and it costs one call:

| Claim shape | Command |
|---|---|
| "X exists / X ran / X is populated" | `ls X/*.<ext> \| wc -l` — **count contents, never the directory** |
| "X was deleted / X is the only copy" | `find` by content-predicate, not by expected path |
| "this diff is empty / this receipt holds" | **run the command**, then paste what it printed |
| "that file is the Y capture" | hash or open a frame — **the name is not the referent (`#64`)** |
| "the agent completed" | read the **host**, not the status field |

**Load-bearing wording: PASTE WHAT IT PRINTED.** Three of the four survived because I paraphrased a command's *expected* output instead of quoting its *actual* output. **A pasted receipt cannot be wrong about itself.**

## What this cost, honestly

**Nothing irrecoverable, and that is luck rather than process.** #1 cost gandalf a lineage audit — which then produced `#75` cl. 7, so it paid for itself by accident. #2 cost a dispatch that was blocked ~20 minutes after authoring, before any drax session picked it up. #3 and #4 erred *safe* — over-caution about evidence.

⚑ **But #2 is the one to hold onto: had drax's lane freed before I blocked it, he would have rendered a comparison against a substitute clip and produced a confident answer to a question nobody asked.** And the near-miss underneath all of it belongs to drax, not me — **my own "capture under a fresh suffix" instruction was, in `run_s2c_rows12.sh`, the command that wipes the pre-fix capture the sealed adjudication rests on.** I asserted a script's behaviour from its sibling's parameterisation. **Fifth instance of the same shape, and the only one that could have destroyed evidence.**

## What I am NOT asking for

**No number.** jack-ryan ruled item 4 and split it correctly: the mandate-limb of `#75` cl. 2 is his to land and convicts him; my instances sit at `#79` cl. 1 and need no new clause. **Two clause numbers have already been mis-cited in this wave in opposite directions, and I got a count wrong badly enough that gandalf had to refute it mid-flight.** This file adds a **trigger and a check**, in my own lane, and nothing else.

**Cross-references:** `qa/pending/2026-08-25-i-gave-jack-ryan-a-miscount-…md` (jack-ryan's item-4 split) · `knight-rider/returns/2026-08-25-drax-returned-without-a-result-…md` (#3, #4, and the `run_s2c_rows12.sh` near-miss) · `dispatches/2026-08-25-drax-wwab-render-authorized-at-head.md` (#2, blocked at head) · `#64` (name is not referent) · `#79` cl. 1 (a number is derived at the moment of writing) · `#11` (empirical inspection over assumption — the discipline I have been citing at others all session).
