#!/usr/bin/python3.9
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
    global a0,a1,a2,a3,a4,a5
    (x,y,z)=(500,500,500)
    if space.t==1:    #C+C
        a0 = Atom(x+20,y+40,z,4)
        space.appendatom(a0)
        a1 = Atom(x+40,y+20,z,4)
        space.appendatom(a1)
        a2 = Atom(x+40,y-20,z,4)
        space.appendatom(a2)
        a3 = Atom(x+20,y-40,z,4)
        space.appendatom(a3)
#        a4 = Atom(x-40,y-20,z,4)
#        space.appendatom(a4)
#        a5 = Atom(x-40,y+20,z,4)
#        space.appendatom(a5)

        bond_atoms(a0,a1,0,0)
        space.atoms2compute()

    if space.t==200: #C+C+C
        space.compute2atoms()
        bond_atoms(a0,a1,1,2)
        space.atoms2compute()

    if space.t==400: #C+C+C
        space.compute2atoms()
        bond_atoms(a2,a3,0,0)
        space.atoms2compute()

    if space.t==600: #C+C
        space.compute2atoms()
        bond_atoms(a2,a3,1,2)
        space.atoms2compute()


#    if space.t==800: #C+C
#        space.compute2atoms()
        #bond_atoms(a4,a5,0,0)
        #space.atoms2compute()


#    if space.t==1000: #C+C
#        space.compute2atoms()
#        bond_atoms(a4,a5,1,2)
#        space.atoms2compute()

############
    if space.t==1200: #C+C
        space.compute2atoms()
        bond_atoms(a1,a2,3,2)
        space.atoms2compute()


    if space.t==1500: #C+C
        space.compute2atoms()
        bond_atoms(a0,a3,3)
        space.atoms2compute()



########
    if space.t==2200: #C+H
        space.compute2atoms()
        a = Atom(x-60,y+60,z,1,f=0)
        space.appendatom(a)
        bond_atoms(a0,a)
        space.atoms2compute()


    if space.t==2400: #C+H
        space.compute2atoms()
        a = Atom(x+60,y+60,z,1,f=pi)
        space.appendatom(a)
        bond_atoms(a1,a)
        space.atoms2compute()


    if space.t==2600: #C+H
        space.compute2atoms()
        a = Atom(x+60,y-60,z,1,f=pi)
        space.appendatom(a)
        bond_atoms(a2,a)
        space.atoms2compute()


    if space.t==2800: #C+H
        space.compute2atoms()
        a = Atom(x+60,y-60,z,1,f=pi)
        space.appendatom(a)
        bond_atoms(a3,a)
        space.atoms2compute()







    if space.t==50:
        pass

if __name__ == '__main__':
#
    random.seed(1)
    App = mychemApp()
    space = App.space
    space.action = action1
    #space.INTERACT_KOEFF = 0.5
    #space.BONDS_KOEFF = 0.5
    space.REPULSION_KOEFF1 = 7
    space.update_delta = 5
    #space.gpu_compute.set(False)
    space.bondlock.set(True)
    App.run()
#
#
