import random
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
    App = mychemApp(maxatoms=10000)
    space = App.space
    space.setSize(200,200,200)

    #space.merge_from_file("examples/simple/H2O.json",100,100,100)        
    space.merge_from_file("examples/simple/OH.json",100,100,100)        

    a1 = Atom(50,100,100,1)
    a1.nodes[0].q = 1.0
    space.appendatom(a1)

    a2 = Atom(530,500,500,1)
    a2.nodes[0].q = -1.0

    space.appendatom(a2)
    space.update_delta = 1
    #space.cpucompute = True
    space.pause = True
    #space.stoptime=2
    #space.highlight_unbond=True
    App.run()
#
