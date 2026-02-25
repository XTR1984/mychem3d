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
def action1(space:Space):
    global f,c1,c2,c3,c4,n1,n2,n3,n4,o1,o2,o3,o4
    (x,y,z)=(500,500,500)
    if space.t==1:    #OH
        c1 = Atom(550,500,881, 6)
        c2 = Atom(550,500,900, 6,f2=pi)
        space.appendatom(c1)
        space.appendatom(c2)


        ##n1 = Atom(400,500,900, 7,f=0,f2=-pi/2)
        #n2 = Atom(400,500,883, 7,f=0,f2=0)
        #space.appendatom(n1)
        #space.appendatom(n2)


        #c3 = Atom(350,500,900, 6,f=0,f2=0)
        #n3 = Atom(350,500,882, 7,f=0,f2=0)
        #space.appendatom(c3)
        #space.appendatom(n3)

        #c4 =  Atom(500,500,800,6)
        #o1 =  Atom(500,500,785,8)
        #space.appendatom(c4)
        #space.appendatom(o1)

        #n4 = Atom(600,500, 800,7)
        #o2 = Atom(600,500, 785,8)
        #space.appendatom(n4)
        #space.appendatom(o2)


        #na1 = Atom(100,100,900,11)
        #space.appendatom(na1)

        #cl = Atom(200,100,900,17)
        #space.appendatom(cl)


        #space.pause=True
        space.atoms2compute()

    if space.t==100:
        return
        space.compute2atoms()
        bond_atoms(c1,c2,1,2)
        bond_atoms(n1,n2)
        bond_atoms(c3,n3,1,0)
        bond_atoms(c4,o1,1,0)
        bond_atoms(n4,o2)
        space.atoms2compute()

    if space.t==1200:
        return
        space.compute2atoms()
        bond_atoms(c1,c2,2,1)
        bond_atoms(n1,n2,1,2)
        bond_atoms(c3,n3,2,1)
        bond_atoms(c4,o1)
        bond_atoms(n4,o2)
        space.atoms2compute()


    if space.t==2600:
        return
        space.compute2atoms()
        bond_atoms(n1,n2,2,1)
        bond_atoms(c3,n3,3)
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
    #space.INTERACT_KOEFF = 10
    #space.BOND_KOEFF = 0.3
    #space.ROTA_KOEFF = 1
    #space.REPULSION_KOEFF2=2.0
    space.update_delta = 10
    #space.gpu_compute.set(False)
    #space.bondlock.set(True)



    App.run()
#
#

