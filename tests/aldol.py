import random
from re import S
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from mychem3d import mychemApp, Atom,Space
from mychem_functions import bond_atoms
from math import pi 
import mychem3d
from math import *
import glm


f = 0
def action1(space):
    global f
    (x,y,z)=(100,100,100)
    if space.t==1:    #OH
            f = random.random()*2*pi
            rot = glm.normalize(glm.quat(cos(f/2), sin(f/2)* glm.vec3(random.random(),random.random(),random.random())))
            dx = 30
            dy = 0
            dz = 0
            (i1,_)=space.merge_from_file("examples/simple/OH.json",x+dx,y+dz,z+dy,rot)
            space.atoms[i1].nodes[1].q=-1
            space.atoms[i1].nodes[1].spin=-1
#        for i in range(0,20):
#            f = random.random()*pi
#            rot = glm.normalize(glm.quat(cos(f/2), sin(f/2)* glm.vec3(random.random(),random.random(),random.random())))
#            dx = random.randint(-400,400)
            #dy = random.randint(-400,400)
#            dz = random.randint(-400,400)
            #i1=space.merge_from_file("examples/simple/OH.json",x+dx,y+dz,z+dy,rot)
#            a = Atom(x+dx,y+dy,z+dz,1)
            #a.nodes[0].q=1
#            space.appendatom(a)
            
            f = random.random()*2*pi
            rot = glm.normalize(glm.quat(cos(f/2), sin(f/2)* glm.vec3(random.random(),random.random(),random.random())))
            dx = 0
            dy = 0
            dz = 0
            i4=space.merge_from_file("examples/aldehyde/acetaldehyde.json",x+dx,y+dy,z+dz,rot)
            #i4=space.merge_from_file("examples/aminoacids/asparagine.json",x+dx,y+dy,z+dz,rot)


            for i in range(0,3):
                f = random.random()*pi
                rot = glm.normalize(glm.quat(cos(f/2), sin(f/2)* glm.vec3(random.random(),random.random(),random.random())))
                dx = random.randint(-50,50)
                dy = random.randint(-50,50)
                dz = random.randint(-50,50)
                i4=space.merge_from_file("examples/aldehyde/formaldehyde.json",x+dx,y+dy,z+dz,rot)
                #i4=space.merge_from_file("examples/aminoacids/asparagine.json",x+dx,y+dy,z+dz,rot)

            space.atoms2compute()

    #if space.t==450: #OH
    #    space.compute2atoms()
    #    a2 = Atom(x,y,z+50,4)
    #    space.appendatom(a2)
    #    bond_atoms(space.atoms[1],a2)
    #    space.atoms2compute()




if __name__ == '__main__':
#
    App = mychemApp()
    space = App.space
    space.setSize(200,200,200)
    space.action = action1
    #space.INTERACT_KOEFF = 0.3
    #space.BOND_KOEFF = 0.4
#    space.ROTA_KOEFF = 1
    #space.REPULSION_KOEFF2=5
    space.update_delta = 10
    #space.gpu_compute.set(False)
    #space.bondlock.set(True)
    App.run()
#
#

