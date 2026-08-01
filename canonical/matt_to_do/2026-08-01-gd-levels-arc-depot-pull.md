# T12 — GD `Levels.arc` depot pull (campaign per-room placement data)

**Parked:** 2026-08-01, gandalf (from legolas density probe Q5,
`agentic_orchestration/legolas/notes/2026-08-01-gd-pack-density-ranking.md`)
**Why only Matt:** Steam depot fetch on the authenticated account (same pattern as T-gdx3 creatures
pull, `2026-07-30-gdx3-creatures-depot-pull.md`).

## The action

Fetch the level-geometry archives the Edition-II pull omitted: **`resources/Levels.arc`** (base) +
**`gdx1/resources/Levels.arc`** + **`gdx2/resources/Levels.arc`** + **`gdx3/resources/Levels.arc`**,
into `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/` alongside the existing databases.

**Size check FIRST:** `Levels.arc` is the largest archive class in a GD install — likely several GB
against the current 189 MB fetch. If the depot browser shows the size, report it before pulling if
it's surprising.

## What it unblocks

- **Per-room campaign placement counts** — converts every pack *template* in the density ranking
  into a per-room *instance count* (how many proxies the Fleshworks carries per corridor; whether
  Cronley's Hideout beats Steps of Torment once placement is counted). The four UNPROBED folklore
  rooms (Cronley / Fleshworks / Ancient Grove / Tomb of the Heretic) become measurable.
- **Room volume** → monsters-per-square-metre — the metric the Godot dense-room render actually
  needs for camera framing (join target confirmed: `.lvl` region files referenced by name from the
  `.arz` we hold).
- Downstream code note (agent-side, not Matt's): the ARC reader
  (`gd_arc_reader_2026_07_26.py`) currently parses `Text_EN.arc` string tables only; a `.lvl`
  binary-region extension is a legolas/elrond work item once the archives land.

**Not blocking:** the EoR playtest v2 (Q51) proceeds without this — the DB-resident rooms
(Crucible t13w06, SR Shard-33+) and the Ceremony-5 camera referent cover the near-term need.
