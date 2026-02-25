import random
from re import S
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from mychem3d import mychemApp, Atom,Space
from functions import bond_atoms
from math import pi 
from math import *
import glm

#formula = [5,4,3,2,2,2,2,2,2,1,1,1,1,1]
#formula = [4,3,3,3,2,2,2,2,2,2]
formula = [4,4,2,1,1,1,1]
#formula = [4,1,1,1,1]
#def select_atom

dist = 35

def action1(space:Space):
    global curindex,tp, startindex,molecule
    if space.t==1:    #C
        tp = 0
        a0 = Atom(300,500,500,formula[tp])
        space.appendatom(a0)
        space.atoms2compute()
        startindex = 0
        molecule = [a0]
        

    if space.t>0 and space.t%500==0: #C
        tp+=1
        if tp>=len(formula): tp=0
        space.compute2atoms()
        N = len(space.atoms)
        npos = glm.vec3(0,0,0)
        apos = glm.vec3(500,500,500)
        found = False
        #a1 = Atom(p.x+60,p.y,p.z,random.randint(1,4))
        for i in range(startindex,len(space.atoms)):
            target = space.atoms[i]
            apos = space.atoms[i].pos
            print("i=",i)
            for n in target.nodes:
                if not n.bonded:
                    npos = n.pos
                    found = True
                    break
            else:
                print("start inc")
                startindex+=1
            if found: break
        if found:
            print(f"found {target.type}")
            npos = target.rot * npos
            npos = glm.normalize(npos)
            a1 = Atom(apos.x+npos.x*dist,apos.y+npos.y*dist,apos.z+npos.z*dist,formula[tp])
            v1 = glm.normalize(a1.nodes[0].pos)
            v2 = glm.normalize(apos-a1.pos)
            dt = glm.dot(v1,v2)
            angle = acos(dt)
            print("angle=", angle)
            axes = glm.cross(v1,v2)
            print("axes=", axes)
            if axes == glm.vec3(0,0,0):
                a1.rot = glm.quat(cos(pi/2), sin(pi/2)*glm.vec3(0,1,0))
            else:
                a1.rot = glm.normalize(glm.quat(cos(angle/2), sin(angle/2)*axes))
            a1.calc_node_positions()
            space.appendatom(a1)
            bond_atoms(target,a1) 
            molecule.append(a1)
        else:
            #center = space.get_atoms_center(molecule)
            apos = glm.vec3(random.randint(100,900), random.randint(100,900), random.randint(100,900))
            a0 = Atom(apos.x,apos.y,apos.z,formula[tp])
            space.appendatom(a0)
            molecule = [a0]
        space.atoms2compute()

    if space.t==503:
        pass

if __name__ == '__main__':
#
    random.seed(1)
    App = mychemApp()
    space = App.space
    space.action = action1
    #space.INTERACT_KOEFF = 1
    space.BOND_KOEFF = 0.4
    space.REPULSION_KOEFF2 = 0.1
    space.REPULSION_KOEFF1 = 7
    space.update_delta = 15
    #space.gpu_compute.set(False)
    #space.bondlock.set(True)
    App.run()
#
#
