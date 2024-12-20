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
    for i in range(0,400):
            #makealcohol(space,random.randint(100,900),random.randint(100,900),random.randint(100,900),3)
        #space.merge_from_file("examples/simple/NH3.json",random.randint(-500,500),random.randint(-500,500),random.randint(-500,500))
        #space.merge_from_file("examples/simple/H2O.json",random.randint(-400,500),random.randint(-500,500),random.randint(-400,400))
        #space.merge_from_file("examples/alkene/etylen.json",random.randint(-400,500),random.randint(-500,500),random.randint(-400,400))
        #space.merge_from_file("examples/alkane/decane.json",random.randint(-400,500),random.randint(-500,500),random.randint(-400,400))
        #space.merge_from_file("examples/aldehyde/glycolaldehyde.json",random.randint(-500,500),random.randint(-500,500),random.randint(-500,500))
        f = random.random()*pi
        rot = glm.normalize(glm.quat(cos(f/2), sin(f/2)* glm.vec3(random.random(),random.random(),random.random())))
        x = random.randint(0,space.WIDTH)
        y = random.randint(0,space.HEIGHT)
        z = random.randint(0,space.DEPTH)        
        space.merge_from_file("examples/amide/formamide.json",x,y,z,rot)
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
