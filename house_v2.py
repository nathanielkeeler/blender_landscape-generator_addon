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



def generate_town():
    for row in range(5):
        for column in range(5):
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


#####################Cube erstellen ##########################################
def createTowerBase(name, pX,pY, height, width):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(pX+width/2, pY+width/2, height/2), scale=(width*2, width*2, height*2),rotation = (0,0,0))

def createHouseBase(name, pX,pY, height, width,length,rot):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(pX+width/2, pY+width/2, height/2), scale=(length*2, width*2, height*2),rotation = (0,0,rot))
    bpy.ops.mesh.primitive_cylinder_add(vertices=3, radius=1, depth=1, location=(pX+width/2, pY+width/2, height+(height/4)), scale=(width*1.155, (height*2)/2, length*2), rotation = (PI/2 ,0,PI/2+rot ))
      
##################### TOWER Roof###########################################
def createTowerRoof(name, pX,pY, height, width):
    mesh = bpy.data.meshes.new("mesh")
    topCoords = []
    topFaces = []
    pZ = height
    idx = 0
    roof_height = height/50

    createTowerRoofVertices(topCoords,pX,pY,pZ, height, width, roof_height)
    createTowerRoofFaces(topFaces, idx)

    top_object = bpy.data.objects.new(name, mesh)

    bpy.context.collection.objects.link(top_object)
    mesh.from_pydata(topCoords, [], topFaces)
    mesh.update( calc_edges=True )

def createTowerRoofVertices(coords ,px, py, pz, height, width,roof_height):
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
    
def createTowerRoofFaces(faces, idx):
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
def createHouseRoof(name, pX,pY, height, width,length,rot):
    bpy.ops.mesh.primitive_cylinder_add(vertices=3, radius=1, depth=1, location=(pX+width/2, pY+width/2, height+(height/4)), scale=(width*1.155, (height*2)/2, length*2), rotation = (PI/2 ,0,PI/2+rot))
    bpy.ops.transform.resize(value=(1.2,1.2,1.2))
    roof1=bpy.context.object
      
    
    bpy.ops.mesh.primitive_cylinder_add(vertices=3, radius=1, depth=1, location=(pX+width/2, pY+width/2, height+(height/4)-0.03), scale=(width*1.155, (height*2)/2, length*2.9), rotation = (PI/2 ,0,PI/2+rot))
    roof2=bpy.context.object
    bpy.context.object.display_type = 'WIRE' 
    
    modifier_bool = roof1.modifiers.new("Cube bool", "BOOLEAN")
    modifier_bool.object = roof2
    

    
def createGreens(posX, posY):
    
    for row in range(3):
        for column in range(3):
            #Baumstamm
            bpy.ops.mesh.primitive_cube_add(size=0.1, location=(0.3 * row + 0.5+(posX - 0.3) ,0.3 * column + 0.5+(posY - 0.3), 0.22), scale=(1, 1, 9))
            object_color = (0.102474, 0.0215169, 0.00329, 1)
            bpy.context.object.color = object_color
          
            #Baumkrone
            bpy.ops.mesh.primitive_cube_add(size=0.2, location=(0.3 * row + 0.5 +(posX - 0.3) ,0.3 * column + 0.5+ (posY - 0.3), 0.3), scale=(1, 1, 4))
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
    
    width = random.uniform(0.5,0.7)
    length = random.uniform(0.6,0.8)
    height = (width * 2)/3
    createHouseBase("House Base", posX, posY, height, width,length,rot)
    createHouseRoof('Top of House', posX,posY, height, width,length,rot)
    

generate_town()