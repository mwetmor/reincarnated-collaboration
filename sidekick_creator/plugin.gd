@tool
class_name SidekickCreatorPlugin extends EditorPlugin

var import_plugin: SidekickCreatorScenePostImportPlugin

const setting_bone_map = "addons/sidekick_creator/bone_map"
const setting_skeleton_name = "addons/sidekick_creator/skeleton_name"

const setting_sidekick_root = "addons/sidekick_creator/sidekick_root"
const setting_sidekick_root_default = "res://Assets/Synty/SidekickCharacters/"

func _enter_tree():
	import_plugin = SidekickCreatorScenePostImportPlugin.new()
	add_scene_post_import_plugin(import_plugin)

	if not ProjectSettings.has_setting(setting_bone_map):
		ProjectSettings.set_setting(setting_bone_map, "res://addons/sidekick_creator/sidekick_bone_map.tres")
	ProjectSettings.add_property_info({
		"name": setting_bone_map,
		"type": TYPE_STRING,
		"usage": PROPERTY_USAGE_DEFAULT | PROPERTY_USAGE_EDITOR,
		"hint": PROPERTY_HINT_FILE,
		"hint_string": "*.res,*.tres",
	})
	ProjectSettings.set_initial_value(setting_bone_map, "res://addons/sidekick_creator/sidekick_bone_map.tres")

	if not ProjectSettings.has_setting(setting_skeleton_name):
		ProjectSettings.set_setting(setting_skeleton_name, "GeneralSkeleton")
	ProjectSettings.add_property_info({
		"name": setting_skeleton_name,
		"type": TYPE_STRING,
		"usage": PROPERTY_USAGE_DEFAULT | PROPERTY_USAGE_EDITOR
	})
	ProjectSettings.set_initial_value(setting_skeleton_name, "GeneralSkeleton")


	if not ProjectSettings.has_setting(setting_sidekick_root):
		ProjectSettings.set_setting(setting_sidekick_root, setting_sidekick_root_default)
	ProjectSettings.add_property_info({
		"name": setting_sidekick_root,
		"type": TYPE_STRING,
		"hint": PROPERTY_HINT_DIR,
		"usage": PROPERTY_USAGE_DEFAULT | PROPERTY_USAGE_EDITOR
	})
	ProjectSettings.set_initial_value(setting_sidekick_root, setting_sidekick_root_default)

func _exit_tree():
	remove_scene_post_import_plugin(import_plugin)
