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
    App = mychemApp()
    space = App.space
    space.setSize(2000,1000,200)
    
    
    space.merge_from_file_random("examples/simple/NH3.json", 300)
    space.merge_from_file_random("examples/aldehyde/glycolaldehyde.json",300)

    space.update_delta = 10
     #space.recording = True
    #space.INTERACT_KOEFF = 5.0
    #space.REPULSION_KOEFF2=50
    space.SIGMA=0
    space.BOND_KOEFF = 100
#    space.MASS_KOEFF = 5
    space.appendmixer(1)
    #space.redox.set(True)
    space.NODEDIST = 40
    space.NEARDIST = 200
    space.pause = True
    #space.highlight_unbond=True
    App.run()
#
#
#300 - 9 fps  update_delta=5    nodesinter 100
#300 - 40 fps update_delta=5    nodesinter 40  near field 200, <5000 atoms
#300 - 26 fps update_delta=5    nodesinter 40  near field 300, <5000 atoms
#300 - 26 fps update_delta=5    nodesinter 40  near field 300, <`0000 atoms
#300 - 36 fps update_delta=5    nodesinter 40  near field 200,  atoms
#300 - 23 fps update_delta=5    nodesinter 40  near field 200, 3600 atoms
#300 - 40.5 fps update_delta=5    nodesinter 40  near field 200, 3600 atoms 
#300 - 27-29 fps update_delta=10    nodesinter 40  near field 200, 3600 atoms 
#300 - 32 fps update_delta=10    nodesinter 40  near field 200, 3600 atoms 

