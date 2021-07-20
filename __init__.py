bl_info = {
    "name": "Landscape Generator",
    "author": "Nathaniel Keeler, Maren Röttele",
    "blender": (2,92,0),
    "version": (1,0),
    "category": "Mesh",
    "location": "Add > Mesh > Generate Landscape or VIEW3D > UI Panel > Landscape Gen",
    "description": "Adds a generated landscape to the scene.",
    "url": "https://github.com/nathanielkeeler/Umgebungsgenerator"
}


import bpy
from .OP_terrain import Object_OT_generate_terrain, VIEW3D_PT_landscape_generator

class landscape_generator(bpy.types.Operator):
    """The Tooltip"""
    bl_idname = "mesh.generate_landscape"
    bl_label = "generate_landscape"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        Object_OT_generate_terrain()
        VIEW3D_PT_landscape_generator()

        return {'FINISHED'}


def register():
    bpy.utils.register_class(landscape_generator)
    bpy.utils.register_class(Object_OT_generate_terrain)
    bpy.utils.register_class(VIEW3D_PT_landscape_generator)
    bpy.types.VIEW3D_MT_mesh_add.append(OP_terrain.mesh_add_menu_draw)

def unregister():
    bpy.utils.unregister_class(landscape_generator)
    bpy.utils.unregister_class(Object_OT_generate_terrain)
    bpy.utils.unregister_class(VIEW3D_PT_landscape_generator)
    bpy.types.VIEW3D_MT_mesh_add.remove(OP_terrain.mesh_add_menu_draw)