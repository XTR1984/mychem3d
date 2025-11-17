import random
import time
from re import S
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from mychem3d import mychemApp, Atom
from math import pi 
import mychem3d
from math import *
import glm



#            
# #
#
if __name__ == '__main__':
#
    random.seed(1)
    App = mychemApp()
    space = App.space
    space.setSize(500,500,500)
    for i in range(0,2000):
        f = random.random()*pi
        rot = glm.normalize(glm.quat(cos(f/2), sin(f/2)* glm.vec3(random.random(),random.random(),random.random())))
        x = random.randint(0,space.WIDTH)
        y = random.randint(0,space.HEIGHT)
        z = random.randint(0,space.DEPTH)        
        (i,_)=space.merge_from_file("examples/simple/H2O.json",x,y,z,rot)
        for n in range(0,3):
            color = space.atoms[i+n].color
            space.atoms[i+n].color=color[0:3] + (0.1,)
        #space.merge_from_file("examples/alcohol/methanol.json",x,y,z)
    space.update_delta = 10
    #space.INTERACT_KOEFF = 5.0
    #space.REPULSION_KOEFF2 = 500.0
    #space.BOND_KOEFF = 0.3
    #space.NEARDIST = 200
    #space.NODEDIST = 60
    
    #space.sideheat.set(True)
    #space.heat= -50
    #App.heat.set(-200)

    #space.MASS_KOEFF = 5    space.NEARDIST=100
    #space.tranparentmode= True
     #space.recording = True
    #space.appendmixer(1)
    #space.redox.set(True)
    space.highlight_unbond=True
    App.run()
#
#
#300 - 9 fps
#300 - 1delta 40 fps
#2000 - 1delta 14,34 
#2000 - 5 delta 3,89
#2000 - 5 delta 29 fps  6000 atoms
#2000 - 10 delta 20 fps 6000 atoms