# Ruling — Corpus disposition: snapshot with editions, and the co-pinning rule

**Ruled by:** Matt, 2026-07-24 — *"snapshot with editions — cut Edition II, co-pinning ruled."*
**Surfaced by:** gandalf (ELICITOR) when a Grim Dawn expansion landed 2026-07-23
**Status:** RULED. Proposed for jack-ryan ratification → decisions-log.
**Scope:** all primary-source corpora in the TRUE-SOURCES program, not GD alone.

---

## 1. The fork that was ruled

A DLC landing forced a question that had never been asked deliberately: **is the corpus a
dated snapshot, or does it track the live game?** We had been implicitly building a snapshot
— manifest-pinned depot, byte-match certificates, exact-fields schema all assume it — and
were about to implicitly become a tracker, simply because re-fetching felt like the obvious
response to an expansion.

Both options were real:

- **Snapshot** — every row pinned to an immutable manifest. Derived work never expires; it
  says "as of build X." Reproducible and citable indefinitely.
- **Tracking** — the corpus always reflects current retail. More useful for "what does the
  game do today," but every downstream derivation acquires a shelf life and re-validation
  becomes a standing cost paid on the publisher's schedule rather than ours.

## 2. RULING-A — Snapshot with editions

**Every banked row carries the manifest pin of the edition it was derived from. Expansions
and patches produce NEW editions alongside existing ones; they never overwrite.**

Rationale: the property that makes TRUE-SOURCES worth its cost is that a claim stays
checkable years later. Tracking destroys exactly that property. Steam manifest IDs are the
correct pin — they name exact bytes rather than a label a publisher can reuse.

**Immediate consequence (owed, elrond):** `source_version` is currently EMPTY on the one
banked `exact_skill` row. The adapter has the column and its schema comment even anticipates
this ("GD build/patch if determinable"), but nothing populates it. **Backfill Edition-I rows
before any Edition-II row is written.** Mixed populated/blank version columns are worse than
uniformly blank, because the blanks begin reading as "same as the others."

## 3. RULING-B — The co-pinning rule

**The playtest build and the corpus edition must be co-pinned. Where they cannot be, every
human-oracle observation must carry the build it came from.**

This is the rule with the longest reach and it did not come from the data side. It came from
Matt observing that his Asterkarn playtesting "may confound things."

The mechanism, stated precisely: **Matt is the human oracle for everything the primary source
is silent about.** TSF6-TRACK-A closed 2026-07-24 with a gap register of 1 faithful / 1
partial / 5 BLOCKED-MECHANISM, headlined by the finding that our sim has *no aggro-onset
concept at all* (`aggro_radius_m` dead at `spatial_engine.py:1124`). Aggro onset is not
readable from a file. It is learned by playing.

Expansions are precisely when a developer touches monster AI and pacing. The controller
fields we hold as first-of-kind documentation — `ViewDistance`, `InnerViewDistance`,
`SightAngerRate`, `MaxPursuitDistance`, `fleeDistance` — are therefore live risk, not
theoretical.

So an observation learned on Asterkarn and banked against Edition-I controller values is not
merely stale. **It is a version-skewed row wearing the badge of human-validated ground
truth**, which is worse than an honestly blank one — an unpinned row invites checking, a
falsely-corroborated row forecloses it.

## 4. RULING-C — Cut Edition II promptly

Follows from B. **An edition nobody plays is a museum piece.** Snapshotting is not an excuse
to let the substrate fall behind the oracle. The correct response to "Matt has moved to a new
build" is to make the substrate catch up — never to constrain what Matt plays. Telling the
senior architect not to play his new expansion is not a design position.

## 5. What this obligates going forward

| Obligation | Owner |
|---|---|
| `source_version` populated on every new row, pinned to a manifest ID | elrond (schema), adapter authors |
| Backfill Edition-I rows before Edition-II ingest | elrond |
| Freeze + fingerprint the current edition BEFORE any re-fetch that could overwrite it | whoever conducts the fetch run |
| Human-oracle observations recorded with the build they were made on | whoever banks the observation |
| New-edition cut when a patch lands that the oracle has adopted | gandalf surfaces, Matt rules |

**Generalization beyond GD:** this applies to every primary-source lane — PoE1/PoE2, D2, LE.
Any lane whose source is a live, patchable product inherits both rulings. Lanes sourced from
frozen artifacts (D2's `Skills.txt` from a fixed patch) already satisfy them trivially, but
should still carry an explicit pin rather than an implicit one.

## 6. Standing hazard this makes visible

Two independent version hazards surfaced within minutes of each other once the question was
asked: an unpopulated `source_version` column, and an oracle/substrate build mismatch.
Neither was visible before a DLC forced the issue. That is the signature of a class of defect
that only appears under change — worth remembering the next time a lane looks settled.

## 7. Ratification

gandalf proposes; **jack-ryan ratifies**; decisions-log entry follows per governance
(gandalf does not write decisions-log directly). Flagged for the next Gate-1 pass.
