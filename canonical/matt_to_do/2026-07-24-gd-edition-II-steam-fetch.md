# Matt to-do — Grim Dawn Edition-II depot fetch (Steam-authenticated)

**Raised:** 2026-07-24 by gandalf
**Status:** ✓ **DONE 2026-07-24.** Matt ran it; fetch succeeded on the first invocation.
The closing `find` errored only because `DST` was unset in the `bash` subshell (typed during
shell startup), so DepotDownloader fell back to its default `~/depots/` layout. gandalf
assembled `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/`. **Outcome + the
manifest-identity finding: `agentic_orchestration/gandalf/notes/2026-07-24-gd-edition-II-cut-record.md`.**
Kept for lineage — the two-invocation correction below is what made the fetch complete.
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

## Command — READY (verified 2026-07-24)

**Title verified from Steam Web API (primary source):** `Grim Dawn - Fangs of Asterkarn`,
**app ID 2699230**. Neither recollection was used as a parameter; the ID came from the API.

Fangs' individual depot IDs are not retrievable without auth (SteamDB 403s; the Steam Web
API does not expose depot IDs for DLC apps). That's fine — passing `-app` without `-depot`
makes DepotDownloader enumerate every depot the account owns for that app. Depot IDs can be
read back from `.DepotDownloader/*.manifest` filenames afterward and recorded as the
Edition-II pin.

```bash
DST=/Users/admin/Games/vendor/grim-dawn-edition-II-20260724
mkdir -p "$DST"

# Fetch only the data-bearing files (~140 MB) instead of the full ~10 GB depot.
cat > /tmp/gd-filelist.txt <<'EOF'
regex:.*\.arz$
regex:.*Text_EN\.arc$
EOF

# 1 — base game + owned expansions AT CURRENT (post-patch) MANIFESTS.
#     REQUIRED. Expansions patch the base game; skipping this yields a hybrid edition.
depotdownloader -app 219990 \
  -username mhwetmore -os windows \
  -filelist /tmp/gd-filelist.txt \
  -dir "$DST"

# 2 — Fangs of Asterkarn. Safety net: if Fangs' depots already registered under app
#     219990 above, this is a no-op. If they didn't, this is what gets them.
depotdownloader -app 2699230 \
  -username mhwetmore -os windows \
  -filelist /tmp/gd-filelist.txt \
  -dir "$DST"

# 3 — verify the expansion actually arrived before declaring the fetch done.
find "$DST" -name "*.arz" | sort
```

**Step 3 must show a new expansion archive** (a `gdx3/`-style path, or whatever Crate named
it) alongside base/gdx1/gdx2. If it doesn't, the fetch is incomplete — stop and report rather
than proceeding to the delta.

**Why two invocations, corrected from legolas's single-app draft:** his command fetched only
app 2699230 (the DLC). That would have produced exactly the hybrid edition warned about
below — new expansion content on Edition-I's stale base archives. The gap was gandalf's
briefing error, not legolas's: the hybrid-edition hazard was written into this file *after*
his commission was dispatched, so he never saw it.

**Note on the filelist:** written to a real temp file rather than piped via heredoc into
`/dev/stdin`. Same effect, but it won't fail depending on how DepotDownloader opens the path
— and this runs inside an authenticated interactive session, which is a bad place to debug.

## Hard constraints

1. **`-dir` MUST be a new directory.** Never fetch into `/Users/admin/Games/vendor/grim-dawn/`.
   That path still holds Edition-I bytes.
2. **Do not delete `/Users/admin/Games/vendor/grim-dawn-edition-I-20260723/`.** It is the
   verified frozen snapshot (11/11 SHA-256 match) and the only thing that makes a diff possible.
3. Expect ~140 MB, not ~10 GB — the `-filelist` filter restricts the fetch to `.arz` and
   `Text_EN.arc`. (Supersedes the earlier note that the full depot must be pulled and trimmed
   afterward; filtering at fetch time is strictly better and was legolas's improvement.)

## After it lands

Report the new directory path. Legolas runs the delta; elrond backfills `source_version`
on Edition-I rows **before** any Edition-II row is written.

## Related

- Freeze record: `agentic_orchestration/gandalf/notes/2026-07-24-gd-edition-I-freeze-fingerprint.md`
- Commission: `agentic_orchestration/research/commissions/2026-07-24-gandalf-gd-asterkarn-and-rank-adjudication.md`
- Ruling: `agentic_orchestration/gandalf/notes/2026-07-24-corpus-edition-disposition-ruling.md`
