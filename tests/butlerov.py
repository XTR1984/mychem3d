import random
from re import S
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from mychem3d import mychemApp, Atom,Space
from functions import bond_atoms
from math import pi 
import mychem3d
from math import *
import glm


f = 0
def action1(space):
    global f
    (x,y,z)=(0,0,0)
    if space.t==1:    #OH
        for i in range(0,20):
            f = random.random()*pi
            rot = glm.normalize(glm.quat(cos(f/2), sin(f/2)* glm.vec3(random.random(),random.random(),random.random())))
            dx = random.randint(0,space.WIDTH)
            dy = random.randint(0,space.HEIGHT)
            dz = random.randint(0,space.DEPTH)
            (i1,_)=space.merge_from_file("examples/simple/OH.json",x+dx,y+dz,z+dy,rot)
            space.atoms[i1].nodes[1].q=-1
            space.atoms[i1].nodes[1].spin=0
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
            


        for i in range(0,10):
            f = random.random()*pi
            rot = glm.normalize(glm.quat(cos(f/2), sin(f/2)* glm.vec3(random.random(),random.random(),random.random())))
            dx = random.randint(0,space.WIDTH)
            dy = random.randint(0,space.HEIGHT)
            dz = random.randint(0,space.DEPTH)
            i4=space.merge_from_file("examples/aldehyde/acetaldehyde.json",x+dx,y+dy,z+dz,rot)
            #i4=space.merge_from_file("examples/aminoacids/asparagine.json",x+dx,y+dy,z+dz,rot)

        for i in range(0,300):
            f = random.random()*pi
            rot = glm.normalize(glm.quat(cos(f/2), sin(f/2)* glm.vec3(random.random(),random.random(),random.random())))
            dx = random.randint(0,space.WIDTH)
            dy = random.randint(0,space.HEIGHT)
            dz = random.randint(0,space.DEPTH)
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
    space.setSize(1000,300,300)
    space.action = action1
    #space.INTERACT_KOEFF = 0.4
    #space.BOND_KOEFF = 0.2
    #space.ROTA_KOEFF = 1
    #space.REPULSION_KOEFF2=0.4
    space.update_delta = 10
    space.highlight_unbond = True
    #space.bondlock.set(True)
    App.run()
#
#

