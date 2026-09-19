extends Node2D
# F-C7-1 TRUE SHAPE: null instance, VALID method, down a dispatch branch never taken.
func dispatch(mode: String) -> void:
    var child: Node2D = null
    if mode == "branch_never_taken":
        child.set_modulate(Color(1, 1, 1, 1))
