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



def action1(space):
    (x,y,z)=(100,100,100)
    if space.t==1:    #OH
        i1=space.merge_from_file("examples/simple/OH.json",x+50,y,z)
        #i2=space.merge_from_file("examples/simple/OH.json",x+50,y+40,z)
        #i3=space.merge_from_file("examples/simple/OH.json",x+50,y+80,z)
        #i1=space.merge_from_file("examples/simple/OH.json",0,30,0)
        #i1=space.merge_from_file("examples/simple/OH.json",0,60,0)
        i4=space.merge_from_file("examples/aldehyde/acetaldehyde.json",x+50,y+50,z+10)
        i4=space.merge_from_file("examples/aldehyde/acetaldehyde.json",x-100,y+80,z+10)
        i2=space.merge_from_file("examples/aldehyde/acetaldehyde.json",50,50,10)
        #i2=space.merge_from_file("examples/aldehyde/acetaldehyde.json",50,50,10)
        i2=space.merge_from_file("examples/aldehyde/acetaldehyde.json",0,50,10)
        i3=space.merge_from_file("examples/aldehyde/acetaldehyde.json",100,20,10)
        #bond_atoms(space.atoms[0],space.atoms[2])
        space.atoms[i1].nodes[1].q=-1
        #space.atoms[i2].nodes[1].q=-1
        #space.atoms[i3].nodes[1].q=-1
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
    space.INTERACT_KOEFF = 2.8
    space.BOND_KOEFF = 0.2
#    space.ROTA_KOEFF = 2
    space.REPULSION_KOEFF2=0.2
    space.update_delta = 10
    space.ROTA_KOEFF = 2
    #space.gpu_compute.set(False)
    #space.bondlock.set(True)
    App.run()
#
#
