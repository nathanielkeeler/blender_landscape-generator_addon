import bpy
import random
import typing
from bpy.types import Nodes
from mathutils import Vector
import os

class terrain():
    # Szene leeren
    bpy.ops.object.select_all(action='SELECT') # selektiert alle Objekte
    bpy.ops.object.delete(use_global=False, confirm=False) # löscht selektierte objekte
    bpy.ops.outliner.orphans_purge() # löscht überbleibende Meshdaten etc.

    # Delete world nodes
    world_nodes = bpy.data.worlds['World'].node_tree
    for currentNode in world_nodes.nodes:
        world_nodes.nodes.remove(currentNode)

    
    
    def add_lighting(self):
        light_data = bpy.data.lights.new('light', type='SUN')
        light = bpy.data.objects.new('light', light_data)
        bpy.context.collection.objects.link(light)
        light.location = (7.5, 7.5, 7.5)
        light.data.energy = 1.5

    def add_sky(self):
        world = bpy.data.worlds['World']
        world.use_nodes = True

        nodes_world: typing.List[bpy.types.Node] = world.node_tree.nodes

        node_output: bpy.types.Node = nodes_world.new("ShaderNodeOutputWorld")
        node_output.location = Vector((200, 300))

        node_background: bpy.types.Node = nodes_world.new("ShaderNodeBackground")
        node_background.location = Vector((0, 300))

        # Color Node
        node_sky: bpy.types.Node = nodes_world.new("ShaderNodeValToRGB")
        node_sky.location = Vector((-300, 300))
        node_sky.color_ramp.interpolation = 'B_SPLINE'
        node_sky.color_ramp.elements.new(0.1)
        node_sky.color_ramp.elements[0].position = 0.13
        node_sky.color_ramp.elements[0].color = (0.062, 0.14, 0.38, 1)
        node_sky.color_ramp.elements[1].color = (0.14, 0.23, 0.5, 1)
        node_sky.color_ramp.elements[1].position = 0.27
        node_sky.color_ramp.elements[2].position = 0.48

        node_gradient: bpy.types.Node = nodes_world.new("ShaderNodeTexGradient")
        node_gradient.location = Vector((-500, 300))
        
        node_map: bpy.types.Node = nodes_world.new("ShaderNodeMapping")
        node_map.location = Vector((-700, 300))
        node_map.inputs[1].default_value[0] = 0.2
        node_map.inputs[2].default_value[1] = -1.5708
        
        node_tex_coord: bpy.types.Node = nodes_world.new("ShaderNodeTexCoord")
        node_tex_coord.location = Vector((-900, 300))

        # Links
        links = world.node_tree.links
        links.new(node_background.outputs[0], node_output.inputs[0])
        links.new(node_sky.outputs[0], node_background.inputs[0])
        links.new(node_gradient.outputs[1], node_sky.inputs[0])
        links.new(node_map.outputs[0], node_gradient.inputs[0])
        links.new(node_tex_coord.outputs[0], node_map.inputs[0])

        # Ray Settings
        world.cycles_visibility.scatter = False
        world.cycles_visibility.transmission = False
        world.cycles_visibility.glossy = False
        world.cycles_visibility.diffuse = False

    def generate_terrain(self):
        bpy.context.scene.render.engine = 'CYCLES'

        bpy.ops.mesh.primitive_plane_add(size=(20))
        plane = bpy.context.object

        mod_terrain = plane.modifiers.new("t_subsurf", "SUBSURF")
        mod_terrain.subdivision_type = 'SIMPLE'
        mod_terrain.levels = 5
        mod_terrain.render_levels = 5

        # Set smooth shading
        bpy.context.object.data.polygons.foreach_set('use_smooth',  [True] * len(bpy.context.object.data.polygons))

        mat_terrain: bpy.types.Material = bpy.data.materials.new("t_material")
        mat_terrain.cycles.displacement_method = 'BOTH'

        mat_terrain.use_nodes = True

        # Variables
            # Terrain Form
        scale = random.uniform(1.5, 2.5)
        distortion = random.uniform(-1, 1)
        detail = 7.5
        detail_roughness = 0.3
        displace_scale = random.uniform(1.5, 3)
        random_noise = random.uniform(0.1, 1)
        color_ramp_black = random.uniform(0.3, 0.4)
        color_ramp_white = random.uniform(0.5, 0.6)

        # Nodes: Terrain Form
        nodes_terrain: typing.List[bpy.types.Node] = mat_terrain.node_tree.nodes
        
        node_output: bpy.types.Node =  nodes_terrain["Material Output"]

            #
        node_terrain_displace: bpy.types.Node = nodes_terrain.new("ShaderNodeDisplacement")
        node_terrain_displace.location = Vector((130, 200))
        node_terrain_displace.inputs[2].default_value = displace_scale

            #
        node_color_ramp: bpy.types.Node = nodes_terrain.new("ShaderNodeValToRGB")
        node_color_ramp.location = Vector((-2400, 800))
        node_color_ramp.color_ramp.interpolation = 'EASE'
        node_color_ramp.color_ramp.elements[0].position = color_ramp_black
        node_color_ramp.color_ramp.elements[1].position = color_ramp_white

            #
        node_terrain_type: bpy.types.Node = nodes_terrain.new("ShaderNodeTexNoise")
        node_terrain_type.location = Vector((-2600, 800))
        node_terrain_type.inputs[2].default_value = scale
        node_terrain_type.inputs[3].default_value = detail
        node_terrain_type.inputs[4].default_value = detail_roughness
        node_terrain_type.inputs[5].default_value = distortion

            #
        node_map: bpy.types.Node = nodes_terrain.new("ShaderNodeMapping")
        node_map.location = Vector((-2800, 800))
        node_map.inputs[1].default_value[1] = random_noise

            #
        node_tex_coord: bpy.types.Node = nodes_terrain.new("ShaderNodeTexCoord")
        node_tex_coord.location = Vector((-3000, 800))
        
            #
        node_pbsdf: bpy.types.Node =  nodes_terrain["Principled BSDF"]
        node_pbsdf.location = Vector((-600, -200))

            # Combine nodes
        mat_terrain.node_tree.links.new(node_terrain_displace.outputs[0], node_output.inputs[2])
        mat_terrain.node_tree.links.new(node_color_ramp.outputs[0], node_terrain_displace.inputs[0])
        mat_terrain.node_tree.links.new(node_terrain_type.outputs[1], node_color_ramp.inputs[0])
        mat_terrain.node_tree.links.new(node_map.outputs[0], node_terrain_type.inputs[0])
        mat_terrain.node_tree.links.new(node_tex_coord.outputs[0], node_map.inputs[0])
        mat_terrain.node_tree.links.new(node_pbsdf.outputs[0], node_output.inputs[0])

        

        # Variables
            # Textures


        # Nodes: Texture (Water)
            # color ramp (left) 2
        node_color_ramp_2: bpy.types.Node = nodes_terrain.new("ShaderNodeValToRGB")
        node_color_ramp_2.location = Vector((-2400, 550))
        node_color_ramp_2.color_ramp.interpolation = 'EASE'
        node_color_ramp_2.color_ramp.elements[0].position = color_ramp_black
        node_color_ramp_2.color_ramp.elements[1].position = color_ramp_white
            # color ramp (left) 3
        node_color_ramp_3: bpy.types.Node = nodes_terrain.new("ShaderNodeValToRGB")
        node_color_ramp_3.location = Vector((-2400, 300))
        node_color_ramp_3.color_ramp.interpolation = 'EASE'
        node_color_ramp_3.color_ramp.elements[0].position = color_ramp_black
        node_color_ramp_3.color_ramp.elements[1].position = color_ramp_white
            # color ramp (left) 4
        node_color_ramp_4: bpy.types.Node = nodes_terrain.new("ShaderNodeValToRGB")
        node_color_ramp_4.location = Vector((-2400, 50))
        node_color_ramp_4.color_ramp.interpolation = 'EASE'
        node_color_ramp_4.color_ramp.elements[0].position = color_ramp_black
        node_color_ramp_4.color_ramp.elements[1].position = color_ramp_white
            # color ramp (left) 5
        node_water_level: bpy.types.Node = nodes_terrain.new("ShaderNodeValToRGB")
        node_water_level.location = Vector((-700, 850))
        node_water_level.color_ramp.interpolation = 'CONSTANT'
        node_water_level.color_ramp.elements[0].position = 0
        node_water_level.color_ramp.elements[1].position = 0.355 # changes water level height

            # connect noise texture to color ramp
        mat_terrain.node_tree.links.new(node_terrain_type.outputs[1], node_color_ramp_2.inputs[0])
        mat_terrain.node_tree.links.new(node_terrain_type.outputs[1], node_color_ramp_3.inputs[0])
        mat_terrain.node_tree.links.new(node_terrain_type.outputs[1], node_color_ramp_4.inputs[0])
        mat_terrain.node_tree.links.new(node_terrain_type.outputs[1], node_water_level.inputs[0])

            

            # water gloss
        node_water_gloss: bpy.types.Node = nodes_terrain.new("ShaderNodeBsdfGlossy")
        node_water_gloss.location = Vector((-600, 1200))
        node_water_gloss.inputs[1].default_value = 0.045

            # Mix Shader
        node_mix_shader: bpy.types.Node = nodes_terrain.new("ShaderNodeMixShader")
        node_mix_shader.location = Vector((-100, 800))

            # connect gloss, color_ramp and pbsdf shaders to mix shader and mix shader to output
        mat_terrain.node_tree.links.new(node_water_level.outputs[0], node_mix_shader.inputs[0])
        mat_terrain.node_tree.links.new(node_water_gloss.outputs[0], node_mix_shader.inputs[1])
        mat_terrain.node_tree.links.new(node_pbsdf.outputs[0], node_mix_shader.inputs[2])
        mat_terrain.node_tree.links.new(node_mix_shader.outputs[0], node_output.inputs[0])
        
        # Nodes: Texture (Rock)
        path = os.path.dirname(os.path.abspath(__file__))

        # Append Material to Plane
        plane.data.materials.append(mat_terrain)
            


t = terrain()    
t.generate_terrain()
t.add_lighting()
t.add_sky()