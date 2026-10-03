import random
from re import S
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from mychem3d import mychemApp, Atom
from math import pi 
import mychem3d
from math import *
import glm


def action1(space):
    global f
    (x,y,z)=(0,0,0)
    if space.t%150==0:    #OH
        (f,s) = space.merge_from_file("examples/simple/NH3.json",100,100,500)
        for i in range(f,f+s):
            space.atoms[i].v = glm.vec3(0.5,0.5,0)
        #space.atoms[f+0].color = glm.vec4(0,0,0,1)
        space.glframe.atoms2ssbo(first=f,size=s)


if __name__ == '__main__':
#
    random.seed(1)
    App = mychemApp()
    space = App.space
    space.setSize(1000,1000,1000)
    space.update_delta = 10
    space.action = action1
     #space.recording = True
    #space.INTERACT_KOEFF = 5.0
    #space.REPULSION_KOEFF2=50
#    space.BOND_KOEFF = 100
#    space.MASS_KOEFF = 5
    #space.appendmixer(1)
    #space.redox.set(True)
#    space.NODEDIST = 40
    space.pause = True
    space.highlight_unbond=True
    App.run()

