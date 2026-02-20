from math import sin,cos,sqrt,pi
import glm

class Camera():
    def __init__(self):
        self.yaw = 0
        self.pitch = 0
        self.up = glm.vec3(0,1,0)
        self.front = glm.vec3(0.5,0.5,-1)

        self.pos = glm.vec3(0,0,0)
        self.yaw = -90
        self.pitch = 0 
        self.fov = 45        

    def update(self, a, b):    
        front = ( cos(glm.radians(self.pitch))*cos(glm.radians(self.yaw)),
                 sin(glm.radians(self.pitch)),
                 cos(glm.radians(self.pitch))*sin(glm.radians(self.yaw)),
                )
        self.front = glm.normalize(front)
        self.view = glm.lookAt(self.pos, self.pos + self.front, self.up)
        self.projection = glm.perspective(glm.radians(self.fov), a/b, 0.01,20.0)

    def rotate(self, offsetx, offsety):
        self.pitch -=offsety
        self.yaw += offsetx
        if self.pitch > 89:
           self.pitch = 89
        if self.pitch < -89:
           self.pitch = -89

    def move(self,offsetx,offsety):
        self.pos -= glm.normalize(glm.cross(self.front, self.up)) * offsetx*0.05
        self.pos += self.up * offsety*0.05

    def go(self,delta,shift):
        if shift:
            cameraSpeed = 0.01
        else:
            cameraSpeed = 0.1
        if delta>0:
            self.pos += cameraSpeed * self.front
        else:
            self.pos -= cameraSpeed * self.front   

