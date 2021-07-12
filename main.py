import bpy

import terrain

from .assets import pine
from .assets import tree
from .assets import house


terrain.generate_terrain()

#pine.Pine()
#tree.Tree()


# bpy.ops.mesh.primitive_plane_add(size=20)
# #terrain = bpy.context.object

# bpy.ops.object.mode_set(mode = 'EDIT')
# bpy.ops.mesh.subdivide(number_cuts=9)#-1
# bpy.ops.object.mode_set(mode = 'OBJECT')

# #Partikelsystem hinzufügen cubes
# bpy.ops.object.particle_system_add()
# particle = terrain.particle_systems.active
# particle.name= 'Cubes'
# particle.settings.type = 'HAIR'
# particle.settings.hair_length = 0.5
# particle.settings.render_type = 'OBJECT'
# house.House()
# blockhouse = bpy.data.objects["Blockhouse"] 
# blockhouse.location[2] = -100

# bpy.context.scene.tool_settings.use_transform_data_origin = True
# bpy.context.scene.tool_settings.snap_elements = {'VERTEX'}
# bpy.ops.transform.translate(value=(0, -0.25, -0.35), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
# bpy.context.scene.tool_settings.use_transform_data_origin = False


# particle.settings.instance_object = blockhouse
# particle.settings.particle_size = 1
# #particle.settings.rotation_mode = 'GLOB_Y'
# particle.settings.count = 60
# particle.settings.use_advanced_hair = True
# particle.settings.use_rotations = True
# particle.settings.rotation_mode = 'GLOB_X'