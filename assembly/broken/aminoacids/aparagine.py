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



def action1(space:Space):
    global i0,i1,i2,i3,i4,a1,a2,a3
    if space.t==1:    
        i0=space.merge_from_file("examples/simple/carbonyl.json",0,0,0)
        rot = glm.quat(cos(pi/2), glm.vec3(0,0,sin(pi/2)))
        i1=space.merge_from_file("examples/simple/OH.json",-50,0,+30, rot)
        bond_atoms(space.atoms[i0],space.atoms[i1])
        #bond_atoms(space.atoms[0],space.atoms[1])
        space.atoms2compute()

    if space.t==200:
        space.compute2atoms()
        a1 = Atom(500,500,500,4)
        space.appendatom(a1)
        bond_atoms(space.atoms[i0],a1)
        space.atoms2compute()
        pass


    if space.t==400:
        space.compute2atoms()
        h1 = Atom(500,550,500,1)
        space.appendatom(h1)
        bond_atoms(a1,h1)
        space.atoms2compute()
        pass



    if space.t==600:
        space.compute2atoms()
        ami = space.merge_from_file("examples/simple/aminogroup.json",0,0,0)
        #space.appendatom(a1)
        bond_atoms(a1,space.atoms[ami],3)
        space.atoms2compute()


    if space.t==800:
        space.compute2atoms()
        i2 = space.merge_from_file("examples/simple/CH2.json",0,30,0)
        bond_atoms(a1,space.atoms[i2])  #L/D
        space.atoms2compute()


#    if space.t==1200:
#        space.compute2atoms()
#        i3 = space.merge_from_file("examples/simple/CH2.json",30,30,0)
#        bond_atoms(space.atoms[i2],space.atoms[i3])  #L/D
#        space.atoms2compute()

    if space.t==1400:
        space.compute2atoms()
        i4 = space.merge_from_file("examples/simple/carbonyl.json",80,0,0)
        bond_atoms(space.atoms[i4],space.atoms[i2])  #L/D
        space.atoms2compute()

    if space.t==2000:
        space.compute2atoms()
        i5 = space.merge_from_file("examples/simple/aminogroup.json",80,0,0)
        bond_atoms(space.atoms[i4],space.atoms[i5])  #L/D
        space.atoms2compute()




if __name__ == '__main__':
#
    random.seed(1)
    App = mychemApp()
    space = App.space
    space.action = action1
    #space.INTERACT_KOEFF = 0.6
    space.update_delta = 5
    #space.gpu_compute.set(False)
    #space.bondlock.set(True)
    App.run()
#
#
