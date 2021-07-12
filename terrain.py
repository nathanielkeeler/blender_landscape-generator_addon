import bpy
import random
import typing
from bpy.types import Nodes
from mathutils import Vector
import os

class Terrain():
    # Szene leeren
    # bpy.ops.object.select_all(action='SELECT') # selektiert alle Objekte
    # bpy.ops.object.delete(use_global=False, confirm=False) # löscht selektierte objekte
    # bpy.ops.outliner.orphans_purge() # löscht überbleibende Meshdaten etc.

    # # Delete world nodes
    # world_nodes = bpy.data.worlds['World'].node_tree
    # for currentNode in world_nodes.nodes:
    #     world_nodes.nodes.remove(currentNode)

    
    
    def add_lighting(self):
        light_data = bpy.data.lights.new('light', type='SUN')
        light = bpy.data.objects.new('light', light_data)
        bpy.context.collection.objects.link(light)
        light.location = (10, -10, 7.5)
        light.data.energy = 1.5

    def add_sky(self):
        world = bpy.data.worlds['World']
        world.use_nodes = True

        nodes_world: typing.List[bpy.types.Node] = world.node_tree.nodes

        node_output: bpy.types.Node = nodes_world.new("ShaderNodeOutputWorld")
        node_output.location = Vector((200, 300))

        node_background: bpy.types.Node = nodes_world.new("ShaderNodeBackground")
        node_background.location = Vector((0, 300))
        node_background.inputs[1].default_value = 0.2

        # add HDRI image
        node_env_tex: bpy.types.Node = nodes_world.new("ShaderNodeTexEnvironment")
        node_env_tex.location = Vector((-400, 300))
        hdr_image: bpy.types.Image = bpy.data.images.load(
            os.path.dirname(os.path.realpath(__file__)).replace(
                'terrain.blend',
                'resources\\hdr\\flower_road_2k.hdr'
            )
        )
        node_env_tex.image = hdr_image
        
        node_map: bpy.types.Node = nodes_world.new("ShaderNodeMapping")
        node_map.location = Vector((-700, 300))
        node_map.inputs[1].default_value[2] = 0.2
        
        node_tex_coord: bpy.types.Node = nodes_world.new("ShaderNodeTexCoord")
        node_tex_coord.location = Vector((-900, 300))

        # Links
        links = world.node_tree.links
        links.new(node_background.outputs[0], node_output.inputs[0])
        links.new(node_env_tex.outputs[0], node_background.inputs[0])
        links.new(node_map.outputs[0], node_env_tex.inputs[0])
        links.new(node_tex_coord.outputs[0], node_map.inputs[0])

        # Ray Settings
        world.light_settings.use_ambient_occlusion = True
        world.cycles_visibility.diffuse = True
        world.cycles_visibility.glossy = True
        world.cycles_visibility.transmission = True
        world.cycles_visibility.scatter = True

    def generate_terrain(self):
        bpy.context.scene.render.engine = 'CYCLES'

        bpy.ops.mesh.primitive_plane_add(size=(20))
        plane = bpy.context.object

        mod_terrain = plane.modifiers.new("t_subsurf", "SUBSURF")
        mod_terrain.subdivision_type = 'SIMPLE'
        mod_terrain.levels = 5
        mod_terrain.render_levels = 6

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
        node_pbsdf.location = Vector((-250, -200))

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
            # color ramp (left) 3
        node_color_ramp_3: bpy.types.Node = nodes_terrain.new("ShaderNodeValToRGB")
        node_color_ramp_3.location = Vector((-2400, 300))
        node_color_ramp_3.color_ramp.interpolation = 'EASE'
            # color ramp (left) 4
        node_color_ramp_4: bpy.types.Node = nodes_terrain.new("ShaderNodeValToRGB")
        node_color_ramp_4.location = Vector((-2400, -1300))
        node_color_ramp_4.color_ramp.interpolation = 'EASE'
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
            # Rock Texture Nude
        node_rock_tex: bpy.types.Node = nodes_terrain.new("ShaderNodeTexImage")
        image_rock: bpy.types.Image = bpy.data.images.load(
            os.path.dirname(os.path.realpath(__file__)).replace(
                'terrain.blend',
                'resources\\textures\\rock\\TexturesCom_Rock_Cliff3_2x2_512_albedo.tif'
            )
        )
        node_rock_tex.image = image_rock
        node_rock_tex.location = Vector((-1800, -350))

            # mix_rgb node
        node_rock_mix_rgb: bpy.types.Node = nodes_terrain.new("ShaderNodeMixRGB")
        node_rock_mix_rgb.location = Vector((-1450, -550))

            # connect texture to mix rgb
        mat_terrain.node_tree.links.new(node_rock_tex.outputs[0], node_rock_mix_rgb.inputs[1])


            # add rock roughness texture node
        node_rock_roughness_tex: bpy.types.Node = nodes_terrain.new("ShaderNodeTexImage")
        image_rock_roughness: bpy.types.Image = bpy.data.images.load(
            os.path.dirname(os.path.realpath(__file__)).replace(
                'terrain.blend',
                'resources\\textures\\rock\\TexturesCom_Rock_Cliff3_2x2_512_roughness.tif'
            )
        )
        image_rock_roughness.colorspace_settings.name = 'Non-Color'
        node_rock_roughness_tex.image = image_rock_roughness
        node_rock_roughness_tex.location = Vector((-1800, -900))

            # mix_rgb node
        node_rock_mix_rgb_1: bpy.types.Node = nodes_terrain.new("ShaderNodeMixRGB")
        node_rock_mix_rgb_1.location = Vector((-1450, -1000))

            # connect texture to mix rgb and pbsdf
        mat_terrain.node_tree.links.new(node_rock_roughness_tex.outputs[0], node_rock_mix_rgb_1.inputs[1])


            # add rock normal map texture node
        node_rock_normal_tex: bpy.types.Node = nodes_terrain.new("ShaderNodeTexImage")
        image_rock_normal: bpy.types.Image = bpy.data.images.load(
            os.path.dirname(os.path.realpath(__file__)).replace(
                'terrain.blend',
                'resources\\textures\\rock\\TexturesCom_Rock_Cliff3_2x2_512_normal.tif'
            )
        )
        image_rock_normal.colorspace_settings.name = 'Non-Color'
        node_rock_normal_tex.image = image_rock_normal
        node_rock_normal_tex.location = Vector((-1800, -1500))

            # mix_rgb node
        node_rock_mix_rgb_2: bpy.types.Node = nodes_terrain.new("ShaderNodeMixRGB")
        node_rock_mix_rgb_2.location = Vector((-1450, -1300))

            # normal map node
        node_normal_map: bpy.types.Node = nodes_terrain.new("ShaderNodeNormalMap")
        node_normal_map.location = Vector((-550, -1190))
        node_normal_map.inputs[0].default_value = 10

            # connect texture to mix rgb, that to normal map node and that to pbsdf
        mat_terrain.node_tree.links.new(node_rock_normal_tex.outputs[0], node_rock_mix_rgb_2.inputs[1])

            # add mapping and tex_coordinate node to connect to all three textures
        node_tex_coord_1: bpy.types.Node = nodes_terrain.new("ShaderNodeTexCoord")
        node_tex_coord_1.location = Vector((-2250, -900))

        node_map_1: bpy.types.Node = nodes_terrain.new("ShaderNodeMapping")
        node_map_1.location = Vector((-2050, -900))
        node_map_1.inputs[3].default_value[0] = 30
        node_map_1.inputs[3].default_value[1] = 30


        mat_terrain.node_tree.links.new(node_tex_coord_1.outputs[2], node_map_1.inputs[0])
        mat_terrain.node_tree.links.new(node_map_1.outputs[0], node_rock_roughness_tex.inputs[0])
        mat_terrain.node_tree.links.new(node_map_1.outputs[0], node_rock_normal_tex.inputs[0])
        mat_terrain.node_tree.links.new(node_map_1.outputs[0], node_rock_tex.inputs[0])


        # Nodes: Texture (Moss)
            # add moss texture node
        node_moss_tex: bpy.types.Node = nodes_terrain.new("ShaderNodeTexImage")
        image_moss: bpy.types.Image = bpy.data.images.load(
            os.path.dirname(os.path.realpath(__file__)).replace(
                'terrain.blend',
                'resources\\textures\\moss\\TexturesCom_Nature_Moss_512_albedo.tif'
            )
        )
        node_moss_tex.image = image_moss
        node_moss_tex.location = Vector((-1800, -630))

            # connect map node to texture to mix rgb
        mat_terrain.node_tree.links.new(node_map_1.outputs[0], node_moss_tex.inputs[0])
        mat_terrain.node_tree.links.new(node_moss_tex.outputs[0], node_rock_mix_rgb.inputs[2])

            # add moss roughness texture node
        node_moss_roughness_tex: bpy.types.Node = nodes_terrain.new("ShaderNodeTexImage")
        image_moss_roughness: bpy.types.Image = bpy.data.images.load(
            os.path.dirname(os.path.realpath(__file__)).replace(
                'terrain.blend',
                'resources\\textures\\moss\\TexturesCom_Nature_Moss_512_roughness.tif'
            )
        )
        image_moss_roughness.colorspace_settings.name = 'Non-Color'
        node_moss_roughness_tex.image = image_moss_roughness
        node_moss_roughness_tex.location = Vector((-1800, -1200))
            
            # connect map node to normal texture to mix rgb
        mat_terrain.node_tree.links.new(node_map_1.outputs[0], node_moss_roughness_tex.inputs[0])
        mat_terrain.node_tree.links.new(node_moss_roughness_tex.outputs[0], node_rock_mix_rgb_1.inputs[2])


            # add moss normal_map texture node
        node_moss_normal_tex: bpy.types.Node = nodes_terrain.new("ShaderNodeTexImage")
        image_moss_normal: bpy.types.Image = bpy.data.images.load(
            os.path.dirname(os.path.realpath(__file__)).replace(
                'terrain.blend',
                'resources\\textures\\moss\\TexturesCom_Nature_Moss_512_normal.tif'
            )
        )
        image_moss_normal.colorspace_settings.name = 'Non-Color'
        node_moss_normal_tex.image = image_moss_normal
        node_moss_normal_tex.location = Vector((-1800, -1800))
            
            # connect map node to normal texture to mix rgb
        mat_terrain.node_tree.links.new(node_map_1.outputs[0], node_moss_normal_tex.inputs[0])
        mat_terrain.node_tree.links.new(node_moss_normal_tex.outputs[0], node_rock_mix_rgb_2.inputs[2])


        # Nodes: Geometry (for separating moss and rock)
            # add geometry node
        node_geometry: bpy.types.Node = nodes_terrain.new("ShaderNodeNewGeometry")
        node_geometry.location = Vector((-2550, -500))

            # add normal node
        node_normal: bpy.types.Node = nodes_terrain.new("ShaderNodeNormal")
        node_normal.location = Vector((-2350, -500))
            
            # add color ramp node
        node_moss_vs_rock: bpy.types.Node = nodes_terrain.new("ShaderNodeValToRGB")
        node_moss_vs_rock.location = Vector((-2120, -500))
        node_moss_vs_rock.color_ramp.elements[0].position = 0.8
        node_moss_vs_rock.color_ramp.elements[1].position = 0.9

            # connect that shit to eachother
        mat_terrain.node_tree.links.new(node_geometry.outputs[1], node_normal.inputs[0])
        mat_terrain.node_tree.links.new(node_normal.outputs[1], node_moss_vs_rock.inputs[0])
        mat_terrain.node_tree.links.new(node_moss_vs_rock.outputs[0], node_rock_mix_rgb.inputs[0])
        mat_terrain.node_tree.links.new(node_moss_vs_rock.outputs[0], node_rock_mix_rgb_1.inputs[0])
        mat_terrain.node_tree.links.new(node_moss_vs_rock.outputs[0], node_rock_mix_rgb_2.inputs[0])


        # Nodes: Texture (Sand)
            # add sand texture node
        node_sand_tex: bpy.types.Node = nodes_terrain.new("ShaderNodeTexImage")
        image_sand: bpy.types.Image = bpy.data.images.load(
            os.path.dirname(os.path.realpath(__file__)).replace(
                'terrain.blend',
                'resources\\textures\\sand\\TexturesCom_Ground_SandDesert1_3x3_512_albedo.tif'
            )
        )
        node_sand_tex.image = image_sand
        node_sand_tex.location = Vector((-1250, -400))

            # mix_rgb node
        node_sand_mix_rgb: bpy.types.Node = nodes_terrain.new("ShaderNodeMixRGB")
        node_sand_mix_rgb.location = Vector((-900, -400))

            # connect them
        mat_terrain.node_tree.links.new(node_rock_mix_rgb.outputs[0], node_sand_mix_rgb.inputs[2])
        mat_terrain.node_tree.links.new(node_sand_tex.outputs[0], node_sand_mix_rgb.inputs[1])
        mat_terrain.node_tree.links.new(node_sand_mix_rgb.outputs[0], node_pbsdf.inputs[0])

            # add sand roughness_map texture node
        node_sand_roughness_tex: bpy.types.Node = nodes_terrain.new("ShaderNodeTexImage")
        image_sand_roughness: bpy.types.Image = bpy.data.images.load(
            os.path.dirname(os.path.realpath(__file__)).replace(
                'terrain.blend',
                'resources\\textures\\sand\\TexturesCom_Ground_SandDesert1_3x3_512_roughness.tif'
            )
        )
        image_sand_roughness.colorspace_settings.name = 'Non-Color'
        node_sand_roughness_tex.image = image_sand_roughness
        node_sand_roughness_tex.location = Vector((-1250, -900))

            # mix_rgb node
        node_sand_mix_rgb_1: bpy.types.Node = nodes_terrain.new("ShaderNodeMixRGB")
        node_sand_mix_rgb_1.location = Vector((-900, -900))

            # connect nodes
        mat_terrain.node_tree.links.new(node_sand_roughness_tex.outputs[0], node_sand_mix_rgb_1.inputs[1])
        mat_terrain.node_tree.links.new(node_rock_mix_rgb_1.outputs[0], node_sand_mix_rgb_1.inputs[2])
        mat_terrain.node_tree.links.new(node_sand_mix_rgb_1.outputs[0], node_pbsdf.inputs[8])

            # add sand normal_map texture node
        node_sand_normal_tex: bpy.types.Node = nodes_terrain.new("ShaderNodeTexImage")
        image_sand_normal: bpy.types.Image = bpy.data.images.load(
            os.path.dirname(os.path.realpath(__file__)).replace(
                'terrain.blend',
                'resources\\textures\\sand\\TexturesCom_Ground_SandDesert1_3x3_512_normal.tif'
            )
        )
        image_sand_normal.colorspace_settings.name = 'Non-Color'
        node_sand_normal_tex.image = image_sand_normal
        node_sand_normal_tex.location = Vector((-1250, -1300))

            # mix_rgb node
        node_sand_mix_rgb_2: bpy.types.Node = nodes_terrain.new("ShaderNodeMixRGB")
        node_sand_mix_rgb_2.location = Vector((-900, -1300))

            # connect nodes
        mat_terrain.node_tree.links.new(node_normal_map.outputs[0], node_pbsdf.inputs[20])
        mat_terrain.node_tree.links.new(node_rock_mix_rgb_2.outputs[0], node_sand_mix_rgb_2.inputs[2])
        mat_terrain.node_tree.links.new(node_sand_normal_tex.outputs[0], node_sand_mix_rgb_2.inputs[1])
        mat_terrain.node_tree.links.new(node_sand_mix_rgb_2.outputs[0], node_normal_map.inputs[1])

            # connect mapping node to sand textures
        mat_terrain.node_tree.links.new(node_map_1.outputs[0], node_sand_roughness_tex.inputs[0])
        mat_terrain.node_tree.links.new(node_map_1.outputs[0], node_sand_normal_tex.inputs[0])
        mat_terrain.node_tree.links.new(node_map_1.outputs[0], node_sand_tex.inputs[0])

            # separate sand from other textures
        mat_terrain.node_tree.links.new(node_color_ramp_4.outputs[0], node_sand_mix_rgb.inputs[0])
        mat_terrain.node_tree.links.new(node_color_ramp_4.outputs[0], node_sand_mix_rgb_1.inputs[0])
        mat_terrain.node_tree.links.new(node_color_ramp_4.outputs[0], node_sand_mix_rgb_2.inputs[0])

            # adjust sand levels
        node_color_ramp_4.color_ramp.elements[0].position = 0.34
        node_color_ramp_4.color_ramp.elements[1].position = 0.38



        # Append Material to Plane
        plane.data.materials.append(mat_terrain)
            


t = terrain()    
t.generate_terrain()
t.add_lighting()
t.add_sky()