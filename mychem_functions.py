from math import sin, cos, pi


def create_sphere(radius, num_segments):
    vertex_data = []
    index_data = []

    for i in range(num_segments + 1):
        for j in range(num_segments + 1):
            theta = i * (2 * pi) / num_segments
            phi = j * pi / num_segments

            x = radius * sin(phi) * cos(theta)
            y = radius * sin(phi) * sin(theta)
            z = radius * cos(phi)

            vertex_data.append((x, y, z))

            if i < num_segments and j < num_segments:
                first = i * (num_segments + 1) + j
                second = first + num_segments + 1
                index_data.extend([first, second, first + 1, second, second + 1, first + 1])

    return vertex_data, index_data


def make_sphere_vert(radius, segments):
    vertices = []
    vertex_data, index_data = create_sphere(radius, segments)
    for i in index_data:
            vertices.extend(list(vertex_data[i]))
    return vertices





