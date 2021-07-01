import bpy
import random
import typing
import math

class pine():

    bpy.ops.object.select_all(action='SELECT') # selektiert alle Objekte
    bpy.ops.object.delete(use_global=False, confirm=False) # löscht selektierte objekte
    bpy.ops.outliner.orphans_purge() # löscht überbleibende Meshdaten etc.

    verts = [(0,0,-0.02),(0,0,0.02),(0,0,0.15),(0.02,0,0.3),(0,0.01,0.45),(0.01,0,0.6),(0,0,0.75),(0,0,0.9),(0,0.01,1)]
    edges = [(0,1), (1,2), (2,3), (3,4),(4,5), (5,6) ,(6,7),(7,8)]
    
    pine_size = 1
    posX = 0
    posY = 0
    posZ = 0
        
    def pineNeedles(self): 
        pine_needles = []
        for i in range(len(self.verts)):
            randomSize = random.uniform(0.21,0.33)
            if i >= 2 and i <= len(self.verts) - 3:
                bpy.ops.mesh.primitive_cone_add(vertices=12, radius1 = 0.5-(i/15), depth=0.5-(i/20), location=(self.verts[1+i]), scale=(1, 1, 1))
                num = random.randint(0,2)
                randomRot = random.uniform(0,0.1)
                bpy.context.object.rotation_euler[num] = randomRot
                cur_needle = bpy.context.object
                pine_needles.append(cur_needle)
            elif i >= len(self.verts) - 3 and i <= len(self.verts) - 2:
                bpy.ops.mesh.primitive_cone_add(vertices=12, radius1 = 0.5-(i/15), depth=0.5-(i/17), location=(self.verts[1+i]), scale=(1, 1, 1))
                num = random.randint(0,2)
                randomRot = random.uniform(0,0.1)
                bpy.context.object.rotation_euler[num] = randomRot
                cur_needle = bpy.context.object
                pine_needles.append(cur_needle)
        
        for cur_needle in pine_needles:
            cur_needle.select_set(True)
            
        bpy.ops.object.join()
            
        needle =bpy.context.object
        modifier_array=needle.modifiers.new("Needle Array","ARRAY")#Erster Name selber angeben
        modifier_array.use_relative_offset = False
        modifier_array.use_constant_offset = False
        
        for obj in bpy.context.selected_objects:
            obj.name = "Needles"
        
    def pineTrunk(self,trunk):

        bpy.context.view_layer.objects.active = trunk
    
        for i, vert in enumerate(trunk.data.skin_vertices[0].data):
            if i == 0:
                vert.radius = 0.1,0.1  
            else:
                vert.radius =0.07/(i+0.05), 0.07/(i+0.05)  
        return trunk 
    
    def clear(self,mat):
        node_to_delete =  mat.node_tree.nodes['Principled BSDF']
        mat.node_tree.nodes.remove( node_to_delete )
        node_to_delete =  mat.node_tree.nodes['Material Output']
        mat.node_tree.nodes.remove( node_to_delete )           
    
    
    def trunk_material(self):
        trunk_mat = bpy.data.materials.new("Trunk Material")
        trunk_mat.use_nodes = True
        self.clear(trunk_mat)
        
        object_color = (0.0270712, 0.0173909, 0.00806169, 1) #hier farbe ändern

        nodes = trunk_mat.node_tree.nodes
        links = trunk_mat.node_tree.links
        output = nodes.new( type = 'ShaderNodeOutputMaterial' )
        diffuse = nodes.new( type = 'ShaderNodeBsdfDiffuse' )
        link = links.new( diffuse.outputs['BSDF'], output.inputs['Surface'] )
        diffuse.inputs[0].default_value = object_color
        return trunk_mat  
    
    def needle_material(self):
        needle_mat = bpy.data.materials.new("Needles Material")
        needle_mat.use_nodes = True
        self.clear(needle_mat)
        
        object_color = (0.00302355, 0.0578026, 0.00302355, 1)#Hier Farbe ändern

        nodes = needle_mat.node_tree.nodes
        links = needle_mat.node_tree.links
        output = nodes.new( type = 'ShaderNodeOutputMaterial' )
        diffuse = nodes.new( type = 'ShaderNodeBsdfDiffuse' )
        link = links.new( diffuse.outputs['BSDF'], output.inputs['Surface'] )
        diffuse.inputs[0].default_value = object_color
        return needle_mat    

    def generatePine(self):
        
        num_needles = len(self.verts)
        
        mesh = bpy.data.meshes.new("Trunk")
        object = bpy.data.objects.new("Trunk", mesh)

        bpy.context.collection.objects.link(object)
 
        mesh.from_pydata(self.verts,[],self.edges)
        mesh.update(calc_edges=True)

        mod_skin: bpy.types.SkinModifier = object.modifiers.new("Pine Skin Modifier", "SKIN")
        mod_subsurf: bpy.types.SubsurfModifier = object.modifiers.new("Pine Subsurf Modifier", "SUBSURF")
        
        trunk = bpy.data.objects["Trunk"]
        trunk_mat = self.trunk_material()
        trunk = self.pineTrunk(trunk)
        trunk.data.materials.append(trunk_mat) 
        #größe
        trunk.scale = self.pine_size,self.pine_size,self.pine_size
        trunk.location = self.posX, self.posY, self.posZ 
        
        needles = self.pineNeedles()
        needles = bpy.data.objects["Needles"]
        needle_mat = self.needle_material()
        needles.data.materials.append(needle_mat)
        #größe
        needles.scale = self.pine_size,self.pine_size,self.pine_size
        needles.location = self.posX, self.posY, self.posZ + self.pine_size
        
        
t = pine()
t.generatePine()
