import random
from re import S
from mychem3d import mychemApp, Atom
from math import pi 
import mychem3d
from math import *
import glm





def makealkane(space,x,y,z,n):
     space.appendatom(Atom(x-3,y-15,z-5,1,f=pi/2))
     for i in range(0,n):
         f2 = i%2 * pi
         dx = -10 * (i%2) 
         dz = -5 * (i%2) 
         space.appendatom(Atom(x+dx,y+i*15,z+dz,6,f2=f2))  # 4->6 (C)
         if i%2 == 0:
             space.appendatom(Atom(x,y+i*15,z+17,1,f2=-pi/2))
             space.appendatom(Atom(x+17,y+i*15,z-5,1,f=pi,f2=0))
         else:
             space.appendatom(Atom(x+dx,y+i*15,z+dz-17,1,f2=pi/2))
             space.appendatom(Atom(x+dx-15,y+i*15,z+dz+5,1,f=0,f2=0))
     space.appendatom(Atom(x-5,y+n*15,z,1,f=3*pi/2))

def makecarboxylic(space,x,y,z,n):
     f = pi/2
     rot1 = glm.normalize(glm.quat(cos(f/2), sin(f/2)* glm.vec3(1,0,0)))
     f = pi
     rot2 = glm.normalize(glm.quat(cos(f/2), sin(f/2)* glm.vec3(0,1,0)))
     space.merge_from_file("examples/simple/carboxyl.json", x+5,y-10,z, rot2*rot1)
     for i in range(1,n):
         f2 = i%2 * pi
         dx = -10 * (i%2) 
         dz = -5 * (i%2) 
         space.appendatom(Atom(x+dx,y+i*15,z+dz,6,f2=f2))  # 4->6 (C)
         if i%2 == 0 :
             space.appendatom(Atom(x,y+i*15,z+17,1,f2=-pi/2))
             space.appendatom(Atom(x+17,y+i*15,z-5,1,f=pi,f2=0))
         elif not i%2==0:
             space.appendatom(Atom(x+dx,y+i*15,z+dz-17,1,f2=pi/2))
             space.appendatom(Atom(x+dx-15,y+i*15,z+dz+5,1,f=0,f2=0))
     space.appendatom(Atom(x-5,y+n*15,z,1,f=3*pi/2))

def makealcohol(space,x,y,z,n):
     space.appendatom(Atom(x-3,y-15,z-5,1,f=pi/2))
     for i in range(0,n):
         f2 = i%2 * pi
         dx = -10 * (i%2) 
         dz = -5 * (i%2) 
         space.appendatom(Atom(x+dx,y+i*15,z+dz,6,f2=f2))  # 4->6 (C)
         if i%2 == 0:
             space.appendatom(Atom(x,y+i*15,z+17,8,f2=-pi/2))  # 2->8 (O)
             space.appendatom(Atom(x,y+i*15+15,z+20,1,f=3*pi/2))
             space.appendatom(Atom(x+17,y+i*15,z-5,1,f=pi,f2=0))
         else:
             space.appendatom(Atom(x+dx,y+i*15,z+dz-17,8,f2=pi/2))  # 2->8 (O)
             space.appendatom(Atom(x+dx,y+i*15+15,z+dz-20,1,f=3*pi/2))
             space.appendatom(Atom(x+dx-15,y+i*15,z+dz+5,1,f=0,f2=0))
     space.appendatom(Atom(x-5,y+n*15,z,1,f=3*pi/2))


def makepoly1(space,x,y,z,n=5): 
    D=20
    a1= Atom(x-D, y, z, 1)
    space.appendatom(a1)
    a1= Atom(x+n*D, y, z, 1,pi)
    space.appendatom(a1)
    for i in range(0,n):
        a1= Atom(x+i*D, y, z,6, pi if i%2!=0 else 0)  # 5->6? Был тип 5, заменяем на 6 (C)
        space.appendatom(a1)
        if i%2==0:
            a1= Atom(x+i*D, y-D,z, 1, pi/2)  # 2->8? Оставим 1
            space.appendatom(a1)
            a1= Atom(x+i*D, y-2*D,z, 1, pi/2*3)
            space.appendatom(a1)
        else:
            a1= Atom(x+i*D, y+D, z, 1, pi/2*3)  # 2->8? Оставим 1
            space.appendatom(a1)
            a1= Atom(x+i*D, y+2*D, z, 1, pi/2)
            space.appendatom(a1)





if __name__ == '__main__':
    random.seed(1)
    App = mychemApp()
    space = App.space
    space.setSize(1000,4000,1000)
    
    #makecarboxylic(space,500,500,500,10)
    #makecircleplane(space, 500)
    makealcohol(space,500,500,500,50)
    
    space.update_delta = 5  
    App.run()