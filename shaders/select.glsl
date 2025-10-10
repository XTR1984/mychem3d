#version 430
// Set up our compute groups
layout(local_size_x=1, local_size_y=1,local_size_z=1) in;

// Input uniforms go here if you need them.

//uniform float frame_time;
uniform float TDELTA;
float BONDR = 4;
uniform float BOND_KOEFF;
layout(binding = 0) uniform atomic_uint nselected;

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

layout(std430, binding=4) buffer rpos_buffer
{
    vec4 rpos[][6];
};


layout(std430, binding=7) buffer selected_in
{
    int indexes[];
} SelIn;

layout(std430, binding=8) buffer selected_out
{
    int indexes[5000];
} SelOut;






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
    //for (int ni = 0; ni<In.atoms[i].ncount; ni++ ) {
    //            rpos[i][ni].xyz = rotate_vector(In.atoms[i].nodes[ni].pos.xyz, In.atoms[i].rot);
    //} 
    //   return;
    //}

    AtomD atom_i = In.atoms[i];
    AtomS atom_iS = Static.atoms[i];
    vec3 pos_i= atom_i.pos.xyz;
    int bonded = 0;
    for (int jj=0;jj<SelIn.indexes.length();jj++){
        int j = SelIn.indexes[jj];
        if (i==j) return;
    }

    for (int jj=0;jj<SelIn.indexes.length();jj++){
        int j = SelIn.indexes[jj];
        //uint n = atomicCounterIncrement(nselected);
        AtomD atom_j = In.atoms[j];
        AtomS atom_jS = Static.atoms[j];
        vec3 pos_j = atom_j.pos.xyz;
        vec3 delta = pos_i - pos_j;
        float r =     distance(pos_i, pos_j);
        if (r>=50) continue;
        for (int ni = 0; ni<atom_iS.ncount; ni++ ) {
            vec3 ni_realpos = rpos[i][ni].xyz;
            float ni_type = atom_i.nodes[ni].type;
                for (int nj = 0; nj<atom_jS.ncount; nj++){
                    float nj_type = atom_j.nodes[nj].type;
                    vec3 nj_realpos = rpos[j][nj].xyz;
                    float rn = distance(pos_i + ni_realpos, pos_j + nj_realpos);
                    if (rn<=BONDR){
                        bonded = 1;
                    }
                }
        }

    }
    if (bonded==1){
        uint n = atomicCounterIncrement(nselected);
        SelOut.indexes[n] = i;
    }

 
}