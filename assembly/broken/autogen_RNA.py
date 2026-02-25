import random
from re import S
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from mychem3d import mychemApp, Atom,Space
from functions import bond_atoms
from math import pi 
from math import *
import glm


seq = "ATCGATCGATCGATCG"

data = { "A": {"name":"adenosine", "corr":(0,0,0)},
         "T": {"name":"thymidine", "corr":(0,0,30)},
         "C": {"name":"cytidine",  "corr":(0,20,30)},
         "G": {"name":"guanosine", "corr":(0,0,0)},
         "U": {"name":"uridine",   "corr":(-20,40,30)}
       }


deltat=8000

def action1(space):
    global curindex,tp,nexttime,counter,index1,index2,index3
    (x,y,z)=(200,200,800)
    if space.t==0:
        counter = 0
        tp = seq[counter]
        corr = glm.vec3(data[tp]["corr"])
        index1=space.merge_from_file("examples/nucleobase/"+data[tp]["name"]+".json",x+corr.x,y+corr.y,z+corr.z)
        #space.atoms[index1+3].color=(0,1,0)
        #space.atoms[index1+5].color=(0,1,0)
        space.atoms[index1+5].nodes[2].q=0  #-OH

        space.atoms2compute()

    if space.t==counter*deltat+100: #C
        space.compute2atoms()
#        space.atoms[index1+5].nodes[0].q=0
        if counter+1==len(seq): return

        pos = space.atoms[index1].pos
        rot = glm.quat(cos(pi/4), sin(pi/4)*glm.vec3(0,0,1))
        index2=space.merge_from_file("examples/simple/h3po4.json",pos.x-20,pos.y+50,pos.z,rot)

        tp = seq[counter+1]
        corr = glm.vec3(data[tp]["corr"])
        space.atoms[index1].color=(0,1,0)  
        #space.atoms[index2+4].color=(0,1,0)
        space.atoms[index2+2].nodes[0].q=0  #H3PO4 -H down
        space.atoms[index2+6].nodes[0].q=0  #H3PO4 -H up
        index3=space.merge_from_file("examples/nucleobase/"+data[tp]["name"]+".json",pos.x+corr.x, pos.y+130+corr.y,pos.z+corr.z)
        space.atoms[index3+3].nodes[2].q=0        

        #curindex = 0
        space.atoms2compute()

    if space.t==counter*deltat+1500:  #H3PO4 + n1
            space.compute2atoms()
            bond_atoms(space.atoms[index1+5],space.atoms[index2+2])  
            #space.atoms[index3].v = glm.vec3(0,0,0)
            space.atoms2compute()

    if space.t==counter*deltat+2700:  #bond  H3PO4 + n2
            space.compute2atoms()
            bond_atoms(space.atoms[index3+3],space.atoms[index2+6])
            space.atoms2compute() 

    if space.t==counter*deltat+4200:  #bond
            space.compute2atoms()
            space.atoms[index3+5].nodes[2].q=0   #riboza 5-oh
            #space.atoms[index1].v = glm.vec3(0,0,0)
            index1 = index3  #next
            space.atoms2compute() 
            if counter+1!=len(seq): counter+=1



if __name__ == '__main__':
#
    random.seed(1)
    App = mychemApp()
    space = App.space
    space.setSize(2000,2000,2000)
    space.action = action1
    #space.INTERACT_KOEFF = 0.5
    #space.BOND_KOEFF = 0.2
    #space.REPULSION_KOEFF2=0.2
    space.update_delta = 15
    #space.gpu_compute.set(False)
    #space.bondlock.set(True)
    App.run()
#
#
