#version 430
// Set up our compute groups
layout(local_size_x=LOCALSIZEX, local_size_y=1,local_size_z=1) in;

// Input uniforms go here if you need them.
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


layout(std430, binding=4) buffer far_field
{
    vec4 F[];
} Far;

layout(std430, binding=5) buffer rpos_buffer
{
    vec4 rpos[][6];
};

float rand(vec2 co){
    return fract(sin(dot(co, vec2(12.9898, 78.233))) * 43758.5453);
}

int i = int(gl_GlobalInvocationID);

void main()
{
    AtomD atom_i = In.atoms[i];
    AtomS atom_iS = Static.atoms[i]; 
    vec3 pos_i= atom_i.pos.xyz;

    //auto spin set
    for (int ni = 0; ni<atom_iS.ncount; ni++ ) {
        vec3 ni_realpos = rpos[i][ni].xyz;
        float ni_type = atom_i.nodes[ni].type;
        //if (ni_type>1) continue;
        if (atom_i.nodes[ni].spin ==0 && atom_i.nodes[ni].q==0){
            for (int j=0;j<i;j++){  //half matrix
                AtomD atom_j = In.atoms[j];
                AtomS atom_jS = Static.atoms[j];
                vec3 pos_j = atom_j.pos.xyz;
                vec3 delta = pos_i - pos_j;
                float r =     distance(pos_i, pos_j);
                if (r==0.0) continue;
                for (int nj = 0; nj<atom_jS.ncount; nj++){
                    vec3 nj_realpos = rpos[j][nj].xyz;
                    float nj_type = atom_j.nodes[nj].type;
                    //if (nj_type>1) continue;
                    float rn = distance(pos_i + ni_realpos, pos_j + nj_realpos);
                    if (rn<BONDR){
                        In.atoms[i].nodes[ni].bonded=1.0;
                        if (atom_j.nodes[nj].spin !=0){
                            In.atoms[i].nodes[ni].spin = - atom_j.nodes[nj].spin;
                        }
                        else {
                            //randspin
                            if (rand(atom_i.pos.xy)>=0.5){
                                In.atoms[i].nodes[ni].spin = 1;
                                In.atoms[j].nodes[nj].spin = -1;
                            }
                            else {
                                In.atoms[i].nodes[ni].spin = -1;
                                In.atoms[j].nodes[nj].spin = 1;
                            }


                        }
                    }
                }
            }
            if (In.atoms[i].nodes[ni].spin==0) In.atoms[i].nodes[ni].spin= 2*mod(i+ni,2)-1;
        }
    }                
 
}