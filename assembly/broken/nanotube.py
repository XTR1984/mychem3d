import random
from re import S
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from mychem3d import mychemApp, Atom,Space
from functions import bond_atoms
from math import pi 
import mychem3d
from math import *
import glm


def action1(space):
    (x,y,z)=(500,500,500)
    if space.t==0:    #C + H
#ring1
          n= 6
          f = 0
          f2 = -pi/6
          df = 2*pi/n
          r = 21*n/(2*pi)
          while(f<=2*pi-df):
            dx = r* cos(f)
            dy = r* sin(f)
            a = Atom(500+dx,500+dy,900,4,f=f,f2=f2)
            space.appendatom(a)
            f +=df
# ring2  
          n= 12
          f = 0
          df = 2*pi/n
          for i in range(0,n):
            r = 19*n/(2*pi)
            f = 2*pi/n*i
            f2 = pi/3
            dz = 0
            if i%2==1:
                #f+=pi
                f2+=-2*pi/3
                dz=-9
                r+=3
            dx = r* cos(f)
            dy = r* sin(f)
            a = Atom(500+dx,500+dy,885+dz,4,f=f,f2=f2)
            space.appendatom(a)
#ringN
          offset=855      
          for j in range(0,20):
            n= 12
            f = 0
            df = 2*pi/n
            r = 19*n/(2*pi)
            shift = 0
            if j%2==0:
               shift=1
            for i in range(0,n):
                f = 2*pi/n*(i+shift)
                f2 = 0
                dx = r* cos(f)
                dy = r* sin(f)
                dz = 0
                if i%2==1:
                    f2=-pi/2
                    dz-=7
                a = Atom(500+dx,500+dy,offset+dz,4,f=f,f2=f2)
                space.appendatom(a)
            offset-=25
           
#ring 5
          n= 12
          f = 0
          df = 2*pi/n
          for i in range(0,n):
            r = 19*n/(2*pi)
            f = 2*pi/n*(i+1)
            f2 = 0
            dz = 0
            if i%2==1:
                #f+=pi
                f2+=-2*pi/3
                dz=-8
            dx = r* cos(f)
            dy = r* sin(f)
            a = Atom(500+dx,500+dy,offset+dz,4,f=f,f2=f2)
            space.appendatom(a)
#ring6
          n= 6
          f = 0
          df = 2*pi/n
          r = 20*n/(2*pi)
          for i in range(0,n):
            f = 2*pi/n*i
            f2 = 5*pi/6
            dx = r* cos(f)
            dy = r* sin(f)
            a = Atom(500+dx,500+dy,offset-24,4,f=f+pi,f2=f2)
            #if i%2==1:
                #f+=pi
                #f2*=-1
            space.appendatom(a)

          space.atoms2compute()
          space.pause = True




if __name__ == '__main__':
#
    random.seed(1)
    App = mychemApp()
    space = App.space
    space.action = action1
#    space.INTERACT_KOEFF = 0.1
    #space.REPULSION_KOEFF2 = 5
    #space.BOND_KOEFF = 0.1
    #space.INTERACT_KOEFF = 0.1
    space.update_delta = 15
    #space.gpu_compute.set(False)
#    space.bondlock.set(True)
    App.run()
#
#
