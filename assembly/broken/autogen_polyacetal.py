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
    global curindex,tp,g1,g2,nexttime,counter,turn
    if space.t==0:    #C
        tp = 0
        g1=space.merge_from_file("examples/aldehyde/formaldehyde.json",500,600,950)
        #space.atoms[g1+3].nodes[1].q=0
#        space.atoms[g1].nodes[2].q=0 
        space.atoms2compute()
        counter = 0
        turn =0 

    if space.t==counter*timeout+50: #C
        space.compute2atoms()
        if turn == 1: 
            space.atoms[g1].nodes[2].q=0 
            #space.atoms[g2].color = (0,1,0)
            turn=0 
        else:
            space.atoms[g1+3].nodes[0].q=0 
            #space.atoms[g2+3].color = (0,1,0)
            turn=1
        pos = space.atoms[g1].pos
        g2=space.merge_from_file("examples/aldehyde/formaldehyde.json",pos.x+80,pos.y,pos.z-20)
        curindex = 0
        space.atoms2compute()

    if space.t==counter*timeout+100:  # remove H
            space.compute2atoms()
            #space.atoms[g1].v=glm.vec3(0,0,0)
            #space.atoms[g2].v=glm.vec3(0,0,0)
            #bond_atoms(space.atoms[g1+3],space.atoms[g2])
            space.atoms2compute()


    if space.t==counter*timeout+300:  #bond
            space.compute2atoms()
        #    space.atoms[g1].nodes[0].q=-1
            #space.atoms[g2+2].nodes[1].q=1
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
    #space.BOND_KOEFF = 0.3
    space.update_delta = 10
    App.run()
#
#
