import random
from re import S
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from mychem3d import mychemApp, Atom,Space
from functions import bond_atoms
from math import pi 
from math import *
import glm

#formula = [3,2,2,2,2,2,2,2,2,2,2,2]
formula = [4,2,2,2,2,4,4,]
#def select_atom


def action1(space):
    global curindex,tp, startindex
    if space.t==1:    #C
        tp = 0
        a0 = Atom(50,500,500,formula[tp])
        space.appendatom(a0)
        space.atoms2compute()
        startindex = 0
        

    if space.t>0 and space.t%600==0: #C
        tp+=1
        if tp>=len(formula): tp=0
        space.compute2atoms()
        N = len(space.atoms)
        (c,d) = space.get_atoms_distant()
        p = c+d*0.8
        #a1 = Atom(p.x+60,p.y,p.z,random.randint(1,4))
        a1 = Atom(p.x+60,p.y,p.z,formula[tp])
        space.appendatom(a1)
        curindex = startindex
        while  curindex == space.atoms.index(a1) or not bond_atoms(space.atoms[curindex],a1) :
            curindex+=1
            #startindex+=1
            if curindex>N: break
        space.atoms2compute()

    if space.t==503:
        pass

if __name__ == '__main__':
#
    random.seed(1)
    App = mychemApp()
    space = App.space
    space.action = action1
    space.INTERACT_KOEFF = 1
    space.BOND_KOEFF = 0.2
    space.REPULSION_KOEFF2 = 0.1
    space.update_delta = 15
    #space.gpu_compute.set(False)
    #space.bondlock.set(True)
    App.run()
#
#
