#version 430
// Set up our compute groups
layout(local_size_x=LOCALSIZEX, local_size_y=1,local_size_z=1) in;

// Input uniforms go here if you need them.
uniform int N;
uniform vec3 box;


//uniform float frame_time;
uniform float TDELTA;
uniform float CHARGE_KOEFF;
uniform float MASS_KOEFF;
uniform float NEARDIST;
uniform float NODEDIST;
uniform float HEAT;
float WIDTH = box.x;
float HEIGHT = box.y;
float DEPTH = box.z;

#include "common.glsl"

// Input buffer
layout(std430, binding=0) buffer atoms_in
{
    AtomD atoms[];
} In;

layout(std430, binding=1) buffer atoms_out
{
    AtomD atoms[];
} Out;


layout(std430, binding=2) buffer atoms_static
{
    AtomS atoms[];
} Static;


layout(std430, binding=3) buffer near_atoms
{
    int indexes[][NEARATOMSMAX];
} Near;

layout(std430, binding=4) buffer far_field
{
    vec4 F[];
} Far;

layout(std430, binding=5) buffer rpos_buffer
{
    vec4 rpos[][6];
};

layout(std430, binding=6) buffer qs_buffer
{
    float qshift_buffer[][6];
};

vec4 qmul(vec4 q1, vec4 q2)
{
         return vec4(
             q2.xyz * q1.w + q1.xyz * q2.w + cross(q1.xyz, q2.xyz),
             q1.w * q2.w - dot(q1.xyz, q2.xyz)
         );
}
   
     // Vector rotation with a quaternion
     // http://mathworld.wolfram.com/Quaternion.html
vec3 rotate_vector(vec3 v, vec4 r)
{
         vec4 r_c = r * vec4(-1, -1, -1, 1);
         return qmul(r, qmul(vec4(v, 0), r_c)).xyz;
}


int i = int(gl_GlobalInvocationID);

void main()
{
    AtomD atom_i = In.atoms[i];
    AtomS atom_iS = Static.atoms[i]; 
    vec3 pos_i= atom_i.pos.xyz;

    //calc near atoms  and far field
    int index = 0;
    vec3 E = vec3(0,0,0);
    for (int j=0;j<N;j++){
        if (i == j) continue;
        float r = distance(pos_i, In.atoms[j].pos.xyz);
        if (r==0.0) continue;
        if (r<NEARDIST){
            Near.indexes[i][index+1]=j;
            index++;
        }
        else {  //far field
            vec3 delta = In.atoms[i].pos.xyz - In.atoms[j].pos.xyz;
            float e1= Static.atoms[j].q*CHARGE_KOEFF/r/r;
            E += e1 * delta/r;  
        }
    }
    Near.indexes[i][0]=index;  // near atoms count
    Far.F[i].xyz = E * Static.atoms[i].q;

}