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

    ### Variables
    MAP_SIZE_X: int = 5
    MAP_SIZE_Y: int = 5
    PI = math.pi

    def execute(self, context):
        self.clearScene()

        for row in range(self.MAP_SIZE_X):
            for column in range(self.MAP_SIZE_Y):
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
            


    #####################Cube erstellen ##########################################
    def createTowerBase(self, name, pX,pY, height, width):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(pX+width/2, pY+width/2, height/2), scale=(width*2, width*2, height*2),rotation = (0,0,0))

    def createHouseBase(self, name, pX,pY, height, width):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(pX+width/2, pY+width/2, height/2), scale=(width*2, width*2, height*2),rotation = (0,0,0))
        bpy.ops.mesh.primitive_cylinder_add(vertices=3, radius=1, depth=1, location=(pX+width/2, pY+width/2, height+(height/4)), scale=(width*1.155, (height*2)/2, width*2), rotation = (self.PI/2 ,0,self.PI/2 ))
        
    ##################### TOWER Roof###########################################
    def createTowerRoof(self, name, pX,pY, height, width):
        mesh = bpy.data.meshes.new("mesh")
        topCoords = []
        topFaces = []
        pZ = height
        idx = 0
        roof_height = height/50

        self.createTowerRoofVertices(topCoords,pX,pY,pZ, height, width, roof_height)
        self.createTowerRoofFaces(topFaces, idx)

        top_object = bpy.data.objects.new(name, mesh)

        bpy.context.collection.objects.link(top_object)
        mesh.from_pydata(topCoords, [], topFaces)
        mesh.update( calc_edges=True )

    def createTowerRoofVertices(self, coords ,px, py, pz, height, width,roof_height):
        coords.append(( px, py, pz ))
        coords.append(( px + width, py, pz ))
        coords.append(( px + width, py + width, pz ))
        coords.append(( px, py+width , pz ))
        
        coords.append(( px, py, pz + roof_height))
        coords.append(( px + width, py, pz + roof_height))
        coords.append(( px + width, py + width, pz + roof_height))
        coords.append(( px, py+width , pz + roof_height))
        
        
        coords.append(( px+(roof_height/4), py+(roof_height/4), pz +roof_height))
        coords.append(( px + width-(roof_height/4), py+(roof_height/4), pz+roof_height))
        coords.append(( px + width-(roof_height/4), py + width-(roof_height/4), pz+roof_height))
        coords.append(( px+(roof_height/4), py+width -(roof_height/4), pz+roof_height ))
        
        coords.append(( px +(roof_height/4), py+(roof_height/4), pz + (roof_height/2)))
        coords.append(( px + width-(roof_height/4), py+(roof_height/4), pz + (roof_height/2)))
        coords.append(( px + width-(roof_height/4), py + width-(roof_height/4), pz + (roof_height/2)))
        coords.append(( px+(roof_height/4), py+width -(roof_height/4), pz + (roof_height/2)))
        
    def createTowerRoofFaces(self, faces, idx):
        faces.append(( idx, idx+1, idx+2, idx+3 ))
        
        faces.append(( idx, idx+1, idx+5, idx+4 ))
        faces.append(( idx+1, idx+2, idx+6, idx+5 ))
        faces.append(( idx+2, idx+3, idx+7, idx+6 ))
        faces.append(( idx+3, idx, idx+4, idx+7 ))
        
        faces.append(( idx+4, idx+5, idx+9, idx+8 ))
        faces.append(( idx+5, idx+6, idx+10, idx+9 ))
        faces.append(( idx+6, idx+7, idx+11, idx+10 ))
        faces.append(( idx+7, idx+4, idx+8, idx+11 ))
        
        faces.append(( idx+12, idx+13, idx+9, idx+8 ))
        faces.append(( idx+13, idx+14, idx+10, idx+9 ))
        faces.append(( idx+14, idx+15, idx+11, idx+10 ))
        faces.append(( idx+15, idx+12, idx+8, idx+11 ))
        
        faces.append(( idx+12, idx+13, idx+14, idx+15 ))

    ##################### House Roof ##########################################
    def createHouseRoof(self, name, pX,pY, height, width):
        mesh = bpy.data.meshes.new("mesh")
        topCoords = []
        topFaces = []
        pZ = height
        idx = 0
        roof_height = height/1.2

        self.createHouseRoofVertices(topCoords,pX,pY,pZ, height, width,roof_height)
        self.createHouseRoofFaces(topFaces, idx)
        
        top_object = bpy.data.objects.new(name, mesh)

        bpy.context.collection.objects.link(top_object)
        mesh.from_pydata(topCoords, [], topFaces)
        mesh.update( calc_edges=True )
        
    def createHouseRoofVertices(self, coords ,px, py, pz, height, width,roof_height):
        coords.append(( px - (roof_height/10), py - (roof_height/10), pz - (roof_height/10)))#1
        coords.append(( px + width + (roof_height/10), py - (roof_height/10), pz - (roof_height/10) )) #2
        coords.append(( px + width + (roof_height/10), py + width + (roof_height/10), pz - (roof_height/10))) #3
        coords.append(( px - (roof_height/10), py+width + (roof_height/10) , pz - (roof_height/10) )) #4
        
        coords.append(( px - (roof_height/10), py - (roof_height/10), pz + (roof_height/10) - (roof_height/10)))#5
        coords.append(( px + width + (roof_height/10), py - (roof_height/10), pz + (roof_height/10) - (roof_height/10)))#6
        coords.append(( px + width + (roof_height/10), py + width + (roof_height/10), pz + (roof_height/10) - (roof_height/10)))#7
        coords.append(( px - (roof_height/10), py+width + (roof_height/10) , pz + (roof_height/10)- (roof_height/10) ))#8
        
        
        coords.append(( px - (roof_height/10), py+(width/2), pz +roof_height))
        coords.append(( px + width + (roof_height/10), py+(width/2), pz+(roof_height) - (roof_height/10)  ))
        coords.append(( px - (roof_height/10), py + (width/2), pz+roof_height - (roof_height/10)))
        coords.append(( px + width + (roof_height/10), py+(width/2) , pz+roof_height ))
        
    def createHouseRoofFaces(self, faces, idx):
        faces.append(( idx, idx+1, idx+5, idx+4 ))
        faces.append(( idx + 2, idx+3, idx+7, idx+6 ))
        faces.append(( idx+4,idx+5,idx+11,idx+8))
        faces.append(( idx,idx+1,idx+9,idx+10))
        faces.append(( idx+1, idx+5, idx+11, idx+9 ))
        faces.append(( idx , idx+4, idx+8, idx+10 ))

        faces.append(( idx+2,idx+6,idx+7,idx+3))
        faces.append(( idx+2,idx+9,idx+10,idx+3))
        faces.append(( idx+2,idx+9,idx+11,idx+6))
        faces.append(( idx+3,idx+10,idx+8,idx+7))
        faces.append(( idx+6, idx+11, idx+8, idx+7 ))
        

        
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

        #Würfel erstellen
        width = random.uniform(0.5,0.8)
        height = width * 3
        self.createTowerBase("Tower", posX, posY, height, width)

        #Dach erstellen
        self.createTowerRoof('Top of Tower', posX,posY, height, width)
        
    def createHouse(self, posX, posY):
        #Würfel erstellen
        width = random.uniform(0.5,0.8)
        height = (width * 2)/3
        self.createHouseBase("House Base", posX, posY, height, width)
        #Dachboden
        #createHouseAttic("Attic of small House",posX,posY, height, width)
        #Dach erstellen
        self.createHouseRoof('Top of House', posX,posY, height, width)

    def clearScene(self):
        # Szene leeren
        bpy.ops.object.select_all(action='SELECT') # selektiert alle Objekte
        bpy.ops.object.delete(use_global=False, confirm=False) # löscht selektierte objekte
        bpy.ops.outliner.orphans_purge() # löscht überbleibende Meshdaten etc.

def register():
    bpy.utils.register_class(OBJECT_OT_generate_landscape)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_generate_landscape)

if __name__ == "__main__":
    register()