import os
import json
from math import sqrt,sin,cos,pi,acos
import numpy as np
import random
from mychem_atom import Atom
import glm
import time

class Space:
    def __init__(self,N=50000,width=1500,height=1000,depth=1000):
        self.pause = False
        self.ucounter = 0
        self.maxatoms = N
        self.setSize(width,height,depth)
        self.debug = False
        self.test = False
        self.efield = False
        self.TDELTA = 1.0
        self.BOND_KOEFF = 200
        self.BONDR = 4.0
        self.CHARGE_KOEFF= 500.0
        self.SPIN_KOEFF= 30.0
        self.FIELD_KOEFF= 1.0
        self.ROTA_KOEFF = 10.0
        self.REPULSION1 = -6
        self.REPULSION_SIGMA = 0
        self.REPULSION2 = 6
        self.REPULSION_POW= 6
        self.REPULSION_EPS= 0.10
        self.ATTRACTION_KOEFF = 1
        self.MASS_KOEFF = 1.0
        self.MAXVELOCITY = 1
        self.NEARDIST = 200.0   # near atoms buffering
        self.NODEDIST = 60
        self.heat = 0
        self.t = -1
        self.stoptime = -1
        self.recordtime = 0
        self.recording = False
        self.recording3D = False
        self.record_data = False
        self.atoms = []	
        self.Ek = 0
        self.g = 0.001
        self.merge_atoms = []
        self.merge_rot = glm.quat()
        self.merge_center = glm.vec3(0,0,0)
        self.axis = glm.vec3(0)
        self.axis_origin = glm.vec3(0)
        self.select_mode = 0
        self.selected_atoms = [] 
        self.gravity = False
        self.shake= False
        self.SHAKE_KOEFF = 0.5
        self.redox = False
        self.redox_rate = 1
        self.bondlock =False
        self.highlight_unbond = False
        self.sideheat = False
        self.update_delta= 5
        self.action = None
        self.fdata = open('data.txt',"w")
        self.tranparentmode = False
        print("space created")

    def setSize(self, width,height,depth):
        self.WIDTH=width
        self.HEIGHT=height
        self.DEPTH=depth
        self.box = glm.vec3(self.WIDTH, self.HEIGHT, self.DEPTH)
        #print("box size =  ",self.box)
        self.merge_pos = self.box/2
        


    def appendatom(self,a):
        a.space = self
        self.atoms.append(a)

    def appendatom2(self,a):
        a.space = self
        self.atoms.append(a)
        self.glframe.atom2ssbo(a)
        self.N = len(self.atoms)




    def appendmixer(self,n=1):
        for i in range(0,n):
            m = Atom(random.randint(1,self.WIDTH),random.randint(1,self.HEIGHT),random.randint(1,self.DEPTH),666)
            m.space = self
            m.v = glm.vec3(random.random(),random.random(),random.random())
            m.m = 100
            self.atoms.append(m)
    
    def get_mergeobject_center(self):
         sum = glm.vec3(0,0,0)
         N = len(self.merge_atoms)
         for a in self.merge_atoms:
              sum += a.pos
         center = sum/N
         #print("center=",center)
         return center

    def get_atoms_center(self, atoms=None):
         if atoms==None:
            atoms = self.atoms
         sum = glm.vec3(0,0,0)
         N = len(atoms)
         for a in atoms:
              sum += a.pos
         center = sum/N
         return center

    def move_atoms(self, atoms, vector):
         for a in atoms:
              a.pos += vector

    def rotate_atoms(self, atoms, origin, rot):
         for a in atoms:
              a.pos = a.pos - origin
              a.pos = rot * a.pos
              a.pos = a.pos +  origin
              a.rot = rot * a.rot
        


    def selected2merge(self,duble=False):
        for i in self.selected_atoms:
                if duble:
                    a = self.atoms[i].copy()
                else:
                    a = self.atoms[i]
                self.merge_atoms.append(a)
                #a.unbond()  
        if not duble:
            for m in self.merge_atoms:
                self.atoms.remove(m)
        self.selected_atoms = []
        self.merge_rot = glm.quat()
