import random
from re import S
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '../..'))
from mychem3d import mychemApp, Atom,Space
from mychem_functions import bond_atoms
from math import pi 
import mychem3d
from math import *
import glm



def action1(space):
    global i0,i1,i3,a1
    if space.t==1:    
        i0=space.merge_from_file("examples/simple/carbonyl.json",500,500,500)
        rot = glm.quat(cos(pi/2), glm.vec3(0,0,sin(pi/2)))
        i1=space.merge_from_file("examples/simple/OH.json",500-50,590,500+30, rot)
        bond_atoms(space.atoms[i0],space.atoms[i1])
        #bond_atoms(space.atoms[0],space.atoms[1])
        space.atoms2compute()

    if space.t==1000: # +C
        space.compute2atoms()
        a1 = Atom(500,500,480,6)
        space.appendatom(a1)
        bond_atoms(space.atoms[i0], a1)
        space.atoms2compute()

    if space.t==1500: # +H
        space.compute2atoms()
        a2 = Atom(480,500,460,1)
        space.appendatom(a2)
        bond_atoms(a1,a2,1)
        space.atoms2compute()

    if space.t==2500: # +H
        space.compute2atoms()
        i1=space.merge_from_file("examples/simple/methyl.json",550,500,500+30)
        bond_atoms(a1,space.atoms[i1])
        space.atoms2compute()



    if space.t==3000: # +H
        space.compute2atoms()
        i2=space.merge_from_file("examples/simple/aminogroup.json",500,520,480)
        bond_atoms(a1,space.atoms[i2])
        space.atoms2compute()




    if space.t==1500:
        #space.INTERACT_KOEFF = 0.2
        pass

if __name__ == '__main__':
#
    random.seed(1)
    App = mychemApp()
    space = App.space
    space.action = action1
    #space.INTERACT_KOEFF = 0.6
    space.update_delta = 15
    #space.gpu_compute.set(False)
    #space.bondlock.set(True)
    App.run()
#
#
