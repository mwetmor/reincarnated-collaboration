# E01 — native reference inspection and provisional projection shortlist

Recorded 2026-09-11 UTC / 2026-09-10 America/New_York. Open Codex lane.
User-authorized research and local preparation. Parent handoff `0730fa88` verified;
HEAD was that exact commit at intake. No existing design/skill content had drifted.
Unrelated tracked Godot settings and many untracked teammate artifacts were left alone.

**Outcome: review packet delivered; E01 and G1 INDETERMINATE, not PASS.**
All four games now have inspected, publisher-attributed native world-view evidence.
The packet retains 27 publisher files (22 world views, including dialogs and
HUD-hidden scenes; five menu/graphic rejections) and one separate project frame.
Required uncut gameplay motion is absent; Last Epoch ordinary HUD framing is
also absent. H01/H08/H10 remain hypotheses. No original ASTRA thresholds changed.

Open [labelled comparison](comparison.html), [projection study](projection-study.png),
[source manifest](sources.json), [measurements](measurements.json) and
[receipt](RECEIPT.json). The offline HTML keeps original aspect/framing, adds
separate review overlays, and includes a clearly marked project replica.
The companion [Canvas](/Users/admin/.cursor/projects/Users-admin-Games/canvases/astra-E01-native-comparison.canvas.tsx)
provides the four-game comparison beside chat. The repository artifacts are the
portable record; Canvas does not own gate or approval state.

## Findings from actually inspected native pictures

