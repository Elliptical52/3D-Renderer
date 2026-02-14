# Imports
import pygame, math, random, file
from config import *

# Constants
SCREEN_SIZE = min(WIDTH, HEIGHT)

# Pygame Setup
clock = pygame.time.Clock()
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption(f'3D Renderer - {object_to_load}')
# Rendering Setup
vertices, faces = file.load(object_to_load)

def project_vertex(x, y, z):
    projected_x = x / -z
    projected_y = y / -z
    screen_x = (projected_x * SCREEN_SIZE/2) + SCREEN_SIZE/2
    screen_y = (-projected_y * SCREEN_SIZE/2) + SCREEN_SIZE/2
    return screen_x, screen_y

# Camera
def camera_transform(x, y, z):
    return x - camera_position[0], y - camera_position[1], z - camera_position[2]

# Rotation
def rotate_about_axis(a, b, angle):
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return (
        a * cos_a - b * sin_a,
        a * sin_a + b * cos_a
    )

def rotate_vertex(x, y, z):
    x, z = rotate_about_axis(x, z, camera_rotation[1]) # yaw
    y, z = rotate_about_axis(y, z, camera_rotation[0]) # pitch
    x, y = rotate_about_axis(x, y, camera_rotation[2]) # roll
    return x, y, z

# Lighting
def calculate_normal(v1, v2, v3): 
    # Edges
    ax = v2[0] - v1[0]
    ay = v2[1] - v1[1]
    az = v2[2] - v1[2]

    bx = v3[0] - v1[0]
    by = v3[1] - v1[1]
    bz = v3[2] - v1[2]

    # Cross product
    nx = ay*bz - az*by
    ny = az*bx - ax*bz
    nz = ax*by - ay*bx
    
    return nx, ny, nz

def normalize(x, y, z):
    mag = math.hypot(x, y, z)
    return x / mag, y / mag, z / mag

def dot_product(vector_a, vector_b):
    x1, y1, z1 = vector_a
    x2, y2, z2 = vector_b
    return x1 * x2 + y1 * y2 + z1 * z2

# Main Loop
while True:
    # Check for Exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
            
        if event.type == pygame.WINDOWRESIZED:
            WIDTH, HEIGHT = pygame.display.get_window_size()
        
    # Clear Screen
    window.fill((0, 0, 0))

    # Rendering    
    faces_queue = []
    for i, face in enumerate(faces):
        points = []
        z_total = 0
        visible = True
        
        for index in face:
            x, y, z = vertices[index]
            x, y, z = rotate_vertex(x, y, z)
            x, y, z = camera_transform(x, y, z)
            
            if z >= -0.01:
                visible = False
                break
            
            z_total += z
            
            screen_pos = project_vertex(x, y, z)
            points.append(screen_pos)
        
        if not visible:
            continue
        
        average_z = z_total / len(face)
        face_vertices = [vertices[i] for i in face][:3]
        faces_queue.append((average_z, points,calculate_normal(*face_vertices)))
    
    faces_queue.sort(key=lambda f: f[0], reverse=False)
    
    for depth, points, normal in faces_queue:
        v = normalize(*normal)
        brightness = max(0, (dot_product(v, normalize(*light_direction))) * 100) +60
        pygame.draw.polygon(window,
                            (
                                brightness , brightness, brightness
                            ),
        points)


    SCREEN_SIZE = min(WIDTH, HEIGHT)

    camera_rotation[1] += 0.01
    
    # Update Screen
    pygame.display.flip()
    
    # Timing Control
    clock.tick(FPS)

