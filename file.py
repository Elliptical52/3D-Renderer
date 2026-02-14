def load(fp):
    vertices = []
    faces = []
    
    with open(fp) as file:
        content = file.read().split('\n')
    for line in content:
        if line.startswith('v '):
            vertices.append([float(n) for n in line.split(' ')[1:4]])
        if line.startswith('f '):
            parts = line.strip().split()[1:]
            face = []
            for part in parts:
                vertex_index = part.split("/")[0]
                face.append(int(vertex_index) - 1)
            faces.append(face)

        
    return vertices, faces
