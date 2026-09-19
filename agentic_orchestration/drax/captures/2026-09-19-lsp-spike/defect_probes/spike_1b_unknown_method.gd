extends Node2D
# ADJACENT SHAPE: unknown method on a typed var, down a branch never taken.
func dispatch(mode: String) -> void:
    var child: Node2D = Node2D.new()
    if mode == "branch_never_taken":
        child.definitely_not_a_method_on_node2d()
