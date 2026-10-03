import random
from re import S
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from mychem3d import mychemApp, Atom
from math import pi 
import mychem3d
from math import *
import glm
import time


#            
# #
#
if __name__ == '__main__':
#    random.seed(1)
    App = mychemApp()
    space = App.space
    space.setSize(1500,500,200)
    time.sleep(1)
    
    space.merge_from_file_random("examples/amide/formamide.json",400)
    #space.export = True
    #space.merge_from_file("examples/alkane/30ane.json",glm.vec3(100,100,100))
    space.update_delta = 10
    #space.gpu_compute.set(False)
    space.highlight_unbond = True
    #space.ROTA_KOEFF = 5
    #space.recording.set(True)
    #space.appendmixer(2)
    #space.redox.set(True)
    #space.export_nodes = True
    #space.competitive =True
    #space.stoptime=5
    App.run()
#
#
