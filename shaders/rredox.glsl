#version 430
// Set up our compute groups
layout(local_size_x=LOCALSIZEX, local_size_y=1,local_size_z=1) in;

// Input uniforms go here if you need them.
uniform int N;
uniform vec3 box;


//uniform float frame_time;
float WIDTH = box.x;
float HEIGHT = box.y;
float DEPTH = box.z;


#include "common.glsl"

// Input buffer
layout(std430, binding=0) buffer atoms_in
{
    AtomD atoms[];
} In;

layout(std430, binding=2) buffer atoms_static
{
    AtomS atoms[];
} Static;


float rand(vec2 co){
    return fract(sin(dot(co, vec2(12.9898, 78.233))) * 43758.5453);
}


int i = int(gl_GlobalInvocationID);

void main()
{
    vec3 pos_i= In.atoms[i].pos.xyz;
    vec3 v_i = In.atoms[i].v.xyz;

    //random redox 
    if (pos_i.x<300){
                if (rand(v_i.xy)>=0.99){
                    In.atoms[i].nodes[0].q = 1;
                    In.atoms[i].nodes[0].spin = 0;
                    Static.atoms[i].highlight = 500;                    
                }
    }
    if (pos_i.x>WIDTH-300){
       if (rand(v_i.xy)>=0.99) {
            In.atoms[i].nodes[0].q = -1;
            In.atoms[i].nodes[0].spin = 0;
            Static.atoms[i].highlight = 500;
            }    
    }
 
}