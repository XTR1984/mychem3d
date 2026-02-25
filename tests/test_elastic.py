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
    if space.t==1:    #OH
        (x,y,z) = (500,500,500)
        space.merge_from_file("examples/alkane/30ane.json",x,y,z)

        #(x,y,z) = (500,500,540)
        #space.merge_from_file("examples/alkane/30ane.json",x,y,z)

        a = Atom(750,700,500,8)
        a.v = glm.vec3(-1,0,0)
        space.appendatom(a)

        space.atoms2compute()

    #if space.t>1 and space.t %4 == 0: #OH
#        space.compute2atoms()
    #    a2 = Atom(x,y,z+50,4)
    #    space.appendatom(a2)
    #    bond_atoms(space.atoms[1],a2)
#        space.atoms[46].v = glm.vec3(-0.5*sin(space.t/100),0,0)
#        space.atoms2compute()




if __name__ == '__main__':
#
    App = mychemApp()
    space = App.space
    space.setSize(1000,1000,1000)
    space.action = action1
    #space.INTERACT_KOEFF = 0.1
    space.BOND_KOEFF = 50
    space.ROTA_KOEFF = 10
    #space.REPULSION_KOEFF1=30
    #space.REPULSION_KOEFF2=0.2
    space.update_delta = 10
    #space.gpu_compute.set(False)
    #space.bondlock.set(True)
    App.run()
#
#

