// Structure of the ball data
struct NodeS {
    vec4 pos;
};

struct NodeD {
    float q;
    float bonded;
    float type;
    float spin;
};



struct AtomS
{
    float type;
    float r;
    float m;
    float ncount;
    float highlight;
    float q;    
    float fxd;
    float _pad;
    vec4 color;
    NodeS nodes[5];
};

struct AtomD {
    vec4 pos;
    vec4 v;
    vec4 rot;
    vec4 rotv;
    NodeD nodes[5];
};

