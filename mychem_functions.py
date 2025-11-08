from math import sin, cos, pi
import numpy as np, glm

def create_sphere(radius, num_segments):
    vertex_data = []
    index_data = []
    normal_data = []

    for i in range(num_segments + 1):
        for j in range(num_segments + 1):
            theta = i * (2 * pi) / num_segments
            phi = j * pi / num_segments

            x = radius * sin(phi) * cos(theta)
            y = radius * sin(phi) * sin(theta)
            z = radius * cos(phi)

            vertex_data.append((x, y, z))
            normal_data.append(glm.normalize(glm.vec3(x,y,z)))

            if i < num_segments and j < num_segments:
                first = i * (num_segments + 1) + j 
                second = first + num_segments + 1 
                index_data.extend([first, second, first + 1, second, second + 1, first + 1])
    
    return vertex_data, index_data, normal_data


def make_sphere_vert(radius, segments):
    vertices = []
    vertex_data, index_data,normal_data = create_sphere(radius, segments)
    for i in index_data:
            vertices.extend(list(vertex_data[i]))
            vertices.extend(list(normal_data[i]))
    return vertices



from mychem_data import cube2_surfaces, cube2_vertices
def make_cube2():
     vertices = []
     for s in cube2_surfaces:
        for s2 in s:
            vertices.extend(list(cube2_vertices[s2]))
            vertices.extend([0,0,-1])
     return vertices



def OnOff(b):
	if b: return "On"
	else: return "Off"


#def molecule_extend(space, a1, nn1, type, nn2=1):

#    node1=a1.nodes[nn1]



def bond_atoms(a1, a2, ni1=-1, ni2=-1):
    bi1 = 0
    bi2 = 0
    if ni1==-1:
        for i in range(0, len(a1.nodes)):
            if not a1.nodes[i].bonded and a1.nodes[i].type<=1:
                bi1 = i
                break
        else: return False
    else:
       bi1 = ni1
    if ni2==-1:
        for i in range(0, len(a2.nodes)):
            if not a2.nodes[i].bonded and a2.nodes[i].type<=1:
                bi2 = i
                break
        else: return False
    else:
       bi2 = ni2
    print("bi1bi2" , bi1,bi2)       
    a1.nodes[bi1].q = -1
    a1.nodes[bi1].spin = 0
    a1.nodes[bi1].bonded = True
    a2.nodes[bi2].q = 1
    a2.nodes[bi2].spin = 0
    a2.nodes[bi2].bonded = True
    return True




class UndoStack:
    def __init__(self, limit=10):
        self.stack = []
        self.limit = limit

    def push(self, data):
        print("push to undostack")
        if len(self.stack) >= self.limit:
            self.stack.pop(0)  
        self.stack.append(data)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        else:
            return None

    def is_empty(self):
        return len(self.stack) == 0
    

def double_info(a1, a2,space):
    print("A1")
    a1.info()
    print("A2")
    a2.info()
    delta = a1.pos - a2.pos
    print(f"Delta = {delta}, Distance={glm.length(delta):.3f}")
    print(f"R1 = {a1.r}, R2= {a2.r}, sumrad = {a1.r+a2.r} ")
    r = glm.length(delta)
    FK = space.CHARGE_KOEFF*a1.q * a2.q/glm.length2(delta)
    sumradius = a1.r + a2.r
    sgm = sumradius+space.REPULSION_SIGMA; 
    FR = space.REPULSION_EPS*pow(sgm/r,space.REPULSION_POW);    
    F = FK+FR
    print(f"FK={FK:.3f}  FR={FR:.3f} F={F:.3f}")
    print("node distance:")
    bondedinfo = ""
    for ni in range(len(a1.nodes)):
        nodei = a1.nodes[ni]
        str = ""
        for nj in range(len(a2.nodes)):
            nodej = a2.nodes[nj]
            rposi = a1.rot * nodei.pos
            rposj = a2.rot * nodej.pos
            rn = glm.length(rposi-rposj+a1.pos-a2.pos)
            str += f"{rn:.4f} "
            if rn<4:
                bondedinfo+=f"rn {ni}, {nj}  spins: {nodei.spin}, {nodej.spin} q: {nodei.q}, {nodej.q} bonded: {nodei.bonded}, {nodej.bonded} \r\n"
        print(str)
    print(bondedinfo)



def print_bytes_with_highlights(byte_array, highlights):
    # ANSI-коды для красного цвета и сброса
    red = '\033[91m'
    end = '\033[0m'
    
    # Создание множества для быстрого поиска выделяемых индексов
    highlight_indices = set()
    for offset, n in highlights:
        if offset < 0 or offset >= len(byte_array):
            print(f"Ошибка: смещение {offset} вне диапазона.")
            return
        if n < 0 or offset + n > len(byte_array):
            print(f"Ошибка: количество байтов {n} для смещения {offset} вне диапазона.")
            return
        highlight_indices.update(range(offset, offset + n))

    # Вывод байтов с выделением
    for i in range(len(byte_array)):
        if i in highlight_indices:
            print(f"{red}{byte_array[i]:02x}{end}", end=' ')
        else:
            print(f"{byte_array[i]:02x}", end=' ')
    
    print()  # Переход на новую строку после вывода

