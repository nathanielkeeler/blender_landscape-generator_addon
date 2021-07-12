import bpy
import math


class House():
    def __init__(self):
        self.generateHouse()

    '''bpy.ops.object.select_all(action='SELECT') # selektiert alle Objekte
    bpy.ops.object.delete(use_global=False, confirm=False) # löscht selektierte objekte
    bpy.ops.outliner.orphans_purge() # löscht überbleibende Meshdaten etc.'''
    
    height = 1#nicht verändern
    width_Y = 1.5
    width_X = 1.4
    num_wood_logs = 7
    log_radius = height/num_wood_logs
    roof_overhang = log_radius*3
    posX = 0
    posY = 0
    posZ = 0
    house_size = 0.5
        
    def create_door(self):#Tree Leaves 
        doorArray = []
        bpy.ops.mesh.primitive_cube_add(size=1, location=(self.posX+self.width_X/2+(self.log_radius/2 /1.75),self.posY+ self.width_Y/4, self.posZ+(self.height/1.3)/2), scale=(1, 1, 1))
        bpy.context.object.scale= (self.log_radius,self.width_Y/4.5, self.height/1.3)
        for obj in bpy.context.selected_objects:
            obj.name = "Doorframe"
        frame = bpy.data.objects["Doorframe"]    
        frame_mat = self.roof_material()
        frame.data.materials.append(frame_mat)
        doorArray.append(frame)
        
        bpy.ops.mesh.primitive_uv_sphere_add(radius =1,segments=16, ring_count=16, location=(self.width_X/2+self.log_radius*1.05+ self.posX, self.posY+self.width_Y/3.75+(self.width_Y/6)/4,self.posZ+ (self.height/1.3)/2), scale=(1, 1, 1))
        bpy.context.object.scale= (self.log_radius/7,self.log_radius/7, self.log_radius/7)
        for obj in bpy.context.selected_objects:
            obj.name = "Dooropener"
        opener = bpy.data.objects["Dooropener"]    
        opener_mat = self.steel_material()
        opener.data.materials.append(opener_mat)
        doorArray.append(opener)
        
        bpy.ops.mesh.primitive_cube_add(size=1, location=(self.posX+self.width_X/2+(self.log_radius/2.5), self.posY+self.width_Y/4, self.posZ+(self.height/1.4)/2), scale=(1, 1, 1))
        bpy.context.object.scale= (self.log_radius,self.width_Y/6, self.height/1.4)
        for obj in bpy.context.selected_objects:
            obj.name = "Door"
        door = bpy.data.objects["Door"]    
        door_mat = self.roof_material()
        door.data.materials.append(door_mat)
        doorArray.append(door)
        
        for door in doorArray:
            opener.select_set(True)
            frame.select_set(True)
            door.select_set(True)
        bpy.ops.object.join()
        door = bpy.data.objects["Door"] 
        return door
    '''def createWindows(self):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0.5, 0, self.height), scale=(1, 1, 1))
        bpy.context.object.display_type = 'WIRE'   
        return bpy.context.object '''
    def clear(self,mat):
        node_to_delete =  mat.node_tree.nodes['Principled BSDF']
        mat.node_tree.nodes.remove( node_to_delete )
        node_to_delete =  mat.node_tree.nodes['Material Output']
        mat.node_tree.nodes.remove( node_to_delete )
    
    def base_material(self):
        base_mat = bpy.data.materials.new("Trunk Material")
        base_mat.use_nodes = True
        self.clear(base_mat)
        
        object_color = (0.0732357, 0.0446962, 0.0183669, 1)
 #hier farbe ändern
 

        nodes = base_mat.node_tree.nodes
        links = base_mat.node_tree.links
        output = nodes.new( type = 'ShaderNodeOutputMaterial' )
        diffuse = nodes.new( type = 'ShaderNodeBsdfDiffuse' )
        link = links.new( diffuse.outputs['BSDF'], output.inputs['Surface'] )
        diffuse.inputs[0].default_value = object_color
        return base_mat
    
    def steel_material(self):
        steel_mat = bpy.data.materials.new("Steel Material")
        steel_mat.use_nodes = True
        self.clear(steel_mat)
        object_color = (0.0871402, 0.0756772, 0.0826101, 1)

        nodes = steel_mat.node_tree.nodes
        links = steel_mat.node_tree.links
        output = nodes.new( type = 'ShaderNodeOutputMaterial' )
        diffuse = nodes.new( type = 'ShaderNodeBsdfDiffuse' )
        link = links.new( diffuse.outputs['BSDF'], output.inputs['Surface'] )
        diffuse.inputs[0].default_value = object_color     
        return steel_mat
    
    def roof_material(self):
        roof_mat = bpy.data.materials.new("Trunk Material")
        roof_mat.use_nodes = True
        self.clear(roof_mat)
        
        object_color = (0.0310635, 0.0197552, 0.00890669, 1)
 #hier farbe ändern

        nodes = roof_mat.node_tree.nodes
        links = roof_mat.node_tree.links
        output = nodes.new( type = 'ShaderNodeOutputMaterial' )
        diffuse = nodes.new( type = 'ShaderNodeBsdfDiffuse' )
        link = links.new( diffuse.outputs['BSDF'], output.inputs['Surface'] )
        diffuse.inputs[0].default_value = object_color
        return roof_mat
    
    def generateHouse(self):
        #bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0,self.height/2), scale=(1, 1, 1))
        #bpy.context.object.scale = (self.width_X,self.width_Y, self.height)
        #bpy.ops.object.modifier_add(type='SOLIDIFY')
        #bpy.context.object.modifiers["Solidify"].thickness = 0.14
        woodlogs = []
        i=0
        for i in range(self.num_wood_logs*4):

            if i <self.num_wood_logs:
                bpy.ops.mesh.primitive_cylinder_add(vertices=6, location=(self.posX+self.width_X/2, self.posY, self.posZ+i*(self.log_radius)+(self.log_radius/2)), scale=(1, 1, 1))
                bpy.context.object.scale= (self.log_radius/2,self.log_radius/2, self.width_Y/2+(self.log_radius/2)*2)
                cur_log = bpy.context.object
                woodlogs.append(cur_log)
            elif i>self.num_wood_logs-1 and i<=self.num_wood_logs*2-1:
                bpy.ops.mesh.primitive_cylinder_add(vertices=6, location=(-self.width_X/2+self.posX, self.posY, self.posZ+i*(self.log_radius)-(self.height-(self.log_radius/2))), scale=(1, 1, 1))
                bpy.context.object.scale= (self.log_radius/2,self.log_radius/2, self.width_Y/2+(self.log_radius/2)*2)
                cur_log = bpy.context.object
                woodlogs.append(cur_log)
            elif i>self.num_wood_logs*2-1 and i<=self.num_wood_logs*3-1:
                bpy.ops.mesh.primitive_cylinder_add(vertices=6, location=(self.posX, self.posY+self.width_Y/2,self.posZ+ i*(self.log_radius)-(self.height*2-(self.log_radius/2))), scale=(1, 1, 1))
                bpy.context.object.scale= (self.log_radius/2,self.log_radius/2,self.width_X/2+self.log_radius )
                bpy.context.object.rotation_euler[2] = math.pi/2  
                cur_log = bpy.context.object
                woodlogs.append(cur_log)
            else:
                bpy.ops.mesh.primitive_cylinder_add(vertices=6, location=(self.posX, -self.width_Y/2+self.posY,self.posZ+ i*(self.log_radius)-(self.height*3-(self.log_radius/2))), scale=(1, 1, 1))
                bpy.context.object.scale= (self.log_radius/2,self.log_radius/2, self.width_X/2+self.log_radius)
                bpy.context.object.rotation_euler[2] = math.pi/2
                cur_log = bpy.context.object
                woodlogs.append(cur_log)
            bpy.context.object.rotation_euler[0] = math.pi/2
        for cur_log in woodlogs:
            cur_log.select_set(True)
            
        bpy.ops.object.join()
            
        woodlogs =bpy.context.object
        modifier_array=woodlogs.modifiers.new("Woodlogs Array","ARRAY")#Erster Name selber angeben
        modifier_array.use_relative_offset = False
        modifier_array.use_constant_offset = False
        
        for obj in bpy.context.selected_objects:
            obj.name = "Base"
        base = bpy.data.objects["Base"]
        base_mat = self.base_material()
        base.data.materials.append(base_mat)
         
        #ROOF
        bpy.ops.mesh.primitive_cube_add(size=1, location=(self.posX, self.posY, self.posZ+self.height), scale=(1, 1, 1))
        bpy.context.object.scale= (self.width_X+self.roof_overhang,self.width_Y+self.roof_overhang,self.log_radius )
        bpy.context.object.rotation_euler[1] = -0.06
        for obj in bpy.context.selected_objects:
            obj.name = "Roof"
        roof = bpy.data.objects["Roof"]
        roof_mat = self.roof_material()
        roof.data.materials.append(roof_mat)
        
        #DOOR
        door = self.create_door()
        houseArray = []
        houseArray.append(door)
        houseArray.append(base)
        houseArray.append(roof)

        for h in houseArray:
            door.select_set(True)
            base.select_set(True)
            roof.select_set(True)
        bpy.ops.object.join()
        for obj in bpy.context.selected_objects:
            obj.name = "Blockhouse"
        
        #Sclae
        '''door.scale = self.house_size,self.house_size,self.house_size
        base.scale = self.house_size,self.house_size,self.house_size
        roof.scale = self.house_size,self.house_size,self.house_size'''
        '''
        win = self.createWindows()
        modifier_bool = base.modifiers.new("Windows bool","BOOLEAN")
        modifier_bool.object = win'''
        
        
        


