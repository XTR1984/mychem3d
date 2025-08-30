#version 430
// Set up our compute groups
layout(local_size_x=LOCALSIZEX, local_size_y=1,local_size_z=1) in;

// Input uniforms go here if you need them.
uniform int N;
uniform int stage;
uniform vec3 box;
uniform int iTime;
uniform int bondlock;
uniform int gravity;
uniform int redox;
uniform int shake;
uniform int test;
uniform int efield;
uniform int highlight_unbond;
uniform int sideheat;


//uniform float frame_time;
uniform float TDELTA;
float BONDR = 4;
uniform float BOND_KOEFF;
uniform float ATTRACTION_KOEFF;
uniform float INTERACT_KOEFF;
uniform float INTERACT_KOEFF2=30;
uniform float FIELD_KOEFF;
uniform float ROTA_KOEFF;
uniform float CONUS_KOEFF = 0.866;
float REPULSION1 = -6;
uniform float REPULSION_SIGMA;
uniform float REPULSION_POW;
uniform float REPULSION_EPS;
uniform float MASS_KOEFF;
uniform float NEARDIST;
uniform float NODEDIST;
uniform float HEAT;
float WIDTH = box.x;
float HEIGHT = box.y;
float DEPTH = box.z;


float tbl_elneg[18]= float[] (0, 2.2, 0.0, 0.0, 0.0,
                                0.0, 2.55, 3.04, 3.44,
                                0.0,  0.0,  0.93, 0.0,
                                0.0,  0.0,  2.19, 2.58, 3.16);


#include "common.glsl"

// Input buffer
layout(std430, binding=0) buffer atoms_in
{
    Atom atoms[];
} In;

layout(std430, binding=1) buffer atoms_out
{
    Atom atoms[];
} Out;

layout(std430, binding=2) buffer near_atoms
{
    int indexes[][NEARATOMSMAX];
} Near;

layout(std430, binding=3) buffer far_field
{
    vec4 F[];
} Far;

layout(std430, binding=4) buffer rpos_buffer
{
    vec4 rpos[][6];
};

layout(std430, binding=6) buffer qs_buffer
{
    float qshift_buffer[][6];
};



float rand(vec2 co){
    return fract(sin(dot(co, vec2(12.9898, 78.233))) * 43758.5453);
}


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

void limits(inout vec3 pos,  inout vec3 v, in float radius){
    vec3 outlim;
    outlim = pos - box;
    outlim = clamp(outlim,vec3(0.0),vec3(100.0));
    v -= outlim * 0.005 ;
    outlim = clamp(pos, vec3(-100.0), vec3(0.0));
    v -= outlim * 0.005;
}


int i = int(gl_GlobalInvocationID);

