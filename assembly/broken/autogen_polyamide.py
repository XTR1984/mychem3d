import random
from re import S
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from mychem3d import mychemApp, Atom,Space
from functions import bond_atoms
from math import pi 
from math import *
import glm


timeout=1500


def action1(space):
    global curindex,tp,g1,g2,nexttime,counter
    if space.t==0:    #C
        tp = 0
        g1=space.merge_from_file("examples/amide/formamide.json",-450+500,100+500,450+500)
        space.atoms2compute()
        counter = 0

    if space.t==counter*timeout: #C
        space.compute2atoms()
        space.atoms[g1].nodes[0].q=0  #remove H
        pos = space.atoms[g1].pos
        g2=space.merge_from_file("examples/amide/formamide.json",pos.x+50,pos.y,pos.z-20)
        curindex = 0
        space.atoms2compute()

    if space.t==counter*timeout+10:  # remove H
            space.compute2atoms()
            space.atoms[g1].v=glm.vec3(0,0,0)
            space.atoms[g2].v=glm.vec3(0,0,0)
            space.atoms[g2+2].nodes[1].q=0
            space.atoms[g2+3].nodes[0].q=-1
            space.atoms2compute()


    if space.t==counter*timeout+300:  #bond
            space.compute2atoms()
            space.atoms[g1].nodes[0].q=-1
            space.atoms[g2+2].nodes[1].q=1
            g1 = g2  #next
            space.atoms2compute() 
            if counter<24: 
                 counter+=1



if __name__ == '__main__':
#
    random.seed(1)
    App = mychemApp()
    space = App.space
    space.action = action1
    space.INTERACT_KOEFF = 0.3
    space.BOND_KOEFF = 0.3
    space.update_delta = 10
    #space.gpu_compute.set(False)
    #space.bondlock.set(True)
    App.run()
#
#