**Original Diablo II, LoD-era official guide; NOT D2R.**
[D2-06](media/D2-06.jpg) shows a relatively isolated sorceress and her contact
shadow among cave torches. [D2-01](media/D2-01.jpg) shows Frozen Orb shards spanning
a dark room while bodies overlap at the centre. [D2-05](media/D2-05.jpg) exposes
diagonal masonry, a tall wall and a foreground sarcophagus: the floor remains
readable in the gaps, while vertical props consume navigable-looking screen area.
The [hire dialog](media/D2-03.jpg) is a visible camp interaction, but most of the
world is obscured by its menu. The stash image is rejected for camera use.
These are native screenshots distributed by Blizzard’s
[Arreat Summit](https://classic.battle.net/diablo2exp/skills/sorceress-cold.shtml),
not screenshots of D2R legacy mode. The precise game patch is unknown.

**Path of Exile 1; NOT PoE2.**
The three pre-existing fire references were recovered byte-for-byte from publisher
screenshots on [Steam app 238960](https://store.steampowered.com/app/238960/).
[POE-04](media/POE-04.jpg) adds an actor/fence/large-monster relationship on pale
sand; [POE-02](media/POE-02.jpg) combines industrial walls, barrels and fine blue
arcs. The blue arcs leave ground-visible gaps; gold equipment, red effects and
body overlap prevent a defensible tight-body box in the primary actor example.
The circular arena’s oblique outline is an image clue, not a calibrated camera
probe. Quiet traversal and ordinary hideout/interactable views remain missing;
a barrel’s appearance does not prove breakability. No PoE2 image enters this packet.

**Grim Dawn; source rows distinguish base/AoM/FG.**
The [Crate media page](https://www.grimdawn.com/media/) supplied three HUD-equipped
combat stills. Large creatures, rock tops and spell illumination compete for ground
visibility. Actor scale differs appreciably between promotional scenes; unknown
zoom and pose prevent treating one ratio as a game-wide constant. Crate’s
[exploration guide](https://www.grimdawn.com/guide/gameplay/exploration/) supplied
[broken](media/GD-04.jpg) and [repaired](media/GD-05.jpg) Devil’s Crossing bridge views.
The bridge visibly spans the gap only in the repaired image, while the tall arch
and nearby actor retain the framing. This is concrete art/state correspondence
at two instants. It does not verify transition timing, traversal or path-cache
invalidation. The chest among standing stones has no HUD and is an object/occlusion
reference only. Original GAL-CAM video remains missing after the targeted search;
its old numeric outputs are retained history, not independently regenerated evidence.

**Last Epoch.**
All four retained source images were recovered byte-for-byte against the current
publisher listing on [Steam app 899770](https://store.steampowered.com/app/899770/).
[LE-08](media/LE-08.jpg) shows an actor beside a raised runic plinth; the monumental
floor has readable steps and sidewalls. [LE-09](media/LE-09.jpg) places gold/red
combat arcs against a green-lit floor and foreground railing. [LE-11](media/LE-11.jpg)
shows a beam beside a shore whose water highlights also compete for attention.
Additional [NPC clearing](media/LE-05.jpg), [dialog](media/LE-06.jpg), and
[opened chest](media/LE-07.jpg) examples support environment/interactable composition.
All lack the ordinary combat HUD or enter a dialog/menu state. They are admitted
for visible art relationships and **excluded from normal gameplay-camera inference**.
Menus initially returned by the screenshot API were explicitly rejected, preserved,
and labelled. The forge menu carries BETA 0.9.2; that patch label is not propagated
to other images without evidence.

## Image quantities, uncertainty and limits

The manual annotation record uses native-file coordinates. Boxes exclude weapons/effects when possible; opaque clothing and helmets
remain unavoidable visible bounds. Per-endpoint uncertainty is additive, not a
statistical confidence interval. No anatomical proportions or pixel alpha were inferred.

- D2-06: body estimate 59 px; **12.3% of the 480 px file**, or 13.7% of its
  432 px active rectangle, with conservative active interval 11.8–15.5%. Foot
  approximately (0.506, 0.537) within the active rectangle. The bottom continuous
  bar is excluded from the active denominator; its side orbs intrude farther upward.
- GD-05: body estimate 58 px, **10.1% of 576 px**, interval 9.0–11.1%. Foot
  approximately (0.500, 0.540). The HUD overlays world rendering, so the full raster
  is retained as denominator. GD-03 gives 166 px/1080 = **15.4%**, interval
  13.9–16.9%; armor and unknown zoom are material limitations, not noise to average.
- PoE-04: **tight-body height INDETERMINATE**. Gear/FX hide the top boundary.
  Approximate foot (0.502, 0.456) has ±12 px coordinate uncertainty. The separately
  noted actor-plus-gear extent cannot substitute for the required-body measure.
- LE-05/08: composition-only body estimates **12.0%/13.4%** of the publisher
  raster, with ±16 px height uncertainty. No ordinary gameplay-scale conclusion
  follows; the lower-centre actor assignment in LE-05 is provisional.

HUD footprints are explicit in the originals: D2’s continuous bottom bar and
corner globes; PoE1’s tall bottom-corner globes/action areas plus top-left status
icons; GD’s central bottom panel and top-right minimap. Last Epoch’s selected
promotion images hide this information. **A precise opaque-HUD area is unmeasured**;
a rectangle envelope would count transparent/open areas as opaque. No mask-area measurement is reported. Our diagnostic 9% strip is a proposed control, not a
reconstruction of any game’s HUD.

D2 masonry exhibits two diagonal edge families; the modern samples have exposed
floor and prop-top planes with variable local orientations. **Calibrated floor-edge
slopes, roof/shoulder proportions and view orientation cannot be reliably recovered
for every category from this selected material and are not asserted as measurements.**
Near/far scaling is UNIDENTIFIED: the different scene objects have unknown physical
sizes and heights. The broken/repaired bridge pair changes state at essentially one
view rather than moving an equal-size probe through depth. Exact metres, elevation,
FOV and camera distance for the native games remain UNIDENTIFIED.
Ordinary gameplay zoom, motion legibility, temporal occlusion, effect lifetime,
collision response, and material-driven dust/splash/decal behavior remain UNVERIFIED.
A still never licenses a motion or interaction-runtime pass.

## Recommendation and three controlled candidates

**Recommendation: B, high affine, for the first painted feasibility probe.**
This is an engineering preference: it offers more projected ground area than A
at matched central body height, while retaining one constant affine mapping for
painted floors, actor roots, prop footprints and ground effects. The native packet
supports testing both body readability and floor visibility; it does not identify
52.95° as the games’ camera angle. B’s elevation comes from the recovered PROJECT
candidate, retained to isolate affine versus perspective in B/C.

1. **A — low affine:** elevation 30°, ground compression q=0.5, yaw 47°
   (the symmetric 2:1 diamond would use 45° yaw). Tests stronger vertical-body emphasis
   and flatter ground against the same physical room. Original D2 is a useful
   flat-world comparator, but A is not claimed to recreate its exact projection.
2. **B — high affine:** elevation approximately 52.95°, q≈0.798, yaw 47°.
   More floor separation at the same projected 2 m body size, no depth scale field.
   Qualification still requires paintings and occlusion tests, especially where
   tall props hide actors and where upper-body views affect gear/head readability.
3. **C — Godot-informed perspective:** same elevation/yaw, vertical FOV≈31.79°.
   Camera distance recalibrated to match the 9.5% central body-height control.
   This is not a bit-identical recovered camera; the real [project replica](media/REPLICA-01.png)
   is separately identified. Near/far root, footprint and depicted-view compatibility
   make C a higher-risk painted-sprite candidate. The geometric study exposes this difference before runtime investment.

Held constants: 10×8 m logical chamber; actor stature/footprints; object and surface
layout; 47° yaw; 720×405 diagnostic viewport; foot anchor (about 50.1%,55.1%);
central 2 m probe at 9.5% viewport height; colors; 9% HUD reserved strip. All geometry
vertices, including vertical bodies and ground circles, use the selected projection.
Scale is applied to the whole affine world; it is not independent sprite scaling
that hides a wrong floor/actor match. The C probe’s vertical screen height varies
by ground position, including the effect of changed apparent elevation; it is
not a camera-facing billboard test. The projection code/data preserve exact operands.

D01 was presented with concrete labelled comparisons and a recommendation.
**No answer has been recorded and no visual approval inferred.** These diagrams
can choose a test preference only; no paintings have yet demonstrated the preference.

## Independent preparation and next action

The [layout draft](chamber-layout.draft.json) includes two exits, a 2.5 m doorway
in a partition, tall pillar, crate, chest, mage, larger monster, NPC and stone/soil.
[24 local checks](preparation-checks.json) passed under the predeclared
[preparation contract](PREPARATION.md): open/closed exit reachability, both actor
radii, open interaction approaches, conservative segment blocking and owner-safe
blocker removal. Three projections each passed independent homogeneous-matrix
round trips at 99 ground probes; a shifted inverse and wall-crossing straight
route were rejected. These are logical preparation results, not Godot runtime,
art/data alignment, physical collision or full G2 acceptance.

**Exact next unblocked action:** register E02 capability/data proof using this
layout, probe the installed 2D runtime version and actual alpha/import/attachment
controls, and freeze its numerical/negative controls before implementing the
chamber state pilot. Keep it local and diagnostic; generation requires its own registered limits; paid services require actual
access and spending authority. D01 preference remains
pending. G1 remains open until the eight native HUD motion segments (quiet+combat
for four games, preferably 5–10 s uncut) are inspected, along with ordinary PoE1
stronghold/interactable coverage and Last Epoch HUD framing. Before further web
search, register a changed acquisition method or obtain the missing known media;
do not restart the exhausted two-pass search unchanged.
