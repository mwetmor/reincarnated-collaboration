# E01 independent G2 preparation — registered before checks

Scope: exercise the draft chamber's logical geometry while D01 is pending.
This is a component check, not E02 runtime execution or a G2 pass. No painting,
animation, user preference or runtime target is assumed.

Inputs: `chamber-layout.draft.json`, `projection-candidates.json`.
Controls: closed versus open door; small versus large actor; independent blocker
ownership; intentional straight path through a wall; intentional shifted inverse
mapping. Hold layout fixed. 0 generation calls, 0 paid spend, 2 local runs maximum
before diagnosis, 5 minutes and 5 MB additional output ceiling.

Preregistered checks: 0 forbidden reachable exit states; all required approach
points reachable when open for radii 0.35/0.65 m; 0 blocker ownership loss after
removal; exact projected origin; analytic ground round trip below 1e-9 m on 99
known points per candidate; corrupt inverse offset 0.25 m must fail. The numerical
transform band is a floating-point implementation check, not an art tolerance.

Use a 0.25 m four-neighbor grid. Expand obstacles by radius using conservative
axis-aligned bounds. Continuous segment/AABB intersection also checks route edges,
so sampling at path nodes alone cannot license wall penetration. Over-conservative
corner clearance is disclosed. Boundary exit approach points are (-4.25,0) and
(4.25,0); external room links and their clearance are a later test.

Not exercised: runtime character shape sweeps, diagonal movement, event timing,
art masks, planted feet, height-aware sorting, loot persistence or rewards, door
occupied-state transitions, runtime imports/alpha/attachments, performance. These
remain requirements for the registered E02 capability/data proof and later gates.
