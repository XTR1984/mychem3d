#version 430
// Set up our compute groups
layout(local_size_x=LOCALSIZEX, local_size_y=1,local_size_z=1) in;

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

layout(std430, binding=5) buffer rpos_buffer
{
    vec4 rpos[][6];
};



int i = int(gl_GlobalInvocationID);

void main()
{
    AtomD atom_i = In.atoms[i];
    AtomS atom_iS = Static.atoms[i]; 
    vec3 pos_i= atom_i.pos.xyz;

 // bonded state set
    for (int ni = 0; ni<atom_iS.ncount; ni++ ) {
        vec3 ni_realpos = rpos[i][ni].xyz;
        float ni_type = atom_i.nodes[ni].type;
        float bonded = 0.0;
        //if (ni_type>1) continue;
        for (int jj=1;jj<=Near.indexes[i][0];jj++){
            int j = Near.indexes[i][jj];
            AtomD atom_j = In.atoms[j];
            AtomS atom_jS = Static.atoms[j];
            vec3 pos_j = atom_j.pos.xyz;
            vec3 delta = pos_i - pos_j;
            float r =     distance(pos_i, pos_j);
            //if (r>=40) continue;
            for (int nj = 0; nj<atom_jS.ncount; nj++){
                float nj_type = atom_j.nodes[nj].type;
                vec3 nj_realpos = rpos[j][nj].xyz;
                //if (nj_type>1) continue;
                float rn = distance(pos_i + ni_realpos, pos_j + nj_realpos);
                
                if (rn<=BONDR){
                    bonded = 1.0;
                }
            }
        }
        In.atoms[i].nodes[ni].bonded = bonded;
        //In.atoms[i].color = vec4(1.0);
    }
 
}