// Structure of the ball data
struct Node {
    vec4 pos;
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
};

struct AtomD {
    vec4 pos;
    vec4 v;
    vec4 rot;
    vec4 rotv;
    Node nodes[5];
};

