"""Load the installed MCP add-on into a fresh Blender session, without saving preferences."""
import importlib.util
import sys
from pathlib import Path
import bpy

ROOT = Path(__file__).resolve().parents[1]
addon_path = next((ROOT / '.venv/lib').glob('python*/site-packages/blender_mcp/bundled/addon.py'))
spec = importlib.util.spec_from_file_location('wizard_blender_mcp', addon_path)
addon = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = addon
spec.loader.exec_module(addon)
addon.register()
if getattr(bpy.types, 'blendermcp_server', None):
    bpy.types.blendermcp_server.stop()
bpy.context.scene.blendermcp_auto_start_server = False
bpy.context.scene.blendermcp_use_polyhaven = False
bpy.context.scene.blendermcp_use_hyper3d = False
bpy.types.wizard_mcp_server = addon.BlenderMCPServer(host='127.0.0.1', port=9877)
bpy.types.wizard_mcp_server.start()
print('WIZARD_MCP_READY port=9877', flush=True)
