import random
from re import S
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from mychem3d import mychemApp, Atom,Space
from functions import bond_atoms
from math import pi 
from math import *
import glm

formula = [4,2,1,1]
#def select_atom

timeout=2000


def action1(space):
    global curindex,tp,g1,g2,nexttime,counter
    if space.t==0:    #C
        tp = 0
        g1=space.merge_from_file("examples/aminoacids/glycine.json",500,500,100)
        space.atoms2compute()
        counter = 0

    if space.t==counter*timeout: #C
        space.compute2atoms()
        space.atoms[g1].nodes[0].q=0  #remove OH
        pos = space.atoms[g1].pos
        g2=space.merge_from_file("examples/aminoacids/glycine.json",pos.x,pos.y,pos.z)
        curindex = 0
        space.atoms2compute()

    if space.t==counter*timeout+20:  #remove H
            space.compute2atoms()
            space.atoms[g2+7].nodes[0].q=0
            space.atoms2compute()


    if space.t==counter*timeout+1000:  #bond
            space.compute2atoms()
            space.atoms[g1].nodes[0].q=-1
            space.atoms[g2+7].nodes[0].q=1
            g1 = g2  #next
            space.atoms2compute() 
            if counter<15: 
                 counter+=1



if __name__ == '__main__':
#
    random.seed(1)
    App = mychemApp()
    space = App.space
    space.action = action1
    #space.INTERACT_KOEFF = 0.5
    space.BOND_KOEFF = 0.2
    space.update_delta = 35
    #space.gpu_compute.set(False)
    #space.bondlock.set(True)
    App.run()
#
#
