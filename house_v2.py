import bpy
import bmesh
import math
import mathutils
import random
from random import randint

# Szene leeren
bpy.ops.object.select_all(action='SELECT') # selektiert alle Objekte
bpy.ops.object.delete(use_global=False, confirm=False) # löscht selektierte objekte
bpy.ops.outliner.orphans_purge() # löscht überbleibende Meshdaten etc.

### Variables
MAP_SIZE_X = 5
MAP_SIZE_Y = 5

# bpy.context.active_object.rotation_euler[2] = math.radians(90 * random.randint(0,3))

def generate_town():
    for row in range(MAP_SIZE_X):
        for column in range(MAP_SIZE_Y):
            positionX = 1 * row
            positionY = 1 * column 
            randomInt = randint(0,7)
                                
            if randomInt == 0:
                    createTower(positionX, positionY)	
            elif randomInt >= 1 and randomInt < 5:
                    createHouse(positionX, positionY)
            elif randomInt >=5:
                    createGreens(positionX, positionY)
        
                    
PI = math.pi                    


#####################House ##########################################

def createHouseBase(name, pX,pY, height, width,length,rot):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(pX+width/2+0.25, pY+width/2+0.25, height/2), scale=(length*2, width*2, height*2),rotation = (0,0,rot))
    bpy.ops.mesh.primitive_cylinder_add(vertices=3, radius=1, depth=1, location=(pX+width/2+0.25, pY+width/2+0.25, height+(height/4)), scale=(width*1.155, (height*2)/2, length*2), rotation = (PI/2 ,0,PI/2+rot ))

def createHouseRoof(name, pX,pY, height, width,length,rot):
    bpy.ops.mesh.primitive_cylinder_add(vertices=3, radius=1, depth=1, location=(pX+width/2+0.25, pY+width/2+0.25, height+(height/4)), scale=(width*1.155, (height*2)/2, length*2), rotation = (PI/2 ,0,PI/2+rot))
    bpy.ops.transform.resize(value=(1.2,1.2,1.2))
    roof1=bpy.context.object
      
    bpy.ops.mesh.primitive_cylinder_add(vertices=3, radius=1, depth=1, location=(pX+width/2+0.25, pY+width/2+0.25, height+(height/4)-0.03), scale=(width*1.155, (height*2)/2, length*2.9), rotation = (PI/2 ,0,PI/2+rot))
    roof2=bpy.context.object
    bpy.context.object.display_type = 'WIRE' 
    
    modifier_bool = roof1.modifiers.new("Cube bool", "BOOLEAN")
    modifier_bool.object = roof2      

##################### Tower ##########################################
def createTowerBase(name, pX,pY, height, width):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(pX+width/2+(1/4), pY+width/2+(1/4), height/2), scale=(width*2, width*2, height*2),rotation = (0,0,0))

def createTowerRoof(name, pX,pY, height, width):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(pX+width/2+(1/4), pY+width/2+(1/4), height+(0.15/4)), scale=(width*2, width*2, 0.15))
    roof2=bpy.context.object
    bpy.ops.mesh.primitive_cube_add(size=1, location=(pX+width/2+(1/4), pY+width/2+(1/4), height), scale=(width*2, width*2, height*2))
    bpy.ops.transform.resize(value=(0.8,0.8,0.2))
    roof1=bpy.context.object
    
    bpy.context.object.display_type = 'WIRE' 
    
    modifier_bool = roof2.modifiers.new("Roof Bool", "BOOLEAN")
    modifier_bool.object = roof1
    

    
def createGreens(posX, posY):

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
    


def createTower(posX, posY):
    width = random.uniform(0.5,0.8)
    height = width * 3
    createTowerBase("Tower", posX, posY, height, width)
    createTowerRoof('Top of Tower', posX,posY, height, width)
    
def createHouse(posX,posY):
    rotation = [0,PI/2, PI,PI*1.5]
    rInt = randint(0,3)
    rot = rotation[rInt]
    
    width = random.uniform(0.4,0.6)
    length = random.uniform(0.4,0.7)
    height = (width * 2)/3
    createHouseBase("House Base", posX, posY, height, width,length,rot)
    createHouseRoof('Top of House', posX,posY, height, width,length,rot)
    

generate_town()