# ARPG Camera Specs — Diablo 2/3/4 + Path of Exile 1/2

**Commissioned by:** gandalf (design steward), 2026-06-21
**Mode:** A (analytical research)
**Purpose:** ground-truth the genre-canonical combat-camera angle/zoom so the wall-top/wizard player-perspective build uses a real ARPG camera, not the ravine traversal follow-cam (which Matt flagged: "too much behind and the character isn't centered").

---

## Headline

All five games use a **FIXED-yaw, fixed-pitch combat camera** — NOT a traversal follow-cam. The camera does not orbit, does not rotate with movement, and does not sit "behind" the character along the travel axis. The character is held **above frame-center** (camera leads slightly forward/down so more of the playfield ahead is visible). Field of view is **narrow** (telephoto-ish, 15–25°), which flattens the scene toward the 2.5D isometric read. This is the opposite of a wide-FOV third-person follow-cam.

The single biggest fix for the wall-top build: **drop FOV from 52° to ~15–25°** and **use a fixed yaw with the character placed via a forward look-offset**, not a behind-the-back follow rig.

---

## Two tiers

The genre splits into two camera families:

### Tier 1 — Overhead/isometric (Diablo 2, PoE 1, PoE 2)
- **Elevation above horizontal:** ~53–56°
- **Godot `rotation_degrees.x`:** ≈ **−34 to −37** (convention: x = elevation − 90)
- **FOV:** ~15–20° (strongly telephoto; near-orthographic read)
- **Feel:** classic flat tactical board; you read the whole engagement footprint; less verticality of props but MORE of any surface-top is visible (relevant to the void-fade illusion — a steeper look-down shows more wall TOP).

### Tier 2 — Perspective/over-the-shoulder-ish (Diablo 3, Diablo 4)
- **Elevation above horizontal:** ~40–45°
- **Godot `rotation_degrees.x`:** ≈ **−45 to −50**
- **FOV:** ~20–25°
- **Feel:** more modern, more visible prop height and depth, slightly more cinematic; the current genre-standard "Diablo feel."

### Shared across all five
- **Yaw is FIXED** (no rotation with movement). D2/PoE typically a fixed diagonal; D3/D4 a fixed forward-down.
- **No roll.**
- **Character sits ABOVE center** — roughly 30% up from the bottom of the frame; the camera "leads" forward so the player sees what's ahead, not what's behind.
- **Narrow FOV** is universal — the wide-angle look is explicitly NOT genre.

---

## Godot recommendations (for the wall-top/wizard build)

Convention: `rotation_degrees.x = elevation_above_horizontal − 90`; fixed yaw on `.y`; `projection = PERSPECTIVE`.

**Primary (Diablo 3/4 feel — recommended default):**
```
projection = PROJECTION_PERSPECTIVE
fov = 20
rotation_degrees = (-50, 45, 0)
```
Character placed lower-center via a look-at target offset **1.5–2.0 units ahead** of the hero along the camera's forward-ground vector (this is what puts the character below center and shows the playfield ahead — directly fixing "too much behind / not centered").

**PoE/D2 variant (steeper, flatter, shows more wall-top — better for the void-fade showcase):**
```
projection = PROJECTION_PERSPECTIVE
fov = 15
rotation_degrees = (-35, 45, 0)
```

The yaw of 45° is a placeholder diagonal; pick whatever fixed yaw frames the scene — the point is it is FIXED, not movement-coupled.

---

## Design tension to flag (gandalf note)

The two tiers pull in opposite directions for THIS build:
- The **steeper Tier-1 (x≈−35, ~55° elevation)** shows MORE wall-top surface → better for the void-fade "is this a wall or the edge of an infinite structure" illusion.
- The **shallower Tier-2 (x≈−50, ~40°)** is the more genre-standard modern combat feel, but shows LESS top → weaker void-fade showcase.

There is no free lunch: the angle that best sells the void-fade is slightly less "Diablo-modern" than the angle that best sells combat feel. Matt's call.

---

## Sources consulted
- Diablo 2 / Diablo 2 Resurrected camera analyses (community + remaster dev commentary on preserved camera pitch)
- Diablo 3 + Diablo 4 camera/FOV discussions (dev interviews, community FOV-mod measurements)
- Path of Exile 1 + Path of Exile 2 camera-angle community measurements (GGG fixed-camera rationale)
- General ARPG camera-design writeups on fixed-yaw isometric vs follow-cam tradeoffs

**Note:** elevation/FOV figures are convergent community measurements, not published engine values (these are closed-source); treat as well-triangulated approximations, not exact spec sheets. They are precise enough to set the Godot camera correctly.
