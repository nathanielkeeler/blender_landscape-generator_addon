bl_info = {
    "name": "Landscape generator",
    "author": "Maren Röttele, Niclas Cravaack, Nathaniel Keeler",
    "version": (1, 0),
    "blender": (2, 92, 0),
    "location": "View3D > Add > Generate landscape",
    "description": "Adds a randomly generated landscape to the scene with customizable parameters.",
    "doc_url": "https://github.com/nathanielkeeler/Umgebungsgenerator",
    "category": "Add Mesh",
}

import bpy
import bmesh
import math
import mathutils
import random
from random import randint

class OBJECT_OT_generate_landscape(bpy.types.Operator):
    """Adds a randomly generated landscape to the scene with customizable parameters."""
    bl_idname = "object.generate_landscape"
    bl_label = "Generate landscape"
    bl_description = "Adds a randomly generated landscape to the scene"
    bl_options = {"REGISTER", "UNDO"}

    ### Customizable Variables
    #Map size
    MAP_SIZE: bpy.props.IntProperty(
        name = "Map size",
        description = "Changes map size in square proportion.",
        min = 3,
        max = 8,
        default = 5
    )
    #Vegetation
    TREE_DENSITY: bpy.props.IntProperty(
        name = "Tree number",
        description = "Changes number of trees per square.",
        min = 1,
        max = 3,
        default = random.randint(1, random.randint(1,3))
    )

    ### Fixed variables
    PI = math.pi

    def execute(self, context):
        self.clearScene()

        for row in range(self.MAP_SIZE):
            for column in range(self.MAP_SIZE):
                positionX = 1 * row
                positionY = 1 * column 
                randomInt = randint(0,7)
                                    
                if randomInt == 0:
                        self.createTower(positionX, positionY)	
                elif randomInt >= 1 and randomInt < 5:
                        self.createHouse(positionX, positionY)
                elif randomInt >=5:
                        self.createGreens(positionX, positionY)

        return {'FINISHED'}
            


        ##################### House ##########################################
    def createHouseBase(self, name, pX,pY, height, width,length,rot):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(pX+width/2+0.25, pY+width/2+0.25, height/2), scale=(length*2, width*2, height*2),rotation = (0,0,rot))
        bpy.ops.mesh.primitive_cylinder_add(vertices=3, radius=1, depth=1, location=(pX+width/2+0.25, pY+width/2+0.25, height+(height/4)), scale=(width*1.155, (height*2)/2, length*2), rotation = (self.PI/2 ,0, self.PI/2+rot ))

    def createHouseRoof(self, name, pX,pY, height, width,length,rot):
        bpy.ops.mesh.primitive_cylinder_add(vertices=3, radius=1, depth=1, location=(pX+width/2+0.25, pY+width/2+0.25, height+(height/4)), scale=(width*1.155, (height*2)/2, length*2), rotation = (self.PI/2 ,0, self.PI/2+rot))
        bpy.ops.transform.resize(value=(1.2,1.2,1.2))
        roof1=bpy.context.object
        
        bpy.ops.mesh.primitive_cylinder_add(vertices=3, radius=1, depth=1, location=(pX+width/2+0.25, pY+width/2+0.25, height+(height/4)-0.03), scale=(width*1.155, (height*2)/2, length*2.9), rotation = (self.PI/2 ,0, self.PI/2+rot))
        roof2=bpy.context.object
        bpy.context.object.display_type = 'WIRE' 
        
        modifier_bool = roof1.modifiers.new("Cube bool", "BOOLEAN")
        modifier_bool.object = roof2      

    ##################### Tower ##########################################
    def createTowerBase(self, name, pX,pY, height, width):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(pX+width/2+(1/4), pY+width/2+(1/4), height/2), scale=(width*2, width*2, height*2),rotation = (0,0,0))

    def createTowerRoof(self, name, pX,pY, height, width):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(pX+width/2+(1/4), pY+width/2+(1/4), height+(0.15/4)), scale=(width*2, width*2, 0.15))
        roof2=bpy.context.object
        bpy.ops.mesh.primitive_cube_add(size=1, location=(pX+width/2+(1/4), pY+width/2+(1/4), height), scale=(width*2, width*2, height*2))
        bpy.ops.transform.resize(value=(0.8,0.8,0.2))
        roof1=bpy.context.object
        
        bpy.context.object.display_type = 'WIRE' 
        
        modifier_bool = roof2.modifiers.new("Roof Bool", "BOOLEAN")
        modifier_bool.object = roof1
        
    ################### Vegetation ########################################
    def createGreens(self, posX, posY):

        max = random.randint(1,3)
        TREE_DENSITY = random.randint(1,max)
        
        for row in range(TREE_DENSITY):
            for column in range(TREE_DENSITY):
                #Baumstamm
                bpy.ops.mesh.primitive_cube_add(size=0.1, location=(0.3 * row + 0.5+(posX - 0.3), 0.3 * column + 0.5+(posY - 0.3), 0.22), scale=(1, 1, 9))
                object_color = (0.102474, 0.0215169, 0.00329, 1)
                bpy.context.object.color = object_color
            
                #Baumkrone
                bpy.ops.mesh.primitive_cube_add(size=0.2, location=(0.3 * row + 0.5 +(posX - 0.3), 0.3 * column + 0.5+ (posY - 0.3), 0.3), scale=(1, 1, 4))
                object_color = (0.0106683, 0.147314, 0.0176817, 1)
                bpy.context.object.color = object_color    
        

    def createTower(self, posX, posY):
        width = random.uniform(0.5,0.8)
        height = width * 3
        self.createTowerBase("Tower", posX, posY, height, width)
        self.createTowerRoof('Top of Tower', posX,posY, height, width)
        
    def createHouse(self, posX, posY):
        rotation = [0,self.PI/2, self.PI, self.PI*1.5]
        rInt = randint(0,3)
        rot = rotation[rInt]
        
        width = random.uniform(0.4,0.6)
        length = random.uniform(0.4,0.7)
        height = (width * 2)/3
        self.createHouseBase("House Base", posX, posY, height, width,length,rot)
        self.createHouseRoof('Top of House', posX,posY, height, width,length,rot)

    def clearScene(self):
        # Szene leeren
        bpy.ops.object.select_all(action='SELECT') # selektiert alle Objekte
        bpy.ops.object.delete(use_global=False, confirm=False) # löscht selektierte objekte
        bpy.ops.outliner.orphans_purge() # löscht überbleibende Meshdaten etc.


def menu_func(self, context):
    self.layout.operator(OBJECT_OT_generate_landscape.bl_idname, icon="OUTLINER_OB_IMAGE")

def register():
    bpy.utils.register_class(OBJECT_OT_generate_landscape)
    bpy.types.VIEW3D_MT_add.append(menu_func)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_generate_landscape)
    bpy.types.VIEW3D_MT_add.remove(menu_func)

if __name__ == "__main__":
    register()