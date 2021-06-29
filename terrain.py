import bpy
import random
import typing
from mathutils import Vector

class terrain():
    # Szene leeren
    bpy.ops.object.select_all(action='SELECT') # selektiert alle Objekte
    bpy.ops.object.delete(use_global=False, confirm=False) # löscht selektierte objekte
    bpy.ops.outliner.orphans_purge() # löscht überbleibende Meshdaten etc.

    def generate_terrain(self):
        bpy.context.scene.render.engine = 'CYCLES'

        bpy.ops.mesh.primitive_plane_add(size=(6))
        plane = bpy.context.object

        mod_terrain = plane.modifiers.new("t_subsurf", "SUBSURF")
        mod_terrain.subdivision_type = 'SIMPLE'
        mod_terrain.levels = 6
        mod_terrain.render_levels = 6

        mat_terrain: bpy.types.Material = bpy.data.materials.new("t_material")
        mat_terrain.cycles.displacement_method = 'BOTH'

        mat_terrain.use_nodes = True

        # Create and access nodes
        nodes_terrain: typing.List[bpy.types.Node] = mat_terrain.node_tree.nodes

        node_terrain_type: bpy.types.Node = nodes_terrain.new("ShaderNodeTexNoise")
        node_terrain_type.location = Vector((-350, 200))

        node_terrain_displace: bpy.types.Node = nodes_terrain.new("ShaderNodeDisplacement")
        node_terrain_displace.location = Vector((130, 200))

        node_color_ramp: bpy.types.Node = nodes_terrain.new("ShaderNodeValToRGB")
        node_color_ramp.location = Vector((-150, 200))

        node_pbsdf: bpy.types.Node =  nodes_terrain["Principled BSDF"]
        node_pbsdf.location = Vector((-650, 300))

        node_output: bpy.types.Node =  nodes_terrain["Material Output"]

        # Variables
        scale = random.uniform(2, 3)
        distortion = random.uniform(-1, 1)
        detail = 7.5
        detail_roughness = 0.3

        # Modify node values
        node_terrain_type.inputs[2].default_value = scale
        node_terrain_type.inputs[3].default_value = detail
        node_terrain_type.inputs[4].default_value = detail_roughness
        node_terrain_type.inputs[5].default_value = distortion

        displace_scale = random.uniform(0.3, 0.4)

        node_terrain_displace.inputs[2].default_value = displace_scale

        bpy.data.materials["t_material"].node_tree.nodes["ColorRamp"].color_ramp.elements[0].position = random.uniform(0.4, 0.5)
        bpy.data.materials["t_material"].node_tree.nodes["ColorRamp"].color_ramp.elements[1].position = random.uniform(0.5, 0.6)

        # Combine nodes
        mat_terrain.node_tree.links.new(node_pbsdf.outputs[0], node_output.inputs[0])
        mat_terrain.node_tree.links.new(node_terrain_type.outputs[1], node_color_ramp.inputs[0])
        mat_terrain.node_tree.links.new(node_color_ramp.outputs[0], node_terrain_displace.inputs[0])
        mat_terrain.node_tree.links.new(node_terrain_displace.outputs[0], node_output.inputs[2])

        plane.data.materials.append(mat_terrain)      

t = terrain()    
t.generate_terrain()