void main()
{
    if (stage==1){  //calc atom q and rpos of nodes
       //In.atoms[i].q=0;
       float q = 0; 
       for (int ni = 0; ni<In.atoms[i].ncount; ni++ ) {
                rpos[i][ni].xyz = rotate_vector(In.atoms[i].nodes[ni].pos.xyz, In.atoms[i].rot);
                q += qshift_buffer[i][ni]; 
                if (In.atoms[i].nodes[ni].type == 2.0 ) { 
                    q +=  1;
                }
                q +=  In.atoms[i].nodes[ni].q;
                
       } 
       In.atoms[i].q = q;
       return;
    }

    vec3 F,E,M;  

    Atom atom_i = In.atoms[i];
    vec3 pos_i= atom_i.pos.xyz;

    if (stage==2){ //calc near atoms  and far field
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
                float e1= In.atoms[j].q*INTERACT_KOEFF/r/r;
                E += e1 * delta/r;  
            }

        }
        Near.indexes[i][0]=index;  // near atoms count
        Far.F[i].xyz = E * In.atoms[i].q;
        return;
    }

    if(stage==3){   //auto spin set
        for (int ni = 0; ni<atom_i.ncount; ni++ ) {
            vec3 ni_realpos = rpos[i][ni].xyz;
            float ni_type = atom_i.nodes[ni].type;
            //if (ni_type>1) continue;
            if (atom_i.nodes[ni].spin ==0 && atom_i.nodes[ni].q==0){
                for (int j=0;j<i;j++){  //half matrix
                    Atom atom_j = In.atoms[j];
                    vec3 pos_j = atom_j.pos.xyz;
                    vec3 delta = pos_i - pos_j;
                    float r =     distance(pos_i, pos_j);
                    if (r==0.0) continue;
                    for (int nj = 0; nj<atom_j.ncount; nj++){
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
        return;
    }

    if (stage==4){ // bonded state set
        for (int ni = 0; ni<atom_i.ncount; ni++ ) {
            vec3 ni_realpos = rpos[i][ni].xyz;
            float ni_type = atom_i.nodes[ni].type;
            float bonded = 0.0;
            //if (ni_type>1) continue;
            for (int jj=1;jj<=Near.indexes[i][0];jj++){
                int j = Near.indexes[i][jj];
                Atom atom_j = In.atoms[j];
                vec3 pos_j = atom_j.pos.xyz;
                vec3 delta = pos_i - pos_j;
                float r =     distance(pos_i, pos_j);
                //if (r>=40) continue;
                for (int nj = 0; nj<atom_j.ncount; nj++){
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
        return;
    }

    vec3 v_i = atom_i.v.xyz;
    //In.atoms[i].pos.x +=rand(atom_i.pos.yz);

    F = vec3(0.0);
    E = vec3(0.0);
    M = vec3(0.0);
    vec4 totalrot = vec4(0.0, 0.0, 0.0, 1.0);

    
    //highlight
    if (atom_i.highlight >0) atom_i.highlight-=1;

    //random redox 
    if (redox==1){
            if (pos_i.x<300){
                if (rand(v_i.xy)>=0.9994) {
                    atom_i.nodes[0].q = 1;
                    atom_i.nodes[0].spin = 0;
                    atom_i.highlight = 500;                    
                }
            }
            if (pos_i.x>WIDTH-300){
                if (rand(v_i.xy)>=0.9994) {
                    atom_i.nodes[0].q = -1;
                    atom_i.nodes[0].spin = 0;
                    atom_i.highlight = 500;
                }
            }    
    }

    float bondcheck[5]= {0.0,0.0,0.0,0.0,0.0};

    //forj
    for (int jj=1;jj<=Near.indexes[i][0];jj++){
            int j = Near.indexes[i][jj];
            Atom atom_j = In.atoms[j];
            vec3 pos_j = atom_j.pos.xyz;
            vec3 delta = pos_i - pos_j;
            float r = distance(pos_i, pos_j);
            float sumradius = atom_i.r + atom_j.r;
            if (r==0.0) continue;
            float f2,f3,f4,f5;

            //if (r>sumradius){
            float e= atom_j.q*INTERACT_KOEFF/r/r;
            E += delta/r * e;
            //}
            
            
            f2 = -ATTRACTION_KOEFF*0.01/r/r;
            F += delta/r*f2; 

            if (r<NODEDIST) {
                float sgm = sumradius+REPULSION_SIGMA;
                f3 = REPULSION_EPS* pow(sgm/r,REPULSION_POW);
                F += delta/r*f3; 

            //nodes
            for (int ni = 0; ni<atom_i.ncount; ni++ ) {
                vec3 ni_realpos = rpos[i][ni].xyz;
                float ni_q=atom_i.nodes[ni].q ;
                float ni_spin = atom_i.nodes[ni].spin;
                float ni_bonded = atom_i.nodes[ni].bonded;
                float ni_type = atom_i.nodes[ni].type;

                vec3 FN = vec3(0);
                for (int nj = 0; nj<atom_j.ncount; nj++){
                    float nj_type = atom_j.nodes[nj].type;
                    vec3 nj_realpos = rpos[j][nj].xyz;
                    float nj_bonded = atom_j.nodes[nj].bonded;
                    float nj_q=atom_j.nodes[nj].q;
                    float nj_spin=atom_j.nodes[nj].spin;

                    f4 = 0, f5=0;
                    //node interact
                    float rn,rn2;
                    vec3 ndelta,force_dir;
                    

                    ndelta =  ni_realpos - nj_realpos + delta;
    
                    rn = distance(pos_i + ni_realpos, pos_j + nj_realpos);
                    if (rn == 0) continue;                    

                    //vec3 m = mix(ndelta,cdelta,0.0);
                    //vec3 m = cdelta;
                    if (ndelta!=vec3(0.0)){
                        force_dir = normalize(ndelta);
                    }

                    float edelta = tbl_elneg[int(atom_j.type)] - tbl_elneg[int(atom_i.type)];
                    
                    if (rn<=BONDR  ){                        
                        if (ni_spin + nj_spin==0 && ni_q + nj_q == 0){
                            qshift_buffer[i][ni]=0.3*edelta + 0.1*(atom_j.q-atom_i.q);
                            atom_i.nodes[ni].q = 0;
                            atom_i.nodes[ni].spin = 2*int(i<j)-1;   //+mod(time,2)?
                            bondcheck[ni]=1.0;
                            float f = -rn* BOND_KOEFF*0.01;
                            f4 = f;
                            f5 = f;
                        }
                        else {
                            f4 = 500*exp(-1.2*rn); // pauli!
                            //atom_i.highlight = 50;
                        }
                    }

                    else {
                    
                        /*if (rn < BONDR*1.5  ){
                            float f= abs(edelta) * ni_spin * nj_spin * INTERACT_KOEFF/rn/rn;
                            f4+=f;
                            f5+=f;
                        }*/

                        if (ni_bonded == 0.0 && nj_bonded ==0.0 &&  ni_spin + nj_spin==0 ){
                            float f= ni_spin * nj_spin * INTERACT_KOEFF2/rn/rn;
                            f4+= f;
                            f5+= f;
                        }
                                    
                        if (ni_bonded == 0.0 && nj_bonded==0.0 && ni_q + nj_q==0 ){ 
                            float f = ni_q * nj_q * INTERACT_KOEFF/rn/rn;
                            //f4+= f;
                            f5+= f;
                            
                        }
                        
                    }
                    
                    //hydrogen bond, node to atom
                    if (ni_bonded==0.0 && atom_j.type==1.0 && nj_bonded==1.0){
                                vec3 cdelta = ni_realpos + delta;
                                float rc = distance(pos_i + ni_realpos, pos_j);
                                float ld = length(delta);
                                if (ld==0.0) continue;
                                float conus_i  = dot(ni_realpos,-delta)/atom_i.r/ld;
                                if(  conus_i>CONUS_KOEFF ){   
                                    float f = atom_j.q* ni_q * INTERACT_KOEFF/rc/rc;
                                    FN+= cdelta/rc*f;
                                    
                                }
                    }

                    FN +=force_dir*f5;
                    F += force_dir*f4;
                    

                } //nj 
                                        
                M+= cross(ni_realpos,FN);

                
            } //for ni



        } //if r<NODEDIST



    } //for jj

    F += E * atom_i.q;  

    if(atom_i.r==0.0 || atom_i.m==0.0){
        atom_i.color == vec4(1.0,0.0,1.0,1.0);
    }

    atom_i.rotv.xyz += M*TDELTA;   // dL/dt = M ;
    vec4 rotv = vec4(0,0,0,1); 
    float ll = length(atom_i.rotv.xyz);
    if (ll!=0.0){
        //if (ll>300) atom_i.rotv.xyz = normalize(atom_i.rotv.xyz)*300.0;

        vec3 axis = atom_i.rotv.xyz/ll;
        float angle = 0.01* ROTA_KOEFF* TDELTA* ll/atom_i.m/MASS_KOEFF/atom_i.r/atom_i.r;
        rotv = vec4(sin(angle*0.5)* axis,cos(angle*0.5) ); // quat
    }



    for (int ni = 0; ni<atom_i.ncount; ni++ ) {
        float old = atom_i.nodes[ni].bonded;
        atom_i.nodes[ni].bonded = bondcheck[ni];
        if (old==1.0 && atom_i.nodes[ni].bonded==0.0) {  //unbond
            if (highlight_unbond==1) {
                atom_i.highlight = 50;                    
            }                
            if (abs(qshift_buffer[i][ni])>0.4){
                if(qshift_buffer[i][ni]>0){
                    atom_i.nodes[ni].q= 1;
                    atom_i.nodes[ni].spin= 0;
                }
                if(qshift_buffer[i][ni]<0){
                    atom_i.nodes[ni].q=-1;
                    atom_i.nodes[ni].spin= 0;
                }
            }
            qshift_buffer[i][ni] = 0;
        }


    }

    //totalrot = vec4(0, sin(-0.01),sin(-0.01), cos(-0.01));    
    //atom_i.rotv = normalize(qmul(totalrot, atom_i.rotv));
    //atom_i.rotv = totalrot;


 // mixer
    if (atom_i.type==666){
        if (v_i!= vec3(0.0,0.0,0.0))
            v_i = normalize(v_i);
    }

//heating
   if (sideheat==1){
        if (pos_i.y<50.0) v_i +=  v_i * HEAT*0.0001;      
   }
   else v_i +=  v_i * HEAT*0.0001;      
   
 

 //gravity
   if (gravity==1) v_i.y -= 0.001; //gravity

   //if (pos_i.y < 30) v_i.y += 0.1;
     
     
//shake
   if (shake==1) v_i+= vec3(rand(pos_i.xy)-0.499,rand(pos_i.yz)-0.499,rand(pos_i.xz)-0.499)*0.05;

// far field
   F += Far.F[i].xyz;

//e-field
   if (efield==1)
     F.x += atom_i.q*FIELD_KOEFF;

//next
    //if (length(F)>3){
//        F = normalize(F)*3;
    //}
    vec3 a = F/(atom_i.m*MASS_KOEFF);
    v_i += a*TDELTA;

    if (atom_i.fxd==1)  v_i = vec3(0.0);

    //v_i = clamp(v_i , vec3(-MAXVEL,-MAXVEL,-MAXVEL), vec3(MAXVEL,MAXVEL,MAXVEL));
    float vl = length(v_i);
    if (vl>MAXVEL){
        //atom_i.color = vec4(0,0,0,1);
        v_i = v_i/vl*MAXVEL;
    }

    pos_i += v_i*TDELTA;

    //atom_i.rot = normalize(qmul(atom_i.rotv,atom_i.rot));
    atom_i.rot = normalize(qmul(rotv,atom_i.rot));
    

// 
//   if (length(v_i)>length(atom_i.v.xyz)+0.05)
//        atom_i.highlight=5;
    
//limits    
    limits(pos_i,v_i,atom_i.r); //borders of container
 
    atom_i.v.xyz = v_i;
    atom_i.pos.xyz = pos_i;
    Out.atoms[i] = atom_i;
}