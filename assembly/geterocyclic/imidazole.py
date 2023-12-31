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
        a0 = Atom(x+20,y+40,z,3)
        space.appendatom(a0)
        a1 = Atom(x+40,y+20,z,4)
        space.appendatom(a1)
        a2 = Atom(x+40,y-20,z,3)
        space.appendatom(a2)
        a3 = Atom(x,y-40,z,4)
        space.appendatom(a3)
        a4 = Atom(x-40,y-20,z,4)
        space.appendatom(a4)

        space.atoms2compute()

    if space.t==200: #N+C 2
        space.compute2atoms()

        space.atoms2compute()

    if space.t==400: #N+C
        space.compute2atoms()
        bond_atoms(a1,a2,0,0)
        space.atoms2compute()

    if space.t==600: #
        space.compute2atoms()
        bond_atoms(a1,a2,1,2)
        space.atoms2compute()


    if space.t==800: #
        space.compute2atoms()
        bond_atoms(a3,a4,0,0)
        space.atoms2compute()


    if space.t==1000: #
        space.compute2atoms()
        bond_atoms(a3,a4,1,2)
        space.atoms2compute()

############
    if space.t==1200: #C+C
        space.compute2atoms()
        bond_atoms(a0,a1)
        space.atoms2compute()


    if space.t==1500: #C+C
        space.compute2atoms()
        bond_atoms(a2,a3)
        space.atoms2compute()


    if space.t==2300: #C+C
        space.compute2atoms()
        bond_atoms(a0,a4)
        space.atoms2compute()



    if space.t==2600: #C+H
        space.compute2atoms()
        a = Atom(x+60,y+60,z,1,f=pi)
        space.appendatom(a)
        bond_atoms(a1,a)
        space.atoms2compute()


    if space.t==3500: #C+H
        space.compute2atoms()
        a = Atom(x+60,y-60,z,1,f=pi)
        space.appendatom(a)
        bond_atoms(a3,a)
        space.atoms2compute()

    if space.t==3700: #C+H
        space.compute2atoms()
        a = Atom(x-60,y-60,z,1)
        space.appendatom(a)
        bond_atoms(a4,a)
        space.atoms2compute()


    if space.t==3900: #C+H
        space.compute2atoms()
        a = Atom(x-60,y+60,z,1)
        space.appendatom(a)
        bond_atoms(a0,a)
        space.atoms2compute()




    if space.t==50:
        pass

if __name__ == '__main__':
#
    random.seed(1)
    App = mychemApp()
    space = App.space
    space.action = action1
    space.INTERACT_KOEFF = 0.4
    #space.BONDS_KOEFF = 0.5
    space.REPULSION_KOEFF1 = 7
    space.update_delta = 10
    #space.gpu_compute.set(False)
    space.bondlock.set(True)
    App.run()
#
#
