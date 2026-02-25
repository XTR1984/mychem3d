from atom import Atom
from space import Space
import glm
from functions import bond_atoms
from math import acos,cos,sin,pi
from itertools import permutations


# https://www.molinstincts.com/search

def load_sdf(f, atoms):
#read file        
        natoms = 0
        nlinks = 0
        atoms_counter =0
        links_counter =0
        #data = 
        counter = 0
        result = True
        for l in f:
            counter+=1
            if counter<3: continue
            if counter==4:
                natoms = int(l[:3])
                nlinks = int(l[3:7])
                print(f"Loading: atoms:{natoms} links:{nlinks} ")
                if natoms>100000 or nlinks>100000: 
                    print(" too many natoms or links!")
                    result = False
                    break
                atoms_counter = natoms
                links_counter = nlinks
                continue
            if counter>4 and atoms_counter>0:
                atoms_counter -= 1
                sp = l.split()
                print(f"x={float(sp[0])} y={sp[1]} z={sp[2]} type={sp[3]}")
                k = 12
                x = float(sp[0])*k
                y = float(sp[1])*k
                z = float(sp[2])*k
                type = acr2type(sp[3])
                if type==None: 
                    print("Error in string ", counter)
                    result = False
                    a = Atom(x,y,z,1)
                    a.color = glm.vec3(0,0,0)
                else:
                    a = Atom(x,y,z,type)
                    a.neibs_n = []
                a.fixed = 1.0
                atoms.append(a)
            if (counter>4+natoms) and links_counter>0:
                links_counter -= 1
                #sp = l.split()
                #print(f"n1={l[:3]},n2={l[3:7]},bt={l[7:10]}")
                n1 = int(l[:3].strip())-1
                n2 = int(l[3:7].strip())-1
                bt = int(l[7:10].strip())
                #print(f"n1={n1},n2={n2},bt={bt}")
                #print("neib append",n1,n2)
                if bt<=3:
                    for k in range(0,bt):
                        atoms[n1].neibs_n.append( (n2,bt))
                        atoms[n2].neibs_n.append( (n1,bt))
#align
        #align hydrogen
        for a in atoms:
            i = atoms.index(a)
#            if i == 3: a.color = glm.vec4(0,1,0,1)
#            if i == 0: a.color = glm.vec4(1,0,1,1)
#            print(f"i= {i } type = {a.type} neibs_n = ", a.neibs_n)
            if a.type==1:
                if len(a.neibs_n)!=1:
                     print("no neibs")
                     continue
                v1 = glm.normalize(a.nodes[0].pos)
                delta = atoms[a.neibs_n[0][0]].pos-a.pos
                v2 = glm.normalize(delta )
                a.rot = glm.quat(v1,v2)
        #for other atoms, turn node 0 to 1-link neib, and rotate for fit to other
        for a in atoms:
            i = atoms.index(a)
            if a.type==1:
                 continue
            single_i = -1
            for j in a.neibs_n:
                if j[1]==1: #single-link
                    single_i = j[0]
                    H = atoms[single_i]
                    break
            if single_i == -1: continue
            print(f"rotate {i} over {single_i}")
            v1 = a.nodes[0].pos
            v2 = H.pos - a.pos
            rot1 = glm.quat(v1,v2)
            neibs = [x[0] for x in a.neibs_n]
            l1 = list(permutations(range(len(neibs)-1) ))
            neibs2 = neibs.copy()
            neibs2.remove(single_i)
            l2 = list(permutations(neibs2))
            bestrot = rot1
            bestangle = 0
            minr = 100000
            for i1 in l1:
                 for i2 in l2:
                      angle = 0
                      while (angle<2*pi):
                        rot2 = glm.normalize(glm.quat(cos(angle/2), sin(angle/2)* glm.normalize(-v2)))
                        rot = glm.normalize(rot2*rot1)
                        sum = 0
                        for pair in zip(i1,i2):
                            o1 = rot* a.nodes[pair[0]+1].pos  + a.pos
                            o2 = atoms[pair[1]].pos
                            sum += glm.distance(o1,o2)
                        if sum < minr:
                            minr = sum
                            bestrot = rot
                            bestangle = angle
#                        if i==3:
#                            print(f"angle={glm.degrees(angle)} sum={sum}")
                        angle+=2* pi/24.0
            a.rot = bestrot
#            print("bestangle=",glm.degrees(bestangle))
        #align O with 2-link
        for atom_i in atoms:
            i = atoms.index(atom_i)
            if atom_i.type==8 and atom_i.neibs_n[0][1]==2:
                #atom_i.color = glm.vec4(1,0,1,1)
                neib_j = atom_i.neibs_n[0][0]
                atom_j = atoms[neib_j]
                v1 = glm.normalize(atom_i.nodes[0].pos + atom_i.nodes[1].pos)
                v2 = atom_j.pos - atom_i.pos
                rot1 = glm.quat(v1,v2)
                angle = 0
                near_nj = 0
                minr=1000
                o1= rot1* atom_i.nodes[0].pos + atom_i.pos
                for nj in range (len(atom_j.nodes)):
                    o2 = atom_j.rot * atom_j.nodes[nj].pos + atom_j.pos
                    rn = glm.distance(o1,o2)
                    if (rn<minr):
                        near_nj = nj
                        minr = rn
                realpos_ni = rot1*atom_i.nodes[0].pos
                realpos_nj = atom_j.rot* atom_j.nodes[near_nj].pos
                v2 = glm.normalize(v2)
                v3 = realpos_ni - glm.dot(realpos_ni, v2)  * v2
                v4 = realpos_nj - glm.dot(realpos_nj, v2)  * v2
                rot2 = glm.quat(v3,v4)
                atom_i.rot = rot2*rot1
        #bond nearest
        for atom_i in atoms:
            for ni in range(len(atom_i.nodes)):                
                if atom_i.nodes[ni].bonded == True: continue
                if atom_i.nodes[ni].type==2: continue
                nearest_node = -1
                nearest_neib = -1
                minr = 10000
                neibs = [x[0] for x in atom_i.neibs_n]
                for j in neibs:
                    atom_j = atoms[j]
                    for nj in range(len(atom_j.nodes)):
                        if atom_j.nodes[nj].bonded == True: continue
                        if atom_j.nodes[nj].type==2: continue
                        o1 = atom_i.rot* atom_i.nodes[ni].pos + atom_i.pos
                        o2 = atom_j.rot* atom_j.nodes[nj].pos + atom_j.pos
                        rn = glm.distance(o1,o2)
                        if rn<minr:
                            minr = rn
                            nearest_node = nj
                            nearest_neib = j
                if (nearest_node!=-1):
                    #info = f"i={atoms.index(atom_i)} typei={atom_i.type} j={nearest_neib } typej={atom_j.type}"
                    #print(info)
                    bond_atoms(atom_i,atoms[nearest_neib],ni,nearest_node)        
        return result


def acr2type(acr):
        if acr=="H": return 1
        if acr=="O": return 8
        if acr=="N": return 7
        if acr=="C": return 6
        if acr=="P": return 15
        if acr=="S": return 16
        print("unknown atom's type")
        return None
