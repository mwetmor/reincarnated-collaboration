# Commission — GD Edition-II lane + re-adjudication of the 60-vs-26 contradiction

**Date:** 2026-07-24
**Commissioner:** gandalf
**Addressed to:** `legolas` (UNKNOWN-RESEARCHER) — **not** `legolas-crawler`
**Authorized by:** Matt, 2026-07-24
**Priority:** Q1 before Q2 if you must serialize. Q1 may invalidate canon; Q2 only adds to it.

---

## Why this exists

A Grim Dawn expansion landed 2026-07-23. Matt owns it and is playing it. Two problems
followed, and the second one is worse than the first.

**Problem A — the corpus is pinned to a build that is no longer retail.** Our GD source is
a DepotDownloader snapshot fetched 2026-07-23, now frozen as **Edition-I** at
`/Users/admin/Games/vendor/grim-dawn-edition-I-20260723/` with full SHA-256 inventory and
manifest pins recorded at
`agentic_orchestration/gandalf/notes/2026-07-24-gd-edition-I-freeze-fingerprint.md`.
**Read that first.** The live directory `/Users/admin/Games/vendor/grim-dawn/` is
untouched and still holds Edition-I bytes; do not let anything overwrite it.

**Problem B — the founding evidence of the TRUE-SOURCES program may be wrong.** Matt asked
whether grimtools had simply been updated for the DLC ahead of us. Chasing that turned up
something else, and it needs adjudicating by someone who will go to the bytes.

---

## Q1 — Re-adjudicate the 60-vs-26 "contradiction" (HIGH STAKES)

### The canon as it currently stands

TSR-3 and the whole TRUE-SOURCES framing rest on this claim: *grimtools' community-harvested
60-rank arrays contradict the `.arz`'s actual 26 ranks, and nobody noticed until a primary
source was consulted.* It is written into the `legolas-crawler` role charter as the
justification for the non-improvisation law, and into `AGENTS.md` as the split rationale.

### What I found that puts it in doubt

Gandalf-level grep, not proper analysis — treat every item as a hypothesis to test, not a
finding to confirm:

1. **The two records compared may not be the same skill.** The `.arz` side is
   `records/skills/playerclass07/purifyingflame1.dbr` (Flames of Ignaffar, a Purifier class
   skill; `skillMaxLevel=16`, `skillUltimateLevel=26`, 26-element arrays). The grimtools
   side, per `2026-07-23-join-surface-probe.md` §2c, is **`sk296`** — a Canister Bomb-class
   ring projectile tagged `tagCompSkillA014Name`. `tagComp…` reads as a *component /
   item-granted* skill, a different namespace from `tagGDX1Class07…`.

2. **FoI appears to be absent from the grimtools harvest entirely.**
   `grep -c "GDX1Class07SkillName04A" all_skills.js` → **0**. If that holds, the two sources
   were never compared on the same skill and the contradiction was never observed.

3. **grimtools looks like it pads all rank arrays to a uniform 60.** Distribution of
   `skillMaxLevel` across `all_skills.js`: **60 → ~2,888 skills**, 1 → ~302, 200 → 24,
   50 → 20, 6 → 34, **16 → only 2**. Nearly three thousand skills at exactly 60 is a
   normalization, not a design fact.

4. **The tails saturate.** First record in the file, `sk497`:
   `petBurstSpawn:[1×15, 2,2,2,2, 3,3,3 …3]` — climbs, plateaus at 3, repeats for the
   remaining ~35 entries. `petLimit` does the same. That is a short real array padded to 60,
   most plausibly to the maximum a skill can be pushed to via `+skill` gear overcap so the
   site's UI never bounds-checks.

**If 1–4 hold, then nobody was ever wrong about Grim Dawn.** grimtools stores
overcap-padded 60-element arrays; the `.arz` stores the true 16+10. Both encode something
correct. Someone read a storage convention as a factual assertion, and compared two
different skills while doing it.

### Why this matters enough to spend Opus attention on

If the diagnosis is wrong, we canonized a **plausible-looking wrong conclusion drawn from a
secondary artifact that nobody checked against primary source** — which is the exact failure
class TRUE-SOURCES exists to prevent. Committed while justifying the program. I would rather
know.

Note what does *not* change either way: "consult the primary source" remains correct, and 26
remains the true FoI rank count. What is in question is the **diagnosis** — community data
quality — and therefore the reasoning built on top of it.

### Questions to answer

1. Is `sk296` the same skill as `purifyingflame1.dbr`? If not, what is it, and is FoI
   present in the grimtools payload under any identifier?
2. Does the padding hypothesis hold? Test against a **sample of GD class skills whose true
   caps you can read from the Edition-I `.arz`** — pick several with differing real caps —
   and check whether grimtools' arrays for those same skills saturate at the true cap and
   repeat thereafter. This is the decisive test; design it as you see fit.
3. Explain the two `skillMaxLevel:16` outliers. Why does grimtools carry a real cap there
   and a padded 60 nearly everywhere else? That asymmetry is the strongest evidence
   *against* a simple padding story, so take it seriously.
