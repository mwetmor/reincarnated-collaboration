# T11 — Pull a SECOND Grim Dawn character save (`.gdc`) for field-semantics diffing

**Filed:** 2026-07-30, gandalf (RUN-CONDUCTOR, WR3-KITE-COMMIT) · **Source:** R-WR3-26(6), legolas discriminator note U-1/U-2

## The ask

Copy **one more `player.gdc`** from the live Grim Dawn install — any character other than the
referent (a throwaway level-1 works; ideally take a snapshot, get hit once by a known weak enemy,
save, and snapshot again so we get a before/after pair). Drop it anywhere under
`/Users/admin/Games/vendor/` and say the word.

Save location on a standard install: `<GD user dir>/save/main/_<CharacterName>/player.gdc`.

## What it unblocks

The WR3 stage-map arm ruling (S0/S1/S2) currently leans on two save floats
(`greatestDamageReceived` 260.498 / `lastHitBy` 273.704) whose **labels are community
convention, not engine truth** (`Game.dll` carries no such symbols), whose ordering **violates
the invariant `greatest ≥ last` as labelled** (possible label swap, U-1), and whose
single-event-vs-aggregate semantics are unproven (U-2 — `lastHitBy` is PROVEN aggregate; its
neighbour is untested). A second save, diffed against known events, closes U-1 + U-2 together —
legolas: "everything ambiguous in this note traces to having exactly one save."

**Not blocking:** the conductor lean (S1_PAK) rests on the roster ceiling sweep, which is
independent of save-field semantics. This to-do hardens the ruling; it does not gate it.
