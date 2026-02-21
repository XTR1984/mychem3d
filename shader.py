#import OpenGL.GL.shaders

from OpenGL.GL import *
import glm
import re

class CommonShader:
    def __init__(self):
        self.source = ""

    def load_shader_source(self,filepath, current_line=1, is_root=True):
        with open("shaders/"+filepath, 'r') as file:
            lines = file.readlines()
        source = ""
        if not is_root:
            source += f'#line {current_line+10000}\n'
        for line in lines:
            include_match = re.match(r'#include\s+"([^"]+)"', line)
            if include_match:
                included_file = include_match.group(1)
                included_source = self.load_shader_source(included_file, current_line=1, is_root=False)
                source += included_source
                source += f'#line {current_line}\n'
            else:
                source += line
                current_line += 1
        return source

    def use(self):
        glUseProgram(self.program)
    
    def unuse(self):
        glUseProgram(0)        

    def extract_uniform_names(self,glsl_code):
        pattern = r'uniform\s+\w+\s+(\w+)(?:\s*=\s*[^;]+)?\s*;'
        uniforms = re.findall(pattern, glsl_code)
        return uniforms

    def init_uniforms(self):
        uniforms = self.extract_uniform_names(self.source)
        if len(uniforms)>0:
            self.init_uniforms0(uniforms)

    def init_uniforms0(self,uniforms= []):
        self.loc = {}
        for u in uniforms:
            self.loc[u] = glGetUniformLocation(self.program, u)
            #self.loc.update( {"stage": glGetUniformLocation(self.compute_shader, "stage")})

    def setInt(self, name, value:int):
        glUniform1i(self.loc[name],value)

    def setFloat(self,name,value):
        glUniform1f(self.loc[name],value)

    def set3f(self,name, x,y,z):
        glUniform3f(self.loc[name],x,y,z)

    def set4f(self,name, x,y,z,w):
        glUniform4f(self.loc[name],x,y,z,w)


    def setMatrix4(self, name, value):
        glUniformMatrix4fv(self.loc[name],1, GL_FALSE, glm.value_ptr(value))





        

        


class Shader(CommonShader):
    def __init__(self, vertex_shader_path, fragment_shader_path):
        self.program = glCreateProgram()
        self.vertex_shader_source = self.load_shader_source(vertex_shader_path)
        self.vertex_shader = self.compile_shader(self.vertex_shader_source, GL_VERTEX_SHADER)
        self.fragment_shader_source = self.load_shader_source(fragment_shader_path)        
        self.fragment_shader = self.compile_shader(self.fragment_shader_source, GL_FRAGMENT_SHADER)
        self.source = self.vertex_shader_source + self.fragment_shader_source
        glAttachShader(self.program, self.vertex_shader)
        glAttachShader(self.program, self.fragment_shader)
        glLinkProgram(self.program)
        self.init_uniforms()

    def compile_shader(self, source, shader_type):
        shader = glCreateShader(shader_type)
        glShaderSource(shader, source)
        glCompileShader(shader)
        if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
            raise RuntimeError(glGetShaderInfoLog(shader))
        return shader


    def cleanup(self):
        glDeleteShader(self.vertex_shader)
        glDeleteShader(self.fragment_shader)
        glDeleteProgram(self.program)


class ComputeShader(CommonShader):
    commonparams = {}
    def __init__(self, source_file, pparams={}):
        self.program = glCreateProgram()
        self.source= self.load_shader_source(source_file)
        pparams = self.commonparams | pparams 
        for key,value in pparams.items():
                self.source = self.source.replace(key,value)
        self.compute_shader = OpenGL.GL.shaders.compileShader(self.source, GL_COMPUTE_SHADER)
        glAttachShader(self.program, self.compute_shader)
        glLinkProgram(self.program)            
        self.init_uniforms()


    def run(self, x,y,z, barrier=True):
        glDispatchCompute(x,y,z)     
        if barrier: 
            glMemoryBarrier(GL_SHADER_STORAGE_BARRIER_BIT)  
