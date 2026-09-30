extends "res://scripts/knight.gd"
## C-9 VFX BAKE-OFF, LANE B -- HIM, STANDING BY (the barbarian, knight.gd unchanged): the Meteor's
## fire must light "nearby dynamic things (her, him)", so he stands near the impact. He reads no
## input -- her keys must not move him too -- and holds his idle where the scene puts him. drax.

func _physics_process(dt: float) -> void:
	drive_dir(Vector2.ZERO, false, dt)