4. Was grimtools serving datamined PTR/pre-release data on 2026-07-21? Matt's original
   hypothesis is chronologically excluded for our artifact — harvest 07-21, expansion 07-23
   — but only if grimtools was tracking retail. This is the one surviving path for it.
5. **Verdict: does TSR-3's founding evidence stand?** If not, state the correct claim
   plainly, in a form that can replace the wrong one in the crawler charter and AGENTS.md.

### Ruling latitude

You are not required to rescue the existing claim, and you are not required to demolish it.
If the evidence is genuinely mixed, say so and say what would resolve it. **A finding of
"the contradiction was real but for different reasons than we recorded" is a perfectly good
outcome** — but it has to be argued from bytes.

---

## Q2 — Establish the Edition-II (expansion) lane

### Standing constraint before anything else

Matt refers to the expansion as **"Flames of Asterkarn."** My recollection says **"Fangs of
Asterkarn."** **Neither recollection gets to be a parameter.** Verify the actual title, Steam
app ID, and depot IDs from source — Steam store page, SteamDB — before any fetch is
constructed. Confident recollection becoming a lookup parameter is the error class this
whole commission is about.

Related trap already checked and cleared: `Asterkarn` strings in the base `.arz` are
**pre-existing Act-4 content** (Asterkarn Valley/Road, a yeti boss). The expansion is named
after an existing region. Do not read those strings as expansion presence.

### The sequence

1. **Verify** title / app ID / depot IDs. Note that our Edition-I fetch already includes
   depots 897670/897671, which I *believe* are Forgotten Gods (gdx2) but have not confirmed.
   Correct the record if I'm wrong.
2. **Fetch to a NEW directory** — `grim-dawn-edition-II-<date>/` or similar. Never in place.
   Edition-I must survive byte-identical. Requires Matt's Steam credentials (paid content
   blocks anonymous manifest requests); if you need them, that is a `matt_to_do/` item, not
   something to work around.
3. **Delta report — this is the deliverable, not the extraction.** Record-level diff of
   Edition-I vs Edition-II: added / removed / **changed**.

### Delta flags, in priority order

- **P0 — any record we have already banked.** Currently one: `purifyingflame1.dbr`
  (`gd-flames-of-ignaffar-purifier`, 22 rows, certified 22/22 byte-match against Edition-I).
  If Crate touched it, that certificate now attests fidelity to a build that no longer ships.
- **P0 — controller spatial fields.** `ViewDistance`, `InnerViewDistance`, `SightAngerRate`,
  `InnerSightAngerRate`, `MaxPursuitDistance`, `PursuitTime`, `fleeDistance`,
  `WanderDistance`, `distressCallRange`. These are first-of-kind documentation from the
  2026-07-23 probe, they feed the TSF6/VDM work, and expansions are exactly when a developer
  touches monster AI and pacing. Highest live risk in the whole diff.
- **P1 — rank-array structure anywhere.** Any change to `skillMaxLevel`,
  `skillUltimateLevel`, or array lengths. Directly interacts with Q1.
- **P1 — new field names in the string table.** Our schema-drift tripwire. A new field name
  means the adapter's field vocabulary is incomplete.
- **P2 — `.arz` header `version` field.** If the format itself bumped, the parser needs
  re-validation before any row is trusted.
- **P2 — whether `templates/` ships in the new depot list.** Zero `.tpl` files were present
  in Edition-I despite every record referencing one via `templateName`. Either a depot was
  omitted or templates live elsewhere. Open question worth closing opportunistically.

---

## Target sources

Steam store + SteamDB (app/depot IDs) · DepotDownloader (fetch) · the frozen Edition-I tree
· `agentic_orchestration/research/datamine-acquisition/gd/raw/all_skills.js` (grimtools
harvest, fetched 2026-07-21 22:49) · `agentic_orchestration/legolas/notes/2026-07-23-gd-arz-extraction-probe.md`
· `agentic_orchestration/legolas/notes/2026-07-23-join-surface-probe.md` §2c ·
`agentic_orchestration/research/scripts/gd_arz_adapter_2026_07_24.py` (working `.arz` parser
— reuse it, don't rebuild it)

## Output

- `research/knowledge/gd/2026-07-24-rank-array-adjudication.md` — Q1, with the verdict stated
  as a replaceable canon sentence
- `research/knowledge/gd/2026-07-24-edition-II-lane-and-delta.md` — Q2

Standard findings format. Distinguish primary from secondary from tertiary. **Note
conflicting information rather than averaging it.** Flag anything uncertain or contested.
Length: whatever the evidence needs; Q1's verdict section should be short enough to quote.

## HALT conditions

Escalate to gandalf rather than improvising if: Steam credentials are required (→
`matt_to_do/`) · the `.arz` format version bumped and the existing parser no longer reads
cleanly · the delta is large enough that "diff" stops being the right frame · **or Q1's
answer implies canon changes beyond TSR-3.** That last one is a design-authority boundary,
not a research one, and it is mine and Matt's to rule, not yours to resolve.

## What is NOT in scope

Corpus DB writes (elrond) · the `source_version` backfill (elrond) · any decision about
whether the corpus tracks live retail or holds dated editions (Matt's ruling, pending) ·
volume re-extraction (hands to `legolas-crawler` once schema is confirmed unchanged).
