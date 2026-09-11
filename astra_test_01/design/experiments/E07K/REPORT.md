# E07K · Painted pilot in both geometry-owned chambers

The depth-bearing painted pilot now shares projection C, range-validated 10–40 m depth and point-light data with F01 waystation and F02 reservoir. Godot is the shipping target; Pixi is the test harness. This is a scoped integration pass, not completed chamber or character art.

Independent CPU nearest-hit ray/triangle witnesses pass 228/228 native and 144/144 fresh 3× checks, including reversed drawing order. An always-front pilot control fails 12 occluded witnesses in each faction at each resolution. The control combines disabled pilot depth and forced-last drawing; it does not isolate those changes independently. Chamber depth spans 17.72181–28.05146 m; planned pilot bounds also fit the clip range. Eight placements and shader capacity pass preparation checks.

Warm and cool point light alter the pilot when the east exit is open. Closing the leaf removes that contribution exactly on the registered stable material pixels: 789 per faction natively, 9,484 in the fresh F01 capture. Ignoring the closed leaf causes measurable leakage and fails the control. This proves sampled receiver response and blocking, not finished F03 lighting or actor-cast shadows.

All 38 interaction checks pass across both factions: actual pointer floor movement, chest reward once, pickup once, crate destruction and traversal, closed/open east and west exits, occupied exit closure rejection, and exact JSON save/restore. Existing E07D simulation is unchanged; the pilot uses an idle pose throughout. Five saved-HTML review checks pass. All recorded runtime GL/page checks pass; the native console contains only a favicon404. A NumPy boolean serialization failure was fixed before numerical report output; original captures were retained and no capture batch repeated.

## Visual assessment and remaining work

Inspected native front and fresh warm-lit pilot views show improved sampling, depth and material response. The rooms remain plain; the large pillar and simple architectural surfaces do not meet F03 detail. NPC/monster are earlier sprite fixtures with unqualified depth/material response. No contact or actor-cast shadow grounds the pilot visually. The actual source minimum Z is approximately zero (idle −4.38e−8 m, sparse walk 8.52e−7 m); absence of a shadow must not be confused with measured hovering. Full painted pilot/gear art, animation inventory and translucent VFX remain unqualified.

The E04 internal locked/opening/closing door state is still unused by current chamber geometry and collision. External exits passing does not close that gap. Next E07N must connect the existing internal-door state to declared geometry, navigation, occupancy, light/depth and saved transition time. Serial combat binding remains separately open.

One adapter revision, four capture batches, zero generation calls and zero paid-service spend. Source artwork and previous failed evidence remain unchanged. Review: [saved comparison](review.html); exact limits, costs and artifacts: [receipt](RECEIPT.json), [index](ARTIFACTS.json).
