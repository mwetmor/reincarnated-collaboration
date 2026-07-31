# W-2 fork: full-heal-on-leash is NOT a Grim Dawn convention — adopt it anyway, or not?

**Filed:** 2026-07-31, gandalf (RUN-CONDUCTOR, WR3-KITE-COMMIT) · **Source:** R-WR3-41(3), from
legolas's first-of-kind extraction (`agentic_orchestration/legolas/research/2026-07-31-wr3-w2-aggro-leash-referent.md`)
· **Blocking:** NOTHING — the W-2 lap proceeds on the referent default meanwhile. This queues the
*departure* option only.

## What changed

The charter's W-2 third mechanism read "leash-in-combat (territory-guard full-heal return) …
per GD's convention." **The premise is false, proven, not merely unsupported:**

- `leash` occurs **0 times** in `Game.dll`; GD has a **pursuit envelope** instead — 75 m / 10 s
  for trash through hero, **210 m for bosses** (functionally un-leashable), triggering on
  **disengagement only** (the envelope is 5× the 15 m aggro radius, so it cannot fire mid-combat).
- **No heal-on-return exists**: the complete 17-group AI template surface has no heal field, the
  binary has no restore symbol, and returning monsters recover by ordinary regen on the walk back.
- Full-heal-on-leash appears in **none of the four ARPGs surveyed** (GD, D2, D3, PoE). It is a
  WoW/MMO convention. Importing it is a genre departure, not a genre borrowing.

Our engine's dormant R2 "territory-guard full-heal return" (`spatial_engine.py:1957`) was built on
the false premise. It stays dormant.

## The two decisions (rule together)

**D1 — Adopt full-heal-on-leash at all?**
- **(a) NO — referent default (conductor's lean, and what W-2 builds meanwhile):** pursuit
  envelope + walk-back + ordinary regen. Player consequence: a half-killed pack you flee from is
  still half-killed when you return — attrition is a real tactic, as in every genre peer.
- **(b) YES — deliberate departure:** full-heal on return. Player consequence: encounters become
  all-or-nothing sieges; hit-and-run attrition dies as a tactic. Defensible only if you want
  encounter-as-puzzle-room pressure — name that goal if so.

**D2 — A distinct "territory-guard" concept (narrower leash than GD's 75 m)?**
- GD has no such concept — only `HomePosition` + the envelope. A tight guard radius would make our
  game MORE restrictive than the referent. Lean: no, unless a specific encounter design (e.g. a
  shrine-guardian) wants it later as a per-monster override — which the design lap can charter.

## Ruled without you (veto-open, declared assumptions — R-WR3-41(3))

D3 pursuit distance home-relative · D4 engagement = hard 15 m radius (GD ships the anger gate
effectively off) · D5 sim distress-groups keyed by spawn species pending the story-side taxonomy ·
D6 stagger explicit four-parameter (GD engineers it; radii are flat and can't carry it) ·
D7 anger per-second. One word overturns any of these.
