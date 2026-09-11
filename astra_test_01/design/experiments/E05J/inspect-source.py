import bpy,json
from pathlib import Path
col=bpy.data.collections['Wizard_Character'];meshes=[o for o in col.objects if o.type=='MESH'];mats={m.name:m for o in meshes for m in o.data.materials if m};rows=[]
for name,m in mats.items():
 bs=m.node_tree.nodes.get('Principled BSDF')if m.use_nodes else None
 rows.append({'name':name,'base_color_links':[(l.from_node.name,l.from_socket.name)for l in bs.inputs['Base Color'].links]if bs else None,'images':[{'node':n.name,'name':n.image.name if n.image else None,'size':list(n.image.size)if n.image else None,'vector_links':[(l.from_node.bl_idname,l.from_node.name,l.from_socket.name)for l in n.inputs['Vector'].links]}for n in m.node_tree.nodes if n.bl_idname=='ShaderNodeTexImage']if m.use_nodes else []})
print(json.dumps({'meshes':len(meshes),'source_vertices':sum(len(o.data.vertices)for o in meshes),'materials':rows,'armature_preserve_volume':[(o.name,m.use_deform_preserve_volume)for o in meshes[:3]for m in o.modifiers if m.type=='ARMATURE']},indent=2))
