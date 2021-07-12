import bpy
import random


class Tree():
    def __init__(self):
        self.generateTree()


    '''bpy.ops.object.select_all(action='SELECT') # selektiert alle Objekte
    bpy.ops.object.delete(use_global=False, confirm=False) # löscht selektierte objekte
    bpy.ops.outliner.orphans_purge() # löscht überbleibende Meshdaten etc.'''
    
    verts = [(0,0,0),(0,0,0.002),(0.02,-0.02, 0.32),(0, -0 , 0.6),( 0.17, 0.15, 0.86),(0.42, 0.13, 1.04),(0.02,0.31,1.06),(-0.3,0 ,0.8),(-0.39,0.15,0.95),( -0.46,-0.11,0.98),( 0,-0.36,0.91),(-0.09, -0.52, 1.06),( 0.18,-0.43,1.08)]
    edges = [(0,1), (1,2), (2,3), (3,4),(4,5), (4,6), (3,7), (7,8),(7,9), (3,10), (10,11), (10,12)]
    tree_size = 1
    posX = 0
    posY=0
    posZ = 0

    def treeTrunk(self,trunk):
        for i, vert in enumerate(trunk.data.skin_vertices[0].data):    
            #vert.radius = 1/(i+0.5), 1/(i+0.5)
            branch = [5,6,8,9,11,12]
            if i == 0:
                vert.radius = 0.15,0.15  
            elif i <= 2:
                vert.radius =0.1/(i+0.05), 0.1/(i+0.05)
            elif i == 5 or i ==6 or i==8 or i == 9 or i==11 or i==12:
                vert.radius =0.01,0.01
            else:
                vert.radius = 0.03,0.03 
        return trunk
        
        
    def treeLeaves(self, branches):#Tree Leaves 
        leaves = []
        for i in range(6):
            randomSize = random.uniform(0.21,0.33)
            bpy.ops.mesh.primitive_ico_sphere_add(radius=randomSize, enter_editmode=True, location=(branches[i]), scale=(1, 1, 1))
            
            bpy.ops.transform.vertex_random(offset=0.05)
            bpy.ops.object.mode_set(mode = 'OBJECT')
            
            cur_leave = bpy.context.object
            
            leaves.append(cur_leave)
        
        for cur_leave in leaves:
            cur_leave.select_set(True)
            
        bpy.ops.object.join()
            
        leave =bpy.context.object
        modifier_array=leave.modifiers.new("Leaf Array","ARRAY")#Erster Name selber angeben
        modifier_array.use_relative_offset = False
        modifier_array.use_constant_offset = False
        
        for obj in bpy.context.selected_objects:
            obj.name = "Leaves"
        
    def clear(self,mat):
        node_to_delete =  mat.node_tree.nodes['Principled BSDF']
        mat.node_tree.nodes.remove( node_to_delete )
        node_to_delete =  mat.node_tree.nodes['Material Output']
        mat.node_tree.nodes.remove( node_to_delete )
        
    def trunk_material(self):
        trunk_mat = bpy.data.materials.new("Trunk Material")
        trunk_mat.use_nodes = True
        self.clear(trunk_mat)
        
        object_color = (0.0946259, 0.0571663, 0.0229202, 1) #hier farbe ändern
 

        nodes = trunk_mat.node_tree.nodes
        links = trunk_mat.node_tree.links
        output = nodes.new( type = 'ShaderNodeOutputMaterial' )
        diffuse = nodes.new( type = 'ShaderNodeBsdfDiffuse' )
        link = links.new( diffuse.outputs['BSDF'], output.inputs['Surface'] )
        diffuse.inputs[0].default_value = object_color
        return trunk_mat
    
    def leaves_material(self):
        leaves_mat = bpy.data.materials.new("Leaves Material")
        leaves_mat.use_nodes = True
        self.clear(leaves_mat)
        
        object_color = (0.01, 0.4, 0.01, 1)#Hier Farbe ändern

        nodes = leaves_mat.node_tree.nodes
        links = leaves_mat.node_tree.links
        output = nodes.new( type = 'ShaderNodeOutputMaterial' )
        diffuse = nodes.new( type = 'ShaderNodeBsdfDiffuse' )
        link = links.new( diffuse.outputs['BSDF'], output.inputs['Surface'] )
        diffuse.inputs[0].default_value = object_color
        return leaves_mat
    
    def generateTree(self):

        mesh = bpy.data.meshes.new("Tree")
        object = bpy.data.objects.new("Tree", mesh)

        bpy.context.collection.objects.link(object)
    
        mesh.from_pydata(self.verts,[],self.edges)
        mesh.update(calc_edges=True)

        mod_skin: bpy.types.SkinModifier = object.modifiers.new("Tree Skin Modifier", "SKIN")
        mod_subsurf: bpy.types.SubsurfModifier = object.modifiers.new("Tree Subsurf Modifier", "SUBSURF")
        
        branches = [self.verts[5],self.verts[6],self.verts[8],self.verts[9],self.verts[11],self.verts[12]]
        
        trunk = bpy.data.objects["Tree"]
        trunk_mat = self.trunk_material()#farbe aufrufen
        trunk = self.treeTrunk(trunk)
        trunk.data.materials.append(trunk_mat)#textur zuweisen
        trunk.scale = self.tree_size,self.tree_size,self.tree_size
        trunk.location = self.posX,self.posY,self.posZ
        #trunk ende
        #leaves anfang
        leaves = self.treeLeaves(branches)
        leaves = bpy.data.objects["Leaves"]
        leaves_mat = self.leaves_material()
        leaves.data.materials.append(leaves_mat) #leaves durch treetop ersetzen hehe
        leaves.scale = self.tree_size,self.tree_size,self.tree_size
        leaves.location = self.posX+self.tree_size/4,-self.tree_size/4+self.posY,self.posZ+self.tree_size


        '''treeArray = []
        treeArray.append(trunk)
        treeArray.append(leaves)

        for p in treeArray:
            p.select_set(True)
            p.select_set(True)
        bpy.ops.object.join()
        for obj in bpy.context.selected_objects:
            obj.name = "TreeTree"'''

