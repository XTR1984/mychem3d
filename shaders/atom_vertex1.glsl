#version 430 

#include "common.glsl"


layout(std430, binding=0) buffer atoms_in
{
    Atom atoms[];
} In;

layout(std430, binding=4) buffer rpos_buffer
{
    vec4 rpos[][6];
};


//layout(std430, binding=0) buffer atoms_in


layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;

uniform vec4 objectColor;
uniform int mode;
uniform int nodeindex;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform float nicefactor;

out AtomData {
    Atom out_a;
};

//out vec4 atom_position;
out vec3 Normal;
out vec4 ObjectColor;
out vec3 FragPos;  

//out Atom currentAtom;



void main()
{
    if (mode==0){  //vbo merge atoms and nodes 
//        float factor = 0.001;
        gl_Position = projection * view * model * vec4(position, 1.0f);
        ObjectColor = objectColor;
        FragPos = vec3(model * vec4(position, 1.0f));
        Normal = normal;
    }
    if (mode==1){ //ssbo atoms
        bool bug = false; 
        float factor = 0.001;
        Atom currentAtom = In.atoms[gl_InstanceID];
//        mat4 model = mat4( factor,  0,  0, 0,
//                           0,  factor, 0,  0 ,
//                           0,   0, factor,  0,
//                           currentAtom.pos.x,  currentAtom.pos.y  ,  currentAtom.pos.z ,    1  
//                           );

        vec4 vposition = vec4(position * currentAtom.r * factor * nicefactor  +  currentAtom.pos.xyz*factor, 1.0f) ;
        //atom_position = currentAtom.pos*factor;
        gl_Position = projection * view * vposition;
//        if (currentAtom.pos.x != 515.0){
//            bug = true;
//        }
        ObjectColor = currentAtom.color;
        if (bug){
            ObjectColor = vec4(1,0,0,1);
        }
        if (currentAtom.highlight>0) ObjectColor = vec4(0,1,0,1);
        FragPos = vposition.xyz;
        Normal = normal;
    }
    if (mode==2) { //nodes
        float factor = 0.001;
        Atom currentAtom = In.atoms[gl_InstanceID];
        float alpha = currentAtom.color.w;
        //vec3 nodepos = rotate_vector(currentAtom.nodes[nodeindex].pos.xyz, currentAtom.rot);
        vec3 nodepos;
        if (nodeindex<currentAtom.ncount)
            nodepos = rpos[gl_InstanceID][nodeindex].xyz;
        else nodepos = vec3(0);

        nodepos += currentAtom.pos.xyz;
        vec4 vposition = vec4(position * 1 * factor +  nodepos*factor, 1.0f) ;
        gl_Position = projection * view * vposition;
        float q = currentAtom.nodes[nodeindex].q;
        float spin = currentAtom.nodes[nodeindex].spin;
        //float bonded = currentAtom.nodes[nodeindex].bonded;
        // node charge and spin color
        if (q==0){
            if (spin==1) ObjectColor = vec4(0.5,0.5,0.5,alpha); 
            if (spin==-1) ObjectColor = vec4(1.0,1.0,1.0,alpha);
        }
        else{
            if (q==1) ObjectColor = vec4(1.0,0.0,0.0,alpha); 
            if (q==-1) ObjectColor = vec4(0.0,0.0,252/256.0,alpha);
        }

        if(currentAtom.nodes[nodeindex].type==2)
            ObjectColor = vec4(30/256.0,144/255.0,1.0, alpha); 

        //if (bonded==1) ObjectColor= ObjectColor/2;
        //else ObjectColor = vec3(1,1,1);
        FragPos = vposition.xyz;
        Normal = normal;
    }
}