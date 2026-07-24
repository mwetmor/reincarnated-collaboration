# Matt to-do — Grim Dawn Edition-II depot fetch (Steam-authenticated)

**Raised:** 2026-07-24 by gandalf
**Status:** BLOCKED on legolas depot-ID verification (in flight)
**Why only Matt:** Steam blocks anonymous manifest requests for paid content.
DepotDownloader prompts interactively for password + Steam Guard. An agent cannot
execute this, and an agent that *could* would be a credential-handling surface we
have deliberately not built.

---

## Credential boundary

**Username:** `mhwetmore` (recorded — a username is not a secret)
**Password / Steam Guard:** **never** recorded, never requested, never routed through an
agent. You type them into your own terminal.

---

## What this unblocks

The entire Edition-II delta run — which is what tells us whether the expansion changed
anything we have already banked. Specifically at risk: the `gd-flames-of-ignaffar-purifier`
22-row byte-match certificate, and the first-of-kind controller spatial fields
(`ViewDistance`, `SightAngerRate`, `MaxPursuitDistance`, `fleeDistance`) that feed the
TSF6/VDM work. Until this runs, your Asterkarn playtest observations cannot be banked
against anything, per the co-pinning rule.

## The thing that would be easy to get wrong

**Edition II is a re-fetch of ALL data depots, not just the new expansion's.**

Expansions patch the base game. Depot 219991's manifest ID will have changed. If we fetch
only the new expansion depot and keep Edition-I's base and gdx1/gdx2 archives, we produce a
**hybrid edition** — new expansion content sitting on stale base balance — which is worse
than either pure edition, because it corresponds to no build that has ever shipped and
nothing would flag it as impossible.

So: fetch base + gdx1 + gdx2 + the new expansion depot(s), all at current manifests, into
one new directory.

## Command (staged — depot IDs pending verification)

```bash
depotdownloader -app 219990 \
  -depot 219991 \
  -depot <GDX1_DEPOT> -depot <GDX2_DEPOT> -depot <NEW_EXPANSION_DEPOT> \
  -username mhwetmore -os windows \
  -dir /Users/admin/Games/vendor/grim-dawn-edition-II-<YYYYMMDD>
```

Legolas is verifying and will return this with real IDs filled in, having also confirmed
whether repeated `-depot` flags are supported in one invocation or whether it must be run
once per depot. **Do not run it until those are verified** — Matt's recollection is "Flames
of Asterkarn," gandalf's is "Fangs of Asterkarn," and neither may become a lookup parameter.

## Hard constraints

1. **`-dir` MUST be a new directory.** Never fetch into `/Users/admin/Games/vendor/grim-dawn/`.
   That path still holds Edition-I bytes.
2. **Do not delete `/Users/admin/Games/vendor/grim-dawn-edition-I-20260723/`.** It is the
   verified frozen snapshot (11/11 SHA-256 match) and the only thing that makes a diff possible.
3. Expect ~10 GB. The data-bearing subset is ~140 MB, but DepotDownloader fetches whole
   depots; the freeze-and-trim happens afterward.

## After it lands

Report the new directory path. Legolas runs the delta; elrond backfills `source_version`
on Edition-I rows **before** any Edition-II row is written.

## Related

- Freeze record: `agentic_orchestration/gandalf/notes/2026-07-24-gd-edition-I-freeze-fingerprint.md`
- Commission: `agentic_orchestration/research/commissions/2026-07-24-gandalf-gd-asterkarn-and-rank-adjudication.md`
- Ruling: `agentic_orchestration/gandalf/notes/2026-07-24-corpus-edition-disposition-ruling.md`
