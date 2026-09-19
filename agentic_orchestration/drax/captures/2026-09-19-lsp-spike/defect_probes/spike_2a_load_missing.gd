extends Node2D
# F-C7-2 TRUE SHAPE: runtime load() of a res:// the kit never emits.
func fetch() -> Resource:
    return load("res://vfx/lightning_blast_e3/materials/Additive.tres")
