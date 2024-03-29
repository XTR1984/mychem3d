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
    (x,y,z)=(500,500,500)
    if space.t==1:    #OH
        for i in range(0,100):
            f = random.random()*pi
            rot = glm.normalize(glm.quat(cos(f/2), sin(f/2)* glm.vec3(random.random(),random.random(),random.random())))
            dx = random.randint(-400,400)
            dy = random.randint(-400,400)
            dz = random.randint(-400,400)
            i1=space.merge_from_file("examples/simple/OH.json",x+dx,y+dz,z+dy,rot)
            #i1=space.merge_from_file("examples/simple/H2O.json",x+dx,y+dz,z+dy,rot)
            space.atoms[i1].nodes[1].q=-1

        for i in range(0,1090):
            f = random.random()*pi
            rot = glm.normalize(glm.quat(cos(f/2), sin(f/2)* glm.vec3(random.random(),random.random(),random.random())))
            dx = random.randint(-400,400)
            dy = random.randint(-400,400)
            dz = random.randint(-400,400)
            #i1=space.merge_from_file("examples/simple/OH.json",x+dx,y+dz,z+dy,rot)
            #i1=space.merge_from_file("examples/simple/H2O.json",x+dx,y+dz,z+dy,rot)
            #space.atoms[i1].nodes[1].q=-1
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
        for i in range(0,50):
            f = random.random()*pi
            rot = glm.normalize(glm.quat(cos(f/2), sin(f/2)* glm.vec3(random.random(),random.random(),random.random())))
            dx = random.randint(-400,400)
            dy = random.randint(-400,400)
            dz = random.randint(-400,400)
            i4=space.merge_from_file("examples/nucleobase/adenosine.json",x+dx,y+dy,z+dz,rot)
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
    space.setSize(1000,1000,1000)
    space.action = action1
    space.INTERACT_KOEFF = 0.4
    space.BOND_KOEFF = 0.15
    #space.ROTA_KOEFF = 1
    space.REPULSION_KOEFF2=0.2
    space.update_delta = 20
    #space.gpu_compute.set(False)
    #space.bondlock.set(True)
    App.run()
#
#

