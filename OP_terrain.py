import bpy
import random
import typing
from mathutils import Vector

class Object_OT_generate_terrain(bpy.types.Operator):
    """Landscape Generator"""
    bl_idname = "mesh.generate_terrain"
    bl_label = "generate_terrain"
    bl_options = {'REGISTER', 'UNDO'}


    # Properties

    terrain_size : bpy.props.IntProperty(
        name='Terrain size',
        description='Size of the terrain plane.',
        default=25,
        min=4,
        soft_max=60
    )

    scale : bpy.props.FloatProperty(
        name='Terrain density',
        description='Scaling of the terrain texture density.',
        default=random.uniform(1.5, 2.5),
        min=0,
        soft_min=1,
        soft_max=10
    )

    distortion : bpy.props.FloatProperty(
        name='Terrain distortion',
        description='Amount of distortion for the terrain texture.',
        default=random.uniform(0, 2),
        min=0,
        soft_max=4
    )

    detail : bpy.props.FloatProperty(
        name='Terrain detail',
        description='Amount of detail for the terrain texture.',
        default=16,
        min=0,
        soft_max=16
    )

    detail_roughness : bpy.props.FloatProperty(
        name='Terrain detail roughness',
        description='Amount of roughness to details.',
        default=0.3,
        min=0,
        soft_max=0.5
    )

    displace_scale : bpy.props.FloatProperty(
        name='Terrain scale',
        description='Scaling of the terrain height.',
        default=random.uniform(1.5, 3),
        min=0,
        soft_max=4
    )

    random_noise : bpy.props.FloatProperty(
        name='Randomness',
        description='Amount of distortion for the terrain texture.',
        default=1,
        min=0
    )
    
    color_ramp_black : bpy.props.FloatProperty(
        name='Terrain steepness',
        description='Amount of distortion for the terrain texture.',
        default=random.uniform(0.3, 0.4),
        soft_min=0.2,
        soft_max=0.5
    )

    color_ramp_white : bpy.props.FloatProperty(
        name='Terrain steepness',
        description='Amount of distortion for the terrain texture.',
        default=random.uniform(0.5, 0.6),
        soft_min=0.5,
        soft_max=0.7
    )


    def execute(self, context):

        bpy.ops.outliner.orphans_purge()
            # add light
        light_data = bpy.data.lights.new('light', type='SUN')
        light = bpy.data.objects.new('light', light_data)
        bpy.context.collection.objects.link(light)
        light.location = (10, -10, 7.5)
        light.data.energy = 1.5

        
        # add HDR
            # delete world nodes
        world_nodes = bpy.data.worlds['World'].node_tree
        for currentNode in world_nodes.nodes:
            world_nodes.nodes.remove(currentNode)
        
        world = bpy.data.worlds['World']
        world.use_nodes = True

        nodes_world: typing.List[bpy.types.Node] = world.node_tree.nodes

        node_output: bpy.types.Node = nodes_world.new("ShaderNodeOutputWorld")
        node_output.location = Vector((200, 300))

        node_background: bpy.types.Node = nodes_world.new("ShaderNodeBackground")
        node_background.location = Vector((0, 300))
        node_background.inputs[1].default_value = 0.1

        bpy.ops.image.open(directory="//resources//hdr//",files=[{"name":"flower_road_2k.hdr", "name":"flower_road_2k.hdr"}], relative_path=True)

        node_env_tex: bpy.types.Node = nodes_world.new("ShaderNodeTexEnvironment")
        node_env_tex.location = Vector((-400, 300))
        node_env_tex.image = bpy.data.images["flower_road_2k.hdr"]
        
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



        # TERRAIN!

        # Variables
            # Terrain Form
        # terrain_size = 25
        # scale = random.uniform(1.5, 2.5)
        # distortion = random.uniform(-1, 1)
        # detail = 16
        # detail_roughness = 0.3
        # displace_scale = random.uniform(1.5, 3)
        # random_noise = 1
        # color_ramp_black = random.uniform(0.3, 0.4)
        # color_ramp_white = random.uniform(0.5, 0.6)
        
        bpy.context.scene.render.engine = 'CYCLES'

        bpy.ops.mesh.primitive_plane_add(size=self.terrain_size)
        plane = bpy.context.object
        plane.name="Landscape"

        mod_terrain = plane.modifiers.new("t_subsurf", "SUBSURF")
        mod_terrain.subdivision_type = 'SIMPLE'
        mod_terrain.levels = 5
        mod_terrain.render_levels = 6

        # Set smooth shading
        bpy.context.object.data.polygons.foreach_set('use_smooth',  [True] * len(bpy.context.object.data.polygons))

        mat_terrain: bpy.types.Material = bpy.data.materials.new("t_material")
        mat_terrain.cycles.displacement_method = 'BOTH'

        mat_terrain.use_nodes = True

        # Nodes: Terrain Form
        nodes_terrain: typing.List[bpy.types.Node] = mat_terrain.node_tree.nodes
        
        node_output: bpy.types.Node =  nodes_terrain["Material Output"]

            #
        node_terrain_displace: bpy.types.Node = nodes_terrain.new("ShaderNodeDisplacement")
        node_terrain_displace.location = Vector((130, 200))
        node_terrain_displace.inputs[2].default_value = self.displace_scale

            #
        node_color_ramp: bpy.types.Node = nodes_terrain.new("ShaderNodeValToRGB")
        node_color_ramp.location = Vector((-2400, 800))
        node_color_ramp.color_ramp.interpolation = 'EASE'
        node_color_ramp.color_ramp.elements[0].position = self.color_ramp_black
        node_color_ramp.color_ramp.elements[1].position = self.color_ramp_white

            #
        node_terrain_type: bpy.types.Node = nodes_terrain.new("ShaderNodeTexNoise")
        node_terrain_type.location = Vector((-2600, 800))
        node_terrain_type.inputs[2].default_value = self.scale
        node_terrain_type.inputs[3].default_value = self.detail
        node_terrain_type.inputs[4].default_value = self.detail_roughness
        node_terrain_type.inputs[5].default_value = self.distortion

            #
        node_map: bpy.types.Node = nodes_terrain.new("ShaderNodeMapping")
        node_map.location = Vector((-2800, 800))
        node_map.inputs[1].default_value[1] = self.random_noise

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


        # Nodes: Texture (Water)
            # color ramp (left) 2
        node_color_ramp_2: bpy.types.Node = nodes_terrain.new("ShaderNodeValToRGB")
        node_color_ramp_2.location = Vector((-1300, 1700))
        node_color_ramp_2.color_ramp.interpolation = 'EASE'
        node_color_ramp_2.color_ramp.elements[0].position = 0.351
        node_color_ramp_2.color_ramp.elements[1].position = 0.365
            # color ramp (left) 3
        node_color_ramp_3: bpy.types.Node = nodes_terrain.new("ShaderNodeValToRGB")
        node_color_ramp_3.location = Vector((-900, -100))
        node_color_ramp_3.color_ramp.interpolation = 'CARDINAL'
        node_color_ramp_3.color_ramp.elements[0].position = 0.357
        node_color_ramp_3.color_ramp.elements[1].position = 0.369
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
        node_water_gloss.inputs[0].default_value = (0.236871, 0.292942, 0.504464, 1)


            # Mix Shader
        node_mix_shader: bpy.types.Node = nodes_terrain.new("ShaderNodeMixShader")
        node_mix_shader.location = Vector((-100, 800))

            # connect gloss, color_ramp and pbsdf shaders to mix shader and mix shader to output
        mat_terrain.node_tree.links.new(node_water_level.outputs[0], node_mix_shader.inputs[0])
        mat_terrain.node_tree.links.new(node_pbsdf.outputs[0], node_mix_shader.inputs[2])
        mat_terrain.node_tree.links.new(node_mix_shader.outputs[0], node_output.inputs[0])
        

        # Nodes: Texture (Rock)
            # load images for rock
        bpy.ops.image.open(directory="//resources//textures//rock//",files=[{"name":"TexturesCom_Rock_Cliff3_2x2_512_albedo.tif", "name":"TexturesCom_Rock_Cliff3_2x2_512_albedo.tif"}, {"name":"TexturesCom_Rock_Cliff3_2x2_512_roughness.tif", "name":"TexturesCom_Rock_Cliff3_2x2_512_roughness.tif"}, {"name":"TexturesCom_Rock_Cliff3_2x2_512_normal.tif", "name":"TexturesCom_Rock_Cliff3_2x2_512_normal.tif"}], relative_path=True)
            
            # Rock Texture Node
        node_rock_tex: bpy.types.Node = nodes_terrain.new("ShaderNodeTexImage")
        node_rock_tex.image = bpy.data.images["TexturesCom_Rock_Cliff3_2x2_512_albedo.tif"]
        node_rock_tex.location = Vector((-1800, -350))

            # mix_rgb node
        node_rock_mix_rgb: bpy.types.Node = nodes_terrain.new("ShaderNodeMixRGB")
        node_rock_mix_rgb.location = Vector((-1450, -550))

            # connect texture to mix rgb
        mat_terrain.node_tree.links.new(node_rock_tex.outputs[0], node_rock_mix_rgb.inputs[1])


            # add rock roughness texture node
        node_rock_roughness_tex: bpy.types.Node = nodes_terrain.new("ShaderNodeTexImage")
        node_rock_roughness_tex.image = bpy.data.images["TexturesCom_Rock_Cliff3_2x2_512_roughness.tif"]
        node_rock_roughness_tex.image.colorspace_settings.name = 'Non-Color'
        node_rock_roughness_tex.location = Vector((-1800, -900))

            # mix_rgb node
        node_rock_mix_rgb_1: bpy.types.Node = nodes_terrain.new("ShaderNodeMixRGB")
        node_rock_mix_rgb_1.location = Vector((-1450, -1000))

            # connect texture to mix rgb and pbsdf
        mat_terrain.node_tree.links.new(node_rock_roughness_tex.outputs[0], node_rock_mix_rgb_1.inputs[1])


            # add rock normal map texture node
        node_rock_normal_tex: bpy.types.Node = nodes_terrain.new("ShaderNodeTexImage")
        node_rock_normal_tex.image = bpy.data.images["TexturesCom_Rock_Cliff3_2x2_512_normal.tif"]
        node_rock_normal_tex.image.colorspace_settings.name = 'Non-Color'
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
            # load textures
        bpy.ops.image.open(directory="//resources//textures//moss//",files=[{"name":"TexturesCom_Nature_Moss_512_albedo.tif", "name":"TexturesCom_Nature_Moss_512_albedo.tif"}, {"name":"TexturesCom_Nature_Moss_512_roughness.tif", "name":"TexturesCom_Nature_Moss_512_roughness.tif"}, {"name":"TexturesCom_Nature_Moss_512_normal.tif", "name":"TexturesCom_Nature_Moss_512_normal.tif"}], relative_path=True)

            # add moss texture node
        node_moss_tex: bpy.types.Node = nodes_terrain.new("ShaderNodeTexImage")
        node_moss_tex.image = bpy.data.images["TexturesCom_Nature_Moss_512_albedo.tif"]
        node_moss_tex.location = Vector((-1800, -630))

            # connect map node to texture to mix rgb
        mat_terrain.node_tree.links.new(node_map_1.outputs[0], node_moss_tex.inputs[0])
        mat_terrain.node_tree.links.new(node_moss_tex.outputs[0], node_rock_mix_rgb.inputs[2])

            # add moss roughness texture node
        node_moss_roughness_tex: bpy.types.Node = nodes_terrain.new("ShaderNodeTexImage")
        node_moss_roughness_tex.image = bpy.data.images["TexturesCom_Nature_Moss_512_roughness.tif"]
        node_moss_roughness_tex.image.colorspace_settings.name = 'Non-Color'
        node_moss_roughness_tex.location = Vector((-1800, -1200))
            
            # connect map node to normal texture to mix rgb
        mat_terrain.node_tree.links.new(node_map_1.outputs[0], node_moss_roughness_tex.inputs[0])
        mat_terrain.node_tree.links.new(node_moss_roughness_tex.outputs[0], node_rock_mix_rgb_1.inputs[2])


            # add moss normal_map texture node
        node_moss_normal_tex: bpy.types.Node = nodes_terrain.new("ShaderNodeTexImage")
        node_moss_normal_tex.image = bpy.data.images["TexturesCom_Nature_Moss_512_normal.tif"]
        node_moss_normal_tex.image.colorspace_settings.name = 'Non-Color'
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

            # load textures
        bpy.ops.image.open(directory="//resources//textures//sand//",files=[{"name":"TexturesCom_Ground_SandDesert1_3x3_512_albedo.tif", "name":"TexturesCom_Ground_SandDesert1_3x3_512_albedo.tif"}, {"name":"TexturesCom_Ground_SandDesert1_3x3_512_roughness.tif", "name":"TexturesCom_Ground_SandDesert1_3x3_512_roughness.tif"}, {"name":"TexturesCom_Ground_SandDesert1_3x3_512_normal.tif", "name":"TexturesCom_Ground_SandDesert1_3x3_512_normal.tif"}], relative_path=True)

            # add sand texture node
        node_sand_tex: bpy.types.Node = nodes_terrain.new("ShaderNodeTexImage")
        node_sand_tex.image = bpy.data.images["TexturesCom_Ground_SandDesert1_3x3_512_albedo.tif"]
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
        node_sand_roughness_tex.image = bpy.data.images["TexturesCom_Ground_SandDesert1_3x3_512_roughness.tif"]
        node_sand_roughness_tex.image.colorspace_settings.name = 'Non-Color'
        node_sand_roughness_tex.location = Vector((-1250, -900))

            # mix_rgb node
        node_sand_mix_rgb_1: bpy.types.Node = nodes_terrain.new("ShaderNodeMixRGB")
        node_sand_mix_rgb_1.location = Vector((-900, -900))

            # connect nodes
        mat_terrain.node_tree.links.new(node_sand_roughness_tex.outputs[0], node_sand_mix_rgb_1.inputs[1])
        mat_terrain.node_tree.links.new(node_rock_mix_rgb_1.outputs[0], node_sand_mix_rgb_1.inputs[2])

            # add sand normal_map texture node
        node_sand_normal_tex: bpy.types.Node = nodes_terrain.new("ShaderNodeTexImage")
        node_sand_normal_tex.image = bpy.data.images["TexturesCom_Ground_SandDesert1_3x3_512_normal.tif"]
        node_sand_normal_tex.image.colorspace_settings.name = 'Non-Color'
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

        # Nodes: Texture (Water Foam)
        node_pbsdf_1: bpy.types.Node = nodes_terrain.new("ShaderNodeBsdfPrincipled")
        node_pbsdf_1.location = Vector((-700, 2000))

        node_mix_shader_1: bpy.types.Node = nodes_terrain.new("ShaderNodeMixShader")
        node_mix_shader_1.location = Vector((-300, 1500))

            # connect both nodes
        mat_terrain.node_tree.links.new(node_pbsdf_1.outputs[0], node_mix_shader_1.inputs[2])
        mat_terrain.node_tree.links.new(node_water_gloss.outputs[0], node_mix_shader_1.inputs[1])
        mat_terrain.node_tree.links.new(node_mix_shader_1.outputs[0], node_mix_shader.inputs[1])
        mat_terrain.node_tree.links.new(node_color_ramp_2.outputs[0], node_mix_shader_1.inputs[0])

            # bump node for foam texture
        node_bump: bpy.types.Node = nodes_terrain.new("ShaderNodeBump")
        node_bump.location = Vector((-1000, 1600))

            # connect to pbsdf and color ramp_2
        mat_terrain.node_tree.links.new(node_color_ramp_2.outputs[0], node_bump.inputs[2])
        mat_terrain.node_tree.links.new(node_bump.outputs[0], node_pbsdf_1.inputs[20])

            # bump node for foam texture
        node_bump_1: bpy.types.Node = nodes_terrain.new("ShaderNodeBump")
        node_bump_1.location = Vector((-1000, 1300))

            # bump node for foam texture
        node_noise_tex: bpy.types.Node = nodes_terrain.new("ShaderNodeTexNoise")
        node_noise_tex.location = Vector((-1200, 1300))

            # connect nodes
        mat_terrain.node_tree.links.new(node_noise_tex.outputs[0], node_bump_1.inputs[2])
        mat_terrain.node_tree.links.new(node_bump_1.outputs[0], node_water_gloss.inputs[2])

            # water surface
        node_map_2: bpy.types.Node = nodes_terrain.new("ShaderNodeMapping")
        node_map_2.location = Vector((-1400, 1300))
        node_map_2.inputs[3].default_value[1] = 30
        node_map_2.inputs[3].default_value[0] = 30


        node_tex_coord_2: bpy.types.Node = nodes_terrain.new("ShaderNodeTexCoord")
        node_tex_coord_2.location = Vector((-1600, 1300))

            # connect to noise tex
        mat_terrain.node_tree.links.new(node_tex_coord_2.outputs[0], node_map_2.inputs[0])
        mat_terrain.node_tree.links.new(node_map_2.outputs[0], node_noise_tex.inputs[0])

            # dark sand near water
        node_dark_sand_mix_rgb: bpy.types.Node = nodes_terrain.new("ShaderNodeMixRGB")
        node_dark_sand_mix_rgb.location = Vector((-600, -400))
        node_dark_sand_mix_rgb.blend_type = 'MULTIPLY'
        node_dark_sand_mix_rgb.inputs[0].default_value = 0.85
        
        node_dark_sand_mix_rgb_1: bpy.types.Node = nodes_terrain.new("ShaderNodeMixRGB")
        node_dark_sand_mix_rgb_1.location = Vector((-600, -700))
        node_dark_sand_mix_rgb_1.blend_type = 'MULTIPLY'

            # connect to pbsdf
        mat_terrain.node_tree.links.new(node_sand_mix_rgb.outputs[0], node_dark_sand_mix_rgb.inputs[1])
        mat_terrain.node_tree.links.new(node_sand_mix_rgb_1.outputs[0], node_dark_sand_mix_rgb_1.inputs[1])
        mat_terrain.node_tree.links.new(node_dark_sand_mix_rgb.outputs[0], node_pbsdf.inputs[0])
        mat_terrain.node_tree.links.new(node_dark_sand_mix_rgb_1.outputs[0], node_pbsdf.inputs[7])

            # connect color ramp_3
        mat_terrain.node_tree.links.new(node_color_ramp_3.outputs[0], node_dark_sand_mix_rgb.inputs[2])
        mat_terrain.node_tree.links.new(node_color_ramp_3.outputs[0], node_dark_sand_mix_rgb_1.inputs[2])

        # Append Material to Plane
        plane.data.materials.append(mat_terrain)


        return {'FINISHED'}

class VIEW3D_PT_landscape_generator(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Landscape Gen"
    bl_label = "Properties"

    def draw(self,context):
        self.layout.operator(
            'mesh.generate_terrain', text='Generate Landscape', icon='OUTLINER_OB_IMAGE'
        )

def mesh_add_menu_draw(self, context):
    self.layout.operator(
        'mesh.generate_terrain', text='Generate Landscape', icon='OUTLINER_OB_IMAGE'
    )


def register():
    bpy.utils.register_class(Object_OT_generate_terrain)
    bpy.utils.register_class(VIEW3D_PT_landscape_generator)
    bpy.types.VIEW3D_MT_mesh_add.append(mesh_add_menu_draw)

def unregister():
    bpy.utils.unregister_class(Object_OT_generate_terrain)
    bpy.utils.unregister_class(VIEW3D_PT_landscape_generator)
    bpy.types.VIEW3D_MT_mesh_add.remove(mesh_add_menu_draw)

if __name__ == '__main__':
    register()