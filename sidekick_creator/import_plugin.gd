@tool
class_name SidekickCreatorScenePostImportPlugin extends EditorScenePostImportPlugin

var path: String

func _pre_process(scene: Node) -> void:
	if not path.begins_with(ProjectSettings.get_setting(SidekickCreatorPlugin.setting_sidekick_root)):
		return

	var subresources: Dictionary = get_option_value("_subresources")
	var opt = subresources.get_or_add("nodes", {}).get_or_add("PATH:Skeleton3D", {})
	opt["retarget/bone_map"] = load(ProjectSettings.get_setting(SidekickCreatorPlugin.setting_bone_map))
	opt["retarget/bone_renamer/unique_node/skeleton_name"] = ProjectSettings.get_setting(SidekickCreatorPlugin.setting_skeleton_name)

func _post_process(scene: Node) -> void:
	path = ""

func _get_import_options(p_path: String) -> void:
	path = p_path
