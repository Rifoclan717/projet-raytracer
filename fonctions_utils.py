from Light import Light
from Sphere import Sphere
from parallelogramme import Parallelogram
from vec3 import addition_vecteurs, multiplication_scalaire, soustraction_vecteurs, produit_scalaire, taille_vecteur
import math

# (AIDE A IA)
# This fonction computes the intersection of a ray with a parallelogram (wall)
def IntersectRayParallelogram(O, D, wall):
    
    N = wall.N
    denom = produit_scalaire(N, D)

    if abs(denom) < 1e-6:
        return float('inf')

    t = produit_scalaire(soustraction_vecteurs(wall.A, O), N) / denom

    if t < 0:
        return float('inf')

    P = addition_vecteurs(O, multiplication_scalaire(D, t))
    AP = soustraction_vecteurs(P, wall.A)

    alpha = produit_scalaire(AP, wall.U) / produit_scalaire(wall.U, wall.U)
    beta  = produit_scalaire(AP, wall.V) / produit_scalaire(wall.V, wall.V)

    if 0 <= alpha <= 1 and 0 <= beta <= 1:
        return t

    return float('inf')

# Compute lighting to get the intensity at point P
def ComputeLighting(P, N, scene, V, s):
    intensity = 0.0

    for light in scene.lights:
        if light.type == 'ambient':
            intensity += light.intensity
            continue

        if light.type == 'point':
            L = soustraction_vecteurs(light.position, P)
            t_max = taille_vecteur(L)
        else:
            L = light.direction
            t_max = float('inf')

        shadow_t, shadow_obj, obj_type = ClosestIntersection(P, L, 0.001, t_max, scene)
        if shadow_obj != None:
            continue

        n_dot_l = produit_scalaire(N, L)
        if n_dot_l > 0:
            intensity += light.intensity * n_dot_l / (taille_vecteur(N) * taille_vecteur(L))

        if s > 0:
            R = ReflectRay(L, N)
            r_dot_v = produit_scalaire(R, V)
            if r_dot_v > 0:
                intensity += light.intensity * pow(r_dot_v / (taille_vecteur(R) * taille_vecteur(V)), s)

    return intensity

# Trace a ray from origin O in direction D within the scene to get the color
def TraceRay(O, D, t_min, t_max, scene, depth):
    t, obj, obj_type = ClosestIntersection(O, D, t_min, t_max, scene)

    if obj is None:
        return (0,0,0)

    P = addition_vecteurs(O, multiplication_scalaire(D, t))

    if obj_type == "sphere":
        N = soustraction_vecteurs(P, obj.center)
        N = multiplication_scalaire(N, 1/taille_vecteur(N))
        color, specular, reflective = obj.color, obj.specular, obj.reflective
    else:
        N, color, specular, reflective = obj.N, obj.color, obj.specular, obj.reflective

    intensity = ComputeLighting(P, N, scene, multiplication_scalaire(D, -1), specular)
    local_color = multiplication_scalaire(color, intensity)

    if depth <= 0 or reflective <= 0:
        return local_color

    R = ReflectRay(multiplication_scalaire(D, -1), N)
    reflected = TraceRay(P, R, 0.001, float('inf'), scene, depth-1)

    return addition_vecteurs(
        multiplication_scalaire(local_color, 1-reflective),
        multiplication_scalaire(reflected, reflective)
    )

# This fonction computes the intersection of a ray with a sphere
def IntersectRaySphere(O, D, sphere):
    r = sphere.radius
    CO = soustraction_vecteurs(O, sphere.center)

    a = produit_scalaire(D, D)
    b = 2 * produit_scalaire(CO, D)
    c = produit_scalaire(CO, CO) - r*r

    discriminant = b*b - 4*a*c

    if discriminant < 0:
        return float('inf'), float('inf')

    t1 = (-b + math.sqrt(discriminant)) / (2*a)
    t2 = (-b - math.sqrt(discriminant)) / (2*a)
    return t1, t2

# Find the closest intersection of a ray with objects in the scene
def ClosestIntersection(O, D, t_min, t_max, scene):
    closest_t = float('inf')
    closest_obj = None
    obj_type = None

    for sphere in scene.objets:
        t1, t2 = IntersectRaySphere(O, D, sphere)
        for t in [t1, t2]:
            if t_min < t < t_max and t < closest_t:
                closest_t = t
                closest_obj = sphere
                obj_type = "sphere"

    for mur in scene.murs:
        t = IntersectRayParallelogram(O, D, mur)
        if t_min < t < t_max and t < closest_t:
            closest_t = t
            closest_obj = mur
            obj_type = "wall"

    return closest_t, closest_obj, obj_type

# Compute the reflection of ray R around normal N
def ReflectRay(R, N):
    n_dot_r = produit_scalaire(N, R)
    return soustraction_vecteurs(multiplication_scalaire(N, 2 * n_dot_r), R)

# Convert canvas coordinates to viewport coordinates
def CanvasToViewport(viewport, canvas, x, y):
    return (x * viewport.width / canvas.width, y * viewport.height / canvas.height, viewport.dist)

# Load scene from a file and populate the scene object
def load_scene_from_file(scene, filename):
    try:
        with open(filename, 'r') as f:
            for line in f:
                parts = line.split()
                if not parts: continue

                if parts[0] == 'sphere':
                    cx, cy, cz = float(parts[1]), float(parts[2]), float(parts[3])
                    radius = float(parts[4])
                    r, g, b = int(parts[5]), int(parts[6]), int(parts[7])
                    specular = int(parts[8])
                    reflective = float(parts[9])
                    sphere = Sphere((cx, cy, cz), radius, (r, g, b), specular, reflective)
                    scene.add_objet(sphere)

                elif parts[0] == 'parallelogram':
                    Ax, Ay, Az = float(parts[1]), float(parts[2]), float(parts[3])
                    Ux, Uy, Uz = float(parts[4]), float(parts[5]), float(parts[6])
                    Vx, Vy, Vz = float(parts[7]), float(parts[8]), float(parts[9])
                    r, g, b = int(parts[10]), int(parts[11]), int(parts[12])
                    specular = int(parts[13])
                    reflective = float(parts[14])
                    p = Parallelogram((Ax, Ay, Az), Ux, Uy, Uz, Vx, Vy, Vz, (r,g,b), specular, reflective)
                    scene.add_mur(p)

                elif parts[0] == 'light':
                    type = parts[1]
                    intensity = float(parts[2])

                    if type == 'ambient':
                        light = Light(type, intensity, None)
                    elif type == 'point':
                        x, y, z = float(parts[3]), float(parts[4]), float(parts[5])
                        light = Light(type, intensity, (x, y, z))
                    elif type == 'directional':
                        dx, dy, dz = float(parts[3]), float(parts[4]), float(parts[5])
                        light = Light(type, intensity, (dx, dy, dz))
                    else:
                        continue

                    scene.add_light(light)

    except FileNotFoundError:
        print("Erreur: Le fichier scene.txt est introuvable.")

