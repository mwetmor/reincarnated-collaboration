# E07N · Internal door committed-state integration

The previously unused internal door now controls matching geometry, physical traversal, paths and point-light blocking in both chambers. All51headless checks,300closed-panel pixel witnesses (150native,150fresh),42browser checks across the two resolutions and6saved-review/live-button checks pass. Godot is the shipping target; Pixi is the test harness. This qualifies committed states only.

The existing E04 timing policy remains: locked cannot open; unlocking leaves the panel closed; opening blocks until the0.5scommit; open permits traversal; closing restores blocking immediately and completes after0.5s. Both mage and larger monster can traverse when open and prevent closing when occupying the doorway. Saved opening/closing states preserve remaining time and subsequent state/events exactly. Navigation signatures include actual obstacle bounds; prior routes are invalidated by the door state/version change. A missing-collider control allows an otherwise forbidden crossing and is detected. Chest rewards/pickup remain single emission under the wrapper. Invalid time, pending transitions, prop/event state and unknown factions are rejected. State input is unchanged and simulation has no rendering imports.

A CPU ray/box oracle chooses25interior front-face witnesses per faction/resolution, guarded by nine neighboring pixels. Closed, reversed-order and closing images match all300within2RGB. All100open-view witnesses change; all100stale-closed-visual control witnesses retain the forbidden panel and are detected. The pilot is behind the panel for these face samples. This is a sampled geometric test, not an exhaustive image oracle.

The closed panel removes warm/cool light exactly on372stable pilot pixels per faction. Open warm red mean rises from99.9032to107.9946; cool blue from79.3065to85.5833. Ignoring the closed leaf exposes leakage. Fresh capture tests geometry, not a repeated fresh lighting qualification. All GL/page checks pass; favicon404 is the only console error.

## Art and motion remain incomplete

F01 uses a timber-faced sliding panel and F02 an iron-faced panel in the existing partition. Open represents retraction inside the north wall pocket. No smooth panel travel is implemented: opening holds closed artwork until commit and closing switches it immediately. This preserves the registered conservative transition rule, but does not prove animated motion or partial-aperture collision.

Native closed/open views and saved review were visually inspected. The door fills the correct aperture and clears it when open. F01 blends too closely into its adjacent wall; both need visible frame, pocket/hardware and interaction treatment before final art acceptance. Source material plates are unchanged. Complete scene detail, NPC/monster depth/materials, character contact/cast shadows, full painted pilot/gear, VFX and serial combat remain open.

Two implementation revisions, three capture batches, zero generation calls or paid-service spend. Revision2 tightens invalid JSON/faction rejection and adds reward regression checks; valid drawing behavior is unchanged. Next E07L: prove geometry-derived pilot contact/cast shadow on floor with a shared directional-light declaration, actual pose/root transforms, independent ray witnesses and missing/stale-shadow controls. Do not expand roster or animation inventory before full pilot art passes.

[Saved review](review.html) · [Receipt](RECEIPT.json) · [Artifacts](ARTIFACTS.json).
