# Matt to-do — **three of your design notes have existed on exactly one disk for over a month**, and only you can decide what happens to them

**Filed:** 2026-08-25 (knight-rider). **Class:** durability / host-level. **Blocks:** nothing. **Risks:** the documents themselves.
**Why it is yours:** they are your notes in a shared tree. *"Commit the owner's notes without asking"* is not a call I make.

---

## The finding

Running the `#62(c)` dirty-state inventory for the first time (jack-ryan ruled it in, escalated to you separately) turned up **695 aged uncommitted entries** across the five repos. Almost all are scratch and captures. **Six are substantive. Three of those are yours:**

| age | path |
|--:|---|
| **36 d** | `matt_notes_handoff_docs/rdr-archive-frame-narrative-spine.md` |
| **35 d** | `matt_notes_handoff_docs/rdr-vdm2-field-delta-spec.md` |
| **34 d** | `matt_notes_handoff_docs/rdr-d2-itemization-design-digest.md` |

*(A fourth, `claude-mobile-session-docs/ARPG-canonical-kit-research/rdr-verify-1-recommendation.md`, is **38 d** and also unowned by any agent.)*

⚑ **Uncommitted → unpushed → unbacked.** There is no second copy of these anywhere. Not on `origin`, not in any agent's tree. **A disk failure loses them and there is nothing to recover from.**

**This composes badly with `matt_to_do/2026-08-24-mac-disk-space-red.md`** — the host is already flagged at red on space, and the same disk is the sole custodian of three of your design documents.

## What I need from you — any one of three, and they are all cheap

1. **Commit them.** One command, and they are on `origin` and backed. If they are drafts you would rather not publish to the shared record, see (2) or (3).
2. **`.gitignore` them** — a deliberate decision that they are local scratch, which at least makes the exclusion *intentional* rather than an accident that has run 36 days.
3. **Move them off the shared tree** to wherever your private notes live.

**Any of the three closes this. None of them is what I am asking for over the other two** — the defect is that the current state is *undecided*, not that it is wrong.

## What I did NOT do

- **I did not commit them.** Deliberately.
- **I did not read them for content.** Filenames, mtimes and sizes only.
- **I did commit two orphaned jack-ryan Gate-2 verdicts** found in the same sweep (34 d, `gamora/v1.14-sim-capacity` and `star-lord/v-emission-demo-critical-1`) — finished team record with no git history for the path, so nothing live owned them. Different fact pattern from yours: those are the team's, these are yours.

## Cross-references

`agentic_orchestration/qa/pending/2026-08-25-a-23-day-old-uncommitted-ocr-regression-nobody-owns.md` (the finding this came out of, and jack-ryan's `#62(c)` ruling + escalation to you) · `canonical/matt_to_do/2026-08-24-mac-disk-space-red.md` (the composing risk).