#        self.merge_center = self.get_mergeobject_center()
#        self.merge_pos = glm.vec3(self.merge_center)
#        if duble:
#            self.merge_pos+=glm.vec3(5,0,0)


    def get_atoms_distant(self,atoms=None):
         if atoms==None:
              atoms = self.atoms
         center = self.get_atoms_center(atoms)
         distant = glm.vec3(0,0,0)
         N = len(atoms)
         for a in atoms:
              if abs(a.pos.x-center.x) > distant.x:
                   distant.x = a.pos.x-center.x
              if abs(a.pos.y-center.y) > distant.y:
                   distant.y = a.pos.y-center.y
              if abs(a.pos.z-center.z) > distant.z:
                   distant.z = a.pos.z-center.z
         return (center,distant)

    def get_node_by_index(self,index):
         index = int(index)
         if index==-1:
            return None
         ai = index//5
         ni = index%5
         #print(f"  for index{index} result = { ai}  {ni}")
         return self.atoms[ai].nodes[ni]
    
    def get_index_by_node(self,n):
        if n != None:
            parentindex = self.atoms.index(n.parent)
            nodeindex = n.parent.nodes.index(n)
            index = parentindex*5+nodeindex
            #print(f"node = {n} parentIndex={parentindex} nodeindex={nodeindex}")
        else:
            index = -1
        return index
         

    def atoms2compute(self):
        t = time.time()
        print("atoms2compute gpu")
        self.glframe.atoms2ssbo()
        delta = time.time() - t
        print("  delta=", delta)            

    
    def compute2atoms(self):
        t = time.time()
        print("compute2atoms gpu")
        self.glframe.ssbo2atoms()
        delta = time.time() - t
        print("  delta=", delta)     

    def merge2atoms(self):
        print("merge2atoms")
        #self.compute2atoms()
        first = len(self.atoms)
        self.merge_center = self.get_mergeobject_center()
        size = len(self.merge_atoms)
        for a in self.merge_atoms:
            self.appendatom(a)
        self.merge_atoms = []
        return first, size
        #self.atoms2compute()


    def merge_from_file(self, filename, x=0,y=0,z=0, merge_rot=glm.quat()):
        f =  open(filename,"r")		
        self.merge_atoms = []
        mergedata = json.loads(f.read())
        r = self.load_data(mergedata, merge=True)
        c = self.get_mergeobject_center()
        self.move_atoms(self.merge_atoms,(-c) + glm.vec3(x,y,z))
        self.rotate_atoms(self.merge_atoms,glm.vec3(x,y,z), merge_rot)
        first,size = self.merge2atoms()
        return first,size
    

    def make_export(self, atoms=None):
        if atoms==None:
            atoms=self.atoms
        frame = {}
        frame["vers"] = "1.1"
        frame["time"] = self.t
        frame["atoms"] = []
        N = len(atoms)
        for i in range(0,N):
            if atoms[i].color == (0,0,0): continue    #spec color for remove atoms on save
            atom = {}
            atom["id"] = atoms[i].id
            atom["type"] = atoms[i].type
            atom["color"] = atoms[i].color
            atom["x"] = round(atoms[i].pos.x,4)
            atom["y"] = round(atoms[i].pos.y,4)
            atom["z"] = round(atoms[i].pos.z,4)
            #atom["f"] = round(self.atoms[i].f,4)
            #atom["f2"] = round(self.atoms[i].f2,4)
            atom["rot"] = atoms[i].rot.to_tuple()
            atom["vx"] = round(atoms[i].v.x,4)
            atom["vy"] = round(atoms[i].v.y,4)
            atom["vz"] = round(atoms[i].v.z,4)
            atom["q"] = atoms[i].q
            atom["m"] = atoms[i].m
            atom["r"] = atoms[i].r
            atom["fixed"] = atoms[i].fixed
            atom["nodes"] = []
            for n in atoms[i].nodes:
                 node ={}
                 node["q"]=n.q
                 node["spin"]=n.spin
                 atom["nodes"].append(node)

            frame["atoms"].append(atom)
        return frame

    def load_data(self, j, merge=False, zerospeed=True):
        errors = False
        if not merge: 
            self.atoms = []
        vers = j["vers"]
        for a in j["atoms"]:
            type = a["type"]
            if vers=="1.0":
                update = {1:1, 2:8, 3:7, 4:6, 5:15, 6:16, 100:666 }
                type = update[type]
            #if type==100: continue
            if "z" in a:
                z = a["z"]
                vz = a["vz"]
                rot = glm.quat(a["rot"])
            aa = Atom(a["x"],a["y"],z, type=type )
            #aa.r = a["r"]
            if zerospeed and type!=666:
                aa.v= glm.vec3(0,0,0) 
            else:
                aa.v = glm.vec3(a["vx"],a["vy"],vz)
            aa.rot = rot
            aa.calc_node_positions()
#            aa.q=a["q"]
            #aa.m=a["m"]
            if "color" in a:
                aa.color = a["color"]
#            if not "version" in j:
#                 aa.f= 2*pi - aa.f
            ni = 0
            if "fixed" in a:
                aa.fixed = a["fixed"]
            if "nodes" in a:
                 for n in a["nodes"]:
                    aa.nodes[ni].q= n["q"]
                    if "spin" in n:
                        aa.nodes[ni].spin= n["spin"]
                    if (aa.nodes[ni].q!=0.0 and aa.nodes[ni].spin!=0.0) or (aa.nodes[ni].q==0.0 and aa.nodes[ni].spin==0.0): 
                        print("Inconsistent spin and q!")
                        errors = True
                    ni+=1
            if merge:
                aa.space = self
                self.merge_atoms.append(aa)
            else:
                self.appendatom(aa)
        return errors


